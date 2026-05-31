<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - GraphAlgo</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/vis-network.min.js"></script>
</head>

% ap = defined('active_page') and active_page or ''
<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">GraphAlgo</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li class="{{ 'active' if ap == 'home' else '' }}"><a href="/">Главная</a></li>
                    <li class="{{ 'active' if ap == 'about' else '' }}"><a href="/about">О нас</a></li>
                    <li class="{{ 'active' if ap == 'graph_theory' else '' }}"><a href="/graph_theory">Теория графов</a></li>
                    <li class="dropdown {{ 'active' if ap in ['dijkstra', 'bridges', 'cpm', 'coloring', 'algorithms'] else '' }}">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button"
                           aria-haspopup="true" aria-expanded="false">
                            Алгоритмы <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a href="/dijkstra">Алгоритм Дейкстры</a></li>
                            <li><a href="/bridges">Мосты Тарьяна</a></li>
                            <li><a href="/cpm">Критический путь</a></li>
                            <li><a href="/coloring">Раскраска графа</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <main class="container body-content">
        {{!base}}
    </main>

    <footer class="site-footer">
        <div class="container">
            GraphAlgo
        </div>
    </footer>

    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
    <script src="/static/scripts/graph-input.js"></script>
</body>
</html>
