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
</div>
% end
