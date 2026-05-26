% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Раскраска графа — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода (динамические строки)
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/coloring/practice">

<div class="theory-section">
    <h3>Шаг 1 — Дисциплины</h3>
    <span class="input-section-label">Добавьте дисциплины учебного расписания:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addNodeRow('nodes-container','Название дисциплины')">
        + Добавить дисциплину
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 — Конфликты</h3>
    <span class="input-section-label">
        Выберите пары дисциплин, которые нельзя ставить в одну смену:
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addEdgeRow('edges-container', false, false, false)">
        + Добавить конфликт
    </button>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Составить расписание</button>
</div>
</form>

<script>
$(function () {
    addNodeRow('nodes-container', 'Название дисциплины');
    addNodeRow('nodes-container', 'Название дисциплины');
    addNodeRow('nodes-container', 'Название дисциплины');
    addEdgeRow('edges-container', false, false, false);
});
</script>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 2: Ошибка
     ═══════════════════════════════════════════════════════════ -->
% if error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 3: Результат (не трогать)
     ═══════════════════════════════════════════════════════════ -->
% if result:
<div class="theory-section">
    <h3>Результат</h3>

    <div class="panel panel-success">
        <div class="panel-heading"><strong>Итог</strong></div>
        <div class="panel-body">
            <p>Минимальное количество смен: <strong>{{result['num_colors']}}</strong></p>
        </div>
    </div>

    <h4>Расписание по сменам</h4>
    % for shift_num in sorted(result['schedule'].keys()):
    <div class="theory-section" style="border-left: 4px solid #2e86ab; padding: 12px 16px; margin-bottom: 12px">
        <h4 style="margin-top:0">Смена {{shift_num}}</h4>
        <p>{{ ', '.join(result['schedule'][shift_num]) }}</p>
    </div>
    % end

    <h4>Таблица назначений</h4>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>Дисциплина</th>
                <th>Смена</th>
            </tr>
        </thead>
        <tbody>
            % for discipline, shift in sorted(result['colors'].items(), key=lambda x: x[1]):
            <tr>
                <td>{{discipline}}</td>
                <td>Смена {{shift}}</td>
            </tr>
            % end
        </tbody>
    </table>

    <div class="theory-section">
        <h4>Граф конфликтов (раскраска)</h4>
        <p class="text-muted" style="font-size:13px">
            Каждый цвет узла — отдельная смена. Рёбра соединяют конфликтующие дисциплины.
        </p>
        <div id="graph-canvas" style="height:450px;border:1px solid #ddd;
             border-radius:4px;background:#fafafa;margin-top:8px"></div>
    </div>

    <script>
    (function() {
        var vertices = {{!result['gv']}};
        var edges    = {{!result['ge']}};
        var colors   = {{!result['gc']}};

        var palette = [
            '#2e86ab','#e74c3c','#2ecc71','#f39c12',
            '#9b59b6','#1abc9c','#e67e22','#34495e'
        ];
        var borderPalette = [
            '#1a5276','#922b21','#1a7a45','#9a6004',
            '#6c3483','#0f6b57','#935116','#1c2833'
        ];

        var nodes = new vis.DataSet(vertices.map(function(v){
            var shift = (colors[v] || 1) - 1;
            var bg  = palette[shift % palette.length];
            var brd = borderPalette[shift % borderPalette.length];
            return {
                id: v,
                label: v + '\n(Смена ' + (shift + 1) + ')',
                color: { background: bg, border: brd },
                font: { color: '#fff', size: 13 }
            };
        }));

        var edgesDS = new vis.DataSet(edges.map(function(e, i){
            return { id: i, from: e[0], to: e[1],
                     color: { color:'#999' }, width: 1 };
        }));

        var container = document.getElementById('graph-canvas');
        new vis.Network(container, { nodes: nodes, edges: edgesDS }, {
            edges: { smooth: false },
            physics: { stabilization: { iterations: 300 } }
        });
    })();
    </script>
</div>
% end
