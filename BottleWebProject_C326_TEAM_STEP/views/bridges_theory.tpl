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
<div class="bt-accordion-controls">
    <button class="btn btn-default btn-sm bt-ctrl-btn" id="bt-open-all">Открыть всё</button>
    <button class="btn btn-default btn-sm bt-ctrl-btn" id="bt-close-all">Закрыть всё</button>
</div>

<div class="panel-group bt-panel-group" id="bt-accordion" role="tablist" aria-multiselectable="true">

    <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="bt-h1">
            <h4 class="panel-title">
                <a role="button" data-toggle="collapse"
                   href="#bt-c1" aria-expanded="true" aria-controls="bt-c1">
                    1. Мосты и точки сочленения в графе
                </a>
            </h4>
        </div>
        <div id="bt-c1" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="bt-h1">
            <div class="panel-body">
                <p>
                    <strong>Мост</strong> &mdash; ребро <em>e &isin; E</em>
                    неориентированного графа G&nbsp;=&nbsp;(V,&nbsp;E), удаление которого
                    увеличивает число компонент связности. Мост &mdash; единственный путь
                    между двумя частями графа.
                </p>
                <p>
                    <strong>Точка сочленения</strong> &mdash; вершина, удаление которой
                    (вместе со всеми инцидентными рёбрами) также увеличивает число
                    компонент связности графа.
                </p>
                <p>
                    В транспортных и телекоммуникационных сетях мосты &mdash; критически
                    важные звенья: выход из строя одного ребра-моста изолирует часть сети.
                </p>
                <p>Алгоритм решает задачу в четыре этапа:</p>
                <ol>
                    <li>Поиск всех мостов алгоритмом Тарьяна (DFS).</li>
                    <li>Вычисление суммарной длины путей исходного графа (Флойд&ndash;Уоршолл).</li>
                    <li>Оценка каждого моста: Флойд&ndash;Уоршолл без данного ребра,
                        &delta;&nbsp;=&nbsp;новая_сумма&nbsp;&minus;&nbsp;база.</li>
                    <li>Формирование результата &mdash; список (u,&nbsp;v,&nbsp;w,&nbsp;&delta;)
                        для каждого моста.</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="bt-h2">
            <h4 class="panel-title">
                <a role="button" data-toggle="collapse"
                   href="#bt-c2" aria-expanded="false" aria-controls="bt-c2" class="collapsed">
                    2. Алгоритм Тарьяна: DFS-обход и формула low[v]
                </a>
            </h4>
        </div>
        <div id="bt-c2" class="panel-collapse collapse" role="tabpanel" aria-labelledby="bt-h2">
            <div class="panel-body">
                <p>Алгоритм находит все мосты за линейное время
                <strong>O(V&nbsp;+&nbsp;E)</strong> с помощью поиска в глубину (DFS).</p>
                <p>Для каждой вершины v вычисляются два значения:</p>
                <ul>
                    <li>
                        <code>disc[v]</code> &mdash; момент первого посещения (таймер DFS)
                    </li>
                    <li>
                        <code>low[v]</code> &mdash; минимальный <code>disc</code> среди
                        всех вершин, достижимых из поддерева v по DFS-рёбрам и одному
                        обратному ребру
                    </li>
                </ul>
                <p>
                    <strong>Критерий моста:</strong> ребро {v,&nbsp;u} является мостом,
                    если <code>low[u]&nbsp;&gt;&nbsp;disc[v]</code>.
                </p>
                <p>Псевдокод:</p>
<pre class="algo-block">DFS(v, parent):
  disc[v] = low[v] = timer; timer++
  for u in adj[v]:
    if u == parent:
      continue                          # не обратное ребро — пропуск
    if disc[u] == -1:                   # вершина не посещена
      DFS(u, v)
      low[v] = min(low[v], low[u])
      if low[u] > disc[v]:
        bridges.add({v, u})             # ребро — мост
    else:
      low[v] = min(low[v], disc[u])     # обратное ребро</pre>
                <p>
                    Инициализация: все <code>disc[v]&nbsp;=&nbsp;&minus;1</code> до запуска;
                    <code>timer&nbsp;=&nbsp;0</code>.
                    Если <code>disc[u]&nbsp;!=&nbsp;&minus;1</code> &mdash; вершина уже
                    посещена, ребро обратное, обновляем <code>low[v]</code>.
                </p>
            </div>
        </div>
    </div>

    <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="bt-h3">
            <h4 class="panel-title">
                <a role="button" data-toggle="collapse"
                   href="#bt-c3" aria-expanded="false" aria-controls="bt-c3" class="collapsed">
                    3. Алгоритм Флойда&ndash;Уоршолла: матрица расстояний
                </a>
            </h4>
        </div>
        <div id="bt-c3" class="panel-collapse collapse" role="tabpanel" aria-labelledby="bt-h3">
            <div class="panel-body">
                <p>Находит кратчайшие пути между <em>всеми</em> парами вершин
                за <strong>O(V&sup3;)</strong>.</p>
                <p>Инициализация матрицы расстояний dist[i][j]:</p>
                <ul>
                    <li><code>dist[i][i]&nbsp;=&nbsp;0</code> для всех вершин</li>
                    <li><code>dist[i][j]&nbsp;=&nbsp;w</code> (вес ребра), если ребро {i,&nbsp;j} существует</li>
                    <li><code>dist[i][j]&nbsp;=&nbsp;&infin;</code>, если прямого ребра нет</li>
                </ul>
                <p>Тройной цикл по промежуточной вершине k:</p>
