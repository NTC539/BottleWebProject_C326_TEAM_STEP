% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Мосты Тарьяна — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода (динамические строки)
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/bridges/practice">

<div class="theory-section">
    <h3>Шаг 1 — Города</h3>
    <span class="input-section-label">Добавьте города / узлы сети:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addNodeRow('nodes-container','Название города')">
        + Добавить город
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 — Дороги</h3>
    <span class="input-section-label">
        Добавьте дороги (неориентированные) с весом — длиной или временем:
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addEdgeRow('edges-container', false, true, false)">
        + Добавить дорогу
    </button>
</div>

<div class="theory-section" style="padding:10px 16px">
    <span style="font-weight:600; margin-right:8px">Данные:</span>
    <button type="button" class="btn btn-default btn-sm" onclick="randomBridges()">
        🎲 Случайные данные
    </button>
    <button type="button" class="btn btn-default btn-sm" onclick="loadFileBridges()">
        📂 Загрузить из файла
    </button>
    <span class="text-muted" style="font-size:12px; margin-left:8px">
        JSON: { "vertices":[...], "edges":[{"from","to","weight"}] }
    </span>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Анализировать сеть</button>
</div>
</form>

<script>
$(function () {
    addNodeRow('nodes-container', 'Название города');
    addNodeRow('nodes-container', 'Название города');
    addNodeRow('nodes-container', 'Название города');
    addEdgeRow('edges-container', false, true, false);
    addEdgeRow('edges-container', false, true, false);
});
</script>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 2: Ошибка
     ═══════════════════════════════════════════════════════════ -->
% if defined('error') and error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 3: Результат (не трогать)
     ═══════════════════════════════════════════════════════════ -->
% if defined('result') and result is not None:

<div style="margin-bottom:12px">
    <button type="button" class="btn btn-default btn-sm"
            onclick="downloadResult('bridges')">
        💾 Скачать результат (JSON)
    </button>
    <button type="button" class="btn btn-default btn-sm"
            onclick="downloadResultTxt('bridges')">
        📄 Скачать результат (TXT)
    </button>
</div>
<script>
window._resultData = window._resultData || {};
window._resultData['bridges'] = {
    total_path_sum: {{result['total_path_sum']}},
    bridges:        {{!result['gb']}}
};
</script>

<div class="panel panel-info">
    <div class="panel-heading"><strong>Общая статистика</strong></div>
    <div class="panel-body">
        <p>Суммарная длина кратчайших путей (исходная сеть):
           <strong>{{result["total_path_sum"]}}</strong></p>
        <p>Найдено мостов: <strong>{{len(result["bridges"])}}</strong></p>
    </div>
</div>

% if result["bridges"]:
<h4>Критические дороги (мосты)</h4>
<table class="table table-bordered table-striped table-hover">
    <thead>
        <tr>
            <th>Дорога</th>
            <th>Вес</th>
            <th>Прирост суммарных путей при удалении</th>
        </tr>
    </thead>
    <tbody>
        % for item in result["bridge_impact"]:
        %   u, v, w = item["edge"]
        %   delta = item["delta"]
        %   delta_str = 'Сеть разрывается (∞)' if delta is None else '+{:.1f}'.format(delta)
        %   row_cls = 'danger' if delta is None else 'warning'
        <tr class="{{row_cls}}">
            <td>{{u}} — {{v}}</td>
            <td>{{w}}</td>
            <td>{{delta_str}}</td>
        </tr>
        % end
    </tbody>
</table>
<div class="alert alert-warning">
    <strong>Красные строки</strong> — удаление полностью разрывает сеть.
    <strong>Жёлтые</strong> — связность сохраняется, но пути удлиняются.
</div>
% else:
<div class="alert alert-success">
    Мостов не найдено. Сеть устойчива — удаление любой одной дороги не нарушит связность.
</div>
% end

<h4>Матрица кратчайших путей (исходная сеть)</h4>
<div class="table-responsive">
<table class="table table-bordered table-condensed">
    <thead>
        <tr>
            <th></th>
            % for col in result["all_pairs"]:
            <th>{{col}}</th>
            % end
        </tr>
    </thead>
    <tbody>
        % for row in result["all_pairs"]:
        <tr>
            <td><strong>{{row}}</strong></td>
            % for col in result["all_pairs"]:
            %   if row == col:
            <td>0</td>
            %   elif result["all_pairs"][row][col] == float('inf'):
            <td>∞</td>
            %   else:
            %     val = result["all_pairs"][row][col]
            %     cell = int(val) if val == int(val) else val
            <td>{{cell}}</td>
            %   end
            % end
        </tr>
        % end
    </tbody>
</table>
</div>

<div class="theory-section">
    <h4>Граф транспортной сети</h4>
    <p class="text-muted" style="font-size:13px">
        Красные жирные рёбра — мосты (критические дороги).
        Серые — обычные дороги.
    </p>
    <div id="graph-canvas" style="height:450px;border:1px solid #ddd;
         border-radius:4px;background:#fafafa;margin-top:8px"></div>
</div>

<script>
(function() {
    var vertices = {{!result['gv']}};
    var edges    = {{!result['ge']}};
    var bridges  = {{!result['gb']}};
    var bSet = {};
    bridges.forEach(function(b){ bSet[b[0]+'—'+b[1]] = true; bSet[b[1]+'—'+b[0]] = true; });

    var nodes = new vis.DataSet(vertices.map(function(v){
        return {
            id: v, label: v,
            color: { background:'#d6eaf8', border:'#2e86ab' },
            font: { size: 14 }
        };
    }));

    var edgesDS = new vis.DataSet(edges.map(function(e, i){
        var u=e[0], v=e[1], w=e[2];
        var isBridge = bSet[u+'—'+v] || false;
        return {
            id: i, from: u, to: v,
            label: String(w),
            color: isBridge ? { color:'#e74c3c' } : { color:'#aaaaaa' },
            width: isBridge ? 4 : 1,
            font: { align: 'middle', size: 11 }
        };
    }));

    var container = document.getElementById('graph-canvas');
    new vis.Network(container, { nodes: nodes, edges: edgesDS }, {
        edges: { smooth: false },
        physics: { stabilization: { iterations: 200 } }
    });
})();
</script>

% end
