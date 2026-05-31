"""
Routes and views for the bottle application.
"""

import json as _json
import os as _os
from bottle import route, view, request
from datetime import datetime
from algorithms.cpm import find_critical_path


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


@route('/dijkstra')
@view('dijkstra_theory')
def dijkstra():
    return dict(year=_year())


@route('/bridges')
@view('bridges_theory')
def bridges():
    return dict(year=_year())


@route('/cpm')
@view('cpm_theory')
def cpm():
    return dict(year=_year())

@route('/cpm/practice', method=['GET', 'POST'])
@view('cpm_practice')
def cpm_practice():
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            names = request.forms.getunicode('task_name[]')
            durations = request.forms.getunicode('task_dur[]')

            tasks = {}

            for i in range(len(names)):
                name = names[i].strip() if i < len(names) else ''
                if not name:
                    continue
                if name in tasks:
                    raise ValueError(f'Задача «{name}» указана дважды.')
                try:
                    dur = int(durations[i]) if i < len(durations) else 0
                except (ValueError, TypeError):
                    raise ValueError(
                        f'Длительность задачи «{name}» должна быть '
                        f'целым числом ≥ 0.'
                    )
                tasks[name] = dur

            if not tasks:
                raise ValueError('Список задач не может быть пустым.')

            df   = request.forms.getall('dep_from[]')
            dt   = request.forms.getall('dep_to[]')
            deps = [
                (df[i], dt[i])
                for i in range(len(df))
                if i < len(dt) and df[i] and dt[i]
            ]

            result = find_critical_path(tasks, deps)
            result['tasks'] = tasks   # для таблицы в шаблоне

            result['gv']     = _json.dumps(list(tasks.keys()))
            result['ge']     = _json.dumps([[a, b] for a, b in deps])
            result['gcrit']  = _json.dumps(result['critical_path'])
            result['gtasks'] = _json.dumps(result['tasks'])
            result['ges']    = _json.dumps(result['es'])
            result['gef']    = _json.dumps(result['ef'])

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f'Ошибка: {e}'

    return dict(
    title='Критический путь — Практика (POST)',
    active_page='cpm',
    year=_year(),
    result=result,
    error=error,
    )



@route('/coloring')
@view('coloring_theory')
def coloring():
    return dict(year=_year())



