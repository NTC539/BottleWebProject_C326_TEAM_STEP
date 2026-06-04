% rebase('layout.tpl', title='Теория — Мосты Тарьяна', year=year, active_page='bridges')
<link rel="stylesheet" type="text/css" href="/static/content/bridges_theory.css?v=2">

<!-- СЕКЦИЯ 1: Навигация -->
<div class="bt-header">
    <h1>Мосты Тарьяна &amp; Флойд&ndash;Уоршолл</h1>
    <a href="/bridges/practice" class="btn btn-primary btn-lg">К практике &rarr;</a>
</div>

<!-- СЕКЦИЯ 2: Ошибка -->
% if defined('error') and error:
<div class="alert alert-danger">{{error}}</div>
% end

<!-- СЕКЦИЯ 3: Содержание -->

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
            <li>Для исходной сети &mdash; матрицы весов, смежности и кратчайших
                путей (Флойд&ndash;Уоршолл) и сумма путей <code>total_path_sum</code></li>
            <li>Для каждого графа без одного моста &mdash; те же три матрицы</li>
            <li>Вывод матриц и графа по каждому состоянию сети</li>
        </ol>
    </div>
</div>

<div class="bt-section-title">Ключевые переменные</div>
<div class="bt-defs">
    <div class="bt-def-chip"><code>disc[v]</code> &mdash; момент первого посещения вершины v (таймер DFS)</div>
    <div class="bt-def-chip"><code>low[v]</code> &mdash; минимальный disc, достижимый из поддерева v</div>
    <div class="bt-def-chip"><code>weight[i][j]</code> &mdash; вес прямого ребра (0 на диагонали, &infin; если ребра нет)</div>
    <div class="bt-def-chip"><code>adj[i][j]</code> &mdash; матрица смежности (1 если есть ребро, иначе 0)</div>
    <div class="bt-def-chip"><code>dist[i][j]</code> &mdash; кратчайшее расстояние от i до j</div>
    <div class="bt-def-chip"><code>total_path_sum</code> &mdash; суммарная длина кратчайших путей исходной сети (пары i&nbsp;&lt;&nbsp;j, с учётом &infin;)</div>
</div>

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
            Флойд&ndash;Уоршолл &mdash; матрицы
            <span class="bt-algo-complexity">O(V&sup3;) / O(V&sup2;)</span>
        </div>
        <div class="bt-algo-body">
            <p>Для каждого графа строятся три матрицы:
            <code>weight[i][j]</code> (вес прямого ребра),
            <code>adj[i][j]</code> (смежность 0/1) и
            <code>dist[i][j]</code> (кратчайшие пути).</p>
            <p><code>dist[i][i]&nbsp;=&nbsp;0</code>, <code>dist[i][j]&nbsp;=&nbsp;w</code>
            если ребро есть, иначе <code>&infin;</code>; затем уточняется через
            промежуточную вершину <em>k</em>.</p>
        </div>
    </div>

</div>

<div class="bt-section-title">Описание алгоритма</div>
<div class="bt-description">
    <p>
        <strong>Шаг 1. Подготовка.</strong>
        Граф задаётся списком рёбер вида (u,&nbsp;v,&nbsp;w), где w &mdash;
        вес (длина). Для алгоритма Тарьяна каждой вершине присваивается начальное
        значение <code>disc[v]&nbsp;=&nbsp;&minus;1</code> (не посещена) и заводится
        глобальный счётчик <code>timer&nbsp;=&nbsp;0</code>.
    </p>
    <p>
        <strong>Шаг 2. Поиск мостов &mdash; DFS Тарьяна.</strong>
        Алгоритм выполняет обход в глубину. При первом визите в вершину
        <em>v</em> фиксируется <code>disc[v]&nbsp;=&nbsp;low[v]&nbsp;=&nbsp;timer++</code>.
        Далее перебираются все соседи <em>u</em>. Если сосед ещё не посещён,
        рекурсия уходит в него, а после возврата значение
        <code>low[v]</code> обновляется до минимума с <code>low[u]</code>:
        это отражает, насколько «высоко» поддерево <em>u</em> может дотянуться
        по обратным рёбрам. Если сосед уже посещён и это не родитель по DFS-дереву,
        значит найдено обратное ребро &mdash; <code>low[v]</code> снижается до
        <code>disc[u]</code>. Сразу после возврата из потомка <em>u</em> проверяется
        условие моста: если <code>low[u]&nbsp;&gt;&nbsp;disc[v]</code>, то ребро
        {v,&nbsp;u} &mdash; мост, и оно сохраняется в список.
    </p>
    <p>
        <strong>Шаг 3. Матрицы исходной сети.</strong>
        Для исходного графа строятся три матрицы: матрица весов
        <code>weight[i][j]</code> (вес прямого ребра, 0 на диагонали,
        <code>&infin;</code> при отсутствии ребра), матрица смежности
        <code>adj[i][j]</code> (1 при наличии прямого ребра, иначе 0) и
        матрица кратчайших путей <code>dist[i][j]</code> (Флойд&ndash;Уоршолл:
        вводится промежуточная вершина <em>k</em>, и для каждой пары
        (i,&nbsp;j) проверяется, не короче ли путь через <em>k</em>).
    </p>
    <p>
        <strong>Шаг 4. Суммарная длина путей &mdash; один раз.</strong>
        По матрице <code>dist</code> исходной сети считается
        <code>total_path_sum</code> &mdash; сумма кратчайших расстояний по всем
        парам <em>i&nbsp;&lt;&nbsp;j</em> с учётом <code>&infin;</code>.
        Если хотя бы одна пара недостижима, сумма равна <code>&infin;</code>.
        Эта величина вычисляется <strong>только для исходного графа</strong>.
    </p>
    <p>
        <strong>Шаг 5. Графы без мостов.</strong>
        Для каждого ребра из списка мостов строится копия списка рёбер, из
        которой удаляется это ребро. Для полученного графа заново строятся те же
        три матрицы &mdash; <code>weight</code>, <code>adj</code> и
        <code>dist</code>. Так наглядно видно, какие пары вершин теряют связь:
        в матрице <code>dist</code> между разорванными компонентами появляется
        <code>&infin;</code>.
    </p>
    <p>
        <strong>Шаг 6. Вывод.</strong>
        Результат &mdash; набор состояний сети: исходный граф и по одному графу
        на каждый мост. Для каждого состояния выводятся три матрицы и сам граф;
        мосты на графе выделяются красным.
    </p>
