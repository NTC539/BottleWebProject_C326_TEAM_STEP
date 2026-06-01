"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
from bottle import route, view, request, template
from datetime import datetime
from algorithms.cpm import find_critical_path

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


@route('/graph_theory')
@view('graph_theory')
def graph_theory():
    return dict(year=_year())


@route('/dijkstra')
@view('dijkstra_theory')
def dijkstra():
    return dict(year=_year())


@route('/bridges')
@view('bridges_theory')
def bridges():
    return dict(year=_year())

@route('/coloring/practice', method=['GET', 'POST'])
@view('coloring_practice')
def coloring_practice():
    return dict(year=_year())


@route('/bridges/practice', method=['GET', 'POST'])
@view('bridges_practice')
def bridges_practice():
    return dict(year=_year())


@route('/cpm')
@view('cpm_theory')
def cpm():
    return dict(year=_year())

@route('/cpm/practice', method=['GET', 'POST'])
@view('cpm_practice')
def cpm_practice():
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            # Создаем декодированную копию всех данных формы
            forms = request.forms.decode()
    
            # Получаем списки в правильной UTF-8 кодировке
            names = request.forms.getall('task_name[]')
            durations = request.forms.getall('task_dur[]')

            tasks = {}

            for i in range(len(names)):
                name = names[i].strip() if i < len(names) else ''
                if not name:
                    continue
                if name in tasks:
                    raise ValueError(f'Задача «{name}» указана дважды.')
                try:
                    dur = int(durations[i]) if i < len(durations) else 0
                except (ValueError, TypeError):
                    raise ValueError(
                        f'Длительность задачи «{name}» должна быть '
                        f'целым числом ≥ 0.'
                    )
                tasks[name] = dur

            if not tasks:
                raise ValueError('Список задач не может быть пустым.')

            df   = request.forms.getall('dep_from[]')
            dt   = request.forms.getall('dep_to[]')
            deps = [
                (df[i], dt[i])
                for i in range(len(df))
                if i < len(dt) and df[i] and dt[i]
            ]

            result = find_critical_path(tasks, deps)
            result['tasks'] = tasks   # для таблицы в шаблоне

            result['gv']     = _json.dumps(list(tasks.keys()))
            result['ge']     = _json.dumps([[a, b] for a, b in deps])
            result['gcrit']  = _json.dumps(result['critical_paths'])
            result['gtasks'] = _json.dumps(result['tasks'])
            result['ges']    = _json.dumps(result['es'])
            result['gef']    = _json.dumps(result['ef'])

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
    title='Критический путь — Практика (POST)',
    active_page='cpm',
    year=_year(),
    result=result,
    error=error,
    )



@route('/coloring')
@view('coloring_theory')
def coloring():
    return dict(year=_year())


@route('/dijkstra/practice', method=['GET', 'POST'])
@view('dijkstra_practice')
def dijkstra_practice():
    edges_text = ''
    source = 'A'
    errors = []
    graph_edges = None
    results = None
    results_json = 'null'
    
    errors.append('Ошибка 1')
    errors.append('Ошибка 2')

    edges_text = """A,B,4
A,C,2
C,B,1
B,D,5
C,D,8
D,E,2
A,E,inf"""

    source = "A"

    graph_edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("C", "B", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("D", "E", 2),
        ("A", "E", float("inf")),
    ]

    results = {
        "A": {"dist": 0, "path": ["A"]},
        "B": {"dist": 3, "path": ["A", "C", "B"]},
        "C": {"dist": 2, "path": ["A", "C"]},
        "D": {"dist": 8, "path": ["A", "C", "B", "D"]},
        "E": {"dist": 10, "path": ["A", "C", "B", "D", "E"]},
    }

    prepared_edges = []
    for (frm, to, w) in graph_edges:
        status = "Исключён (∞)" if w == inf else "Участвует"
        weight_display = "∞" if w == inf else str(w)
        prepared_edges.append((frm, to, weight_display, status))

    # Подготавливаем результаты с готовым отображением пути и расстояния
    prepared_results = {}
    for node, data in results.items():
        dist = data['dist']
        dist_display = "недостижим" if dist == inf else str(dist)
        path_display = " → ".join(data['path']) if data['path'] else "—"
        prepared_results[node] = {
            'dist_display': dist_display,
            'path_display': path_display
        }

    # Теперь передаём в шаблон подготовленные данные
    return template('dijkstra_practice.tpl',
                    edges=edges_text,
                    source=source,
                    errors=errors,
                    prepared_edges=prepared_edges,   # вместо graph_edges
                    prepared_results=prepared_results,  # вместо results
                    year=2025)



