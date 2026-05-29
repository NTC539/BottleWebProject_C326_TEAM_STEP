% rebase('layout.tpl', title='Критический путь (CPM)', year=year)

<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px;">
    <h2 style="margin:0;border:none;padding:0;">Метод критического пути (CPM)</h2>
    <a href="/cpm/practice" class="btn btn-primary btn-lg">К практике &rarr;</a>
</div>

<div>
    <h3>Что такое метод критического пути?</h3>
    <p>
        CPM (Critical Path Method) &mdash; метод сетевого планирования проектов,
        определяющий наиболее длинную последовательность взаимозависимых задач.
        Задержка любой задачи на критическом пути задерживает весь проект на то же время.
        Применяется в управлении строительством, разработкой ПО, производством и логистикой.
    </p>
</div>

<div>Ключевые понятия</div>
<div>
    <div><strong>ES</strong> &mdash; ранний старт (Early Start)</div>
    <div><strong>EF</strong> &mdash; раннее окончание (Early Finish)</div>
    <div><strong>LS</strong> &mdash; поздний старт (Late Start)</div>
    <div><strong>LF</strong> &mdash; позднее окончание (Late Finish)</div>
    <div><strong>Float</strong> &mdash; резерв времени (LS &minus; ES)</div>
</div>
<p>
    <strong>Резерв (Float)</strong> = LS &minus; ES &mdash; время, на которое задача может
    быть отложена без задержки всего проекта. Задачи критического пути имеют
    <strong>Float&nbsp;=&nbsp;0</strong>.
</p>

<div>Алгоритм вычисления</div>

<div>
    <h4>Шаг 1 &mdash; Подготовка графа (Алгоритм Кана)</h4>
    <p>
        Для каждой вершины подсчитывается входящая степень (<code>in_degree</code>).
        Все вершины с <code>in_degree&nbsp;=&nbsp;0</code> добавляются в очередь
        и сортируются по алфавиту.
    </p>
    <p>
        Основной цикл: извлекается вершина V &rarr; добавляется в топологический порядок
        &rarr; для каждого последователя W уменьшается <code>in_degree[W]</code>;
        если стало 0 &mdash; W добавляется в очередь.
        Если в результате топологический порядок содержит меньше вершин, чем всего в
        графе, &mdash; граф содержит цикл (CPM неприменим).
    </p>
</div>

<div>
    <h4>Шаг 2 &mdash; Прямой проход (ES, EF)</h4>
    <p>
        Обход по топологическому порядку слева направо.
        Для стартовых задач (без предшественников): <code>ES&nbsp;=&nbsp;0</code>,
        <code>EF&nbsp;=&nbsp;ES&nbsp;+&nbsp;t</code>.
    </p>
    <p>
        Для остальных:
        <code>ES[v]&nbsp;=&nbsp;max(EF[u])</code> по всем предшественникам u;
        <code>EF[v]&nbsp;=&nbsp;ES[v]&nbsp;+&nbsp;t</code>.<br>
        Длительность проекта: <code>T<sub>кр</sub>&nbsp;=&nbsp;max(EF)</code>
        по всем вершинам.
    </p>
</div>

<div>
    <h4>Шаг 3 &mdash; Обратный проход (LS, LF)</h4>
    <p>
        Всем вершинам присваивается <code>LF&nbsp;=&nbsp;&infin;</code>.
        Вершинам, у которых <code>EF&nbsp;==&nbsp;T<sub>кр</sub></code>:
        <code>LF&nbsp;=&nbsp;T<sub>кр</sub></code>.
    </p>
    <p>
        Обход от конца к началу топологического порядка:
        <code>LF[v]&nbsp;=&nbsp;min(LS[u])</code> по всем последователям u.
        Если <code>LF[v]</code> осталось &infin; (изолированная вершина) &mdash;
        <code>LF[v]&nbsp;=&nbsp;T<sub>кр</sub></code>.
        Затем: <code>LS[v]&nbsp;=&nbsp;LF[v]&nbsp;&minus;&nbsp;t</code>.
    </p>
</div>

<div>
    <h4>Шаг 4 &mdash; Критический путь и резервы</h4>
    <p>
        Резерв каждой задачи: <code>R&nbsp;=&nbsp;LS&nbsp;&minus;&nbsp;ES</code>.
        Критические задачи &mdash; те, у которых <code>R&nbsp;=&nbsp;0</code>.
    </p>
    <p>
        Поиск критических путей: начиная со стартовых критических вершин
        (<code>ES&nbsp;=&nbsp;0</code>), рекурсивный обход только по критическим
        вершинам, для которых выполняется
        <code>EF[текущая]&nbsp;==&nbsp;ES[следующая]</code>.
    </p>
</div>

<div>Пример: 6 задач с зависимостями</div>
<table>
    <thead>
        <tr>
            <th>Задача</th>
            <th>Длит.</th>
            <th>Предшественники</th>
            <th>ES</th>
            <th>EF</th>
            <th>LS</th>
            <th>LF</th>
            <th>Float</th>
            <th>Критич.?</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>A</td><td>3</td><td>&mdash;</td>
            <td>0</td><td>3</td><td>0</td><td>3</td><td>0</td>
            <td><strong>Да</strong></td>
        </tr>
        <tr>
            <td>B</td><td>2</td><td>&mdash;</td>
            <td>0</td><td>2</td><td>1</td><td>3</td><td>1</td>
            <td>Нет</td>
        </tr>
        <tr>
            <td>C</td><td>4</td><td>A</td>
            <td>3</td><td>7</td><td>3</td><td>7</td><td>0</td>
            <td><strong>Да</strong></td>
        </tr>
        <tr>
            <td>D</td><td>1</td><td>A, B</td>
            <td>3</td><td>4</td><td>6</td><td>7</td><td>3</td>
            <td>Нет</td>
        </tr>
        <tr>
            <td>E</td><td>2</td><td>C</td>
            <td>7</td><td>9</td><td>7</td><td>9</td><td>0</td>
            <td><strong>Да</strong></td>
        </tr>
        <tr>
            <td>F</td><td>3</td><td>D</td>
            <td>4</td><td>7</td><td>6</td><td>9</td><td>2</td>
            <td>Нет</td>
        </tr>
    </tbody>
</table>
<p>
    <strong>Критический путь: A &rarr; C &rarr; E</strong>,
    длительность проекта: <strong>9 ед.</strong>
    Путь B&nbsp;&rarr;&nbsp;D&nbsp;&rarr;&nbsp;F имеет резерв 2 ед.
</p>

<div>Применение</div>
<ul>
    <li>Строительство и инженерные проекты</li>
    <li>Разработка программного обеспечения</li>
    <li>Производственное планирование</li>
    <li>Организация мероприятий</li>
    <li>Управление цепочками поставок</li>
</ul>