"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
import random
import json
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
    # Значения по умолчанию
    stage = 'input_count'
    edge_count = 0
    source = 'A'
    edges = []
    errors = []
    graph_edges = None
    results = None

    if request.method == 'POST':
        action = request.forms.get('action', '')

        # 1. Пользователь указал количество рёбер
        if action == 'generate_count':
            try:
                count_str = request.forms.getunicode('edge_count', '').strip()
                if not count_str:
                    errors.append('Введите количество рёбер.')
                else:
                    edge_count = int(count_str)
                    if edge_count <= 0:
                        errors.append('Количество рёбер должно быть положительным числом.')
                    elif edge_count > 25:
                        errors.append('Количество рёбер не может превышать 25.')
                    else:
                        source = request.forms.getunicode('source', 'A').strip()
                        if not source:
                            errors.append('Вершина-источник не может быть пустой.')
                        else:
                            # Восстанавливаем рёбра из скрытых полей (если были)
                            edges = []
                            for i in range(edge_count):
                                from_val = request.forms.getunicode(f'from_{i}', '')
                                to_val = request.forms.getunicode(f'to_{i}', '')
                                weight_val = request.forms.getunicode(f'weight_{i}', '')
                                edges.append((from_val, to_val, weight_val))
                            if all(f == '' and t == '' and w == '' for f, t, w in edges):
                                edges = [('', '', '') for _ in range(edge_count)]
                            stage = 'input_edges'
            except ValueError:
                errors.append('Количество рёбер должно быть целым числом.')

            if errors:
                stage = 'input_count'
                # Сохраняем уже введённые данные для повторного показа
                edge_count = int(request.forms.getunicode('edge_count', 0)) if request.forms.getunicode('edge_count', '').isdigit() else 0
                source = request.forms.getunicode('source', 'A').strip()

        # 2. Назад с шага 2 на шаг 1
        elif action == 'back_to_count':
            edge_count = int(request.forms.getunicode('edge_count', '0'))
            source = request.forms.getunicode('source', 'A').strip()
            edges = []
            for i in range(edge_count):
                from_val = request.forms.getunicode(f'from_{i}', '')
                to_val = request.forms.getunicode(f'to_{i}', '')
                weight_val = request.forms.getunicode(f'weight_{i}', '')
                edges.append((from_val, to_val, weight_val))
            stage = 'input_count'

        # 3. Случайный граф
        elif action == 'random':
            vertices = ['A', 'B', 'C', 'D', 'E', 'F']
            edge_count = random.randint(4, 9)
            source = random.choice(vertices)
            edges = []
            used_pairs = set()
            for _ in range(edge_count):
                from_v = random.choice(vertices)
                to_v = random.choice(vertices)
                while from_v == to_v or (from_v, to_v) in used_pairs:
                    to_v = random.choice(vertices)
                used_pairs.add((from_v, to_v))
                weight = str(random.randint(1, 20)) if random.random() < 0.85 else 'inf'
                edges.append((from_v, to_v, weight))
            stage = 'input_edges'

        # 4. Загрузка файла
        elif action == 'upload':
            upload = request.files.getunicode('file')
            if not upload:
                errors.append('Файл не выбран.')
                stage = 'input_count'
            else:
                content = upload.file.read().decode('utf-8')
                lines = content.splitlines()
                edges = []
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.replace(',', ' ').split()
                    if len(parts) >= 3:
                        from_v = parts[0].strip()
                        to_v = parts[1].strip()
                        weight = parts[2].strip().lower()
                        edges.append((from_v, to_v, weight))
                    else:
                        errors.append(f'Строка {line_num}: игнорируется (не хватает данных)')
                if edges:
                    if len(edges) > 100:
                        errors.append('Файл содержит более 100 рёбер, это слишком много.')
                        stage = 'input_count'
                    else:
                        edge_count = len(edges)
                        all_vertices = set()
                        for f, t, _ in edges:
                            all_vertices.add(f)
                            all_vertices.add(t)
                        source = sorted(all_vertices)[0] if all_vertices else 'A'
                        stage = 'input_edges'
                else:
                    errors.append('Файл не содержит корректных рёбер.')
                    stage = 'input_count'

        # 5. Расчёт алгоритма
        elif action == 'calculate':
            edge_count = int(request.forms.getunicode('edge_count', '0'))
            source = request.forms.getunicode('source', 'A').strip()
            edges_raw = []
            parse_errors = []

            for i in range(edge_count):
                from_v = request.forms.getunicode(f'from_{i}', '').strip()
                to_v = request.forms.getunicode(f'to_{i}', '').strip()
                w_str = request.forms.getunicode(f'weight_{i}', '').strip().lower()
                if not from_v or not to_v or not w_str:
                    parse_errors.append(f'Ребро {i+1}: все поля должны быть заполнены.')
                    continue
                try:
                    if w_str == 'inf':
                        w = float('inf')
                    else:
                        w = float(w_str)
                        if w <= 0:
                            parse_errors.append(f'Ребро {i+1}: вес должен быть > 0, получено {w}')
                            continue
                except ValueError:
                    parse_errors.append(f'Ребро {i+1}: вес "{w_str}" не является числом или "inf"')
                    continue
                edges_raw.append((from_v, to_v, w))

            # Сохраняем введённые строки
            edges = [(request.forms.getunicode(f'from_{i}', ''),
                      request.forms.getunicode(f'to_{i}', ''),
                      request.forms.getunicode(f'weight_{i}', '')) for i in range(edge_count)]

            if parse_errors:
                errors.extend(parse_errors)
                stage = 'input_edges'
            else:
                vertices_set = set()
                for u, v, _ in edges_raw:
                    vertices_set.add(u)
                    vertices_set.add(v)
                vertices = list(vertices_set)

                if source not in vertices:
                    errors.append(f'Вершина-источник "{source}" не найдена среди вершин графа.')
                    stage = 'input_edges'
                else:
                    try:
                        res = route_network(vertices, edges_raw, source)
                        results = {}
                        for v in vertices:
                            dist = res['distances'][v]
                            path = res['paths'][v]
                            results[v] = {
                                'dist': dist,
                                'dist_display': '∞' if dist == float('inf') else str(dist),
                                'path': path,
                                'path_display': ' → '.join(path) if path else '—'
                            }
                        graph_edges = edges_raw
                        stage = 'results'
                    except ValueError as e:
                        errors.append(str(e))
                        stage = 'input_edges'

        # 6. Назад с шага 3 на шаг 2
        elif action == 'back_to_edges':
            edge_count = int(request.forms.getunicode('edge_count', '0'))
            source = request.forms.getunicode('source', 'A').strip()
            edges = []
            for i in range(edge_count):
                from_v = request.forms.getunicode(f'from_{i}', '')
                to_v = request.forms.getunicode(f'to_{i}', '')
                weight = request.forms.getunicode(f'weight_{i}', '')
                edges.append((from_v, to_v, weight))
            stage = 'input_edges'

        # 7. Сброс
        elif action == 'reset':
            stage = 'input_count'
            edge_count = 0
            source = 'A'
            edges = []
            errors = []

    # Подготовка graph_edges для JSON (замена inf на 'inf')
    graph_edges_for_json = None
    if graph_edges:
        graph_edges_for_json = [(u, v, w if w != float('inf') else 'inf') for (u, v, w) in graph_edges]

    return dict(
        stage=stage,
        edge_count=edge_count,
        source=source,
        edges=edges,
        errors=errors,
        graph_edges=graph_edges,
        graph_edges_json=graph_edges_for_json,
        results=results,
        year=2025,
        json=json
    )