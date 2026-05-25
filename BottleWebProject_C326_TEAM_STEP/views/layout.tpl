<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - GraphAlgo | Команда 1</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
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
                <a href="/" class="navbar-brand">GraphAlgo | Команда 1</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li class="{{ 'active' if ap == 'home' else '' }}"><a href="/">Главная</a></li>
                    <li class="{{ 'active' if ap == 'about' else '' }}"><a href="/about">О нас</a></li>
                    <li class="dropdown {{ 'active' if ap == 'algorithms' else '' }}">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button"
                           aria-haspopup="true" aria-expanded="false">
                            Алгоритмы <span class="caret"></span>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a href="/dijkstra">Алгоритм Дейкстры (V1)</a></li>
                            <li><a href="/bridges">Мосты Тарьяна (V2)</a></li>
                            <li><a href="/cpm">Критический путь (V3)</a></li>
                            <li><a href="/coloring">Раскраска графа (V4)</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">
        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - GraphAlgo | Команда 1 | УП02 ПМ02 | 09.02.07</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
    <script src="/static/scripts/graph-input.js"></script>

</body>
</html>