</div>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ: Разбор примера — зеркало практики на конкретном графе
     ═══════════════════════════════════════════════════════════ -->
<div class="bt-section-title">Разбор примера</div>
<div class="bt-example">
    <p>
        <strong>Рёбра:</strong> A&ndash;B:2, B&ndash;C:3, A&ndash;C:1, C&ndash;D:5, D&ndash;E:4.<br>
        Подграф {A,&nbsp;B,&nbsp;C} образует цикл &mdash; обратные рёбра снижают low.
        Цепочка C&ndash;D&ndash;E без обходных путей.
    </p>

    <!-- (а) Тарьян: трассировка DFS -->
    <p><strong>Шаг 1. Поиск мостов (Тарьян, DFS).</strong>
        Обход стартует из A. После возврата из каждого потомка <em>u</em> к
        родителю <em>v</em> проверяется условие <code>low[u]&nbsp;&gt;&nbsp;disc[v]</code>.</p>
    <table class="table table-bordered table-condensed">
        <thead>
            <tr>
                <th>Ребро (v&ndash;u)</th>
                <th>disc[v]</th>
                <th>low[u]</th>
                <th>low[u] &gt; disc[v]?</th>
                <th>Мост?</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>A&ndash;B</td><td>0</td><td>0</td><td>Нет</td><td>Нет</td></tr>
            <tr><td>B&ndash;C</td><td>1</td><td>0</td><td>Нет</td><td>Нет</td></tr>
            <tr><td>A&ndash;C <span class="bt-note">(обратное ребро)</span></td><td>0</td><td>0</td><td>Нет</td><td>Нет</td></tr>
            <tr class="bt-row-bridge">
                <td>C&ndash;D</td><td>2</td><td>3</td><td><strong>Да</strong></td><td><strong>Да</strong></td>
            </tr>
            <tr class="bt-row-bridge">
                <td>D&ndash;E</td><td>3</td><td>4</td><td><strong>Да</strong></td><td><strong>Да</strong></td>
            </tr>
        </tbody>
    </table>
    <p>Условие срабатывает на рёбрах C&ndash;D и D&ndash;E: из поддеревьев D и E
        нет обратных рёбер выше. <strong>Мосты &mdash; C&ndash;D и D&ndash;E.</strong>
        {A,&nbsp;B,&nbsp;C} связаны циклом, D и E держатся только на мостах.</p>

    <!-- (б) Состояния сети: те же матрицы и граф, что выдаёт практика -->
    <p><strong>Шаг 2. Матрицы и графы по состояниям сети.</strong>
        Для исходной сети и для каждого графа без моста строятся те же три
        матрицы и граф, что и на практике.</p>

    % verts = ['A', 'B', 'C', 'D', 'E']
    % INF = 'н/д'   # метка недостижимости в матрицах — как на практике
    %
    % states = [
    %   {
    %     'title': 'Исходная сеть',
    %     'gid': 'orig',
    %     'note': 'Сумма кратчайших путей <code>total_path_sum</code> = '
    %             '2+1+6+10+3+8+12+5+9+4 = <strong>60</strong> (пары i &lt; j).',
    %     'weight': [['0','2','1',INF,INF],['2','0','3',INF,INF],['1','3','0','5',INF],[INF,INF,'5','0','4'],[INF,INF,INF,'4','0']],
    %     'adj':    [['0','1','1','0','0'],['1','0','1','0','0'],['1','1','0','1','0'],['0','0','1','0','1'],['0','0','0','1','0']],
    %     'dist':   [['0','2','1','6','10'],['2','0','3','8','12'],['1','3','0','5','9'],['6','8','5','0','4'],['10','12','9','4','0']],
    %   },
    %   {
    %     'title': 'Без моста C–D',
    %     'gid': 'no_cd',
    %     'note': 'Сеть распалась на компоненты {A,&nbsp;B,&nbsp;C} и {D,&nbsp;E}; '
    %             'в <code>dist</code> между ними &mdash; <code>н/д</code>.',
    %     'weight': [['0','2','1',INF,INF],['2','0','3',INF,INF],['1','3','0',INF,INF],[INF,INF,INF,'0','4'],[INF,INF,INF,'4','0']],
    %     'adj':    [['0','1','1','0','0'],['1','0','1','0','0'],['1','1','0','0','0'],['0','0','0','0','1'],['0','0','0','1','0']],
    %     'dist':   [['0','2','1',INF,INF],['2','0','3',INF,INF],['1','3','0',INF,INF],[INF,INF,INF,'0','4'],[INF,INF,INF,'4','0']],
    %   },
    %   {
    %     'title': 'Без моста D–E',
    %     'gid': 'no_de',
    %     'note': 'Вершина E недостижима из остальных &mdash; в <code>dist</code> '
    %             'её строка и столбец равны <code>н/д</code>.',
    %     'weight': [['0','2','1',INF,INF],['2','0','3',INF,INF],['1','3','0','5',INF],[INF,INF,'5','0',INF],[INF,INF,INF,INF,'0']],
    %     'adj':    [['0','1','1','0','0'],['1','0','1','0','0'],['1','1','0','1','0'],['0','0','1','0','0'],['0','0','0','0','0']],
    %     'dist':   [['0','2','1','6',INF],['2','0','3','8',INF],['1','3','0','5',INF],['6','8','5','0',INF],[INF,INF,INF,INF,'0']],
    %   },
    % ]

    % for st in states:
    <div class="bt-state">
        <div class="bt-state-title">{{ st['title'] }}</div>

        <div class="bt-matrix-grid">
            % mats = [('Матрица весов', st['weight'], True), ('Матрица смежности', st['adj'], False), ('Кратчайшие пути', st['dist'], True)]
            % for mtitle, rows, mark_inf in mats:
            <div class="bt-matrix-card">
                <h2>{{ mtitle }}</h2>
                <table class="table table-bordered table-condensed bt-matrix">
                    <thead>
                        <tr>
                            <th></th>
                            % for v in verts:
                            <th>{{ v }}</th>
                            % end
                        </tr>
                    </thead>
                    <tbody>
                        % for ri, rv in enumerate(verts):
                        <tr>
                            <th>{{ rv }}</th>
                            % for cell in rows[ri]:
                            <td class="{{ 'bt-inf' if mark_inf and cell == INF else '' }}">{{ cell }}</td>
                            % end
                        </tr>
                        % end
                    </tbody>
                </table>
            </div>
            % end
        </div>

        <p class="bt-state-note">{{!st['note']}}</p>
        <p class="bt-graph-hint">
            Красные рёбра &mdash; мосты, серые &mdash; обычные дороги.
            Подписи на рёбрах &mdash; веса.
        </p>
        <div class="bt-graph" id="bt-graph-{{ st['gid'] }}"></div>
    </div>
    % end
