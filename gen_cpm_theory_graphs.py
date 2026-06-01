#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор 3 иллюстраций графа для страницы теории CPM.
Запуск: python gen_cpm_theory_graphs.py
Результат: BottleWebProject_C326_TEAM_STEP/static/content/
    cpm_theory_struct.svg    — структура графа (задачи и зависимости)
    cpm_theory_forward.svg   — прямой проход (ES / EF)
    cpm_theory_critical.svg  — выделенный критический путь A → C → E

Пример полностью соответствует тексту теории:
    A(3), B(2), C(4), D(1), E(2), F(3)
    Зависимости: C←A, D←{A,B}, E←C, F←D
    Критический путь: A → C → E,  T = 9
"""
import os
import math

# ── Данные примера ───────────────────────────────────────────────────────────
NODES = {
    'A': (75, 70), 'B': (75, 180),
    'C': (235, 70), 'D': (235, 180),
    'E': (395, 70), 'F': (395, 180),
}
DUR = {'A': 3, 'B': 2, 'C': 4, 'D': 1, 'E': 2, 'F': 3}
ES = {'A': 0, 'B': 0, 'C': 3, 'D': 3, 'E': 7, 'F': 4}
EF = {'A': 3, 'B': 2, 'C': 7, 'D': 4, 'E': 9, 'F': 7}
EDGES = [('A', 'C'), ('A', 'D'), ('B', 'D'), ('C', 'E'), ('D', 'F')]
CRIT_NODES = {'A', 'C', 'E'}
CRIT_EDGES = {('A', 'C'), ('C', 'E')}

W, H = 470, 250
RX, RY = 36, 26  # полуоси эллипса узла

# ── Цвета (палитра проекта) ──────────────────────────────────────────────────
N_FILL, N_STROKE, N_TEXT = '#e8f4fb', '#2e86ab', '#1a3a5c'
C_FILL, C_STROKE, C_TEXT = '#e84855', '#b3122a', '#ffffff'
E_NORMAL, E_CRIT = '#9bb8cc', '#e84855'
FONT = 'font-family="Arial,sans-serif"'


def trim(x1, y1, x2, y2, d1, d2):
    """Укорачивает отрезок с обоих концов, чтобы стрелка не заходила в узлы."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    return (x1 + ux * d1, y1 + uy * d1, x2 - ux * d2, y2 - uy * d2)


def header():
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n'
            f'<defs>\n'
            f'  <marker id="an" markerWidth="9" markerHeight="7" refX="8" refY="3.5" '
            f'orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="{E_NORMAL}"/></marker>\n'
            f'  <marker id="ac" markerWidth="9" markerHeight="7" refX="8" refY="3.5" '
            f'orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="{E_CRIT}"/></marker>\n'
            f'</defs>\n'
            f'<rect width="{W}" height="{H}" fill="white"/>')


def edge(u, v, crit):
    x1, y1 = NODES[u]
    x2, y2 = NODES[v]
    x1, y1, x2, y2 = trim(x1, y1, x2, y2, RX + 2, RX + 6)
    color = E_CRIT if crit else E_NORMAL
    width = 3 if crit else 1.4
    mk = 'ac' if crit else 'an'
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" marker-end="url(#{mk})"/>')


def node(name, mode):
    x, y = NODES[name]
    crit = mode == 'critical' and name in CRIT_NODES
    fill, stroke, text = (C_FILL, C_STROKE, C_TEXT) if crit else (N_FILL, N_STROKE, N_TEXT)
    sw = 3 if crit else 1.6
    out = [f'<ellipse cx="{x}" cy="{y}" rx="{RX}" ry="{RY}" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    if mode == 'forward':
        out.append(f'<text x="{x}" y="{y - 7}" text-anchor="middle" '
                   f'dominant-baseline="central" font-size="14" font-weight="bold" '
                   f'{FONT} fill="{text}">{name}</text>')
        out.append(f'<text x="{x}" y="{y + 10}" text-anchor="middle" '
                   f'dominant-baseline="central" font-size="10" '
                   f'{FONT} fill="{text}">ES{ES[name]} · EF{EF[name]}</text>')
    else:
        out.append(f'<text x="{x}" y="{y - 6}" text-anchor="middle" '
                   f'dominant-baseline="central" font-size="15" font-weight="bold" '
                   f'{FONT} fill="{text}">{name}</text>')
        out.append(f'<text x="{x}" y="{y + 11}" text-anchor="middle" '
                   f'dominant-baseline="central" font-size="10" '
                   f'{FONT} fill="{text}">d={DUR[name]}</text>')
    return '\n'.join(out)


def build(mode):
    buf = [header()]
    for (u, v) in EDGES:
        crit = mode == 'critical' and (u, v) in CRIT_EDGES
        buf.append(edge(u, v, crit))
    for name in NODES:
        buf.append(node(name, mode))
    buf.append('</svg>')
    return '\n'.join(buf)


def main():
    out_dir = os.path.join(
        os.path.dirname(__file__),
        'BottleWebProject_C326_TEAM_STEP', 'static', 'content'
    )
    os.makedirs(out_dir, exist_ok=True)
    files = {
        'cpm_theory_struct.svg': 'struct',
        'cpm_theory_forward.svg': 'forward',
        'cpm_theory_critical.svg': 'critical',
    }
    for fname, mode in files.items():
        path = os.path.join(out_dir, fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(build(mode))
        print(f'SVG saved: {path}')


if __name__ == '__main__':
    main()
