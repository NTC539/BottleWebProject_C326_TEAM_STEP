"""
Генератор случайных входных данных для метода критического пути (CPM).

Используется маршрутом /cpm/generate. Не относится к самому алгоритму
(algorithms/cpm.py) и сознательно вынесен в отдельный модуль.
"""

import random
import string


def generate_random_cpm(min_tasks=4, max_tasks=10, min_dur=1, max_dur=12,
                         extra_edge_prob=0.35):
    """
    Возвращает словарь со случайным набором задач и зависимостей.

    Формат:
        {
            "tasks": [{"name": "A", "dur": 5}, ...],   # от 4 до 10 задач
            "deps":  [["A", "B"], ...]                 # рёбра предшествования
        }

    Гарантии:
        * имена задач — A, B, C, ... по алфавиту;
        * длительности — случайные целые из [min_dur, max_dur];
        * граф зависимостей всегда ацикличен: ребро строится только
          от задачи с меньшим индексом к задаче с большим (i < j),
          поэтому цикл невозможен в принципе.
    """
    n = random.randint(min_tasks, max_tasks)
    names = list(string.ascii_uppercase[:n])  # A..J максимум при n=10

    tasks = [{"name": name, "dur": random.randint(min_dur, max_dur)}
             for name in names]

    deps = []
    # Для каждой задачи (кроме первой) гарантируем хотя бы одного
    # предшественника — чтобы граф был связным, а критический путь осмысленным.
    for j in range(1, n):
        guaranteed = random.randint(0, j - 1)
        deps.append([names[guaranteed], names[j]])
        # Дополнительные случайные «прямые» рёбра (i < j) — без дублей и циклов.
        for i in range(j):
            if i != guaranteed and random.random() < extra_edge_prob:
                deps.append([names[i], names[j]])

    return {"tasks": tasks, "deps": deps}
