# Соответствие блок-схемы и кода алгоритма

Файл схемы: `graph.drawio` (диаграмма `color_graph_FULL`)
Файл кода: `algorithms/coloring.py`

Схема разбита на четыре секции и две подсекции. Ниже каждая секция сопоставлена с функцией Python — с указанием конкретных узлов схемы и строк кода.

---

## Общий конвейер

Точка входа для всего алгоритма — функция `solve_coloring` ([строки 109–134](algorithms/coloring.py)):

```
check_input → make_graph → sort_vertices → greedy_coloring
    → compact_schedule → reduce_color_count → optimize_teachers
    → renumber_colors → make_schedule
```

Схема охватывает четыре этапа этого конвейера. Два вызова (`reduce_color_count`, `renumber_colors`) в схему **не включены** — см. раздел «Что не отражено в схеме» в конце.

---

## Секция 1: Построение графа → `make_graph`

**Код:** [строки 212–220](algorithms/coloring.py)

```python
def make_graph(vertices, conflicts):
    graph = {vertex: set() for vertex in vertices}
    for first, second in conflicts:
        graph[first].add(second)
        graph[second].add(first)
    return graph
```

| Узел схемы | Содержимое | Строка кода |
|------------|-----------|-------------|
| A1 | Начало | — |
| A2 | Ввод: vertices, edges | параметры `vertices`, `conflicts` |
| A3 | `adj[v] = {}` для всех v | `graph = {vertex: set() for vertex in vertices}` |
| A4 | Цикл для каждого `(u, v) ∈ edges` | `for first, second in conflicts:` |
| A5 | `u ≠ v ?` | в коде эта проверка делается раньше — в `check_input`, петли отсеиваются там |
| A6 | `adj[u] += v; adj[v] += u` | `graph[first].add(second); graph[second].add(first)` |

**Переход из секции 1 в секцию 2:** конец цикла A4 по левой стрелке `e05` ведёт сразу в B1 — в схеме это выход из цикла по ребру (exhausted).

---

## Секция 2: Welsh-Powell → `sort_vertices` + `greedy_coloring`

**Код:** [строки 223–240](algorithms/coloring.py)

```python
def sort_vertices(vertices, graph):
    return sorted(vertices, key=lambda vertex: (-len(graph[vertex]), vertex.lower()))

def greedy_coloring(order, graph):
    colors = {}
    for vertex in order:
        forbidden = {colors[neighbor] for neighbor in graph[vertex] if neighbor in colors}
        color = 1
        while color in forbidden:
            color += 1
        colors[vertex] = color
    return colors
```

| Узел схемы | Содержимое | Строка кода |
|------------|-----------|-------------|
| B1 | `order = сортировка по (−степень, имя)` | `sort_vertices` целиком |
| B2 | `colors = {}` | `colors = {}` в `greedy_coloring` |
| B3 | Цикл для каждой `v ∈ order` | `for vertex in order:` |
| B4 | `forbidden = {colors[u] \| u∈adj[v], u∈colors}` | `forbidden = {colors[neighbor] for neighbor in graph[vertex] if neighbor in colors}` |
| B5 | `color = 1` | `color = 1` |
| B6 | `color ∈ forbidden ?` | `while color in forbidden:` |
| B7 | `color += 1` (Да) | `color += 1` |
| B8 | `colors[v] = color` (Нет) | `colors[vertex] = color` |

**Цикл B6–B7:** стрелка `e17` из B7 обратно в B6 — это `while color in forbidden: color += 1`.

**Цикл B3–B8:** стрелка `e18` из B8 обратно в B3 — это возврат к следующей `vertex` в `for vertex in order`.

**Переход из секции 2 в секцию 3:** узел `CON-C1` (→С3) — выход из цикла B3 когда все вершины обработаны. Соединитель `CON-from-S2` (←С2) в секции 3 принимает управление.

---

## Секция 3, шаг 3.1: Уплотнение расписания → `compact_schedule`

