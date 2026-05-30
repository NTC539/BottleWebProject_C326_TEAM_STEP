% rebase('layout.tpl', title='Главная', year=year, active_page='home')

<div class="jumbotron">
    <h1>Задачи на теории графов</h1>
    <p class="lead">Алгоритмы на теории графов</p>
    <p>
        Сайт решает задачи маршрутизации сетей, анализа устойчивости и управления проектами
        с помощью алгоритмов теории графов, реализованных на Python / Bottle.
        Каждый раздел содержит теоретическую базу и интерактивную практическую часть,
        позволяющую запустить алгоритм на собственных данных.
    </p>
</div>

<div class="row row-cards">
    <div class="col-md-3">
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">Алгоритм Дейкстры</h3>
            </div>
            <div class="panel-body">
                <p>Нахождение кратчайших путей в графе. Применяется в протоколе маршрутизации OSPF.</p>
                <a href="/dijkstra" class="btn btn-primary btn-block">Подробнее &raquo;</a>
            </div>
            <div class="panel-footer text-muted">Садеков</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="panel panel-success">
            <div class="panel-heading">
                <h3 class="panel-title">Мосты Тарьяна</h3>
            </div>
            <div class="panel-body">
                <p>Поиск мостов и точек сочленения графа для анализа устойчивости сети.</p>
                <a href="/bridges" class="btn btn-success btn-block">Подробнее &raquo;</a>
            </div>
            <div class="panel-footer text-muted">Тигранян</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="panel panel-warning">
            <div class="panel-heading">
                <h3 class="panel-title">Критический путь</h3>
            </div>
            <div class="panel-body">
                <p>Метод критического пути (CPM) для управления проектами и составления расписаний.</p>
                <a href="/cpm" class="btn btn-warning btn-block">Подробнее &raquo;</a>
            </div>
            <div class="panel-footer text-muted">Езерский</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="panel panel-danger">
            <div class="panel-heading">
                <h3 class="panel-title">Раскраска графа</h3>
            </div>
            <div class="panel-body">
                <p>Раскраска вершин графа минимальным числом цветов. Применяется при составлении расписаний.</p>
                <a href="/coloring" class="btn btn-danger btn-block">Подробнее &raquo;</a>
            </div>
            <div class="panel-footer text-muted">Петренко</div>
        </div>
    </div>
</div>
