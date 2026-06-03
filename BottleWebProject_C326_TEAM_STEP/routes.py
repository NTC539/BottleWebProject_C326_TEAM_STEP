"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
from bottle import route, view, request, response, template
from datetime import datetime
from algorithms.coloring import (
    ColoringInputError,
    generate_random_data,
    load_coloring_json,
    make_export_data,
    sample_coloring_data,
    solve_coloring,
)
from algorithms.cpm import find_critical_path
from algorithms.cpm_generator import generate_random_cpm
from algorithms.bridges import analyze_network
from bridges_generator import generate_random_bridges
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


# ── Ограничения ввода практики «Мосты» ──────────────────────────────────────
# Вынесены в константы, чтобы преподаватель/правка лимитов не лезли в код.
BRIDGES_MAX_CITIES   = 15     # читаемость матриц и графа vis.js
BRIDGES_MAX_EDGES    = 100    # защита от чрезмерно большой формы
BRIDGES_MAX_NAME_LEN = 20     # длина названия города
BRIDGES_MAX_WEIGHT   = 1000   # верхняя граница веса дороги
BRIDGES_INF_LABEL    = 'н/д'  # метка вместо ∞ (недостижимо / путь не действителен)


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
    """Страница практики 4-го варианта: ручной ввод, генерация, импорт, экспорт и расчёт."""
    subjects, conflicts = sample_coloring_data()
    errors = []
    result = None
    subject_count = '12'
    density = '0.35'

    if request.method == 'POST':
        action = request.forms.get('form_action') or 'calculate'
        subject_count = request.forms.get('subject_count') or subject_count
        density = request.forms.get('density') or density

        if action == 'generate':
            try:
                subjects, conflicts = generate_random_data(int(subject_count), float(str(density).replace(',', '.')))
            except ValueError:
                errors.append('Проверьте количество дисциплин и плотность графа.')
        elif action == 'load_json':
            try:
                upload = request.files.get('json_file')
                if not upload or not upload.filename:
                    raise ColoringInputError(['Выберите JSON-файл для загрузки.'])
                payload = upload.file.read().decode('utf-8-sig')
                subjects, conflicts = load_coloring_json(json.loads(payload))
            except json.JSONDecodeError:
                errors.append('JSON-файл не удалось прочитать. Проверьте структуру данных.')
            except UnicodeDecodeError:
                errors.append('Файл должен быть сохранён в кодировке UTF-8.')
            except ColoringInputError as exc:
                errors.extend(exc.errors)
        elif action == 'export_json':
            subjects, conflicts = _read_coloring_form()
            try:
                result = solve_coloring(subjects, conflicts)
                subjects = result['subjects']
                conflicts = result['conflicts']
                return _export_coloring_json(subjects, conflicts, result)
            except ColoringInputError as exc:
                errors.extend(exc.errors)
        else:
            subjects, conflicts = _read_coloring_form()
            try:
                result = solve_coloring(subjects, conflicts)
                subjects = result['subjects']
                conflicts = result['conflicts']
                _save_coloring_history(subjects, conflicts, result)
            except ColoringInputError as exc:
                errors.extend(exc.errors)

    return dict(
        year=_year(),
        subjects=subjects,
        conflicts=conflicts,
        errors=errors,
        result=result,
        subject_count=subject_count,
        density=density,
    )


def _read_coloring_form():
    """Читает дисциплины и конфликты из полей отправленной формы."""
    names = request.forms.getall('subject[]')
    teachers = request.forms.getall('teacher[]')
    subjects = []
    for index, name in enumerate(names):
        teacher = teachers[index] if index < len(teachers) else ''
        subjects.append({'name': name, 'teacher': teacher})

    conflict_from = request.forms.getall('conflict_from[]')
    conflict_to = request.forms.getall('conflict_to[]')
    conflicts = []
    for index, left in enumerate(conflict_from):
        right = conflict_to[index] if index < len(conflict_to) else ''
        conflicts.append((left, right))

    return subjects, conflicts


def _export_coloring_json(subjects, conflicts, result):
    """Отдаёт результат расчёта как загружаемый JSON-файл, совместимый с импортом."""
    data = make_export_data(subjects, conflicts, result)
    filename = 'coloring_result_{}.json'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

    response.content_type = 'application/json; charset=utf-8'
    response.set_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
    return json.dumps(data, ensure_ascii=False, indent=2)