</div>

<!-- Визуализация графов по состояниям (vis-network, локальный файл из layout.tpl) -->
<script>
(function () {
    if (typeof vis === 'undefined') { return; }

    // Мосты исходной сети — выделяются красным во всех состояниях (как на практике)
    var BRIDGES = { 'C|D': true, 'D|E': true };
    function keyOf(a, b) { return a < b ? a + '|' + b : b + '|' + a; }

    var VERTS = ['A', 'B', 'C', 'D', 'E'];

    var STATES = [
        { gid: 'orig',  E: [['A','B',2],['B','C',3],['A','C',1],['C','D',5],['D','E',4]] },
        { gid: 'no_cd', E: [['A','B',2],['B','C',3],['A','C',1],['D','E',4]] },
        { gid: 'no_de', E: [['A','B',2],['B','C',3],['A','C',1],['C','D',5]] }
    ];

    function buildNet(s) {
        var container = document.getElementById('bt-graph-' + s.gid);
        if (!container) { return; }

        var nodes = VERTS.map(function (n) {
            return {
                id: n, label: n, shape: 'ellipse',
                color: { background: '#e8f4fb', border: '#2e86ab' },
                font: { color: '#1a3a5c', size: 16 }
            };
        });

        var edges = s.E.map(function (e) {
            var isBridge = BRIDGES[keyOf(e[0], e[1])];
            return {
                from: e[0], to: e[1], label: String(e[2]),
                font: { align: 'top', size: 12, color: '#526173' },
                width: isBridge ? 3 : 1,
                color: { color: isBridge ? '#e84855' : '#9bb8cc' },
                smooth: { type: 'continuous' }
            };
        });

        var data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
        var options = {
            physics: { enabled: true, stabilization: true },
            interaction: { dragNodes: true, dragView: true, zoomView: true }
        };
        var net = new vis.Network(container, data, options);
        net.once('afterDrawing', function () { net.fit({ animation: false }); });
    }

    STATES.forEach(buildNet);
})();
</script>
