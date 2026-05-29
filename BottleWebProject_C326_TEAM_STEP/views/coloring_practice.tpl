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
