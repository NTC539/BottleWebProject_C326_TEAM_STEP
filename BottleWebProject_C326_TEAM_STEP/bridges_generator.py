"""
Генератор случайного взвешенного связного неориентированного графа.

Используется маршрутом /bridges/generate. К самому алгоритму
(algorithms/bridges.py) не относится — сознательно вынесен в отдельный модуль.
"""

import random
import string


def generate_random_bridges(min_nodes=4, max_nodes=8, min_w=1, max_w=9,
                            extra_edge_prob=0.30):
    """
    Возвращает словарь со случайным взвешенным связным графом.

    Формат:
        {
            "nodes": ["A", "B", ...],
            "edges": [["A", "B", 3], ...]   # неориентированные рёбра с весом
        }

    Гарантии:
        * имена вершин — A, B, C, ... по алфавиту;
        * граф связный: сначала строится случайное остовное дерево
          (каждая новая вершина соединяется с одной из предыдущих);
        * дополнительные случайные рёбра создают циклы, поэтому часть
          рёбер перестаёт быть мостами (результат нагляднее);
        * веса — случайные целые из [min_w, max_w].
    """
    n = random.randint(min_nodes, max_nodes)
    names = list(string.ascii_uppercase[:n])

    edges = []
    seen = set()

    def add_edge(a, b):
        key = frozenset((a, b))
        if a == b or key in seen:
            return
        seen.add(key)
        edges.append([a, b, random.randint(min_w, max_w)])

    # Остовное дерево — гарантия связности.
    for j in range(1, n):
        i = random.randint(0, j - 1)
        add_edge(names[i], names[j])

    # Дополнительные рёбра — создают циклы (убирают часть мостов).
    for j in range(n):
        for i in range(j):
            if random.random() < extra_edge_prob:
                add_edge(names[i], names[j])

    return {"nodes": names, "edges": edges}
