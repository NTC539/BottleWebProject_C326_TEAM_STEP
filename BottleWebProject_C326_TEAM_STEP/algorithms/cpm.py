from collections import deque
import sys
import bisect

def find_critical_path(tasks, dependencies):
    """
    Вычисляет критический путь проекта методом CPM.

    Параметры:
    tasks: dict {имя задачи: длительность}
    dependencies: list of tuples (предшественник, последователь)

    Возвращает:
    dict с ключами:
        duration       - общая длительность проекта
        critical_paths - список всех критических путей (списки задач)
        critical_tasks - множество критических задач
        es, ef, ls, lf, total_float - словари с соответствующими параметрами
    """
    # ── 1. Валидация входных данных ──
    task_set = set(tasks.keys())
    for u, v in dependencies:
        if u not in task_set:
            raise ValueError(f"Неизвестная задача: {u}")
        if v not in task_set:
            raise ValueError(f"Неизвестная задача: {v}")

    # ── 2. Построение графа ──
    succs = {task: [] for task in tasks}
    preds = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}

    for u, v in dependencies:
        succs[u].append(v)
        preds[v].append(u)
        in_degree[v] += 1

    # ── 3. Топологическая сортировка (алгоритм Кана, алфавитно стабильная) ──
    # Начальная очередь: все вершины с in_degree == 0, отсортированные по алфавиту
    queue = sorted([task for task in tasks if in_degree[task] == 0])
    topo_order = []
    in_deg = in_degree.copy()  # рабочая копия

    while queue:
        u = queue.pop(0)          # извлечение из начала
        topo_order.append(u)
        # последователи, отсортированные по алфавиту для детерминизма
        for v in sorted(succs[u]):
            in_deg[v] -= 1
            if in_deg[v] == 0:
                # вставка с сохранением алфавитного порядка
                bisect.insort(queue, v)

    if len(topo_order) != len(tasks):
        raise ValueError("Граф содержит цикл")

    # ── 4. Прямой проход (Early Start, Early Finish) ──
    es = {}
    ef = {}

    for v in topo_order:
        if not preds[v]:   # нет предшественников
            es[v] = 0
        else:
            max_ef = 0
            for u in preds[v]:
                if ef[u] > max_ef:
                    max_ef = ef[u]
            es[v] = max_ef
        ef[v] = es[v] + tasks[v]

    duration = max(ef.values())

    # ── 5. Обратный проход (Late Start, Late Finish) ──
    lf = {task: float('inf') for task in tasks}
    ls = {}

    # Конечные задачи: те, у которых ef == duration
    for v in tasks:
        if ef[v] == duration:
            lf[v] = duration

    # Обход в обратном топологическом порядке
    for v in reversed(topo_order):
        if succs[v]:
            min_ls = float('inf')
            for w in succs[v]:
                if ls[w] < min_ls:
                    min_ls = ls[w]
            if min_ls < lf[v]:
                lf[v] = min_ls
        # Если lf остался бесконечным (изолированная вершина)
        if lf[v] == float('inf'):
            lf[v] = duration
        ls[v] = lf[v] - tasks[v]

    # ── 6. Расчёт резервов и выделение критических задач ──
    total_float = {}
    critical_tasks = set()
    for v in tasks:
        total_float[v] = ls[v] - es[v]
        if total_float[v] == 0:
            critical_tasks.add(v)

    # ── 7. Поиск всех критических путей (рекурсивный обход) ──
    critical_paths = []

    # Стартовые критические задачи (es == 0)
    start_tasks = sorted([v for v in tasks if es[v] == 0 and v in critical_tasks])

    # Вспомогательная рекурсивная процедура (замыкание для доступа к переменным)
    def find_paths(current, current_path):
        if not succs[current]:   # нет последователей -> конечная задача
            critical_paths.append(current_path.copy())
            return
        for nxt in sorted(succs[current]):
            if nxt in critical_tasks and ef[current] == es[nxt]:
                current_path.append(nxt)
                find_paths(nxt, current_path)
                current_path.pop()

    for start in start_tasks:
        find_paths(start, [start])

    # ── 8. Возврат результата ──
    return {
        "duration": duration,
        "critical_paths": critical_paths,
        "critical_tasks": critical_tasks,
        "es": es,
        "ef": ef,
        "ls": ls,
        "lf": lf,
        "total_float": total_float
    }   