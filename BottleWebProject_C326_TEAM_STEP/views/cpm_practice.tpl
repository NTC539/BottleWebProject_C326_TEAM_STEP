% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Метод критического пути (CPM) - Практика</h2>

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
        </p>
        <div id="graph-canvas" style="height:450px;border:1px solid #ddd;
             border-radius:4px;background:#fafafa;margin-top:8px"></div>
    </div>
</div>
% end