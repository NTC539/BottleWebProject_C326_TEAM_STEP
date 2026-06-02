"""
algorithms/dijkstra.py — Dijkstra shortest-path routing with OSPF modification.
Standard library only.
"""

import heapq


def route_network(
    vertices: list,
    edges: list,
    source: str,
) -> dict:
    """
    Find shortest paths from source to all vertices in a directed weighted graph,
    ignoring edges with weight float('inf') (OSPF modification).

    Parameters
    ----------
    vertices : list[str]  — unique node names.
    edges    : list[tuple[str, str, float]]  — directed edges (u, v, weight).
               weight must be > 0 or float('inf').
    source   : str  — source node.

    Returns
    -------
    {
        "distances"    : dict[str, float],
        "paths"        : dict[str, list[str]],
        "unreachable"  : list[str],
        "skipped_edges": list[tuple[str, str, float]],
    }

    Raises
    ------
    ValueError("Источник не найден: X")      — source not in vertices.
    ValueError("Неизвестная вершина: X")      — edge endpoint not in vertices.
    ValueError("Вес дуги должен быть > 0 или равен inf") — weight <= 0.
    """
    INF = float('inf')
    vertex_set = set(vertices)

    # ── Validation ────────────────────────────────────────────────────────────
    if source not in vertex_set:
        raise ValueError(f"Источник не найден: {source}")

    for u, v, w in edges:
        if u not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {u}")
        if v not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {v}")
        if w != INF and w <= 0:
            raise ValueError("Вес дуги должен быть > 0 или равен inf")

    # ── Stage 1: separate skipped (∞) edges from working edges ───────────────
    skipped_edges = []
    working_edges = []
    for u, v, w in edges:
        if w == INF:
            skipped_edges.append((u, v, w))
        else:
            working_edges.append((u, v, w))

    # ── Build adjacency list from working edges ───────────────────────────────
    adj = {v: [] for v in vertices}
    for u, v, w in working_edges:
        adj[u].append((v, w))

    # ── Stage 2: Dijkstra ─────────────────────────────────────────────────────
    dist = {v: INF for v in vertices}
    prev = {v: None for v in vertices}
    dist[source] = 0.0

    heap = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:          # stale entry — skip
            continue
        for v, w in adj[u]:
            candidate = dist[u] + w
            if candidate < dist[v]:
                dist[v] = candidate
                prev[v] = u
                heapq.heappush(heap, (candidate, v))

    # ── Stage 3: reconstruct paths ────────────────────────────────────────────
    paths = {}
    for v in vertices:
        if dist[v] == INF:
            paths[v] = []
        else:
            path = []
            cur = v
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            paths[v] = list(reversed(path))

    # ── Stage 4: unreachable list ─────────────────────────────────────────────
    unreachable = [v for v in vertices if dist[v] == INF]

    return {
        "distances":     dist,
        "paths":         paths,
        "unreachable":   unreachable,
        "skipped_edges": skipped_edges,
    }
