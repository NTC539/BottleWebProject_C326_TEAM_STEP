"""
Routes and views for the bottle application.
"""

from bottle import route, view, request
from datetime import datetime
from algorithms.coloring import color_graph
from algorithms.cpm import find_critical_path
from algorithms.bridges import analyze_network
from algorithms.dijkstra import route_network


def _year():
    return datetime.now().year


@route('/')
@route('/home')
@view('index')
def home():
    return dict(year=_year())


@route('/about')
@view('about')
def about():
    return dict(year=_year())


@route('/dijkstra')
@view('dijkstra_theory')
def dijkstra():
    return dict(year=_year())


@route('/bridges')
@view('bridges_theory')
def bridges():
    return dict(year=_year())


@route('/cpm')
@view('cpm_theory')
def cpm():
    return dict(year=_year())


@route('/coloring')
@view('coloring_theory')
def coloring():
    return dict(year=_year())


@route('/cpm/practice', method=['GET', 'POST'])
@view('cpm_practice')
def cpm_practice():
    result = None
    error  = None
    tasks_raw = ''
    deps_raw  = ''

    if request.method == 'POST':
        tasks_raw = request.forms.get('tasks', '').strip()
        deps_raw  = request.forms.get('deps',  '').strip()
        try:
            tasks = {}
            for line in tasks_raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                if ':' not in line:
                    raise ValueError(
                        f'Неверный формат задачи: «{line}». '
                        f'Ожидается: Название: длительность'
                    )
                name, dur = line.split(':', 1)
                name = name.strip()
                dur  = dur.strip()
                if not name:
                    raise ValueError('Имя задачи не может быть пустым.')
                if not dur.isdigit():
                    raise ValueError(
                        f'Длительность задачи «{name}» должна быть '
                        f'целым числом ≥ 0, получено: «{dur}».'
                    )
                if name in tasks:
                    raise ValueError(f'Задача «{name}» указана дважды.')
                tasks[name] = int(dur)

            if not tasks:
                raise ValueError('Список задач не может быть пустым.')

            deps = []
            for line in deps_raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                if '->' not in line:
                    raise ValueError(
                        f'Неверный формат зависимости: «{line}». '
                        f'Ожидается: Задача_А -> Задача_Б'
                    )
                a, b = line.split('->', 1)
                a, b = a.strip(), b.strip()
                if not a or not b:
                    raise ValueError(
                        f'Пустое имя задачи в зависимости: «{line}».'
                    )
                deps.append((a, b))

            result = find_critical_path(tasks, deps)
            result['tasks'] = tasks   # передаём в шаблон для таблицы
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Критический путь — Практика',
        active_page='cpm',
        year=datetime.now().year,
        result=result,
        error=error,
        tasks_raw=tasks_raw,
        deps_raw=deps_raw,
    )


@route('/dijkstra/practice', method=['GET', 'POST'])
@view('dijkstra_practice')
def dijkstra_practice():
    result       = None
    error        = None
    vertices_raw = ''
    edges_raw    = ''
    source_raw   = ''

    if request.method == 'POST':
        vertices_raw = request.forms.get('vertices', '').strip()
        edges_raw    = request.forms.get('edges',    '').strip()
        source_raw   = request.forms.get('source',   '').strip()
        try:
            vertices = []
            for line in vertices_raw.splitlines():
                v = line.strip()
                if v:
                    vertices.append(v)

            if not vertices:
                raise ValueError('Список узлов не может быть пустым.')
            if len(vertices) != len(set(vertices)):
                raise ValueError('Имена узлов должны быть уникальными.')
            if not source_raw:
                raise ValueError('Укажите узел-источник.')
            if source_raw not in vertices:
                raise ValueError(
                    f'Источник «{source_raw}» отсутствует в списке узлов.'
                )

            edges = []
            for line in edges_raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                if '->' not in line or ':' not in line:
                    raise ValueError(
                        f'Неверный формат канала: «{line}». '
                        f'Ожидается: УЗЕЛ_А -> УЗЕЛ_Б : ВЕС'
                    )
                left, rest    = line.split('->', 1)
                mid, weight_s = rest.split(':', 1)
                u = left.strip()
                v = mid.strip()
                weight_s = weight_s.strip().lower()
                if weight_s in ('inf', '∞', 'infinity'):
                    w = float('inf')
                else:
                    try:
                        w = float(weight_s)
                    except ValueError:
                        raise ValueError(
                            f'Вес должен быть числом или inf: «{weight_s}».'
                        )
                edges.append((u, v, w))

            result = route_network(vertices, edges, source_raw)
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Дейкстра — Практика',
        active_page='dijkstra',
        year=datetime.now().year,
        result=result,
        error=error,
        vertices_raw=vertices_raw,
        edges_raw=edges_raw,
        source_raw=source_raw,
    )


