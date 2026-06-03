"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
import random
import json
from bottle import route, view, request, template, response
from datetime import datetime
from algorithms.dijkstra import route_network
from algorithms.dijkstra_utils import (
    parse_edges_from_lists,
    parse_edges_from_text,
    generate_random_graph,
    run_dijkstra_and_prepare_results,
    export_edges_to_string
)


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
    stage = 'input_count'
    edge_count = 0
    source = 'A'
    edges = []
    errors = []
    graph_edges = None
    results = None

    if request.method == 'POST':
        action = request.forms.get('action', '')

        # 1. generate_count
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
                edge_count = int(request.forms.getunicode('edge_count', '0')) if request.forms.getunicode('edge_count', '').isdigit() else 0
                source = request.forms.getunicode('source', 'A').strip()

        # 2. back_to_count
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

        elif action == 'random':
            edges, source = generate_random_graph()
            edge_count = len(edges)
            stage = 'input_edges'

        elif action == 'upload':
            upload = request.files.get('file')
            if not upload:
                errors.append('Файл не выбран.')
                stage = 'input_count'
            else:
                content = upload.file.read().decode('utf-8')
                parsed_edges, parsed_count, all_vertices, parse_errors = parse_edges_from_text(content, max_edges=25)
                errors.extend(parse_errors)
                if parsed_edges:
                    edges = parsed_edges
                    edge_count = parsed_count
                    source = sorted(all_vertices)[0] if all_vertices else 'A'
                    stage = 'input_edges'
                else:
                    stage = 'input_count'

        elif action == 'calculate':
            edge_count = int(request.forms.getunicode('edge_count', '0'))
            source = request.forms.getunicode('source', 'A').strip()

            from_list = [request.forms.getunicode(f'from_{i}', '') for i in range(edge_count)]
            to_list = [request.forms.getunicode(f'to_{i}', '') for i in range(edge_count)]
            weight_list = [request.forms.getunicode(f'weight_{i}', '') for i in range(edge_count)]

            edges_raw, edges_display, parse_errors = parse_edges_from_lists(edge_count, from_list, to_list, weight_list)
            errors.extend(parse_errors)
            edges = edges_display

            if parse_errors:
                stage = 'input_edges'
            else:
                results, graph_edges, dijkstra_errors = run_dijkstra_and_prepare_results(edges_raw, source)
                errors.extend(dijkstra_errors)
                if results:
                    stage = 'results'
                else:
                    stage = 'input_edges'

        # 6. back_to_edges
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

        elif action == 'reset':
            stage = 'input_count'
            edge_count = 0
            source = 'A'
            edges = []
            errors = []

        elif action == 'export':
            edge_count = int(request.forms.getunicode('edge_count', '0'))
            edges_for_export = []
            for i in range(edge_count):
                from_v = request.forms.getunicode(f'from_{i}', '').strip()
                to_v = request.forms.getunicode(f'to_{i}', '').strip()
                weight = request.forms.getunicode(f'weight_{i}', '').strip()
                if from_v and to_v and weight:
                    edges_for_export.append((from_v, to_v, weight))
            content, ok = export_edges_to_string(edges_for_export)
            if not ok:
                response.status = 400
                return "Нет данных для экспорта."
            response.headers['Content-Type'] = 'text/plain; charset=utf-8'
            response.headers['Content-Disposition'] = 'attachment; filename="graph_export.txt"'
            return content

    # Подготовка данных для шаблона
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
        year=2026,
        json=json
    )



