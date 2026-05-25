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
</div>
% end
