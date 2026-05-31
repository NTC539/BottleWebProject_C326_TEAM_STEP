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
        <button type="button" class="btn-default btn-sm">
            🎲 Сгенирировать случайные данные
        </button>
    </div>
</form>

<script>
$(function () {
    addTaskRow('tasks-container');
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
            <p>Критический путь: <strong>{{ ' → '.join(result['critical_paths'][0]) }}</strong></p>
        </div>
    </div>

    <h4 style="margin-top: 40px;">Таблица ранних сроков</h4>
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
            %   on_cp = 'Да' if task_name in result['critical_paths'][0] else 'Нет'
            %   row_class = 'success' if task_name in result['critical_paths'][0] else ''
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

    <div style="margin-bottom:15px">
        <button type="button" class="btn-default btn-sm">
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