def _save_coloring_history(subjects, conflicts, result):
    """Дописывает выполненный расчёт в файл истории data/coloring_history.json."""
    project_root = os.path.abspath(os.path.dirname(__file__))
    history_dir = os.path.join(project_root, 'data')
    history_path = os.path.join(history_dir, 'coloring_history.json')
    os.makedirs(history_dir, exist_ok=True)

    entry = {
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input': {
            'subjects': subjects,
            'conflicts': conflicts,
        },
        'result': {
            'num_colors': result['num_colors'],
            'colors': result['colors'],
            'schedule': result['schedule'],
            'teacher_shifts': result['teacher_shifts'],
        },
    }

    try:
        with open(history_path, 'r', encoding='utf-8') as file:
            history = json.load(file)
        if not isinstance(history, list):
            history = []
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(entry)
    with open(history_path, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def _fmt_num(x):
    """Форматирует число для матрицы: метка недостижимости вместо ∞, без .0 для целых."""
    if x == float('inf'):
        return BRIDGES_INF_LABEL
    f = float(x)
    return str(int(f)) if f.is_integer() else str(f)


def _prepare_bridges_result(vertices, data):
    """Готовит данные analyze_network для шаблона (матрицы и JSON для vis.js)."""
    bridges = data['bridges']
    bridge_pairs = [sorted((u, v)) for (u, v, w) in bridges]

    state_views = []
    download_states = []
    for st in data['states']:
        removed = st['removed']
        title = 'Исходная сеть' if removed is None \
            else 'Без моста %s—%s' % (removed[0], removed[1])
        weight, adj, dist = st['weight'], st['adj'], st['dist']
        weight_rows = [[_fmt_num(weight[i][j]) for j in vertices] for i in vertices]
        adj_rows = [[adj[i][j] for j in vertices] for i in vertices]
        dist_rows = [[_fmt_num(dist[i][j]) for j in vertices] for i in vertices]
        state_views.append({
            'title':       title,
            'removed':     removed,
            'weight_rows': weight_rows,
            'adj_rows':    adj_rows,
            'dist_rows':   dist_rows,
            'gv':          json.dumps(vertices, ensure_ascii=False),
            'ge':          json.dumps([[u, v, w] for (u, v, w) in st['edges']],
                                      ensure_ascii=False),
        })
        # Структура для экспорта в JSON (недостижимость — строкой-меткой, JSON валиден)
        download_states.append({
            'removed': list(removed) if removed is not None else None,
            'edges':   [[u, v, w] for (u, v, w) in st['edges']],
            'weight':  {i: {j: _fmt_num(weight[i][j]) for j in vertices} for i in vertices},
            'adj':     {i: {j: adj[i][j] for j in vertices} for i in vertices},
            'dist':    {i: {j: _fmt_num(dist[i][j]) for j in vertices} for i in vertices},
        })

    download = {
        'vertices':       vertices,
        'total_path_sum': _fmt_num(data['total_path_sum']),
        'bridges':        [list(b) for b in bridges],
        'states':         download_states,
    }

    return {
        'vertices':       vertices,
        'total_path_sum': _fmt_num(data['total_path_sum']),
        'inf_label':      BRIDGES_INF_LABEL,
        'bridges':        bridges,
        'bridge_count':   len(bridges),
        'states':         state_views,
        'gbridges':       json.dumps(bridge_pairs, ensure_ascii=False),
        'gdownload':      json.dumps(download, ensure_ascii=False),
    }


@route('/bridges/generate')
def bridges_generate():
    """Возвращает случайный взвешенный связный граф (узлы и рёбра) в JSON.

    Необязательный параметр ?cities=N фиксирует число городов (2..MAX).
    Без параметра — случайное число городов, как раньше.
    """
    response.content_type = 'application/json'
    raw = request.query.get('cities', '').strip()
    if raw:
        try:
            n = int(raw)
        except (ValueError, TypeError):
            n = None
        if n is not None:
            n = max(2, min(BRIDGES_MAX_CITIES, n))   # зажать в допустимый диапазон
            return json.dumps(generate_random_bridges(min_nodes=n, max_nodes=n),
                              ensure_ascii=False)
    return json.dumps(generate_random_bridges(), ensure_ascii=False)


@route('/bridges/practice', method=['GET', 'POST'])
@view('bridges_practice')
def bridges_practice():
    result = None
    error = None
    nodes_input = []   # ['A', 'B', ...]
    edges_input = []   # [['A', 'B', '4'], ...]

    if request.method == 'POST':
        # Декодированная копия формы → корректный UTF-8 (как в cpm_practice),
        # иначе кириллические названия городов приходят в latin-1 (кракозябры).
        forms = request.forms.decode()
        nodes = forms.getall('node[]')
        ef = forms.getall('edge_from[]')
        et = forms.getall('edge_to[]')
        ew = forms.getall('edge_weight[]')

        # Запоминаем ввод, чтобы форма не очищалась после отправки.
        # Пустые строки при расчёте отбрасываются (не возвращаются в форму).
        nodes_input = [n.strip() for n in nodes if n.strip()]
        for i in range(len(ef)):
            frm = ef[i] if i < len(ef) else ''
            to = et[i] if i < len(et) else ''
            wraw = ew[i] if i < len(ew) else ''
            if not frm.strip() and not to.strip() and not wraw.strip():
                continue   # полностью пустая строка дороги — убрать
            edges_input.append([frm, to, wraw])

        try:
            # ── Города ───────────────────────────────────────────────────────
            vertices = []
            seen_cities = {}          # casefold-ключ → оригинальное имя
            for n in nodes:
                name = n.strip()
                if not name:
                    continue
                if len(name) > BRIDGES_MAX_NAME_LEN:
                    raise ValueError(
                        f'Название города слишком длинное '
                        f'(до {BRIDGES_MAX_NAME_LEN} символов): «{name}».')
                key = name.casefold()    # дубль без учёта регистра: «Москва»=«москва»
                if key in seen_cities:
                    raise ValueError(
                        f'Город «{name}» уже добавлен (как «{seen_cities[key]}»).')
                seen_cities[key] = name
                vertices.append(name)

            if len(vertices) < 2:
                raise ValueError('Добавьте хотя бы два города.')
            if len(vertices) > BRIDGES_MAX_CITIES:
                raise ValueError(
                    f'Слишком много городов (максимум {BRIDGES_MAX_CITIES}).')

            # Канон: имя дороги приводим к уже введённому написанию города.
            vertex_by_key = {v.casefold(): v for v in vertices}

            # ── Дороги ───────────────────────────────────────────────────────
            edges = []
            seen_edges = set()        # frozenset канонических имён — дубль/реверс
            for i in range(len(ef)):
                frm = (ef[i] if i < len(ef) else '').strip()
                to = (et[i] if i < len(et) else '').strip()
                wraw = (ew[i] if i < len(ew) else '').strip()
                if not frm and not to and not wraw:
                    continue
                if not frm or not to:
                    raise ValueError('У каждой дороги должны быть указаны оба города.')

                frm_c = vertex_by_key.get(frm.casefold())
                to_c = vertex_by_key.get(to.casefold())
                if frm_c is None:
                    raise ValueError(f'Неизвестный город в дороге: «{frm}».')
                if to_c is None:
                    raise ValueError(f'Неизвестный город в дороге: «{to}».')
                if frm_c == to_c:
                    raise ValueError(
                        f'Дорога не может вести из города «{frm_c}» в него же.')

                key = frozenset((frm_c, to_c))
                if key in seen_edges:
                    raise ValueError(f'Дорога {frm_c}—{to_c} указана дважды.')
                seen_edges.add(key)

                try:
                    w = int(wraw)
                except (ValueError, TypeError):
                    raise ValueError(
                        f'Вес дороги {frm_c}—{to_c} должен быть целым числом.')
                if w <= 0:
                    raise ValueError(
                        f'Вес дороги {frm_c}—{to_c} должен быть больше 0.')
                if w > BRIDGES_MAX_WEIGHT:
                    raise ValueError(
                        f'Вес дороги {frm_c}—{to_c} слишком большой '
                        f'(максимум {BRIDGES_MAX_WEIGHT}).')

                if len(edges) >= BRIDGES_MAX_EDGES:
                    raise ValueError(
                        f'Слишком много дорог (максимум {BRIDGES_MAX_EDGES}).')
                edges.append((frm_c, to_c, w))

            data = analyze_network(vertices, edges)
            result = _prepare_bridges_result(vertices, data)

        except ValueError as e:
            error = str(e)
            result = None
        except Exception as e:
            error = f'Ошибка: {e}'
            result = None
    else:
        # Пример по умолчанию (две «области», соединённые мостом C—D)
        nodes_input = ['A', 'B', 'C', 'D', 'E']
        edges_input = [
            ['A', 'B', '4'], ['A', 'C', '2'], ['B', 'C', '1'],
            ['C', 'D', '5'], ['D', 'E', '3'],
        ]

    return dict(
        title='Мосты Тарьяна — Практика',
        active_page='bridges',
        year=_year(),
        result=result,
        error=error,
        nodes_input=json.dumps(nodes_input, ensure_ascii=False),
        edges_input=json.dumps(edges_input, ensure_ascii=False),
    )


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



