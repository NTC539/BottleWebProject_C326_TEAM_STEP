% rebase('layout.tpl', title='Об авторе', year=year, active_page='author')

<h2>Об авторе</h2>
<p class="lead">Участники команды 1 и их индивидуальные задания.</p>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Антон — Вариант 1</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Антон</dd>
            <dt>Вариант №</dt>
            <dd>1</dd>
            <dt>Алгоритм</dt>
            <dd>Алгоритм Дейкстры (OSPF)</dd>
            <dt>Описание задачи</dt>
            <dd>
                Реализация алгоритма Дейкстры для нахождения кратчайших путей от одной вершины
                до всех остальных в графе с неотрицательными весами рёбер.
                Алгоритм применяется в протоколе маршрутизации OSPF для построения дерева
                кратчайших путей в компьютерных сетях.
            </dd>
        </dl>
        <a href="/dijkstra" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Дмитрий — Вариант 2</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Дмитрий</dd>
            <dt>Вариант №</dt>
            <dd>2</dd>
            <dt>Алгоритм</dt>
            <dd>Мосты Тарьяна</dd>
            <dt>Описание задачи</dt>
            <dd>
                Нахождение мостов и точек сочленения в неориентированном графе методом
                обхода в глубину (алгоритм Тарьяна).
                Применяется для анализа устойчивости и связности сетевых топологий.
            </dd>
        </dl>
        <a href="/bridges" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Эдуард — Вариант 3</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Эдуард</dd>
            <dt>Вариант №</dt>
            <dd>3</dd>
            <dt>Алгоритм</dt>
            <dd>Критический путь (CPM)</dd>
            <dt>Описание задачи</dt>
            <dd>
                Метод критического пути (Critical Path Method) для планирования и управления
                проектами на основе сетевого графа работ.
                Позволяет определить минимальное время выполнения проекта и выявить работы,
                задержка которых ведёт к задержке всего проекта.
            </dd>
        </dl>
        <a href="/cpm" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>

<div class="panel panel-default author-panel">
    <div class="panel-heading">
        <h3 class="panel-title">Иван — Вариант 4</h3>
    </div>
    <div class="panel-body">
        <dl class="dl-horizontal">
            <dt>ФИО</dt>
            <dd>Иван</dd>
            <dt>Вариант №</dt>
            <dd>4</dd>
            <dt>Алгоритм</dt>
            <dd>Раскраска графа</dd>
            <dt>Описание задачи</dt>
            <dd>
                Раскраска вершин графа минимальным числом цветов так, чтобы никакие две
                смежные вершины не имели одинакового цвета (задача хроматического числа).
                Применяется при составлении расписаний и распределении ресурсов.
            </dd>
        </dl>
        <a href="/coloring" class="btn btn-primary">Перейти к алгоритму</a>
    </div>
</div>
