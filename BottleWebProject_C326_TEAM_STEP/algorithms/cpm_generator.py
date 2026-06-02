import random
import string

def generate_random_cpm(
    min_tasks=4,
    max_tasks=10,
    min_dur=1,
    max_dur=20,
    extra_edge_prob=0.15,
    start_prob=0.15,
    max_in_degree=None,
    density=1.2        
):
    """
    Генерирует случайный направленный ациклический граф (DAG) для задачи CPM.

    Параметры
    ----------
    min_tasks, max_tasks : int
        Границы диапазона, из которого случайно выбирается количество задач n.
    min_dur, max_dur : int
        Границы случайной длительности каждой задачи.
    extra_edge_prob : float (0.0 .. 1.0)
        Используется ТОЛЬКО при density=None.
        Вероятность провести дополнительное ребро i → j для каждой пары (i < j).
    start_prob : float (0.0 .. 1.0)
        Вероятность для задачи (кроме первой) остаться стартовой, т.е. не получить
        ни одного обязательного предшественника. Первая задача всегда стартовая.
    max_in_degree : int или None
        Ограничение на количество входящих рёбер у одной задачи.
        Позволяет избежать узлы, в которые приходит слишком много зависимостей.
    density : float или None
        Если задано число:
        общее количество рёбер будет примерно равно n * density.

    Возвращает
    ----------
    dict с ключами:
        "tasks" : list[dict]  — список словарей {"name": str, "dur": int}
        "deps"  : list[list]  — список рёбер в формате [предшественник, последователь]
    """

    # Определение количества задач
    n = random.randint(min_tasks, max_tasks)
    if n > 26:
        raise ValueError("Максимум 26 задач (букв A-Z)")

    # Имена задач: первые n букв латинского алфавита
    names = list(string.ascii_uppercase[:n])

    tasks = [{"name": name, "dur": random.randint(min_dur, max_dur)}
             for name in names]

    deps = [] # Результирующий список зависимостей
    in_degree = [0] * n  # Входящая степень каждой вершины

    # Ветвление на режим генерации
    if density is not None:
        # -- Генерация зависимостей на основе значения плотности графа --
        
        # Проходим по всем задачам, кроме первой (A всегда стартовая).
        # С вероятностью (1 - start_prob) подвешиваем задачу j к одной
        # случайной задаче i, которая находится левее (i < j).
        # Это гарантирует ацикличность и связность графа.
        for j in range(1, n):
            # С вероятностью start_prob пропускаем — задача остаётся стартовой
            if random.random() < start_prob:
                continue

            # Список возможных предшественников для задачи j:
            # все вершины левее j, у которых ещё не превышен лимит входящих рёбер
            candidates = [i for i in range(j)
                          if max_in_degree is None or in_degree[j] < max_in_degree]
            if not candidates:
                continue # Невозможно добавить предшественника

            # Выбираем одного случайного предшественника и добавляем ребро
            i = random.choice(candidates)
            deps.append([names[i], names[j]])
            in_degree[j] += 1

        # ── Добавляем дополнительные рёбра до достижения желаемой плотности ──
        target_edges = int(n * density) # Количество необходимых ребёр в графе
        current_edges = len(deps) # Количество рёбер на данный момент

        # Составляем список всех возможных направленных рёбер (i → j),
        # которые ещё НЕ добавлены и не нарушают ограничение max_in_degree
        possible = [(i, j) for i in range(n) for j in range(i+1, n)
                    if [names[i], names[j]] not in deps
                    and (max_in_degree is None or in_degree[j] < max_in_degree)]
        
        random.shuffle(possible)

        # Добавляем рёбра, пока не достигнем целевого количества
        for i, j in possible:
            if current_edges >= target_edges:
                break
            deps.append([names[i], names[j]])
            in_degree[j] += 1
            current_edges += 1

    else:
        # -- Генерация зависимостей на основе значения вероятности появления зависимости (extra_edge_prob) --

        for j in range(1, n):
            # С вероятностью start_prob пропускаем — задача остаётся стартовой
            if random.random() < start_prob:
                continue

            # Список возможных предшественников для задачи j:
            # все вершины левее j, у которых ещё не превышен лимит входящих рёбер
            candidates = [i for i in range(j)
                          if max_in_degree is None or in_degree[j] < max_in_degree]
            
            if not candidates:
                continue # Невозможно добавить предшественника
            
            # Один обязательный предшественник (гарантирует связность)
            guaranteed = random.choice(candidates)
            deps.append([names[guaranteed], names[j]])
            in_degree[j] += 1

            # Перебираем все пары (i, j), где i < j, i != guaranteed
            # и с вероятностью extra_edge_prob добавляем дополнительное ребро
            for i in range(j):
                # Избегаем повторного добавления гарантированной зависимости
                if i == guaranteed:
                    continue

                # Если достигнут лимит входящих рёбер — прекращаем
                if max_in_degree is not None and in_degree[j] >= max_in_degree:
                    break
                if random.random() < extra_edge_prob:
                    deps.append([names[i], names[j]])
                    in_degree[j] += 1

    return {"tasks": tasks, "deps": deps}