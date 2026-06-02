"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
from bottle import route, view, request, template, response
from datetime import datetime
from algorithms.cpm import find_critical_path
from algorithms.bridges import analyze_network
from bridges_generator import generate_random_bridges
from algorithms.cpm_generator import generate_random_cpm
import random
import json
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


def _fmt_num(x):
    """Форматирует число для матрицы: ∞ для бесконечности, без .0 для целых."""
    if x == float('inf'):
        return '∞'
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
        # Структура для экспорта в JSON (∞ записывается строкой для валидного JSON)
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
        'bridges':        bridges,
        'bridge_count':   len(bridges),
        'states':         state_views,
        'gbridges':       json.dumps(bridge_pairs, ensure_ascii=False),
        'gdownload':      json.dumps(download, ensure_ascii=False),
    }


@route('/bridges/generate')
def bridges_generate():
    """Возвращает случайный взвешенный связный граф (узлы и рёбра) в JSON."""
    response.content_type = 'application/json'
    return json.dumps(generate_random_bridges(), ensure_ascii=False)


@route('/bridges/practice', method=['GET', 'POST'])
@view('bridges_practice')
def bridges_practice():
    result = None
    error = None
    nodes_input = []   # ['A', 'B', ...]
    edges_input = []   # [['A', 'B', '4'], ...]

    if request.method == 'POST':
        nodes = request.forms.getall('node[]')
        ef = request.forms.getall('edge_from[]')
        et = request.forms.getall('edge_to[]')
        ew = request.forms.getall('edge_weight[]')

        # Запоминаем сырой ввод, чтобы форма не очищалась после отправки
        nodes_input = list(nodes)
        for i in range(len(ef)):
            edges_input.append([
                ef[i] if i < len(ef) else '',
                et[i] if i < len(et) else '',
                ew[i] if i < len(ew) else '',
            ])

        try:
            vertices = []
            for n in nodes:
                name = n.strip()
                if not name:
                    continue
                if name in vertices:
                    raise ValueError(f'Город «{name}» указан дважды.')
                vertices.append(name)
            if not vertices:
                raise ValueError('Добавьте хотя бы один город.')

            edges = []
            for i in range(len(ef)):
                frm = (ef[i] if i < len(ef) else '').strip()
                to = (et[i] if i < len(et) else '').strip()
                wraw = (ew[i] if i < len(ew) else '').strip()
                if not frm and not to and not wraw:
                    continue
                if not frm or not to:
                    raise ValueError('У каждой дороги должны быть указаны оба города.')
                try:
                    w = float(wraw)
                except (ValueError, TypeError):
                    raise ValueError(f'Вес дороги {frm}—{to} должен быть числом.')
                edges.append((frm, to, w))

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

@route('/cpm/generate')
def cpm_generate():
    """Возвращает случайный набор задач и зависимостей (без циклов) в JSON."""
    response.content_type = 'application/json'
    return json.dumps(generate_random_cpm(), ensure_ascii=False)


@route('/cpm/practice', method=['GET', 'POST'])
@view('cpm_practice')
def cpm_practice():
    result = None
    error = None
    
    tasks_input = []
    deps_input = []

    if request.method == 'POST':
        # Создаем декодированную копию всех данных формы
        forms = request.forms.decode()
    
        # Получаем списки в правильной UTF-8 кодировке
        names = forms.getall('task_name[]')
        durations = forms.getall('task_dur[]')
        df   = forms.getall('dep_from[]')
        dt   = forms.getall('dep_to[]')

        for i in range(len(names)):
            dur_raw = durations[i] if i < len(durations) else ''
            tasks_input.append([names[i], dur_raw])
        for i in range(len(df)):
            if i < len(dt):
                deps_input.append([df[i], dt[i]])
            
        try:
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

            deps = [
                (df[i], dt[i])
                for i in range(len(df))
                if i < len(dt) and df[i] and dt[i]
            ]

            # Проверки зависимостей
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

            result = find_critical_path(tasks, deps)
            result['tasks'] = tasks   # для таблицы в шаблоне

            # JSON для отрисовки графа через vis.js (вставляется в шаблон через {{!...}})
            result['gv']     = json.dumps(list(tasks.keys()))
            result['ge']     = json.dumps([[a, b] for a, b in deps])
            result['gcrit']  = json.dumps(result['critical_paths'])
            result['gtasks'] = json.dumps(result['tasks'])
            result['ges']    = json.dumps(result['es'])
            result['gef']    = json.dumps(result['ef'])
            result['gls']    = json.dumps(result['ls'])
            result['glf']    = json.dumps(result['lf']) 
            result['gfloat'] = json.dumps(result['total_float'])

            # Полный результат для скачивания в .json (set → отсортированный список)
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
    """Возвращает случайный набор задач и зависимостей (без циклов) в JSON."""
    response.content_type = 'application/json'
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
                edge_count = int(request.forms.getunicode('edge_count', 0)) if request.forms.getunicode('edge_count', '').isdigit() else 0
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

        # 3. random
        elif action == 'random':
            vertices = ['A', 'B', 'C', 'D', 'E', 'F']
            edge_count = random.randint(4, 9)
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

            source = random.choice(random.choice(edges))
            stage = 'input_edges'

        # 4. upload
        elif action == 'upload':
            upload = request.files.get('file')
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

        # 5. calculate
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
                if len(from_v) > 10:
                    parse_errors.append(f'Ребро {i+1}: название вершины ({from_v}) не должно превышать 10 символов')
                    continue
                if len(to_v) > 10:
                    parse_errors.append(f'Ребро {i+1}: название вершины ({to_v}) не должно превышать 10 символов')
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

        # 7. reset
        elif action == 'reset':
            stage = 'input_count'
            edge_count = 0
            source = 'A'
            edges = []
            errors = []

        # 8. export
        elif action == 'export':
            edge_count = int(request.forms.getunicode('edge_count', '0'))
            source = request.forms.getunicode('source', 'A').strip()
            edges_list = []
            for i in range(edge_count):
                from_v = request.forms.getunicode(f'from_{i}', '').strip()
                to_v = request.forms.getunicode(f'to_{i}', '').strip()
                weight = request.forms.getunicode(f'weight_{i}', '').strip()
                if from_v and to_v and weight:
                    edges_list.append(f"{from_v},{to_v},{weight}")
            if not edges_list:
                response.status = 400
                return "Нет данных для экспорта."
            response.headers['Content-Type'] = 'text/plain; charset=utf-8'
            response.headers['Content-Disposition'] = 'attachment; filename="graph_export.txt"'
            return "\n".join(edges_list)

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