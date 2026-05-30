"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
from bottle import route, view, request, template
from datetime import datetime
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



