"""
Routes and views for the bottle application.
"""

from cmath import inf
import json
import os
from bottle import route, view, request, response, template
from datetime import datetime
from algorithms.coloring import (
    ColoringInputError,
    generate_random_data,
    load_coloring_json,
    make_export_data,
    sample_coloring_data,
    solve_coloring,
)

def _year():
    return datetime.now().year


@route('/')
@route('/home')
@view('index')
def home():
    return dict(year=_year())


@route('/about')
@view('about')
def about():
    return dict(year=_year())


@route('/graph_theory')
@view('graph_theory')
def graph_theory():
    return dict(year=_year())


@route('/dijkstra')
@view('dijkstra_theory')
def dijkstra():
    return dict(year=_year())


@route('/bridges')
@view('bridges_theory')
def bridges():
    return dict(year=_year())

@route('/coloring/practice', method=['GET', 'POST'])
@view('coloring_practice')
def coloring_practice():
    """Страница практики 4-го варианта: ручной ввод, генерация, импорт, экспорт и расчёт."""
    subjects, conflicts = sample_coloring_data()
    errors = []
    result = None
    subject_count = '12'
    density = '0.35'

    if request.method == 'POST':
        action = request.forms.get('form_action') or 'calculate'
        subject_count = request.forms.get('subject_count') or subject_count
        density = request.forms.get('density') or density

        if action == 'generate':
            try:
                subjects, conflicts = generate_random_data(int(subject_count), float(str(density).replace(',', '.')))
            except ValueError:
                errors.append('Проверьте количество дисциплин и плотность графа.')
        elif action == 'load_json':
            try:
                upload = request.files.get('json_file')
                if not upload or not upload.filename:
                    raise ColoringInputError(['Выберите JSON-файл для загрузки.'])
                payload = upload.file.read().decode('utf-8-sig')
                subjects, conflicts = load_coloring_json(json.loads(payload))
            except json.JSONDecodeError:
                errors.append('JSON-файл не удалось прочитать. Проверьте структуру данных.')
            except UnicodeDecodeError:
                errors.append('Файл должен быть сохранён в кодировке UTF-8.')
            except ColoringInputError as exc:
                errors.extend(exc.errors)
        elif action == 'export_json':
            subjects, conflicts = _read_coloring_form()
            try:
                result = solve_coloring(subjects, conflicts)
                subjects = result['subjects']
                conflicts = result['conflicts']
                return _export_coloring_json(subjects, conflicts, result)
            except ColoringInputError as exc:
                errors.extend(exc.errors)
        else:
            subjects, conflicts = _read_coloring_form()
            try:
                result = solve_coloring(subjects, conflicts)
                subjects = result['subjects']
                conflicts = result['conflicts']
                _save_coloring_history(subjects, conflicts, result)
            except ColoringInputError as exc:
                errors.extend(exc.errors)

    return dict(
        year=_year(),
        subjects=subjects,
        conflicts=conflicts,
        errors=errors,
        result=result,
        subject_count=subject_count,
        density=density,
    )


def _read_coloring_form():
    """Читает дисциплины и конфликты из полей отправленной формы."""
    names = request.forms.getall('subject[]')
    teachers = request.forms.getall('teacher[]')
    subjects = []
    for index, name in enumerate(names):
        teacher = teachers[index] if index < len(teachers) else ''
        subjects.append({'name': name, 'teacher': teacher})

    conflict_from = request.forms.getall('conflict_from[]')
    conflict_to = request.forms.getall('conflict_to[]')
    conflicts = []
    for index, left in enumerate(conflict_from):
        right = conflict_to[index] if index < len(conflict_to) else ''
        conflicts.append((left, right))

    return subjects, conflicts


def _export_coloring_json(subjects, conflicts, result):
    """Отдаёт результат расчёта как загружаемый JSON-файл, совместимый с импортом."""
    data = make_export_data(subjects, conflicts, result)
    filename = 'coloring_result_{}.json'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

    response.content_type = 'application/json; charset=utf-8'
    response.set_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
    return json.dumps(data, ensure_ascii=False, indent=2)


def _save_coloring_history(subjects, conflicts, result):
    """Дописывает выполненный расчёт в файл истории data/coloring_history.json."""
    project_root = os.path.abspath(os.path.dirname(__file__))
    history_dir = os.path.join(project_root, 'data')
    history_path = os.path.join(history_dir, 'coloring_history.json')
    os.makedirs(history_dir, exist_ok=True)

    entry = {
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input': {
            'subjects': subjects,
            'conflicts': conflicts,
        },
        'result': {
            'num_colors': result['num_colors'],
            'colors': result['colors'],
            'schedule': result['schedule'],
            'teacher_shifts': result['teacher_shifts'],
        },
    }

    try:
        with open(history_path, 'r', encoding='utf-8') as file:
            history = json.load(file)
        if not isinstance(history, list):
            history = []
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(entry)
    with open(history_path, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


@route('/bridges/practice', method=['GET', 'POST'])
@view('bridges_practice')
def bridges_practice():
    return dict(year=_year())


@route('/cpm')
@view('cpm_theory')
def cpm():
    return dict(year=_year())

@route('/cpm/practice')
@view('cpm_practice')
def cpm():
    return dict(year=_year())


@route('/coloring')
@view('coloring_theory')
def coloring():
    return dict(year=_year())


@route('/dijkstra/practice', method=['GET', 'POST'])
@view('dijkstra_practice')
def dijkstra_practice():
    edges_text = ''
    source = 'A'
    errors = []
    graph_edges = None
    results = None
    results_json = 'null'
    
    errors.append('Ошибка 1')
    errors.append('Ошибка 2')

    edges_text = """A,B,4
A,C,2
C,B,1
B,D,5
C,D,8
D,E,2
A,E,inf"""

    source = "A"

    graph_edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("C", "B", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("D", "E", 2),
        ("A", "E", float("inf")),
    ]

    results = {
        "A": {"dist": 0, "path": ["A"]},
        "B": {"dist": 3, "path": ["A", "C", "B"]},
        "C": {"dist": 2, "path": ["A", "C"]},
        "D": {"dist": 8, "path": ["A", "C", "B", "D"]},
        "E": {"dist": 10, "path": ["A", "C", "B", "D", "E"]},
    }

    prepared_edges = []
    for (frm, to, w) in graph_edges:
        status = "Исключён (∞)" if w == inf else "Участвует"
        weight_display = "∞" if w == inf else str(w)
        prepared_edges.append((frm, to, weight_display, status))

    # Подготавливаем результаты с готовым отображением пути и расстояния
    prepared_results = {}
    for node, data in results.items():
        dist = data['dist']
        dist_display = "недостижим" if dist == inf else str(dist)
        path_display = " → ".join(data['path']) if data['path'] else "—"
        prepared_results[node] = {
            'dist_display': dist_display,
            'path_display': path_display
        }

    # Теперь передаём в шаблон подготовленные данные
    return template('dijkstra_practice.tpl',
                    edges=edges_text,
                    source=source,
                    errors=errors,
                    prepared_edges=prepared_edges,   # вместо graph_edges
                    prepared_results=prepared_results,  # вместо results
                    year=2025)



