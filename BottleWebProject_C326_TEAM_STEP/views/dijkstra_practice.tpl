% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Алгоритм Дейкстры — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода (динамические строки)
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/dijkstra/practice" id="form-dijkstra">
<input type="hidden" name="edge_count" id="edge-count" value="0">

<div class="theory-section">
    <h3>Шаг 1 — Узлы сети</h3>
    <span class="input-section-label">Добавьте маршрутизаторы / узлы:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addNodeRow('nodes-container','Название узла (A, Router-1...)')">
        + Добавить узел
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 — Каналы связи</h3>
    <span class="input-section-label">
        Добавьте направленные каналы. Отметьте «недоступен» для временно
        отключённых каналов (вес = ∞):
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addEdgeRow('edges-container', true, true, true)">
        + Добавить канал
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 3 — Источник</h3>
    <span class="input-section-label">Выберите узел, от которого строить маршруты:</span>
    <select name="source" class="form-control node-select" style="max-width:250px"></select>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Построить маршруты</button>
</div>
</form>

<script>
$(function () {
    // Добавить 3 узла и 2 канала по умолчанию
    addNodeRow('nodes-container', 'Название узла');
    addNodeRow('nodes-container', 'Название узла');
    addNodeRow('nodes-container', 'Название узла');
    addEdgeRow('edges-container', true, true, true);
    addEdgeRow('edges-container', true, true, true);

    // Перед отправкой: нумеруем checkbox-ы и фиксируем edge_count
    $('#form-dijkstra').on('submit', function () {
        var count = $('#edges-container .edge-row').length;
        $('#edge-count').val(count);
        $('#edges-container .edge-row').each(function (i) {
            $(this).find('input[type=checkbox]').attr('name', 'edge_inf_' + i);
        });
    });
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

% if result["skipped_edges"]:
<div class="alert alert-warning">
    <strong>Исключены недоступные каналы (∞):</strong>
    % for se_u, se_v, se_w in result["skipped_edges"]:
    {{se_u}}→{{se_v}}&nbsp;&nbsp;
    % end
</div>
% end

% if result["unreachable"]:
<div class="alert alert-danger">
    <strong>Недостижимые узлы:</strong> {{', '.join(result["unreachable"])}}
</div>
% end

<div class="theory-section">
    <h3>Таблица кратчайших маршрутов от узла {{source_val}}</h3>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>Узел назначения</th>
                <th>Задержка (мс)</th>
                <th>Маршрут</th>
            </tr>
        </thead>
        <tbody>
            % for v in result["distances"]:
            %   dist = result["distances"][v]
            %   path = result["paths"][v]
            %   if v == source_val:
            <tr class="active">
                <td><strong>{{v}}</strong> (источник)</td>
                <td>0</td>
                <td>{{v}}</td>
            </tr>
            %   elif dist == float('inf'):
            <tr class="danger">
                <td>{{v}}</td>
                <td>∞</td>
                <td>Недостижим</td>
            </tr>
            %   else:
            %     dist_display = int(dist) if dist == int(dist) else dist
            <tr>
                <td>{{v}}</td>
                <td>{{dist_display}}</td>
                <td>{{ ' → '.join(path) }}</td>
            </tr>
            %   end
            % end
        </tbody>
    </table>
</div>

<div class="theory-section">
    <h4>Граф сети</h4>
    <p class="text-muted" style="font-size:13px">
        Синие стрелки — кратчайшие маршруты. Серые — остальные рёбра.
        Красные пунктиры — недоступные каналы (∞). Золотой узел — источник.
    </p>
    <div id="graph-canvas" style="height:450px;border:1px solid #ddd;
         border-radius:4px;background:#fafafa;margin-top:8px"></div>
</div>

<script>
(function() {
    var vertices  = {{!result['gv']}};
    var edges     = {{!result['ge']}};
    var pathEdges = {{!result['gpe']}};
    var source    = '{{source_val}}';
    var peSet = {};
    pathEdges.forEach(function(e){ peSet[e[0]+'→'+e[1]] = true; });

    var nodes = new vis.DataSet(vertices.map(function(v){
        return {
            id: v, label: v,
            color: v === source
                ? { background:'#f0ad4e', border:'#d48a00' }
                : { background:'#d6eaf8', border:'#2e86ab' },
            font: { size: 14, bold: v === source }
        };
    }));

    var edgesDS = new vis.DataSet(edges.map(function(e, i){
        var u=e[0], v=e[1], w=e[2];
        var isInf  = (w === null);
        var isPath = peSet[u+'→'+v] || false;
        return {
            id: i, from: u, to: v,
            label: isInf ? '∞' : String(w),
            arrows: 'to',
            dashes: isInf,
            color: isInf
                ? { color:'#e74c3c' }
                : isPath
                    ? { color:'#2e86ab' }
                    : { color:'#aaaaaa' },
            width: isPath ? 3 : 1,
            font: { align: 'middle', size: 11 }
        };
    }));

    var container = document.getElementById('graph-canvas');
    new vis.Network(container, { nodes: nodes, edges: edgesDS }, {
        layout: { improvedLayout: true },
        edges: { smooth: { type: 'curvedCW', roundness: 0.2 } },
        physics: { stabilization: { iterations: 200 } }
    });
})();
</script>

% end
