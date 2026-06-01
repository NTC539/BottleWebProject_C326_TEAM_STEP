"""
Генератор случайных входных данных для метода критического пути (CPM).
Сохранена обратная совместимость с исходным вызовом.
"""

import random
import string

def generate_random_cpm(
    min_tasks=15,
    max_tasks=15,
    min_dur=1,
    max_dur=20,
    extra_edge_prob=0.15, 
    start_prob=0.15,
    max_in_degree=10
):
    """
    Возвращает словарь со случайным набором задач и зависимостей.

    Параметры
    ----------
    min_tasks, max_tasks : int
        Границы числа задач.
    min_dur, max_dur : int
        Границы длительностей задач.
    extra_edge_prob : float
        Вероятность добавления *дополнительного* ребра i→j (i<j) сверх гарантированного.
        (Исходное поведение.)
    start_prob : float
        Вероятность того, что задача (кроме первой) останется без предшественников.
        При 0.0 каждая задача j>0 имеет хотя бы одного предшественника (как в исходном коде).
    max_in_degree : int или None
        Максимально допустимое число входящих рёбер для одной задачи.
    """
    n = random.randint(min_tasks, max_tasks)
    names = list(string.ascii_uppercase[:n])

    tasks = [{"name": name, "dur": random.randint(min_dur, max_dur)}
             for name in names]

    deps = []
    in_degree = [0] * n  # для учёта ограничения max_in_degree, если задано

    for j in range(1, n):
        # По умолчанию (start_prob=0) гарантированно добавляем предшественника,
        # как в исходном коде. Если start_prob>0, с вероятностью start_prob
        # задача остаётся без входящих рёбер (начальная).
        if random.random() < start_prob:
            continue

        # Формируем список допустимых кандидатов в предшественники
        candidates = [i for i in range(j)
                      if max_in_degree is None or in_degree[j] < max_in_degree]
        if not candidates:
            continue

        guaranteed = random.choice(candidates)
        deps.append([names[guaranteed], names[j]])
        in_degree[j] += 1

        # Дополнительные рёбра с вероятностью extra_edge_prob (как в исходном коде)
        for i in range(j):
            if i == guaranteed:
                continue
            if max_in_degree is not None and in_degree[j] >= max_in_degree:
                break
            if random.random() < extra_edge_prob:
                deps.append([names[i], names[j]])
                in_degree[j] += 1

    return {"tasks": tasks, "deps": deps}