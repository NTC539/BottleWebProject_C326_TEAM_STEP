% rebase('layout.tpl', title='О проекте', year=year, active_page='about')

<div class="theory-section">
    <h2><span style="color:#2e86ab; margin-right:8px;">&#9432;</span> О проекте</h2>
    <p>
        Проект — многостраничное веб-приложение на фреймворке Bottle (Python),
        разработанное в рамках учебной практики УП02 по ПМ02 «Осуществление
        интеграции программных модулей» специальности 09.02.07 «Информационные
        системы и программирование». Тематика — алгоритмы на графах:
        маршрутизация, поиск мостов, критический путь в проекте, раскраска графа.
    </p>
</div>

<div class="theory-section">
    <h3>Состав команды 1</h3>
    <table class="table table-bordered table-striped">
        <thead>
            <tr>
                <th>Участник</th>
                <th>Роль</th>
                <th>Вариант</th>
                <th>Алгоритм</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Садеков Дмитрий</td>
                <td>Разработчик, тестирование</td>
                <td>1</td>
                <td>Алгоритм Дейкстры (OSPF)</td>
            </tr>
            <tr>
                <td>Тигранян Эдуард</td>
                <td>Разработчик, архитектура проекта</td>
                <td>2</td>
                <td>Мосты Тарьяна</td>
            </tr>
            <tr>
                <td>Езерский Иван</td>
                <td>Разработчик, документация</td>
                <td>3</td>
                <td>Критический путь (CPM)</td>
            </tr>
            <tr>
                <td>Петренко Антон</td>
                <td>Разработчик, дизайн интерфейса</td>
                <td>4</td>
                <td>Раскраска графа</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Садеков Дмитрий — Вариант 1</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Садеков Дмитрий</dd>
            <dt>Роль</dt>
            <dd>Разработчик, тестирование</dd>
            <dt>Вариант №</dt>
            <dd>1</dd>
            <dt>Алгоритм</dt>
            <dd>Алгоритм Дейкстры (OSPF)</dd>
            <dt>Задача</dt>
            <dd>
                Реализация алгоритма Дейкстры для нахождения маршрута
                с минимальной задержкой в компьютерной сети, заданной взвешенным
                ориентированным графом. Рёбра с весом ∞ считаются временно
                недоступными (модификация для метрики OSPF).
            </dd>
        </dl>
        <a href="/dijkstra" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Тигранян Эдуард — Вариант 2</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Тигранян Эдуард</dd>
            <dt>Роль</dt>
            <dd>Разработчик, архитектура проекта</dd>
            <dt>Вариант №</dt>
            <dd>2</dd>
            <dt>Алгоритм</dt>
            <dd>Мосты Тарьяна</dd>
            <dt>Задача</dt>
            <dd>
                Поиск всех мостов в неориентированном взвешенном графе дорог
                алгоритмом Тарьяна. Для каждого моста вычисляется прирост суммарной
                длины кратчайших путей между всеми парами вершин после его удаления
                (алгоритм Флойда–Уоршелла).
            </dd>
        </dl>
        <a href="/bridges" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Езерский Иван — Вариант 3</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Езерский Иван</dd>
            <dt>Роль</dt>
            <dd>Разработчик, документация</dd>
            <dt>Вариант №</dt>
            <dd>3</dd>
            <dt>Алгоритм</dt>
            <dd>Критический путь (CPM)</dd>
            <dt>Задача</dt>
            <dd>
                Нахождение критического пути в ориентированном ациклическом
                графе проекта — вершины соответствуют задачам, рёбра задают
                зависимости, вес вершины — длительность задачи. Применяются
                топологическая сортировка и динамическое программирование.
            </dd>
        </dl>
        <a href="/cpm" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Петренко Антон — Вариант 4</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Петренко Антон</dd>
            <dt>Роль</dt>
            <dd>Разработчик, дизайн интерфейса</dd>
            <dt>Вариант №</dt>
            <dd>4</dd>
            <dt>Алгоритм</dt>
            <dd>Раскраска графа</dd>
            <dt>Задача</dt>
            <dd>
                Раскраска вершин графа конфликтов учебного расписания
                в минимальное число цветов (смен) так, чтобы конфликтующие
                дисциплины не попадали в одну смену. Алгоритм Welsh–Powell
                с локальной оптимизацией.
            </dd>
        </dl>
        <a href="/coloring" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>
