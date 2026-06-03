import heapq


def route_network(
    vertices: list,
    edges: list,
    source: str,
) -> dict:

    INF = float('inf')
    vertex_set = set(vertices)

    if source not in vertex_set:
        raise ValueError(f"Источник не найден: {source}")

    for u, v, w in edges:
        if u not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {u}")
        if v not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {v}")
        if w != INF and w <= 0:
            raise ValueError("Вес дуги должен быть > 0 или равен inf")

    skipped_edges = []
    working_edges = []
    for u, v, w in edges:
        if w == INF:
            skipped_edges.append((u, v, w))
        else:
            working_edges.append((u, v, w))

    # build adjacency list from working edges 
    adj = {v: [] for v in vertices}
    for u, v, w in working_edges:
        adj[u].append((v, w))

    # Dijkstra 
    dist = {v: INF for v in vertices}
    prev = {v: None for v in vertices}
    dist[source] = 0.0

    heap = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:          # stale entry — skip
            continue
        for v, w in adj[u]:
            new_dist = dist[u] + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    # reconstruct paths
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

    # unreachable list 
    unreachable = [v for v in vertices if dist[v] == INF]

    return {
        "distances":     dist,
        "paths":         paths,
        "unreachable":   unreachable,
        "skipped_edges": skipped_edges,
    }
