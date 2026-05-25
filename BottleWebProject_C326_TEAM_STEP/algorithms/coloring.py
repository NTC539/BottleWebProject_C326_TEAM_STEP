def color_graph(
    vertices: list,
    edges: list,
) -> dict:
    """
    Welsh-Powell greedy graph coloring with single-vertex recoloring optimization.

    Returns:
        {
            "num_colors": int,
            "colors":    {vertex: color_number},
            "schedule":  {color_number: [vertices]},
        }
    Raises:
        ValueError if an edge references a vertex not in `vertices`.
    """
    vertex_set = set(vertices)

    # Validate edges
    for u, v in edges:
        if u not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {u}")
        if v not in vertex_set:
            raise ValueError(f"Неизвестная вершина: {v}")

    # Build undirected adjacency
    adj: dict[str, set] = {v: set() for v in vertices}
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)

    # Stage 1 — Welsh-Powell greedy coloring
    # Sort by degree descending, then alphabetically for ties
    order = sorted(vertices, key=lambda v: (-len(adj[v]), v))

    colors: dict[str, int] = {}
    for v in order:
        forbidden = {colors[u] for u in adj[v] if u in colors}
        color = 1
        while color in forbidden:
            color += 1
        colors[v] = color

    # Stage 2 — single-vertex recoloring optimization
    improved = True
    while improved:
        improved = False
        max_color = max(colors.values())
        for v in list(vertices):
            if colors[v] != max_color:
                continue
            forbidden = {colors[u] for u in adj[v]}
            for c in range(1, max_color):
                if c not in forbidden:
                    colors[v] = c
                    break
        if max_color not in colors.values():
            improved = True

    # Build schedule
    schedule: dict[int, list] = {}
    for v, c in colors.items():
        schedule.setdefault(c, []).append(v)
    for lst in schedule.values():
        lst.sort()

    return {
        "num_colors": len(schedule),
        "colors": colors,
        "schedule": schedule,
    }
