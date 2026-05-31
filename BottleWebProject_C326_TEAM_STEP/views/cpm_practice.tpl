% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Метод критического пути (CPM) - Теория</h2>

<form method="POST" action="/cpm/practice">
    <div class="theory-section">
        <h3>Шаг 1 — Задачи проекта</h3>
        <span class="input-section-label">
            Введите задачи и их длительность (в любых единицах — днях, часах):
        </span>
        <div id="tasks-container">
            <div class="input-row">
                <input type="text" name="task_name[]" class="form-control node-input" placeholder="Название задачи">
                <span class="edge-arrow">:</span>
                <input type="number" name="task_dur[]" class="form-control" min="0" placeholder="Длительность" value="1" style="max-width:120px">
                <button type="button" class="btn-danger btn-xs remove-row">✕</button>
            </div>  
            <div class="input-row">
                <input type="text" name="task_name[]" class="form-control node-input" placeholder="Название задачи">
                <span class="edge-arrow">:</span>
                <input type="number" name="task_dur[]" class="form-control" min="0" placeholder="Длительность" value="1" style="max-width:120px">
                <button type="button" class="btn-danger btn-xs remove-row">✕</button>
            </div>  
        </div>
        <button type="button" class="btn-success btn-sm add-row-btn">
            + Добавить задачу
        </button>
    </div>

    <div class="theory-section">
        <h3>Шаг 2 — Зависимости</h3>
        <span class="input-section-label">
            Укажите порядок выполнения: задача A должна завершиться до начала задачи B:
        </span>
        <div id="deps-container">
            <div class="input-row dep-row">
                <select name="dep_from[]" class="form-control node-select">
                    <option value="Задача">Задача</option>
                </select>
                <span class="edge-arrow">→</span>
                <select name="dep_to[]" class="form-control node-select">
                    <option value="Задача">Задача</option>
                </select>
                <button type="button" class="btn-danger btn-xs remove-row">✕</button>
            </div>
        </div>
        <button type="button" class="btn-success btn-sm add-row-btn">
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

% if error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end

<div class="theory-section">
    <h3>Результат</h3>

    <div class="panel panel-success">
        <div class="panel-heading"><strong>Итог</strong></div>
        <div class="panel-body">
            <p>Общая длительность проекта: <strong>(Длительность)</strong></p>
            <p>Критический путь: <strong>(Критический путь)</strong></p>
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
            <tr class="success">
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
            <tr>
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
            <tr>
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
            <tr>
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
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