@route('/bridges/practice', method=['GET', 'POST'])
@view('bridges_practice')
def bridges_practice():
    result = None
    error  = None
    vertices_raw = ''
    edges_raw    = ''

    if request.method == 'POST':
        vertices_raw = request.forms.get('vertices', '').strip()
        edges_raw    = request.forms.get('edges', '').strip()
        try:
            vertices = []
            for line in vertices_raw.splitlines():
                v = line.strip()
                if v:
                    vertices.append(v)

            if not vertices:
                raise ValueError('Список городов не может быть пустым.')
            if len(vertices) != len(set(vertices)):
                raise ValueError('Названия городов должны быть уникальными.')

            edges = []
            for line in edges_raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                if '-' not in line or ':' not in line:
                    raise ValueError(
                        f'Неверный формат дороги: «{line}». '
                        f'Ожидается: ГОРОД_А - ГОРОД_Б : ВЕС'
                    )
                parts = line.split('-', 1)
                left  = parts[0].strip()
                right_parts = parts[1].split(':', 1)
                if len(right_parts) != 2:
                    raise ValueError(
                        f'Не указан вес для дороги: «{line}».'
                    )
                right = right_parts[0].strip()
                try:
                    weight = float(right_parts[1].strip())
                except ValueError:
                    raise ValueError(
                        f'Вес должен быть числом: «{right_parts[1].strip()}».'
                    )
                edges.append((left, right, weight))

            result = analyze_network(vertices, edges)
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Мосты Тарьяна — Практика',
        active_page='bridges',
        year=datetime.now().year,
        result=result,
        error=error,
        vertices_raw=vertices_raw,
        edges_raw=edges_raw,
    )


@route('/coloring/practice', method=['GET', 'POST'])
@view('coloring_practice')
def coloring_practice():
    result = None
    error = None
    vertices_raw = ''
    edges_raw = ''

    if request.method == 'POST':
        vertices_raw = request.forms.get('vertices', '').strip()
        edges_raw    = request.forms.get('edges', '').strip()
        try:
            vertices = []
            for line in vertices_raw.splitlines():
                v = line.strip()
                if v:
                    vertices.append(v)

            if not vertices:
                raise ValueError('Список дисциплин не может быть пустым.')

            if len(vertices) != len(set(vertices)):
                raise ValueError('Дисциплины должны иметь уникальные имена.')

            edges = []
            for line in edges_raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                if '-' not in line:
                    raise ValueError(
                        f'Неверный формат конфликта: «{line}». '
                        f'Ожидается: ДИСЦИПЛИНА_А - ДИСЦИПЛИНА_Б'
                    )
                parts = line.split('-', 1)
                a, b = parts[0].strip(), parts[1].strip()
                edges.append((a, b))

            result = color_graph(vertices, edges)
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Раскраска графа — Практика',
        active_page='coloring',
        year=datetime.now().year,
        result=result,
        error=error,
        vertices_raw=vertices_raw,
        edges_raw=edges_raw,
    )
