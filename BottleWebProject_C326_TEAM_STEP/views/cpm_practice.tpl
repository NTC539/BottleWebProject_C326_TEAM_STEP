% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Метод критического пути (CPM) - Теория</h2>

<form method="POST" action="/cpm/practice">
    <div class="theory-section">
        <h3>Шаг 1 — Задачи проекта</h3>
        <span class="input-section-label">
            Введите задачи и их длительность (в любых единицах — днях, часах):
        </span>
        <div id="tasks-container">
        </div>
        <button type="button" class="btn-success btn-sm add-row-btn"
                onclick="addTaskRow('tasks-container')">
            + Добавить задачу
        </button>
    </div>

    <div class="theory-section">
        <h3>Шаг 2 — Зависимости</h3>
        <span class="input-section-label">
            Укажите порядок выполнения: задача A должна завершиться до начала задачи B:
        </span>
        <div id="deps-container">
        </div>
        <button type="button" class="btn-success btn-sm add-row-btn"
                onclick="addDepRow('deps-container')">
            + Добавить зависимость
        </button>
    </div>

    <div style="padding:10px 0px; display: flex; gap: 16px;">
        <button type="submit" class="btn-primary btn-lg">Рассчитать</button>
        <button type="button" id="cpm-generate-btn" class="btn-default btn-sm">
            🎲 Сгенерировать случайные данные
        </button>
    </div>
</form>

<script>
// Сохранённый ввод формы (после отправки поля не очищаются)
var CPM_TASKS_INPUT = {{!tasks_input}};
var CPM_DEPS_INPUT  = {{!deps_input}};

$(function () {
    // Восстанавливаем задачи (либо одна пустая строка по умолчанию)
    if (CPM_TASKS_INPUT && CPM_TASKS_INPUT.length) {
        CPM_TASKS_INPUT.forEach(function (t) {
            addTaskRow('tasks-container', t[0], t[1]);
        });
    } else {
        addTaskRow('tasks-container');
    }
    // Восстанавливаем зависимости (после задач — чтобы списки были заполнены)
    if (CPM_DEPS_INPUT && CPM_DEPS_INPUT.length) {
        CPM_DEPS_INPUT.forEach(function (d) {
            addDepRow('deps-container', d[0], d[1]);
        });
    }
    updateSelects();

    // Кнопка генерации случайных данных (данные приходят с сервера, Python)
    $('#cpm-generate-btn').on('click', function () {
        $.getJSON('/cpm/generate', function (data) {
            $('#tasks-container').empty();
            $('#deps-container').empty();
            data.tasks.forEach(function (t) {
                addTaskRow('tasks-container', t.name, t.dur);
            });
            updateSelects();
            data.deps.forEach(function (d) {
                addDepRow('deps-container', d[0], d[1]);
            });
            updateSelects();
        });
    });
});
</script>

% if error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end

% if result:
<div class="theory-section">
    <h3>Результат</h3>

    <div class="panel panel-success">
        <div class="panel-heading"><strong>Итог</strong></div>
        <div class="panel-body">
            <p>Общая длительность проекта: <strong>{{ result['duration'] }}</strong></p>
            <p style="margin-bottom:8px">
                Найдено критических путей:
                <strong>{{ len(result['critical_paths']) }}</strong>
            </p>
            % cp_colors = ['primary', 'success', 'info', 'warning', 'danger', 'default']
            % for idx, path in enumerate(result['critical_paths']):
            <p style="margin:6px 0">
                <span class="label label-{{ cp_colors[idx % len(cp_colors)] }}">
                    Путь {{ idx + 1 }}
                </span>
                &nbsp;<span style="font-size:15px">{{ ' → '.join(path) }}</span>
            </p>
            % end
        </div>
    </div>

    <h4 style="margin-top: 40px;">Таблица сроков и резервов</h4>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>Задача</th>
                <th>Длительность</th>
                <th>ES</th>
                <th>EF</th>
                <th>LS</th>
                <th>LF</th>
                <th>Резерв (Float)</th>
                <th>На крит. пути</th>
            </tr>
        </thead>
        <tbody>
            % for task_name, duration in result['tasks'].items():
            %   is_crit = task_name in result['critical_tasks']
            %   on_cp = 'Да' if is_crit else 'Нет'
            %   row_class = 'danger' if is_crit else ''
            <tr class="{{row_class}}">
                <td><strong>{{task_name}}</strong></td>
                <td>{{duration}}</td>
                <td>{{result['es'][task_name]}}</td>
                <td>{{result['ef'][task_name]}}</td>
                <td>{{result['ls'][task_name]}}</td>
                <td>{{result['lf'][task_name]}}</td>
                <td>{{result['total_float'][task_name]}}</td>
                <td>{{on_cp}}</td>
            </tr>
            % end
        </tbody>
    </table>

    <div style="margin-bottom:15px">
        <button type="button" id="cpm-download-btn" class="btn-default btn-sm">
            💾 Скачать результат (JSON)
        </button>
    </div>

    <div class="theory-section">
        <h4>Граф проекта</h4>
        <p class="text-muted" style="font-size:13px">
            Красные узлы и стрелки — критический путь.
            В каждом узле: название задачи, длительность, ES и EF.
            Наведите курсор на узел, чтобы увидеть LS, LF и резерв.
        </p>
        <div id="graph-canvas" style="height:450px;border:1px solid #ddd;
             border-radius:4px;background:#fafafa;margin-top:8px"></div>
    </div>
