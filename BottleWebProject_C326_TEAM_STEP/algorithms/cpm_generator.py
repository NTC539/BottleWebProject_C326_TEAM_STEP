import random
import string

def generate_random_cpm(
    min_tasks=4,
    max_tasks=15,
    min_dur=1,
    max_dur=20,
    extra_edge_prob=0.15,      # оставлен для совместимости, но игнорируется, если density задан
    start_prob=0.15,
    max_in_degree=None,
    density=1.2                # новое: среднее число исходящих рёбер на вершину (рекомендуется 1.2–2.0)
):
    """
    Генерирует случайный DAG с контролируемой плотностью.

    density : float
        Желаемое отношение общего числа рёбер к числу вершин.
        При density ≈ 1.5 граф будет умеренно связным, без перегруженных узлов.
        Если density=None, используется старый вероятностный метод (перебор всех пар).
    """
    n = random.randint(min_tasks, max_tasks)
    if n > 26:
        raise ValueError("Максимум 26 задач (букв A-Z)")
    names = list(string.ascii_uppercase[:n])

    tasks = [{"name": name, "dur": random.randint(min_dur, max_dur)}
             for name in names]

    deps = []
    in_degree = [0] * n
    out_degree = [0] * n

    if density is not None:
        # ── 1. Строим базовый каркас: случайное ориентированное дерево (от ранних к поздним) ──
        # Для каждой вершины j (кроме первой) с вероятностью (1 - start_prob) подвешиваем её
        # к одной случайной вершине i < j, соблюдая max_in_degree.
        for j in range(1, n):
            if random.random() < start_prob:
                continue   # начальная задача
            candidates = [i for i in range(j)
                          if max_in_degree is None or in_degree[j] < max_in_degree]
            if not candidates:
                continue
            i = random.choice(candidates)
            deps.append([names[i], names[j]])
            in_degree[j] += 1
            out_degree[i] += 1

        # ── 2. Добавляем дополнительные рёбра до достижения желаемой плотности ──
        target_edges = int(n * density)
        current_edges = len(deps)
        # Возможные пары (i,j) i<j, ещё не соединённые
        possible = [(i, j) for i in range(n) for j in range(i+1, n)
                    if [names[i], names[j]] not in deps
                    and (max_in_degree is None or in_degree[j] < max_in_degree)]
        random.shuffle(possible)

        for i, j in possible:
            if current_edges >= target_edges:
                break
            deps.append([names[i], names[j]])
            in_degree[j] += 1
            out_degree[i] += 1
            current_edges += 1

    else:
        # Старый режим (для обратной совместимости), если density=None
        for j in range(1, n):
            if random.random() < start_prob:
                continue
            candidates = [i for i in range(j)
                          if max_in_degree is None or in_degree[j] < max_in_degree]
            if not candidates:
                continue
            guaranteed = random.choice(candidates)
            deps.append([names[guaranteed], names[j]])
            in_degree[j] += 1
            for i in range(j):
                if i == guaranteed:
                    continue
                if max_in_degree is not None and in_degree[j] >= max_in_degree:
                    break
                if random.random() < extra_edge_prob:
                    deps.append([names[i], names[j]])
                    in_degree[j] += 1

    return {"tasks": tasks, "deps": deps}