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
<pre class="algo-block">DFS(v, parent):
  disc[v] = low[v] = timer++
  for u in adj[v]:
    if u == parent: continue
    if disc[u] == -1:
      DFS(u, v)
      low[v] = min(low[v], low[u])
      if low[u] > disc[v]:
        bridges.add({v, u})   # мост
    else:
      low[v] = min(low[v], disc[u])</pre>
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
<pre class="algo-block">for k in range(n):
  for i in range(n):
    for j in range(n):
      dist[i][j] = min(
        dist[i][j],
        dist[i][k] + dist[k][j]
      )</pre>
            <p><strong>База</strong> = &Sigma;&nbsp;dist[i][j] для всех пар i&nbsp;&lt;&nbsp;j
            при dist[i][j]&nbsp;&ne;&nbsp;&infin;.</p>
        </div>
    </div>

</div>

<!-- Algorithm description -->
<div class="bt-section-title">Описание алгоритма</div>
<div class="bt-description">
    <p>
        Пайплайн начинается с обхода DFS по алгоритму Тарьяна: для каждой вершины
        фиксируются время первого посещения <code>disc[v]</code> и минимальное
        достижимое время <code>low[v]</code>. Когда рекурсия возвращается из потомка
        <em>u</em> в вершину <em>v</em> и выполняется условие
        <code>low[u]&nbsp;&gt;&nbsp;disc[v]</code>, ребро {v,&nbsp;u} не имеет
        обходных путей &mdash; это мост. Обход выполняется один раз за
        <em>O(V&nbsp;+&nbsp;E)</em>.
    </p>
    <p>
        После нахождения всех мостов на исходном (полном) графе однократно
        запускается Флойд&ndash;Уоршолл. Результирующая матрица <code>dist[i][j]</code>
        содержит длины кратчайших путей между всеми парами вершин; сумма конечных
        значений при <em>i&nbsp;&lt;&nbsp;j</em> образует
        <strong>базовую сумму</strong> &mdash; отправную точку для последующей
        оценки критичности каждого моста.
    </p>
    <p>
        Для каждого найденного моста алгоритм строит копию графа без данного ребра
        и повторно запускает Флойд&ndash;Уоршолл. По новой матрице вычисляется
        сумма конечных пар, а затем определяется прирост
        <strong>&delta;&nbsp;=&nbsp;новая_сумма&nbsp;&minus;&nbsp;база</strong>.
        Если после удаления ребра в графе появляются недостижимые пары вершин,
        значение &delta; полагается равным <strong>&infin;</strong> &mdash;
        граф утратил связность.
    </p>
    <p>
        Итоговый результат &mdash; список мостов с парами (u,&nbsp;v,&nbsp;&delta;),
        упорядоченный по убыванию &delta;: чем больше прирост, тем критичнее
        данное ребро для транспортной доступности сети.
    </p>
</div>

<!-- Example 1: Tarjan -->
<div class="bt-section-title">Пример &mdash; поиск мостов (граф из 5 вершин)</div>
<div class="bt-example">
    <p>
        <strong>Рёбра:</strong> A&ndash;B:2, B&ndash;C:3, A&ndash;C:1, C&ndash;D:5, D&ndash;E:4.<br>
        Подграф {A,&nbsp;B,&nbsp;C} образует цикл &mdash; обратные рёбра снижают low.
        Цепочка C&ndash;D&ndash;E без обходных путей.
    </p>
    <table class="table table-bordered table-condensed">
        <thead>
            <tr>
                <th>Ребро</th>
                <th>disc[v]</th>
                <th>low[u]</th>
                <th>low[u] &gt; disc[v]?</th>
                <th>Мост?</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>A&ndash;B</td><td>0</td><td>0</td><td>Нет</td><td>Нет</td>
            </tr>
            <tr>
                <td>B&ndash;C</td><td>1</td><td>0</td><td>Нет</td><td>Нет</td>
            </tr>
            <tr>
                <td>A&ndash;C</td><td>0</td><td>0</td><td>Нет</td><td>Нет</td>
            </tr>
            <tr class="bt-row-bridge">
                <td>C&ndash;D</td><td>2</td><td>3</td><td><strong>Да</strong></td><td><strong>Да</strong></td>
            </tr>
            <tr class="bt-row-bridge">
                <td>D&ndash;E</td><td>3</td><td>4</td><td><strong>Да</strong></td><td><strong>Да</strong></td>
            </tr>
        </tbody>
    </table>
    <p>Мосты &mdash; C&ndash;D и D&ndash;E. {A,&nbsp;B,&nbsp;C} связаны циклом; D и E изолируются.</p>
</div>

