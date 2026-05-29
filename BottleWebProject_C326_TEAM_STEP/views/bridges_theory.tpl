% rebase('layout.tpl', title='Теория — Мосты Тарьяна', year=year, active_page='bridges')
<link rel="stylesheet" type="text/css" href="/static/content/bridges_theory.css" />

<!-- СЕКЦИЯ 1: Навигация -->
<div class="bt-header">
    <h2>Мосты Тарьяна &amp; Флойд&ndash;Уоршолл</h2>
    <a href="/bridges/practice" class="btn btn-primary btn-lg">К практике &rarr;</a>
</div>

<!-- СЕКЦИЯ 2: Ошибка -->
% if defined('error') and error:
<div class="alert alert-danger">{{error}}</div>
% end

<!-- СЕКЦИЯ 3: Содержание -->

<!-- Hero: split box -->
<div class="bt-hero">
    <div class="bt-hero-left">
        <div class="bt-hero-label">Ключевое понятие</div>
        <p class="bt-hero-def">
            <strong>Мост</strong> &mdash; ребро <em>e&nbsp;&isin;&nbsp;E</em>,
            удаление которого увеличивает число компонент связности графа.
        </p>
        <p class="bt-hero-sub">
            <strong>Точка сочленения</strong> &mdash; вершина, удаление которой
            (вместе с инцидентными рёбрами) также разбивает граф.
        </p>
    </div>
    <div class="bt-hero-right">
        <div class="bt-hero-label">Алгоритм в 4 шага</div>
        <ol class="bt-hero-steps">
            <li>Поиск мостов &mdash; алгоритм Тарьяна (DFS)</li>
            <li>Базовая сумма путей &mdash; Флойд&ndash;Уоршолл</li>
            <li>Оценка каждого моста: &delta;&nbsp;=&nbsp;новая_сумма&nbsp;&minus;&nbsp;база</li>
            <li>Результат &mdash; список (u,&nbsp;v,&nbsp;w,&nbsp;&delta;) для каждого моста</li>
        </ol>
    </div>
</div>

<!-- Definitions row -->
<div class="bt-section-title">Ключевые переменные</div>
<div class="bt-defs">
    <div class="bt-def-chip"><code>disc[v]</code> &mdash; момент первого посещения вершины v (таймер DFS)</div>
    <div class="bt-def-chip"><code>low[v]</code> &mdash; минимальный disc, достижимый из поддерева v</div>
    <div class="bt-def-chip"><code>dist[i][j]</code> &mdash; кратчайшее расстояние от i до j</div>
    <div class="bt-def-chip"><code>&delta;</code> &mdash; прирост суммарной длины путей после удаления моста</div>
</div>

<!-- Two-column algorithm grid -->
<div class="bt-section-title">Алгоритмы</div>
<div class="bt-algo-grid">

    <div class="bt-algo-card">
        <div class="bt-algo-head bt-algo-head--tarjan">
            Тарьян &mdash; поиск мостов
            <span class="bt-algo-complexity">O(V + E)</span>
        </div>
        <div class="bt-algo-body">
            <p>Ребро {v,&nbsp;u} является мостом, если
            <code>low[u]&nbsp;&gt;&nbsp;disc[v]</code>.</p>
            <p>Инициализация: <code>disc[v]&nbsp;=&nbsp;&minus;1</code> для всех вершин,
            <code>timer&nbsp;=&nbsp;0</code>.</p>
        </div>
    </div>

    <div class="bt-algo-card">
        <div class="bt-algo-head bt-algo-head--floyd">
            Флойд&ndash;Уоршолл &mdash; все пути
            <span class="bt-algo-complexity">O(V&sup3;) / O(V&sup2;)</span>
        </div>
        <div class="bt-algo-body">
            <p>Инициализация: <code>dist[i][i]&nbsp;=&nbsp;0</code>,
            <code>dist[i][j]&nbsp;=&nbsp;w</code> если ребро есть, иначе <code>&infin;</code>.</p>
            <p><strong>База</strong> = &Sigma;&nbsp;dist[i][j] для всех пар i&nbsp;&lt;&nbsp;j
            при dist[i][j]&nbsp;&ne;&nbsp;&infin;.</p>
        </div>
    </div>

</div>