**Код:** [строки 243–267](algorithms/coloring.py)

```python
def compact_schedule(vertices, graph, colors):
    changed = True
    while changed:
        changed = False
        max_color = max(colors.values())
        for vertex in vertices:
            if colors[vertex] != max_color:
                continue
            forbidden = neighbor_colors(vertex, graph, colors)
            for color in range(1, max_color):
                if color not in forbidden:
                    colors[vertex] = color
                    break
            if max_color not in colors.values():
                colors = renumber_colors(colors)
                changed = True
                break
    return colors
```

| Узел схемы | Содержимое | Строка кода |
|------------|-----------|-------------|
| C1 | `есть_улучшения = True` | `changed = True` (инициализация перед `while`) |
| C2 | `есть_улучшения ?` | `while changed:` |
| C3 | `есть_улучшения = False` | `changed = False` |
| C4 | `max_color = max(colors.values())` | `max_color = max(colors.values())` |
| C5 | Цикл `для каждой v ∈ vertices` | `for vertex in vertices:` |
| C6 | `colors[v] = max_color ?` | `if colors[vertex] != max_color: continue` |
| C7 | `forbidden = {colors[u] \| u∈adj[v]}` | `forbidden = neighbor_colors(vertex, graph, colors)` |
| C8 | Цикл `для c от 1 до max_color−1` | `for color in range(1, max_color):` |
| C9 | `c ∉ forbidden ?` | `if color not in forbidden:` |
| C10 | `colors[v] = c` | `colors[vertex] = color; break` |
| C11 | `max_color ∉ colors.values() ?` | `if max_color not in colors.values():` |
| C12 | `есть_улучшения = True` | `changed = True; break` |

**Внешний цикл (C2 → C3 → … → C12 → C2):** `while changed` — повторяется, пока удаётся убрать хотя бы один старший цвет.

**Внутренний цикл C5:** когда все вершины перебраны без успеха, C5 выходит и попадает в C11. Если `max_color` исчез — C12 устанавливает `changed = True` и `break` возвращает к C2. Если нет — C11→C2 и цикл заканчивается (Нет).

**Переход к шагу 3.2:** стрелка `f03` из C2 (Нет) ведёт в E1 — это выход из `compact_schedule` и вход в `optimize_teachers`.

---

## Секция 3, шаг 3.2: Минимизация конфликтов преподавателей → `optimize_teachers`

**Код:** [строки 314–342](algorithms/coloring.py)

```python
def optimize_teachers(vertices, graph, colors, teachers):
    changed = True
    while changed:
        changed = False
        for vertex in vertices:
            old_color = colors[vertex]
            old_cost = teacher_cost(colors, teachers)
            forbidden = neighbor_colors(vertex, graph, colors)
            for color in sorted(set(colors.values())):
                if color == old_color or color in forbidden:
                    continue
                colors[vertex] = color
                new_cost = teacher_cost(colors, teachers)
                if new_cost < old_cost:
                    changed = True
                    break
                colors[vertex] = old_color
            if changed:
                break
    return colors
```

| Узел схемы | Содержимое | Строка кода |
|------------|-----------|-------------|
| E1 | `есть_улучшения = True` | `changed = True` (инициализация) |
| E2 | `есть_улучшения ?` | `while changed:` |
| E3 | `есть_улучшения = False` | `changed = False` |
| E4 | `max_color = max(colors.values())` | не явный — служит для задания диапазона цикла E7; в коде это `sorted(set(colors.values()))` |
| E5 | Цикл `для каждой v ∈ vertices` | `for vertex in vertices:` |
| E6 | `old_c; old_cost; forbidden` | `old_color = colors[vertex]`; `old_cost = teacher_cost(...)`; `forbidden = neighbor_colors(...)` |
| E7 | Цикл `для c от 1 до max_color` | `for color in sorted(set(colors.values())):` |
| E8 | `c = old_c ИЛИ c ∈ forbidden ?` | `if color == old_color or color in forbidden: continue` |
| E9 | `colors[v] = c` | `colors[vertex] = color` |
| E10 | `teacher_conflicts(colors) < old_cost ?` | `new_cost = teacher_cost(...); if new_cost < old_cost:` |
| E11 | `colors[v] = old_c` (откат) | `colors[vertex] = old_color` |