<!-- Example 2: Floyd-Warshall -->
<div class="bt-section-title">Пример &mdash; Флойд&ndash;Уоршолл и оценка моста</div>
<div class="bt-example">
    <p>Тот же граф. <strong>Начальная матрица dist:</strong></p>
    <table class="table table-bordered table-condensed bt-matrix">
        <thead><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr></thead>
        <tbody>
            <tr><td><strong>A</strong></td><td>0</td><td>2</td><td>1</td><td>&infin;</td><td>&infin;</td></tr>
            <tr><td><strong>B</strong></td><td>2</td><td>0</td><td>3</td><td>&infin;</td><td>&infin;</td></tr>
            <tr><td><strong>C</strong></td><td>1</td><td>3</td><td>0</td><td>5</td><td>&infin;</td></tr>
            <tr><td><strong>D</strong></td><td>&infin;</td><td>&infin;</td><td>5</td><td>0</td><td>4</td></tr>
            <tr><td><strong>E</strong></td><td>&infin;</td><td>&infin;</td><td>&infin;</td><td>4</td><td>0</td></tr>
        </tbody>
    </table>

    <div class="bt-iter-row">
        <div class="bt-iter-step">
            <div class="bt-iter-label">k = C</div>
            <p>dist[A][D]&nbsp;=&nbsp;min(&infin;,&nbsp;1+5)&nbsp;=&nbsp;<strong>6</strong><br>
            dist[B][D]&nbsp;=&nbsp;min(&infin;,&nbsp;3+5)&nbsp;=&nbsp;<strong>8</strong></p>
        </div>
        <div class="bt-iter-sep">&rarr;</div>
        <div class="bt-iter-step">
            <div class="bt-iter-label">k = D</div>
            <p>dist[A][E]&nbsp;=&nbsp;6+4&nbsp;=&nbsp;<strong>10</strong><br>
            dist[B][E]&nbsp;=&nbsp;8+4&nbsp;=&nbsp;<strong>12</strong><br>
            dist[C][E]&nbsp;=&nbsp;5+4&nbsp;=&nbsp;<strong>9</strong></p>
        </div>
        <div class="bt-iter-sep">&rarr;</div>
        <div class="bt-iter-step">
            <div class="bt-iter-label">итог</div>
            <p><strong>база</strong>&nbsp;=<br>2+1+6+10+3+8<br>+12+5+9+4&nbsp;=&nbsp;<strong>60</strong></p>
        </div>
    </div>

    <p><strong>Удаляем мост C&ndash;D.</strong> Компоненты {A,B,C} и {D,E} теряют связность:</p>
    <table class="table table-bordered table-condensed bt-matrix">
        <thead><tr><th>dist&prime;</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr></thead>
        <tbody>
            <tr><td><strong>A</strong></td><td>0</td><td>2</td><td>1</td><td class="bt-inf">&infin;</td><td class="bt-inf">&infin;</td></tr>
            <tr><td><strong>B</strong></td><td>2</td><td>0</td><td>3</td><td class="bt-inf">&infin;</td><td class="bt-inf">&infin;</td></tr>
            <tr><td><strong>C</strong></td><td>1</td><td>3</td><td>0</td><td class="bt-inf">&infin;</td><td class="bt-inf">&infin;</td></tr>
            <tr><td><strong>D</strong></td><td class="bt-inf">&infin;</td><td class="bt-inf">&infin;</td><td class="bt-inf">&infin;</td><td>0</td><td>4</td></tr>
            <tr><td><strong>E</strong></td><td class="bt-inf">&infin;</td><td class="bt-inf">&infin;</td><td class="bt-inf">&infin;</td><td>4</td><td>0</td></tr>
        </tbody>
    </table>
    <p>
        новая_сумма конечных пар&nbsp;=&nbsp;10;&nbsp;&nbsp;
        &delta;&nbsp;=&nbsp;&infin;&nbsp;&mdash;
        <strong>граф распался, связность нарушена полностью</strong>.
    </p>
</div>

<!-- Complexity -->
<div class="bt-section-title">Сложность алгоритмов</div>
<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>Этап</th>
            <th>Время</th>
            <th>Память</th>
            <th>Назначение</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Тарьян (мосты)</td>
            <td>O(V&nbsp;+&nbsp;E)</td>
            <td>O(V)</td>
            <td>Поиск всех мостов</td>
        </tr>
        <tr>
            <td>Флойд&ndash;Уоршолл</td>
            <td>O(V&sup3;)</td>
            <td>O(V&sup2;)</td>
            <td>Все кратчайшие пути; базовая сумма</td>
        </tr>
        <tr>
            <td>Оценка N мостов</td>
            <td>O(N&middot;V&sup3;)</td>
            <td>O(V&sup2;)</td>
            <td>N &mdash; количество найденных мостов</td>
        </tr>
    </tbody>
</table>
