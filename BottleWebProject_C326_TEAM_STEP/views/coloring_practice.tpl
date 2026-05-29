% rebase('layout.tpl', title='Раскраска графа — Практика', year=year, active_page='coloring')

<h2>Раскраска графа — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/coloring/practice">

<div class="theory-section">
    <h3>Шаг 1 — Дисциплины</h3>
    <span class="input-section-label">Добавьте дисциплины учебного расписания:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn">
        + Добавить дисциплину
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 — Конфликты</h3>
    <span class="input-section-label">
        Выберите пары дисциплин, которые нельзя ставить в одну смену:
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn">
        + Добавить конфликт
    </button>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Составить расписание</button>
</div>
</form>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 2: Ошибка
     ═══════════════════════════════════════════════════════════ -->
% if defined('error') and error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 3: Результат
     ═══════════════════════════════════════════════════════════ -->

<div style="margin-bottom:12px; margin-top:20px">
    <button type="button" class="btn btn-default btn-sm">
        💾 Скачать результат (JSON)
    </button>
    <button type="button" class="btn btn-default btn-sm">
        📄 Скачать результат (TXT)
    </button>
</div>

<div class="panel panel-success">
    <div class="panel-heading"><strong>Итог</strong></div>
    <div class="panel-body">
        <p>Минимальное количество смен: <strong>3</strong></p>
    </div>
</div>

<h4>Расписание по сменам</h4>

<div class="theory-section" style="border-left: 4px solid #2e86ab; padding: 12px 16px; margin-bottom: 12px">
    <h4 style="margin-top:0">Смена 1</h4>
    <p>Информатика, Математика</p>
</div>
<div class="theory-section" style="border-left: 4px solid #2e86ab; padding: 12px 16px; margin-bottom: 12px">
    <h4 style="margin-top:0">Смена 2</h4>
    <p>Биология, Физика</p>
</div>
<div class="theory-section" style="border-left: 4px solid #2e86ab; padding: 12px 16px; margin-bottom: 12px">
    <h4 style="margin-top:0">Смена 3</h4>
    <p>Химия</p>
</div>

<h4>Таблица назначений</h4>
<table class="table table-bordered table-striped table-hover">
    <thead>
        <tr>
            <th>Дисциплина</th>
            <th>Смена</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>Информатика</td><td>Смена 1</td></tr>
        <tr><td>Математика</td><td>Смена 1</td></tr>
        <tr><td>Биология</td><td>Смена 2</td></tr>
        <tr><td>Физика</td><td>Смена 2</td></tr>
        <tr><td>Химия</td><td>Смена 3</td></tr>
    </tbody>
</table>
