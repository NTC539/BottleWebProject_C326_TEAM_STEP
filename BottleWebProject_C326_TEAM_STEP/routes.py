"""
Routes and views for the bottle application.
"""

import json as _json
import os as _os
import json
from bottle import route, view, request, response
from datetime import datetime
from algorithms.bridges import analyze_network
from bridges_generator import generate_random_bridges


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


@route('/dijkstra')
@view('dijkstra_theory')
def dijkstra():
    return dict(year=_year())


@route('/bridges')
@view('bridges_theory')
def bridges():
    return dict(year=_year())


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


@route('/coloring')
@view('coloring_theory')
def coloring():
    return dict(year=_year())
