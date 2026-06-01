import random


MAX_SUBJECTS = 20

SAMPLE_SUBJECTS = [
    {"name": "Математика", "teacher": "Иванов"},
    {"name": "Физика", "teacher": "Петров"},
    {"name": "Информатика", "teacher": "Сидорова"},
    {"name": "История", "teacher": "Иванов"},
    {"name": "Английский язык", "teacher": "Смирнова"},
    {"name": "Экономика", "teacher": "Петров"},
]

SAMPLE_CONFLICTS = [
    ("Математика", "Физика"),
    ("Математика", "Информатика"),
    ("Физика", "Информатика"),
    ("Физика", "История"),
    ("Информатика", "Экономика"),
    ("История", "Экономика"),
    ("История", "Английский язык"),
    ("Экономика", "Английский язык"),
]

class ColoringInputError(Exception):
    def __init__(self, errors):
        super().__init__("\n".join(errors))
        self.errors = errors


def sample_coloring_data():
    subjects = []
    for subject in SAMPLE_SUBJECTS:
        subjects.append({"name": subject["name"], "teacher": subject["teacher"]})
    return subjects, list(SAMPLE_CONFLICTS)


def load_coloring_json(data):
    if not isinstance(data, dict):
        raise ColoringInputError(["JSON должен содержать объект."])

    if not isinstance(data.get("subjects"), list):
        raise ColoringInputError(["В JSON должен быть список subjects."])
    if not isinstance(data.get("conflicts", []), list):
        raise ColoringInputError(["В JSON поле conflicts должно быть списком."])

    subjects = []
    for i, item in enumerate(data.get("subjects", []), start=1):
        if not isinstance(item, dict):
            raise ColoringInputError(["Дисциплина №{} в JSON должна быть объектом.".format(i)])
        subjects.append({
            "name": clean_text(item.get("name")),
            "teacher": clean_text(item.get("teacher")),
        })

    conflicts = []
    for i, item in enumerate(data.get("conflicts", []), start=1):
        if not isinstance(item, list) or len(item) < 2:
            raise ColoringInputError(["Конфликт №{} в JSON должен быть парой дисциплин.".format(i)])
        conflicts.append((clean_text(item[0]), clean_text(item[1])))

    subjects, conflicts, teachers = check_input(subjects, conflicts)
    return subjects, conflicts


def generate_random_data(count, density):
    count = max(1, min(MAX_SUBJECTS, int(count)))
    density = max(0, min(1, float(density)))
    teachers = ["Иванов", "Петров", "Сидорова", "Смирнова", "Кузнецов"]

    subjects = []
    for i in range(1, count + 1):
        subjects.append({
            "name": "Дисциплина {}".format(i),
            "teacher": teachers[(i - 1) % len(teachers)],
        })

    conflicts = []
    for i in range(count):
        for j in range(i + 1, count):
            if random.random() <= density:
                conflicts.append((subjects[i]["name"], subjects[j]["name"]))

    return subjects, conflicts


def solve_coloring(subjects, conflicts):
    subjects, conflicts, teachers = check_input(subjects, conflicts)
    vertices = []
    for subject in subjects:
        vertices.append(subject["name"])

    graph = make_graph(vertices, conflicts)

    if len(conflicts) == 0:
        colors = {}
        for vertex in vertices:
            colors[vertex] = 1
        order = sorted(vertices)
    else:
        order = sort_vertices(vertices, graph)
        colors = greedy_coloring(order, graph)
        colors = compact_schedule(vertices, graph, colors)
        colors = reduce_color_count(vertices, graph, colors)
        colors = optimize_teachers(vertices, graph, colors, teachers)
        colors = renumber_colors(colors)

    schedule = make_schedule(subjects, colors)

    return {
        "subjects": subjects,
        "num_colors": max(colors.values()) if colors else 0,
        "colors": colors,
        "schedule": schedule,
        "teacher_shifts": make_teacher_table(colors, teachers),
        "teacher_cost": teacher_cost(colors, teachers),
        "order": order,
        "degrees": get_degrees(vertices, graph),
        "conflicts": conflicts,
    }


