"""
Routes and views for the bottle application.
"""

from bottle import route, view, request
from datetime import datetime
from algorithms.coloring import color_graph


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


@route('/author')
@view('author')
def author():
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
