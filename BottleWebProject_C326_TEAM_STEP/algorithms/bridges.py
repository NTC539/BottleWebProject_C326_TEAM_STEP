"""
Для исходного графа и для каждого графа после удаления одного из мостов выдаются
три матрицы (весов, смежности 0/1, кратчайших путей) и список рёбер графа.
"""

import math


def analyze_network(vertices: list, edges: list) -> dict:
    """
    Analyse a weighted undirected graph: find all bridges (Tarjan's DFS) and,
    for the original graph and for the graph after removing each bridge, build
    three matrices (weights, adjacency 0/1, shortest paths) plus the edge list.

    Parameters
    ----------
    vertices : list[str]  — unique vertex names.
    edges    : list[tuple[str, str, float]]  — (u, v, weight), undirected.

    Returns
    -------
    {
        "bridges"        : list[tuple[str, str, float]],
        "total_path_sum" : float,           # сумма кратч. путей ИСХОДНОГО графа;
                                             # ∞, если исходный граф несвязен
        "states"         : list[{
            "removed": None | tuple[str, str, float],   # удалённый мост (None — исходный)
            "edges"  : list[tuple[str, str, float]],    # рёбра этого графа (для vis.js)
            "weight" : dict[str, dict[str, float]],     # матрица весов (прямые рёбра)
            "adj"    : dict[str, dict[str, int]],       # матрица смежности 0/1
            "dist"   : dict[str, dict[str, float]],     # матрица кратчайших путей
        }],
    }
    states[0] всегда описывает исходный граф (removed=None); далее по одному
    элементу на каждый найденный мост в порядке списка bridges.
    Значения матриц весов и кратчайших путей могут быть float('inf').

    Raises
    ------
    ValueError("Неизвестная вершина: X") — vertex in edge not in vertices.
    ValueError("Петля недопустима: ребро X—X") — u == v (self-loop).
    ValueError("Вес ребра должен быть конечным числом") — weight is inf/nan.
    ValueError("Вес ребра должен быть > 0") — weight <= 0.
    ValueError("Ребро X—Y задано дважды") — параллельное/обратное ребро
        (ломает корректность Тарьяна — даёт ложный мост).
    """
    INF = float('inf')
    vertex_set = set(vertices)

    # ── Validation ────────────────────────────────────────────────────────────
    # Дубль/реверс ребра запрещён осознанно: алгоритм Тарьяна ниже пропускает
    # ребро к родителю (`u == parent`), поэтому параллельное ребро было бы
    # ошибочно засчитано как мост. Простой граф — обязательное предусловие.
    seen_edges = set()
    for u, v, w in edges:
        if u not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {u}")
        if v not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {v}")
        if u == v:
            raise ValueError(f"Петля недопустима: ребро {u}—{u}")
        if not math.isfinite(w):
            raise ValueError("Вес ребра должен быть конечным числом")
        if w <= 0:
            raise ValueError("Вес ребра должен быть > 0")
        key = frozenset((u, v))
        if key in seen_edges:
            raise ValueError(f"Ребро {u}—{v} задано дважды")
        seen_edges.add(key)

    # ── Adjacency list ────────────────────────────────────────────────────────
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    # ── Stage 1: Tarjan's bridge finding ─────────────────────────────────────
    # disc[v] == -1  →  вершина ещё не посещена (как на блок-схеме, узлы a3/f5).
    disc = {v: -1 for v in vertices}
    low  = {v: 0 for v in vertices}
    timer   = [0]
    bridges = []

    def dfs(v, parent):
        disc[v] = low[v] = timer[0]
        timer[0] += 1
        for u, w in adj[v]:
            if u == parent:
                continue
            if disc[u] != -1:                       # обратное ребро (u уже посещена)
                low[v] = min(low[v], disc[u])
            else:                                   # дерево DFS
                dfs(u, v)
                low[v] = min(low[v], low[u])
                if low[u] > disc[v]:
                    bridges.append((v, u, w))

    for v in vertices:
        if disc[v] == -1:
            dfs(v, None)

    # ── Stage 2: matrices for a given edge list ───────────────────────────────
    def floyd_warshall(edge_list):
        """Матрица кратчайших путей: диагональ 0, нет пути — ∞ (узлы b*/d*)."""
        d = {u: {v: (0.0 if u == v else INF) for v in vertices} for u in vertices}
        for u, v, w in edge_list:
            fw = float(w)
            if fw < d[u][v]:
                d[u][v] = fw
                d[v][u] = fw
        for k in vertices:
            dk = d[k]
            for i in vertices:
                di = d[i]
                dik = di[k]
                if dik == INF:
                    continue
                for j in vertices:
                    candidate = dik + dk[j]
                    if candidate < di[j]:
                        di[j] = candidate
        return d

    def weight_matrix(edge_list):
        """Матрица весов: вес прямого ребра, 0 на диагонали, ∞ при отсутствии ребра."""
        w_m = {u: {v: (0.0 if u == v else INF) for v in vertices} for u in vertices}
        for u, v, w in edge_list:
            fw = float(w)
            if fw < w_m[u][v]:
                w_m[u][v] = fw
                w_m[v][u] = fw
        return w_m

    def adjacency_matrix(edge_list):
        """Матрица смежности 0/1: 1 при наличии прямого ребра, иначе 0."""
        a_m = {u: {v: 0 for v in vertices} for u in vertices}
        for u, v, w in edge_list:
            a_m[u][v] = 1
            a_m[v][u] = 1
        return a_m

    def make_state(removed, edge_list):
        return {
            "removed": removed,
            "edges":   list(edge_list),
            "weight":  weight_matrix(edge_list),
            "adj":     adjacency_matrix(edge_list),
            "dist":    floyd_warshall(edge_list),
        }

    def path_sum(dist):
        """Сумма кратчайших путей по парам i < j, ВКЛЮЧАЯ ∞.

        Если хотя бы одна пара недостижима, сумма равна ∞ — это наглядно
        показывает несвязность исходной сети (ТЗ раздел 2.2.2, узлы c1–c7).
        """
        total = 0.0
        for idx, i in enumerate(vertices):
            for j in vertices[idx + 1:]:
                d = dist[i][j]
                if d == INF:
                    return INF
                total += d
        return total

    # ── Stage 3: original graph + graph per bridge ────────────────────────────
    states = [make_state(None, edges)]

    # Сумма кратчайших путей считается ОДИН РАЗ — на исходном графе.
    total_path_sum = path_sum(states[0]["dist"])

    for b_u, b_v, b_w in bridges:
        edges_without = [
            (u, v, w) for u, v, w in edges
            if not (
                (u == b_u and v == b_v and w == b_w) or
                (u == b_v and v == b_u and w == b_w)
            )
        ]
        states.append(make_state((b_u, b_v, b_w), edges_without))

    return {
        "bridges":        bridges,
        "total_path_sum": total_path_sum,
        "states":         states,
    }
