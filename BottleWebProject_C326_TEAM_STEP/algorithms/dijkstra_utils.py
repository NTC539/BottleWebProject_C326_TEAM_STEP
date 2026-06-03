import random
from algorithms.dijkstra import route_network

def parse_edges_from_lists(edge_count, from_list, to_list, weight_list):
    """
    Валидация рёбер из переданных списков.
    Параметры:
        edge_count: количество рёбер
        from_list: список строк (от)
        to_list: список строк (до)
        weight_list: список строк (вес)
    Возвращает:
        edges_raw: список кортежей (from, to, weight) где weight – float или inf
        edges_display: список (from, to, weight_str) для повторного отображения
        errors: список ошибок
    """
    edges_raw = []
    edges_display = []
    errors = []

    for i in range(edge_count):
        from_v = from_list[i].strip() if i < len(from_list) else ''
        to_v = to_list[i].strip() if i < len(to_list) else ''
        w_str = weight_list[i].strip().lower() if i < len(weight_list) else ''
        edges_display.append((from_v, to_v, w_str))

        if not from_v or not to_v or not w_str:
            errors.append(f'Ребро {i+1}: все поля должны быть заполнены.')
            continue
        if len(from_v) > 10:
            errors.append(f'Ребро {i+1}: название вершины "{from_v}" не должно превышать 10 символов')
            continue
        if len(to_v) > 10:
            errors.append(f'Ребро {i+1}: название вершины "{to_v}" не должно превышать 10 символов')
            continue

        try:
            if w_str == 'inf':
                w = float('inf')
            else:
                w = float(w_str)
                if w <= 0:
                    errors.append(f'Ребро {i+1}: вес должен быть > 0, получено {w}')
                    continue
        except ValueError:
            errors.append(f'Ребро {i+1}: вес "{w_str}" не является числом или "inf"')
            continue

        edges_raw.append((from_v, to_v, w))

    return edges_raw, edges_display, errors


def parse_edges_from_text(content, max_edges=25):
    """
    Парсит рёбра из текстового содержимого файла (строка).
    Каждая строка: from,to,weight  (разделители запятая или пробел)
    Возвращает:
        edges: список кортежей (from, to, weight_str)
        edge_count: количество успешно распарсенных рёбер
        all_vertices: множество вершин
        errors: список ошибок
    """
    edges = []
    errors = []
    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        parts = line.replace(',', ' ').split()
        if len(parts) >= 3:
            from_v = parts[0].strip()
            to_v = parts[1].strip()
            weight = parts[2].strip().lower()
            if len(from_v) > 10 or len(to_v) > 10:
                errors.append(f'Строка {line_num}: название вершины слишком длинное (макс. 10 символов)')
            else:
                edges.append((from_v, to_v, weight))
        else:
            errors.append(f'Строка {line_num}: игнорируется (не хватает данных)')

    if len(edges) > max_edges:
        errors.append(f'Файл содержит более {max_edges} рёбер, это слишком много.')
        edges = edges[:max_edges]

    all_vertices = set()
    for f, t, _ in edges:
        all_vertices.add(f)
        all_vertices.add(t)

    return edges, len(edges), all_vertices, errors


def generate_random_graph(vertex_set=None, min_edges=4, max_edges=9):
    """
    Генерирует случайный ориентированный граф.
    Параметры:
        vertex_set: список вершин (по умолчанию ['A','B','C','D','E','F'])
        min_edges, max_edges: диапазон количества рёбер
    Возвращает:
        edges: список кортежей (from, to, weight_str)
        source: выбранный источник (первая вершина первого ребра)
    """
    if vertex_set is None:
        vertex_set = ['A', 'B', 'C', 'D', 'E', 'F']
    edge_count = random.randint(min_edges, max_edges)
    edges = []
    used_pairs = set()
    for _ in range(edge_count):
        from_v = random.choice(vertex_set)
        to_v = random.choice(vertex_set)
        while from_v == to_v or (from_v, to_v) in used_pairs:
            to_v = random.choice(vertex_set)
        used_pairs.add((from_v, to_v))
        weight = str(random.randint(1, 20)) if random.random() < 0.85 else 'inf'
        edges.append((from_v, to_v, weight))

    source = edges[0][0] if edges else 'A'
    return edges, source


def run_dijkstra_and_prepare_results(edges_raw, source):
    """
    Выполняет алгоритм Дейкстры и подготавливает структуру results.
    Возвращает:
        results: словарь { vertex: { 'dist', 'dist_display', 'path', 'path_display' } }
        graph_edges: исходный список рёбер (с float)
        errors: список ошибок
    """
    vertices_set = set()
    for u, v, _ in edges_raw:
        vertices_set.add(u)
        vertices_set.add(v)
    vertices = list(vertices_set)

    if source not in vertices:
        return None, None, [f'Вершина-источник "{source}" не найдена среди вершин графа.']

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
        sorted_results = dict(sorted(results.items(), key=lambda item: item[1]['dist']))
        return sorted_results, edges_raw, []
    except ValueError as e:
        return None, None, [str(e)]


def export_edges_to_string(edges_display):
    """
    Формирует строку для экспорта рёбер из списка отображаемых рёбер.
    Параметры:
        edges_display: список кортежей (from, to, weight_str)
    Возвращает:
        content: строка в формате from,to,weight (построчно)
        success: bool
    """
    lines = []
    for from_v, to_v, weight in edges_display:
        if from_v and to_v and weight:
            lines.append(f"{from_v},{to_v},{weight}")
    if not lines:
        return "", False
    return "\n".join(lines), True