def check_input(subjects, conflicts):
    errors = []
    good_subjects = []
    names = set()

    for i, subject in enumerate(subjects, start=1):
        if not isinstance(subject, dict):
            errors.append("Строка {} с дисциплиной задана некорректно.".format(i))
            continue

        name = clean_text(subject.get("name"))
        teacher = clean_text(subject.get("teacher"))

        if name == "" and teacher == "":
            continue
        if name == "":
            errors.append("В строке {} не указана дисциплина.".format(i))
            continue
        if teacher == "":
            errors.append("Для дисциплины «{}» не указан преподаватель.".format(name))

        lower_name = name.lower()
        if lower_name in names:
            errors.append("Дисциплина «{}» указана повторно.".format(name))
            continue

        names.add(lower_name)
        good_subjects.append({"name": name, "teacher": teacher})

    if len(good_subjects) == 0:
        errors.append("Добавьте хотя бы одну дисциплину.")
    if len(good_subjects) > MAX_SUBJECTS:
        errors.append("Количество дисциплин не должно превышать {}.".format(MAX_SUBJECTS))

    subject_names = set()
    for subject in good_subjects:
        subject_names.add(subject["name"])

    good_conflicts = []
    added_conflicts = set()

    for i, conflict in enumerate(conflicts, start=1):
        if not isinstance(conflict, (list, tuple)) or len(conflict) < 2:
            errors.append("Конфликт №{} задан некорректно.".format(i))
            continue

        first = clean_text(conflict[0])
        second = clean_text(conflict[1])

        if first == "" and second == "":
            continue
        if first == "" or second == "":
            errors.append("В конфликте №{} должны быть две дисциплины.".format(i))
            continue
        if first == second:
            continue
        if first not in subject_names:
            errors.append("Не найдена дисциплина «{}».".format(first))
            continue
        if second not in subject_names:
            errors.append("Не найдена дисциплина «{}».".format(second))
            continue

        key = tuple(sorted([first, second]))
        if key not in added_conflicts:
            added_conflicts.add(key)
            good_conflicts.append((first, second))

    if errors:
        raise ColoringInputError(errors)

    teachers = {}
    for subject in good_subjects:
        teachers[subject["name"]] = subject["teacher"]

    return good_subjects, good_conflicts, teachers


def make_graph(vertices, conflicts):
    graph = {}
    for vertex in vertices:
        graph[vertex] = set()

    for first, second in conflicts:
        graph[first].add(second)
        graph[second].add(first)

    return graph


def sort_vertices(vertices, graph):
    return sorted(vertices, key=lambda vertex: (-len(graph[vertex]), vertex.lower()))


def greedy_coloring(order, graph):
    colors = {}

    for vertex in order:
        forbidden = set()
        for neighbor in graph[vertex]:
            if neighbor in colors:
                forbidden.add(colors[neighbor])

        color = 1
        while color in forbidden:
            color += 1

        colors[vertex] = color

    return colors


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


def reduce_color_count(vertices, graph, colors):
    if len(vertices) > 12:
        return colors

    current_count = max(colors.values())

    for limit in range(current_count - 1, 0, -1):
        new_colors = {}
        if paint_with_limit(vertices, graph, new_colors, limit):
            colors = new_colors
            current_count = limit
        else:
            break

    return colors


def paint_with_limit(vertices, graph, colors, limit):
    if len(colors) == len(vertices):
        return True

    vertex = choose_next_vertex(vertices, graph, colors)

    for color in range(1, limit + 1):
        can_use = True
        for neighbor in graph[vertex]:
            if colors.get(neighbor) == color:
                can_use = False
                break

        if can_use:
            colors[vertex] = color
            if paint_with_limit(vertices, graph, colors, limit):
                return True
            del colors[vertex]

    return False


def choose_next_vertex(vertices, graph, colors):
    best_vertex = None
    best_used_colors = -1
    best_degree = -1

    for vertex in vertices:
        if vertex in colors:
            continue

        used_colors = set()
        for neighbor in graph[vertex]:
            if neighbor in colors:
                used_colors.add(colors[neighbor])

        if len(used_colors) > best_used_colors:
            best_vertex = vertex
            best_used_colors = len(used_colors)
            best_degree = len(graph[vertex])
        elif len(used_colors) == best_used_colors and len(graph[vertex]) > best_degree:
            best_vertex = vertex
            best_degree = len(graph[vertex])

    return best_vertex


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


def neighbor_colors(vertex, graph, colors):
    result = set()
    for neighbor in graph[vertex]:
        result.add(colors[neighbor])
    return result


def teacher_cost(colors, teachers):
    shifts = {}

    for subject, color in colors.items():
        teacher = teachers[subject]
        if teacher not in shifts:
            shifts[teacher] = set()
        shifts[teacher].add(color)

    cost = 0
    for teacher in shifts:
        if len(shifts[teacher]) > 1:
            cost += len(shifts[teacher]) - 1

    return cost


def renumber_colors(colors):
    old_numbers = sorted(set(colors.values()))
    numbers = {}

    for i, old_number in enumerate(old_numbers, start=1):
        numbers[old_number] = i

    new_colors = {}
    for vertex in colors:
        new_colors[vertex] = numbers[colors[vertex]]

    return new_colors


def make_schedule(subjects, colors):
    schedule = []
    max_color = max(colors.values()) if colors else 0

    for color in range(1, max_color + 1):
        row = {"shift": color, "subjects": []}
        for subject in subjects:
            if colors[subject["name"]] == color:
                row["subjects"].append(subject)
        schedule.append(row)

    return schedule


def make_teacher_table(colors, teachers):
    table = {}

    for subject, color in colors.items():
        teacher = teachers[subject]
        if teacher not in table:
            table[teacher] = set()
        table[teacher].add(color)

    result = []
    for teacher in sorted(table):
        result.append({"teacher": teacher, "shifts": sorted(table[teacher])})

    return result


def get_degrees(vertices, graph):
    degrees = {}
    for vertex in vertices:
        degrees[vertex] = len(graph[vertex])
    return degrees


def clean_text(value):
    return str(value or "").strip()
