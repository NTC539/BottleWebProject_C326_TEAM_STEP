"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
import random
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

@route('/cpm/practice')
@view('cpm_practice')
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

    if request.method == 'POST':
        edges_text = request.forms.get('edges', '').strip()
        source = request.forms.get('source', '').strip()

        # Парсинг рёбер
        raw_edges = []
        parse_errors = []
        lines = edges_text.splitlines()
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) < 3:
                parse_errors.append(f"Строка {line_num}: недостаточно данных (нужно 'from,to,weight')")
                continue
            u = parts[0].strip()
            v = parts[1].strip()
            w_str = parts[2].strip().lower()
            try:
                if w_str == 'inf':
                    w = float('inf')
                else:
                    w = float(w_str)
                    if w <= 0:
                        parse_errors.append(f"Строка {line_num}: вес должен быть > 0, получено {w}")
                        continue
            except ValueError:
                parse_errors.append(f"Строка {line_num}: вес '{w_str}' не является числом или 'inf'")
                continue
            raw_edges.append((u, v, w))

        if parse_errors:
            errors.extend(parse_errors)
        else:
            vertices_set = set()
            for u, v, _ in raw_edges:
                vertices_set.add(u)
                vertices_set.add(v)
            vertices = list(vertices_set)

            if source not in vertices:
                errors.append(f"Вершина-источник '{source}' не найдена среди вершин графа.")
            else:
                try:
                    res = route_network(vertices, raw_edges, source)
                    results = {v: {'dist': res['distances'][v], 'path': res['paths'][v]} for v in vertices}
                    graph_edges = raw_edges
                    results_json = json.dumps(results, ensure_ascii=False)
                except ValueError as e:
                    errors.append(str(e))

    if request.method == 'GET' and not edges_text:
        edges_text = """A,B,4
A,C,2
C,B,1
B,D,5
C,D,8
D,E,2
A,E,inf"""
        source = 'A'

    return template('dijkstra_practice.tpl',
                    edges=edges_text,
                    source=source,
                    errors=errors,
                    graph_edges=graph_edges,
                    results=results,
                    results_json=results_json,
                    year=2025)

@route('/dijkstra/random')
def random_graph():
    vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    edges = []
    edge_count = random.randint(5, 10)
    used_pairs = set()
    for _ in range(edge_count):
        from_v = random.choice(vertices)
        to_v = random.choice(vertices)
        while from_v == to_v or (from_v, to_v) in used_pairs:
            to_v = random.choice(vertices)
        used_pairs.add((from_v, to_v))
        weight = random.randint(1, 20)
        if random.random() < 0.15:
            weight = 'inf'
        edges.append(f"{from_v},{to_v},{weight}")
    edges_text = "\n".join(edges)
    source = random.choice(vertices)
    return template('practice.tpl',
                    edges=edges_text,
                    source=source,
                    errors=[],
                    graph_edges=None,
                    results=None,
                    results_json='null',
                    year=2025)

@route('/dijkstra/upload', method='POST')
def upload_file():
    upload = request.files.get('file')
    if not upload:
        redirect('/dijkstra/practice')
    content = upload.file.read().decode('utf-8')
    # Преобразуем содержимое в строку рёбер
    lines = content.splitlines()
    edges = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Поддерживаем разделители запятая или пробел
        parts = line.replace(',', ' ').split()
        if len(parts) >= 3:
            edges.append(f"{parts[0]},{parts[1]},{parts[2]}")
    edges_text = "\n".join(edges)
    source = 'A'  # можно оставить как есть или попробовать извлечь из файла
    return template('dijkstra_practice.tpl',
                    edges=edges_text,
                    source=source,
                    errors=[],
                    graph_edges=None,
                    results=None,
                    results_json='null',
                    year=2025)