</div>

<script>
// Скачивание результата в формате .json
(function () {
    var payload = {{!result['gdownload']}};
    var btn = document.getElementById('cpm-download-btn');
    if (btn) {
        btn.addEventListener('click', function () {
            var text = JSON.stringify(payload, null, 2);
            var blob = new Blob([text], { type: 'application/json' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'cpm_result.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }
})();

// Отрисовка графа проекта (vis-network, локальный файл из layout.tpl)
(function () {
    var V  = {{!result['gv']}};
    var E  = {{!result['ge']}};
    var T  = {{!result['gtasks']}};
    var ES = {{!result['ges']}};
    var EF = {{!result['gef']}};
    var LS = {{!result['gls']}};
    var LF = {{!result['glf']}};
    var FL = {{!result['gfloat']}};
    var CP = {{!result['gcrit']}};   // список критических путей

    var container = document.getElementById('graph-canvas');
    if (!container || typeof vis === 'undefined') { return; }

    // Множества критических узлов и рёбер
    var critNodes = {}, critEdges = {};
    CP.forEach(function (path) {
        path.forEach(function (n) { critNodes[n] = true; });
        for (var i = 0; i < path.length - 1; i++) {
            critEdges[path[i] + '->' + path[i + 1]] = true;
        }
    });

    var nodes = V.map(function (n) {
        var crit = critNodes[n];
        return {
            id: n,
            label: n + '\nd=' + T[n] + '\nES=' + ES[n] + '  EF=' + EF[n],
            title: 'Задача ' + n +
                   '\nДлительность: ' + T[n] +
                   '\nES = ' + ES[n] + '   EF = ' + EF[n] +
                   '\nLS = ' + LS[n] + '   LF = ' + LF[n] +
                   '\nРезерв (Float) = ' + FL[n],
            shape: 'box',
            margin: 10,
            color: crit
                ? { background: '#e84855', border: '#b3122a' }
                : { background: '#e8f4fb', border: '#2e86ab' },
            font: { color: crit ? '#ffffff' : '#1a3a5c', size: 14, face: 'monospace' }
        };
    });

    var edges = E.map(function (e) {
        var crit = critEdges[e[0] + '->' + e[1]];
        return {
            from: e[0], to: e[1],
            arrows: { to: { enabled: true, scaleFactor: 0.8 } },
            width: crit ? 3 : 1,
            color: { color: crit ? '#e84855' : '#9bb8cc' },
            smooth: { type: 'cubicBezier', forceDirection: 'horizontal', roundness: 0.4 }
        };
    });

    var data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
    var options = {
        layout: {
            hierarchical: {
                direction: 'LR', sortMethod: 'directed',
                levelSeparation: 170, nodeSpacing: 110
            }
        },
        physics: false,
        interaction: { dragNodes: true, dragView: true, zoomView: true }
    };
    var network = new vis.Network(container, data, options);

    // --- Ограничение «камеры»: граф нельзя потерять ---
    var MIN_SCALE = 0.4, MAX_SCALE = 2.5, PAN_LIMIT = 1500;

    network.once('afterDrawing', function () {
        network.fit({ animation: false });
    });

    // Ограничение масштаба (у vis нет нативного min/max зума)
    network.on('zoom', function () {
        var s = network.getScale();
        if (s < MIN_SCALE) { network.moveTo({ scale: MIN_SCALE }); }
        else if (s > MAX_SCALE) { network.moveTo({ scale: MAX_SCALE }); }
    });

    // Ограничение панорамирования — удерживаем граф в поле зрения
    network.on('dragEnd', function () {
        var p = network.getViewPosition();
        var x = Math.max(-PAN_LIMIT, Math.min(PAN_LIMIT, p.x));
        var y = Math.max(-PAN_LIMIT, Math.min(PAN_LIMIT, p.y));
        if (x !== p.x || y !== p.y) {
            network.moveTo({ position: { x: x, y: y } });
        }
    });
})();
</script>
% end
