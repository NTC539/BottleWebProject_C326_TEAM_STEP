% rebase('layout.tpl', title='Теория — Раскраска графа Welsh–Powell', year=year, active_page='coloring')
<!-- СЕКЦИЯ 1: Навигация -->
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px;">
    <h2 style="margin:0;border:none;padding:0;">Раскраска графа &mdash; Welsh&ndash;Powell</h2>
    <a href="/coloring/practice" class="btn btn-primary btn-lg">К практике &rarr;</a>
</div>
<!-- СЕКЦИЯ 2: Ошибка -->
% if defined('error') and error:
<div class="alert alert-danger">{{error}}</div>
% end
<!-- СЕКЦИЯ 3: Содержание -->
