"""
algorithms/cpm.py — Critical Path Method (CPM) for project scheduling.
Standard library only.
"""

import bisect


def find_critical_path(tasks: dict, dependencies: list) -> dict:
    """
    Find the critical path of a project represented as a DAG.

    Parameters
    ----------
    tasks : dict[str, int]
        Mapping of task name → duration (>= 0).
    dependencies : list[tuple[str, str]]
        Directed edges (predecessor, successor).

    Returns
    -------
    dict with keys:
        "duration"      : int          — total project duration
        "critical_path" : list[str]    — tasks in execution order
        "es"            : dict[str, int] — Early Start for each task
        "ef"            : dict[str, int] — Early Finish for each task

    Raises
    ------
    ValueError("Граф содержит цикл")    if a cycle is detected.
    ValueError("Неизвестная задача: X") if a task referenced in
                                         dependencies is absent from tasks.
    """
    task_set = set(tasks)

    # ── Validate dependencies ─────────────────────────────────────────────────
    for u, v in dependencies:
        if u not in task_set:
            raise ValueError(f"Неизвестная задача: {u}")
        if v not in task_set:
            raise ValueError(f"Неизвестная задача: {v}")

    # ── Build directed graph ──────────────────────────────────────────────────
    succs: dict = {v: [] for v in tasks}   # v → list of successors
    preds: dict = {v: [] for v in tasks}   # v → list of predecessors
    in_degree: dict = {v: 0 for v in tasks}

    for u, v in dependencies:
        succs[u].append(v)
        preds[v].append(u)
        in_degree[v] += 1

    # ── Kahn's topological sort (alphabetically stable for determinism) ───────
    queue = sorted(v for v in tasks if in_degree[v] == 0)
    in_deg = dict(in_degree)      # working copy
    topo_order: list = []

    while queue:
        u = queue.pop(0)
        topo_order.append(u)
        for v in sorted(succs[u]):
            in_deg[v] -= 1
            if in_deg[v] == 0:
                bisect.insort(queue, v)

    if len(topo_order) < len(tasks):
        raise ValueError("Граф содержит цикл")

    # ── Forward pass: compute ES and EF ──────────────────────────────────────
    es: dict = {}
    ef: dict = {}

    for v in topo_order:
        es[v] = max((ef[u] for u in preds[v]), default=0)
        ef[v] = es[v] + tasks[v]

    duration: int = max(ef.values())

    # ── Critical path reconstruction ──────────────────────────────────────────
    # A task belongs to the critical set if EF == duration.
    # A "critical sink" is a critical task whose successors are NOT in the
    # critical set (i.e. the path ends here, it is not an intermediate node).
    critical_set = {v for v in tasks if ef[v] == duration}
    critical_sinks = sorted(
        v for v in critical_set
        if not any(w in critical_set for w in succs[v])
    )

    # Backtrack from the first critical sink (alphabetical tie-break).
    path: list = []
    current = critical_sinks[0]

    while True:
        path.append(current)
        # A predecessor u is on the critical path when EF[u] == ES[current].
        crit_preds = sorted(u for u in preds[current] if ef[u] == es[current])
        if not crit_preds:
            break
        current = crit_preds[0]   # alphabetical tie-break

    path.reverse()

    return {
        "duration": duration,
        "critical_path": path,
        "es": es,
        "ef": ef,
    }
