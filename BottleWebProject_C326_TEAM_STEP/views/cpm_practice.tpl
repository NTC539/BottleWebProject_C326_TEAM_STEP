% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Критический путь — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода (динамические строки)
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/cpm/practice">

<div class="theory-section">
    <h3>Шаг 1 — Задачи проекта</h3>
    <span class="input-section-label">
        Введите задачи и их длительность (в любых единицах — днях, часах):
    </span>
    <div id="tasks-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addTaskRow('tasks-container')">
        + Добавить задачу
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 — Зависимости</h3>
    <span class="input-section-label">
        Укажите порядок выполнения: задача A должна завершиться до начала задачи B:
    </span>
    <div id="deps-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addDepRow('deps-container')">
        + Добавить зависимость
    </button>
</div>

<div class="theory-section" style="padding:10px 16px">
    <span style="font-weight:600; margin-right:8px">Данные:</span>
    <button type="button" class="btn btn-default btn-sm" onclick="randomCPM()">
        🎲 Случайные данные
    </button>
    <button type="button" class="btn btn-default btn-sm" onclick="loadFileCPM()">
        📂 Загрузить из файла
    </button>
    <span class="text-muted" style="font-size:12px; margin-left:8px">
        JSON: { "tasks":[{"name","duration"}], "deps":[{"from","to"}] }
    </span>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Рассчитать</button>
</div>
</form>

<script>
$(function () {
    addTaskRow('tasks-container');
    addTaskRow('tasks-container');
    addTaskRow('tasks-container');
    addDepRow('deps-container');
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

<div style="margin-bottom:12px">
    <button type="button" class="btn btn-default btn-sm"
            onclick="downloadResult('cpm')">
        💾 Скачать результат (JSON)
    </button>
    <button type="button" class="btn btn-default btn-sm"
            onclick="downloadResultTxt('cpm')">
        📄 Скачать результат (TXT)
    </button>
</div>
<script>
window._resultData = window._resultData || {};
window._resultData['cpm'] = {
    duration:      {{result['duration']}},
    critical_path: {{!result['gcrit']}},
    tasks:         {{!result['gtasks']}},
    es:            {{!result['ges']}},
    ef:            {{!result['gef']}}
};
</script>

<div class="theory-section">
    <h3>Результат</h3>

    <div class="panel panel-success">
        <div class="panel-heading"><strong>Итог</strong></div>
        <div class="panel-body">
            <p>Общая длительность проекта: <strong>{{result['duration']}}</strong></p>
            <p>Критический путь: <strong>{{ ' → '.join(result['critical_path']) }}</strong></p>
        </div>
    </div>

    <h4>Таблица ранних сроков</h4>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>Задача</th>
                <th>Длительность</th>
                <th>Ранний старт (ES)</th>
                <th>Раннее окончание (EF)</th>
                <th>На крит. пути</th>
            </tr>
        </thead>
        <tbody>
            % for task_name, duration in result['tasks'].items():
            %   on_cp = 'Да' if task_name in result['critical_path'] else 'Нет'
            %   row_class = 'success' if task_name in result['critical_path'] else ''
            <tr class="{{row_class}}">
                <td>{{task_name}}</td>
                <td>{{duration}}</td>
                <td>{{result['es'][task_name]}}</td>
                <td>{{result['ef'][task_name]}}</td>
                <td>{{on_cp}}</td>
            </tr>
            % end
        </tbody>
    </table>

    <div class="theory-section">
        <h4>Сетевой граф проекта</h4>
        <p class="text-muted" style="font-size:13px">
            Красные узлы и стрелки — критический путь.
            В каждом узле: название задачи, длительность, ES и EF.
        </p>
        <div id="graph-canvas" style="height:450px;border:1px solid #ddd;
             border-radius:4px;background:#fafafa;margin-top:8px"></div>
    </div>

    <script>
    (function() {
        var vertices = {{!result['gv']}};
        var edges    = {{!result['ge']}};
        var critPath = {{!result['gcrit']}};
        var tasks    = {{!result['gtasks']}};
        var es       = {{!result['ges']}};
        var ef       = {{!result['gef']}};
        var critSet  = {};
        critPath.forEach(function(v){ critSet[v] = true; });

        var nodes = new vis.DataSet(vertices.map(function(v){
            var label = v + '\nd=' + tasks[v] + '\nES=' + es[v] + ' EF=' + ef[v];
            var onCrit = critSet[v] || false;
            return {
                id: v, label: label,
                shape: 'box',
                color: onCrit
                    ? { background:'#fadbd8', border:'#e74c3c' }
                    : { background:'#d6eaf8', border:'#2e86ab' },
                font: { size: 12 },
                margin: 8
            };
        }));

        var edgesDS = new vis.DataSet(edges.map(function(e, i){
            var onCrit = critSet[e[0]] && critSet[e[1]];
            return {
                id: i, from: e[0], to: e[1],
                arrows: 'to',
                color: onCrit ? { color:'#e74c3c' } : { color:'#aaaaaa' },
                width: onCrit ? 3 : 1
            };
        }));

        var container = document.getElementById('graph-canvas');
        new vis.Network(container, { nodes: nodes, edges: edgesDS }, {
            layout: { hierarchical: { direction:'LR', sortMethod:'directed', levelSeparation:180 } },
            physics: false
        });
    })();
    </script>
</div>
% end
