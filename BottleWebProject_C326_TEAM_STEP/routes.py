"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os as _os
from bottle import route, view, request, response, template
from datetime import datetime
from algorithms.cpm import find_critical_path
from algorithms.cpm_generator import generate_random_cpm
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

@route('/cpm/practice', method=['GET', 'POST'])
@view('cpm_practice')
def cpm_practice():
    result = None   # Словарь с результатами расчёта (или None при ошибке)
    error = None    # Строка с сообщением об ошибке (или None)
    
    # Сохраняем ввод пользователя для восстановления формы после отправки
    tasks_input = [] # Список пар [название, длительность]
    deps_input = []  # Список пар [предшественник, последователь]

    if request.method == 'POST':
        # Создаем декодированную копию всех данных формы
        forms = request.forms.decode()
    
        # Получаем списки в правильной UTF-8 кодировке
        names = forms.getall('task_name[]')
        durations = forms.getall('task_dur[]')
        df   = forms.getall('dep_from[]')
        dt   = forms.getall('dep_to[]')

        # Сохранение сырых данных для восстановления формы
        for i in range(len(names)):
            dur_raw = durations[i] if i < len(durations) else ''
            tasks_input.append([names[i], dur_raw])
        for i in range(len(df)):
            if i < len(dt):
                deps_input.append([df[i], dt[i]])
            
        # Валидация и парсинг данных
        try:
            # Формирование словаря задач
            tasks = {}
            for i in range(len(names)):
                name = names[i].strip() if i < len(names) else ''
                if not name:
                    continue
                if name in tasks:
                    raise ValueError(f'Задача «{name}» указана дважды.')
                
                # Парсинг длительности: должно быть целое число
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

            # Формирование списка зависимостей ---
            deps = [
                (df[i], dt[i])
                for i in range(len(df))
                if i < len(dt) and df[i] and dt[i]
            ]

            # Проверки зависимостей на корректность
            seen_deps = set()
            for a, b in deps:
                if a == b:
                    raise ValueError(f'Задача «{a}» не может зависеть от самой себя.')
                if (a, b) in seen_deps:
                    raise ValueError(f'Зависимость «{a} → {b}» указана несколько раз.')
                seen_deps.add((a, b))
                if (b, a) in seen_deps:
                    raise ValueError(
                        f'Обнаружена встречная зависимость: «{b} → {a}» и «{a} → {b}».'
                    )

            # Запуск алгоритма CPM ---
            result = find_critical_path(tasks, deps)
            # Добавляем исходные задачи в результат для отображения в таблице
            result['tasks'] = tasks

            # Подготовка данных для фронтенда (JavaScript)
            # Все значения преобразуются в JSON-строки, которые будут
            # вставлены в шаблон через {{!...}} (без экранирования HTML)
            
            result['gv']     = json.dumps(list(tasks.keys()))           # Список вершин графа
            result['ge']     = json.dumps([[a, b] for a, b in deps])    # Список рёбер графа (пары [от, к])
            result['gcrit']  = json.dumps(result['critical_paths'])     # Список всех критических путей
            
            # Словари с параметрами задач (нужны для всплывающих подсказок на графе)
            result['gtasks'] = json.dumps(result['tasks'])              
            result['ges']    = json.dumps(result['es'])
            result['gef']    = json.dumps(result['ef'])
            result['gls']    = json.dumps(result['ls'])
            result['glf']    = json.dumps(result['lf']) 
            result['gfloat'] = json.dumps(result['total_float'])

            # Полный результат для скачивания в .json
            download = {
                'duration':       result['duration'],
                'critical_paths': result['critical_paths'],
                'critical_tasks': sorted(result['critical_tasks']),
                'tasks':          result['tasks'],
                'es':             result['es'],
                'ef':             result['ef'],
                'ls':             result['ls'],
                'lf':             result['lf'],
                'total_float':    result['total_float'],
            }
            result['gdownload'] = json.dumps(download, ensure_ascii=False)

        except ValueError as e:
            error = str(e)
            result = None
        except Exception as e:
            error = f'Ошибка: {e}'
            result = None

    return dict(
        title='Критический путь — Практика (POST)',
        active_page='cpm',
        year=_year(),
        result=result,
        error=error,
        tasks_input=json.dumps(tasks_input, ensure_ascii=False),
        deps_input=json.dumps(deps_input, ensure_ascii=False),
    )

@route('/cpm/generate')
def cpm_generate():
    # Устанавливаем Content-Type для JSON-ответа
    response.content_type = 'application/json'
    # Генерируем данные и возвращаем как JSON-строку
    # ensure_ascii=False — чтобы русские символы (если будут) не экранировались
    return json.dumps(generate_random_cpm(), ensure_ascii=False)



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



