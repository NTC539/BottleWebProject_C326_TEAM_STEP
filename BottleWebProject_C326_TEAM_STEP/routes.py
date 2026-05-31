"""
Routes and views for the bottle application.
"""

import json as _json
import os as _os
from bottle import route, view, request
from datetime import datetime


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
        return dict(
        title='Критический путь — Практика (POST)',
        active_page='cpm',
        year=_year(),
        result=result,
        error=error,
    )
    elif request.method == 'GET':
        return dict(
        title='Критический путь — Практика (GET)',
        active_page='cpm',
        year=_year(),
        result=result,
        error=error,
    )



@route('/coloring')
@view('coloring_theory')
def coloring():
    return dict(year=_year())



