% rebase('layout.tpl', title='Практика — Мосты Тарьяна', year=year, active_page='bridges')

<h2>Мосты Тарьяна &mdash; Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/bridges/practice">

<div class="theory-section">
    <h3>Шаг 1 &mdash; Города</h3>
    <span class="input-section-label">Добавьте города / узлы сети:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn">
        + Добавить город
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 &mdash; Дороги</h3>
    <span class="input-section-label">
        Добавьте дороги (неориентированные) с весом &mdash; длиной или временем:
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn">
        + Добавить дорогу
    </button>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Анализировать сеть</button>
</div>
</form>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 2: Ошибка
     ═══════════════════════════════════════════════════════════ -->
% if defined('error') and error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end