<pre class="algo-block">for k in range(n):
  for i in range(n):
    for j in range(n):
      dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])</pre>
                <p>
                    <strong>Базовая сумма:</strong>
                    база&nbsp;=&nbsp;&Sigma;&nbsp;dist[i][j]
                    для всех пар i&nbsp;&lt;&nbsp;j, где dist[i][j]&nbsp;&ne;&nbsp;&infin;.
                </p>
                <p>
                    <strong>Оценка моста {u,&nbsp;v}:</strong> строится G'&nbsp;=&nbsp;G
                    без данного ребра, запускается Флойд&ndash;Уоршолл, вычисляется
                    новая_сумма. Прирост потерь &delta;&nbsp;=&nbsp;новая_сумма&nbsp;&minus;&nbsp;база.
                    Если &delta;&nbsp;=&nbsp;&infin; &mdash; граф распался (вершины
                    стали недостижимы).
                </p>
            </div>
        </div>
    </div>

    <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="bt-h4">
            <h4 class="panel-title">
                <a role="button" data-toggle="collapse"
                   href="#bt-c4" aria-expanded="false" aria-controls="bt-c4" class="collapsed">
                    4. Пример: граф из 5 вершин &mdash; найти мосты вручную
                </a>
            </h4>
        </div>
        <div id="bt-c4" class="panel-collapse collapse" role="tabpanel" aria-labelledby="bt-h4">
            <div class="panel-body">
                <p>
                    <strong>Граф:</strong> вершины A, B, C, D, E.<br>
                    <strong>Рёбра:</strong> A&ndash;B:2, B&ndash;C:3, A&ndash;C:1,
                    C&ndash;D:5, D&ndash;E:4.
                </p>
                <p>
                    Подграф {A,&nbsp;B,&nbsp;C} образует цикл (три ребра) &mdash;
                    обратные рёбра снижают low. Цепочка C&ndash;D&ndash;E без обходных путей.
                </p>
                <table class="table table-bordered table-condensed">
                    <thead>
                        <tr>
                            <th>Ребро</th>
                            <th>Условие low[u] &gt; disc[v]</th>
                            <th>Мост?</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>A&ndash;B</td>
                            <td>low[B]&nbsp;=&nbsp;0, disc[A]&nbsp;=&nbsp;0 &rarr; нет</td>
                            <td>Нет</td>
                        </tr>
                        <tr>
                            <td>B&ndash;C</td>
                            <td>low[C]&nbsp;=&nbsp;0, disc[B]&nbsp;=&nbsp;1 &rarr; нет</td>
                            <td>Нет</td>
                        </tr>
                        <tr>
                            <td>A&ndash;C</td>
                            <td>low[C]&nbsp;=&nbsp;0, disc[A]&nbsp;=&nbsp;0 &rarr; нет</td>
                            <td>Нет</td>
                        </tr>
                        <tr class="success">
                            <td>C&ndash;D</td>
                            <td>low[D]&nbsp;=&nbsp;3, disc[C]&nbsp;=&nbsp;2
                                &rarr; <strong>да</strong></td>
                            <td><strong>Да</strong></td>
                        </tr>
                        <tr class="success">
                            <td>D&ndash;E</td>
                            <td>low[E]&nbsp;=&nbsp;4, disc[D]&nbsp;=&nbsp;3
                                &rarr; <strong>да</strong></td>
                            <td><strong>Да</strong></td>
                        </tr>
                    </tbody>
                </table>
                <p>
                    <strong>Результат:</strong> мосты &mdash; C&ndash;D и D&ndash;E.
                    Вершины {A,&nbsp;B,&nbsp;C} связаны между собой через цикл;
                    D и E изолируются при удалении соответствующих мостов.
                </p>
            </div>
        </div>
    </div>

    <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="bt-h5">
            <h4 class="panel-title">
                <a role="button" data-toggle="collapse"
                   href="#bt-c5" aria-expanded="false" aria-controls="bt-c5" class="collapsed">
                    5. Сравнение сложности алгоритмов
                </a>
            </h4>
        </div>
        <div id="bt-c5" class="panel-collapse collapse" role="tabpanel" aria-labelledby="bt-h5">
            <div class="panel-body">
                <table class="table table-bordered table-striped">
                    <thead>
                        <tr>
                            <th>Алгоритм / этап</th>
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
                            <td>Поиск мостов и точек сочленения</td>
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
                <p>
                    Алгоритм Тарьяна эффективнее для разреженных графов.
                    Флойд&ndash;Уоршолл применяется, когда нужна полная матрица расстояний.
                </p>
            </div>
        </div>
    </div>

</div>

<script>
    $('#bt-open-all').on('click', function () {
        $('#bt-accordion .panel-collapse').collapse('show');
    });
    $('#bt-close-all').on('click', function () {
        $('#bt-accordion .panel-collapse').collapse('hide');
    });
</script>
