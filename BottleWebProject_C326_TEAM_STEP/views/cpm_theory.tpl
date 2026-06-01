% rebase('layout.tpl', title='Критический путь (CPM)', year=year)
<link rel="stylesheet" type="text/css" href="/static/content/cpm_theory.css" />

<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px;">
    <h2 style="margin:0;border:none;padding:0;">Метод критического пути (CPM) - Теория</h2>
    <a href="/cpm/practice" class="btn btn-primary btn-lg">К практике &rarr;</a>
</div>

<div class="cpm-intro-box">
    <h3>Что такое метод критического пути?</h3>
    <p>
        CPM (Critical Path Method) &mdash; метод сетевого планирования проектов,
        определяющий наиболее длинную последовательность взаимозависимых задач.
        Задержка любой задачи на критическом пути задерживает весь проект на то же время.
        Применяется в управлении строительством, разработкой ПО, производством и логистикой.
    </p>
</div>

<div class="cpm-section-title">Ключевые понятия</div>
<div class="cpm-concepts">
    <div class="cpm-concept-chip"><strong>ES</strong> &mdash; ранний старт (Early Start)</div>
    <div class="cpm-concept-chip"><strong>EF</strong> &mdash; раннее окончание (Early Finish)</div>
    <div class="cpm-concept-chip"><strong>LS</strong> &mdash; поздний старт (Late Start)</div>
    <div class="cpm-concept-chip"><strong>LF</strong> &mdash; позднее окончание (Late Finish)</div>
    <div class="cpm-concept-chip"><strong>Float</strong> &mdash; резерв времени (LS &minus; ES)</div>
</div>
<p>
    <strong>Резерв (Float)</strong> = LS &minus; ES &mdash; время, на которое задача может
    быть отложена без задержки всего проекта. Задачи критического пути имеют
    <strong>Float&nbsp;=&nbsp;0</strong>.
</p>

<div class="cpm-section-title">Алгоритм вычисления</div>

<div class="theory-section">
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

<div class="theory-section">
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

<div class="theory-section">
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

<div class="theory-section">
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

<div class="cpm-section-title">Пример: 6 задач с зависимостями</div>

<div class="theory-section">
    <h4>Дано</h4>
    <pre class="algo-block">Задачи:      A(3), B(2), C(4), D(1), E(2), F(3)
Зависимости: C&larr;A,  D&larr;{A,B},  E&larr;C,  F&larr;D
             (A и B &mdash; стартовые, без предшественников)</pre>
</div>

<div class="theory-section">
    <img src="static\images\cpm_ex_sheme_1.png"/>
</div>

<div class="theory-section">
    <h4>Шаг 1 &mdash; Топологический порядок (алгоритм Кана)</h4>
    <pre class="algo-block">in_degree: A=0, B=0, C=1, D=2, E=1, F=1
Очередь: [A, B]  (оба in_degree=0, сортировка по алфавиту)

Извлекаем A &rarr; порядок=[A];    уменьшаем: in_degree[C]=0, in_degree[D]=1
          &rarr; очередь=[B, C]
Извлекаем B &rarr; порядок=[A, B]; уменьшаем: in_degree[D]=0
          &rarr; очередь=[C, D]
...
Результат: [A, B, C, D, E, F]</pre>
</div>

<div class="theory-section">
    <h4>Шаг 2 &mdash; Прямой проход (ES, EF)</h4>
    <pre class="algo-block">A: ES=0,                              EF=0+3=3
B: ES=0,                              EF=0+2=2
C: ES=max(EF[A])=3,                   EF=3+4=7
D: ES=max(EF[A],EF[B])=max(3,2)=3,   EF=3+1=4
...
T<sub>кр</sub> = max(EF) = max(3, 2, 7, 4, 9, 7) = 9</pre>
</div>

<div class="theory-section">
    <h4>Шаг 3 &mdash; Обратный проход (LS, LF)</h4>
    <pre class="algo-block">Вершины с EF=T<sub>кр</sub>=9: E &rarr; LF[E]=9
Обратный порядок: [F, E, D, C, B, A]

E:  LF=9,                             LS=9&minus;2=7
F:  LF=9,                             LS=9&minus;3=6
...
A:  LF=min(LS[C],LS[D])=min(3,6)=3,  LS=3&minus;3=0</pre>
</div>

<div class="theory-section">
    <h4>Шаг 4 &mdash; Резервы и критический путь</h4>
    <pre class="algo-block">R = LS &minus; ES:
  A: 0&minus;0=0  &rarr; критическая
  B: 1&minus;0=1
  C: 3&minus;3=0  &rarr; критическая
  D: 6&minus;3=3
  E: 7&minus;7=0  &rarr; критическая
  F: 6&minus;4=2

Поиск критических путей:
  Стартовые критические (ES=0, R=0): A
  A(R=0) &rarr; C?  EF[A]=3 == ES[C]=3 и R[C]=0  &rarr; переходим
  C(R=0) &rarr; E?  EF[C]=7 == ES[E]=7 и R[E]=0  &rarr; переходим
  E(R=0) &rarr; нет последователей &rarr; путь завершён

Критический путь: A &rarr; C &rarr; E,  T<sub>кр</sub> = 9 ед.</pre>
</div>

<table class="table table-bordered table-striped">
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
        <tr class="danger">
            <td>A</td><td>3</td><td>&mdash;</td>
            <td>0</td><td>3</td><td>0</td><td>3</td><td>0</td>
            <td><strong>Да</strong></td>
        </tr>
        <tr>
            <td>B</td><td>2</td><td>&mdash;</td>
            <td>0</td><td>2</td><td>1</td><td>3</td><td>1</td>
            <td>Нет</td>
        </tr>
        <tr class="danger">
            <td>C</td><td>4</td><td>A</td>
            <td>3</td><td>7</td><td>3</td><td>7</td><td>0</td>
            <td><strong>Да</strong></td>
        </tr>
        <tr>
            <td>D</td><td>1</td><td>A, B</td>
            <td>3</td><td>4</td><td>6</td><td>7</td><td>3</td>
            <td>Нет</td>
        </tr>
        <tr class="danger">
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

<div class="cpm-section-title">Применение</div>
<ul class="cpm-apply-list">
    <li>Строительство и инженерные проекты</li>
    <li>Разработка программного обеспечения</li>
    <li>Производственное планирование</li>
    <li>Организация мероприятий</li>
    <li>Управление цепочками поставок</li>
</ul>