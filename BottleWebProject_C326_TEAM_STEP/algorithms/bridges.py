"""
algorithms/bridges.py — Bridge finding (Tarjan) + Floyd-Warshall impact analysis.
Standard library only.

Соответствует блок-схеме (algoritm_bridges_horiz.drawio) и ТЗ (разделы 2.2.1–2.2.4):
  • Тарьян: disc[v] == -1 — признак непосещённой вершины, мост при low[u] > disc[v];
  • Флойд–Уоршелл: суммы база/новая_сумма берутся по парам i < j и ВКЛЮЧАЮТ ∞,
    поэтому при потере связности сумма обращается в ∞ (ТЗ стр.233, 407);
  • δ = новая_сумма − база; при разрыве сети δ = ∞ (мост критический);
  • δ_отн = δ / база — относительное увеличение (ТЗ стр.231).
Так как удаление любого моста по определению разрывает граф, для каждого моста
δ = ∞ — это и есть наглядный признак потери связности сети.
"""


def analyze_network(vertices: list, edges: list) -> dict:
    """
    Analyse a weighted undirected graph: find all bridges (Tarjan's DFS)
    and estimate the impact of each bridge removal (Floyd-Warshall).

    Parameters
    ----------
    vertices : list[str]  — unique vertex names.
    edges    : list[tuple[str, str, float]]  — (u, v, weight), undirected.

    Returns
    -------
    {
        "bridges"       : list[tuple[str, str, float]],
        "bridge_impact" : list[{"edge": ..., "delta": float, "delta_rel": float}],
        "total_path_sum": float,            # база; ∞, если исходный граф несвязен
        "all_pairs"     : dict[str, dict[str, float]],
    }
    delta / delta_rel могут быть равны float('inf') при потере связности.

    Raises
    ------
    ValueError("Неизвестная вершина: X") — vertex in edge not in vertices.
    ValueError("Вес ребра должен быть > 0") — weight <= 0.
    """
    INF = float('inf')
    vertex_set = set(vertices)

    # ── Validation ────────────────────────────────────────────────────────────
    for u, v, w in edges:
        if u not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {u}")
        if v not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {v}")
        if w <= 0:
            raise ValueError("Вес ребра должен быть > 0")

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

    # ── Stage 2: Floyd-Warshall ───────────────────────────────────────────────
    def floyd_warshall(verts, edge_list):
        d = {u: {v: (0.0 if u == v else INF) for v in verts} for u in verts}
        for u, v, w in edge_list:
            fw = float(w)
            if fw < d[u][v]:
                d[u][v] = fw
                d[v][u] = fw
        for k in verts:
            dk = d[k]
            for i in verts:
                di = d[i]
                dik = di[k]
                if dik == INF:
                    continue
                for j in verts:
                    candidate = dik + dk[j]
                    if candidate < di[j]:
                        di[j] = candidate
        return d

    def path_sum(dist):
        """Сумма кратчайших путей по парам i < j, ВКЛЮЧАЯ ∞.

        Если хотя бы одна пара недостижима, сумма равна ∞ — это наглядно
        показывает потерю связности сети (ТЗ стр.233, узлы c4/d19 блок-схемы).
        """
        total = 0.0
        for idx, i in enumerate(vertices):
            for j in vertices[idx + 1:]:
                d = dist[i][j]
                if d == INF:
                    return INF
                total += d
        return total

    all_pairs = floyd_warshall(vertices, edges)
    base = path_sum(all_pairs)            # «база»
    total_path_sum = base

    # ── Bridge impact ─────────────────────────────────────────────────────────
    bridge_impact = []
    for b_u, b_v, b_w in bridges:
        edges_without = [
            (u, v, w) for u, v, w in edges
            if not (
                (u == b_u and v == b_v and w == b_w) or
                (u == b_v and v == b_u and w == b_w)
            )
        ]
        d_new = floyd_warshall(vertices, edges_without)
        new_sum = path_sum(d_new)         # «новая_сумма»

        # δ = новая_сумма − база; при разрыве сети новая_сумма == ∞ → δ = ∞.
        if new_sum == INF:
            delta = INF
        else:
            delta = new_sum - base

        # Относительное увеличение δ / база (ТЗ стр.231).
        if base == 0:
            delta_rel = 0.0
        elif delta == INF or base == INF:
            delta_rel = INF
        else:
            delta_rel = delta / base

        bridge_impact.append({
            "edge":      (b_u, b_v, b_w),
            "delta":     delta,
            "delta_rel": delta_rel,
        })

    return {
        "bridges":        bridges,
        "bridge_impact":  bridge_impact,
        "total_path_sum": total_path_sum,
        "all_pairs":      all_pairs,
    }
