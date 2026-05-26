"""
Routes and views for the bottle application.
"""

import json as _json
from bottle import route, view, request
from datetime import datetime
from algorithms.coloring import color_graph
from algorithms.cpm import find_critical_path
from algorithms.bridges import analyze_network
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


@route('/cpm')
@view('cpm_theory')
def cpm():
    return dict(year=_year())


@route('/coloring')
@view('coloring_theory')
def coloring():
    return dict(year=_year())


# ─────────────────────────────────────────────────────────────────────────────
#  /dijkstra/practice
# ─────────────────────────────────────────────────────────────────────────────
@route('/dijkstra/practice', method=['GET', 'POST'])
@view('dijkstra_practice')
def dijkstra_practice():
    result     = None
    error      = None
    source_val = ''          # used in result-section template

    if request.method == 'POST':
        try:
            # ── Vertices ──────────────────────────────────────────────────────
            vertices = [v.strip()
                        for v in request.forms.getall('vertex[]')
                        if v.strip()]
            if not vertices:
                raise ValueError('Список узлов не может быть пустым.')
            if len(vertices) != len(set(vertices)):
                raise ValueError('Имена узлов должны быть уникальными.')

            # ── Source ────────────────────────────────────────────────────────
            source = request.forms.get('source', '').strip()
            if not source:
                raise ValueError('Выберите узел-источник.')
            if source not in vertices:
                raise ValueError(
                    f'Источник «{source}» отсутствует в списке узлов.'
                )
            source_val = source

            # ── Edges (inf-aware via edge_inf_N fields) ───────────────────────
            from_list  = request.forms.getall('edge_from[]')
            to_list    = request.forms.getall('edge_to[]')
            w_list     = request.forms.getall('edge_weight[]')
            edge_count = int(request.forms.get('edge_count', '0') or '0')

            edges = []
            for i in range(edge_count):
                u = from_list[i] if i < len(from_list) else ''
                v = to_list[i]   if i < len(to_list)   else ''
                if not u or not v:
                    continue
                is_inf = request.forms.get(f'edge_inf_{i}') == '1'
                if is_inf:
                    w = float('inf')
                else:
                    try:
                        w = float(w_list[i]) if i < len(w_list) else 1.0
                    except (ValueError, TypeError):
                        raise ValueError(
                            f'Неверный вес для канала {u}→{v}.'
                        )
                edges.append((u, v, w))

            result = route_network(vertices, edges, source)

            result['gv']  = _json.dumps(vertices)
            result['ge']  = _json.dumps([[u, v, (None if w == float('inf') else w)]
                                         for u, v, w in edges])
            _pe = set()
            for _p in result['paths'].values():
                for _i in range(len(_p) - 1):
                    _pe.add((_p[_i], _p[_i + 1]))
            result['gpe'] = _json.dumps(list(_pe))

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Дейкстра — Практика',
        active_page='dijkstra',
        year=_year(),
        result=result,
        error=error,
        source_val=source_val,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  /bridges/practice
# ─────────────────────────────────────────────────────────────────────────────
@route('/bridges/practice', method=['GET', 'POST'])
@view('bridges_practice')
def bridges_practice():
    result = None
    error  = None

    if request.method == 'POST':
        try:
            # ── Vertices ──────────────────────────────────────────────────────
            vertices = [v.strip()
                        for v in request.forms.getall('vertex[]')
                        if v.strip()]
            if not vertices:
                raise ValueError('Список городов не может быть пустым.')
            if len(vertices) != len(set(vertices)):
                raise ValueError('Названия городов должны быть уникальными.')

            # ── Edges ─────────────────────────────────────────────────────────
            from_list = request.forms.getall('edge_from[]')
            to_list   = request.forms.getall('edge_to[]')
            w_list    = request.forms.getall('edge_weight[]')

            edges = []
            for i in range(len(from_list)):
                u = from_list[i] if i < len(from_list) else ''
                v = to_list[i]   if i < len(to_list)   else ''
                if not u or not v:
                    continue
                try:
                    w = float(w_list[i]) if i < len(w_list) else 1.0
                except (ValueError, TypeError):
                    raise ValueError(f'Неверный вес для дороги {u}—{v}.')
                edges.append((u, v, w))

            result = analyze_network(vertices, edges)

            result['gv'] = _json.dumps(vertices)
            result['ge'] = _json.dumps([[u, v, w] for u, v, w in edges])
            result['gb'] = _json.dumps([[u, v] for u, v, w in result['bridges']])

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Мосты Тарьяна — Практика',
        active_page='bridges',
        year=_year(),
        result=result,
        error=error,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  /cpm/practice
# ─────────────────────────────────────────────────────────────────────────────
@route('/cpm/practice', method=['GET', 'POST'])
@view('cpm_practice')
def cpm_practice():
    result = None
    error  = None

    if request.method == 'POST':
        try:
            # ── Tasks ─────────────────────────────────────────────────────────
            names = request.forms.getall('task_name[]')
            durs  = request.forms.getall('task_dur[]')

            tasks = {}
            for i in range(len(names)):
                name = names[i].strip() if i < len(names) else ''
                if not name:
                    continue
                if name in tasks:
                    raise ValueError(f'Задача «{name}» указана дважды.')
                try:
                    dur = int(durs[i]) if i < len(durs) else 0
                except (ValueError, TypeError):
                    raise ValueError(
                        f'Длительность задачи «{name}» должна быть '
                        f'целым числом ≥ 0.'
                    )
                tasks[name] = dur

            if not tasks:
                raise ValueError('Список задач не может быть пустым.')

            # ── Dependencies ──────────────────────────────────────────────────
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
            result['gcrit']  = _json.dumps(result['critical_path'])
            result['gtasks'] = _json.dumps(result['tasks'])
            result['ges']    = _json.dumps(result['es'])
            result['gef']    = _json.dumps(result['ef'])

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Критический путь — Практика',
        active_page='cpm',
        year=_year(),
        result=result,
        error=error,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  /coloring/practice
# ─────────────────────────────────────────────────────────────────────────────
@route('/coloring/practice', method=['GET', 'POST'])
@view('coloring_practice')
def coloring_practice():
    result = None
    error  = None

    if request.method == 'POST':
        try:
            # ── Vertices ──────────────────────────────────────────────────────
            vertices = [v.strip()
                        for v in request.forms.getall('vertex[]')
                        if v.strip()]
            if not vertices:
                raise ValueError('Список дисциплин не может быть пустым.')
            if len(vertices) != len(set(vertices)):
                raise ValueError('Дисциплины должны иметь уникальные имена.')

            # ── Conflict edges ────────────────────────────────────────────────
            cf    = request.forms.getall('edge_from[]')
            ct    = request.forms.getall('edge_to[]')
            edges = [
                (cf[i], ct[i])
                for i in range(len(cf))
                if i < len(ct) and cf[i] and ct[i]
            ]

            result = color_graph(vertices, edges)

            result['gv'] = _json.dumps(vertices)
            result['ge'] = _json.dumps([[u, v] for u, v in edges])
            result['gc'] = _json.dumps(result['colors'])

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
        title='Раскраска графа — Практика',
        active_page='coloring',
        year=_year(),
        result=result,
        error=error,
    )
