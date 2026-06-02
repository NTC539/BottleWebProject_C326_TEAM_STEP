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



