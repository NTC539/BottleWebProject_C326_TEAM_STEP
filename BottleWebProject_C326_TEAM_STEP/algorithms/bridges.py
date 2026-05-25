"""
algorithms/bridges.py — Bridge finding (Tarjan) + Floyd-Warshall impact analysis.
Standard library only.
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
        "bridge_impact" : list[{"edge": ..., "delta": float | None}],
        "total_path_sum": float,
        "all_pairs"     : dict[str, dict[str, float]],
    }

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
    disc = {}
    low  = {}
    visited = set()
    timer   = [0]
    bridges = []

    def dfs(v, parent):
        disc[v] = low[v] = timer[0]
        timer[0] += 1
        visited.add(v)
        for u, w in adj[v]:
            if u == parent:
                continue
            if u not in visited:
                dfs(u, v)
                low[v] = min(low[v], low[u])
                if low[u] > disc[v]:
                    bridges.append((v, u, w))
            else:
                low[v] = min(low[v], disc[u])

    for v in vertices:
        if v not in visited:
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

    all_pairs = floyd_warshall(vertices, edges)
    total_path_sum = float(sum(
        all_pairs[u][v]
        for u in vertices for v in vertices
        if u != v and all_pairs[u][v] != INF
    ))

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
        D2 = floyd_warshall(vertices, edges_without)

        # Was any previously-reachable pair severed?
        graph_split = any(
            all_pairs[i][j] != INF and D2[i][j] == INF
            for i in vertices for j in vertices if i != j
        )

        if graph_split:
            delta = None
        else:
            new_sum = sum(
                D2[i][j]
                for i in vertices for j in vertices
                if i != j and D2[i][j] != INF
            )
            delta = new_sum - total_path_sum

        bridge_impact.append({
            "edge":  (b_u, b_v, b_w),
            "delta": delta,
        })

    return {
        "bridges":        bridges,
        "bridge_impact":  bridge_impact,
        "total_path_sum": total_path_sum,
        "all_pairs":      all_pairs,
    }