**При улучшении (E10 → Да):** `changed = True; break` — стрелка `g13` возвращает в E5. В коде это `if changed: break` после внутреннего цикла, что перезапускает весь `while changed`.

**При откате (E10 → Нет → E11):** стрелка `g15` возвращает в E7 — перебираем следующий цвет.

**Вспомогательная функция `FUNC` в схеме:** блок `teacher_conflicts(colors)` в схеме соответствует `teacher_cost` ([строки 350–358](algorithms/coloring.py)):

```python
def teacher_cost(colors, teachers):
    shifts = {}
    for subject, color in colors.items():
        teacher = teachers[subject]
        shifts.setdefault(teacher, set()).add(color)
    return sum(max(0, len(s) - 1) for s in shifts.values())
```

Штраф = количество смен у преподавателя минус одна. Схема называет это `конфликты`, код — `cost`.

**Переход к секции 4:** стрелка `g02` из E2 (Нет) ведёт в D1.

---

## Секция 4: Построение расписания → `make_schedule`

**Код:** [строки 368–378](algorithms/coloring.py)

```python
def make_schedule(subjects, colors):
    max_color = max(colors.values()) if colors else 0
    return [
        {
            "shift": color,
            "subjects": [subject for subject in subjects if colors[subject["name"]] == color],
        }
        for color in range(1, max_color + 1)
    ]
```

| Узел схемы | Содержимое | Строка кода |
|------------|-----------|-------------|
| D1 | `schedule = {}` | инициализация list comprehension |
| D2 | Цикл `для каждой v ∈ vertices` | внешний `for color in range(...)` + внутренний перебор subjects |
| D3 | `schedule[colors[v]] += v` | `"subjects": [s for s in subjects if colors[s["name"]] == color]` |
| D4 | Вывод: `num_colors, colors, schedule` | словарь в `return` из `solve_coloring` |
| D5 | Конец | `return` |

---

## Что не отражено в схеме

В коде между секцией 3 и секцией 4 вызываются ещё два шага, которых нет в блок-схеме:

### `reduce_color_count` ([строки 270–285](algorithms/coloring.py))

Для графов с **≤ 12 вершинами** запускает рекурсивный перебор с возвратом (`paint_with_limit`): пытается раскрасить граф в `k−1` цветов, где `k` — текущее количество. Если удаётся — принимает результат и пробует ещё раз с `k−2`. Остановка при первой неудаче.

Этот шаг может уменьшить число смен сверх того, что даёт `compact_schedule`.

### `renumber_colors` ([строки 361–365](algorithms/coloring.py))

Перенумеровывает цвета подряд начиная с 1 — устраняет «дыры» вида `{1, 3, 4}` → `{1, 2, 3}`. Вызывается дважды: внутри `compact_schedule` (когда старший цвет исчезает) и в `solve_coloring` после всей оптимизации.

---

## Схема соединений между секциями

```
Секция 1 (A1–A6)
    make_graph
        │  конец цикла A4 → e05
        ▼
Секция 2 (B1–B8)
    sort_vertices + greedy_coloring
        │  CON-C1 (→С3) — конец цикла B3
        ▼
Секция 3.1 (C1–C12)          [не в схеме: reduce_color_count]
    compact_schedule
        │  f03: C2 = False → E1
        ▼
Секция 3.2 (E1–E11)
    optimize_teachers          FUNC = teacher_cost
        │  g02: E2 = False → D1
        ▼                      [не в схеме: renumber_colors]
Секция 4 (D1–D5)
    make_schedule
        │
        ▼
      Конец (D5)
```
