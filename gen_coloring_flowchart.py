#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор блок-схемы алгоритма color_graph (Welsh-Powell) по ГОСТ 19.701-90.
Запуск: python gen_coloring_flowchart.py
Результат: BottleWebProject_C326_TEAM_STEP/static/content/coloring_flowchart.svg
"""
import os, textwrap

# ─── SVG helpers ─────────────────────────────────────────────────────────────

ST   = 'stroke="black" stroke-width="1.5"'
FONT = 'font-family="Arial,sans-serif"'

def e(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def txt(x, y, lines, fs=11, bold=False, anchor='middle', fill='black'):
    if isinstance(lines, str):
        lines = [lines]
    w  = 'bold' if bold else 'normal'
    lh = fs + 4
    n  = len(lines)
    out = []
    for i, ln in enumerate(lines):
        ty = y + (i - (n - 1) / 2.0) * lh
        out.append(
            f'<text x="{x}" y="{ty}" text-anchor="{anchor}" '
            f'dominant-baseline="central" font-size="{fs}" {FONT} '
            f'font-weight="{w}" fill="{fill}">{e(ln)}</text>'
        )
    return '\n'.join(out)

def lbl(x, y, t, anchor='start', fs=10, italic=False, fill='#333'):
    st = 'italic' if italic else 'normal'
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" '
            f'{FONT} font-style="{st}" fill="{fill}">{e(t)}</text>')

def arr(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {ST} '
            f'marker-end="url(#A)"/>')

def seg(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {ST}/>'

def poly(pts, arrow=True):
    ps  = ' '.join(f'{x},{y}' for x, y in pts)
    mk  = 'marker-end="url(#A)"' if arrow else ''
    return f'<polyline points="{ps}" fill="none" {ST} {mk}/>'

# ─── GOST symbols ─────────────────────────────────────────────────────────────

def terminal(x, y, text, w=170, h=36):
    """Терминатор — скруглённый прямоугольник (ГОСТ 3.4.2)"""
    x0, y0 = x - w//2, y - h//2
    return (f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" '
            f'rx="{h//2}" ry="{h//2}" fill="white" {ST}/>\n'
            + txt(x, y, text, fs=12, bold=True))

def process(x, y, lines, w=330, h=40, fs=11):
    """Процесс — прямоугольник (ГОСТ 3.2.1.1)"""
    x0, y0 = x - w//2, y - h//2
    return (f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="white" {ST}/>\n'
            + txt(x, y, lines, fs=fs))

def predef(x, y, lines, w=360, h=48, fs=11):
    """Предопределённый процесс — двойные вертикальные полосы (ГОСТ 3.2.2.1)"""
    x0, y0 = x - w//2, y - h//2
    bar = 8
    return (f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="white" {ST}/>\n'
            f'<line x1="{x0+bar}" y1="{y0}" x2="{x0+bar}" y2="{y0+h}" {ST}/>\n'
            f'<line x1="{x0+w-bar}" y1="{y0}" x2="{x0+w-bar}" y2="{y0+h}" {ST}/>\n'
            + txt(x, y, lines, fs=fs))

def decision(x, y, lines, w=310, h=56, fs=11):
    """Решение — ромб (ГОСТ 3.2.2.4)"""
    pts = f'{x},{y-h//2} {x+w//2},{y} {x},{y+h//2} {x-w//2},{y}'
    return (f'<polygon points="{pts}" fill="white" {ST}/>\n'
            + txt(x, y, lines, fs=fs)), w//2, h//2

def loop_beg(x, y, lines, w=340, h=34, fs=11):
    """Начало цикла — зубец снизу (ГОСТ 3.2.2.6)"""
    x0, y0 = x - w//2, y - h//2
    x1, y1 = x + w//2, y + h//2
    n  = 15
    pts = f'{x0},{y0} {x1},{y0} {x1},{y1} {x},{y1-n} {x0},{y1}'
    return (f'<polygon points="{pts}" fill="white" {ST}/>\n'
            + txt(x, y - n//3, lines, fs=fs)), w//2, h//2

def loop_end(x, y, lines, w=340, h=34, fs=11):
    """Конец цикла — зубец сверху (ГОСТ 3.2.2.6)"""
    x0, y0 = x - w//2, y - h//2
    x1, y1 = x + w//2, y + h//2
    n  = 15
    pts = f'{x0},{y0} {x},{y0+n} {x1},{y0} {x1},{y1} {x0},{y1}'
    return (f'<polygon points="{pts}" fill="white" {ST}/>\n'
            + txt(x, y + n//3, lines, fs=fs)), w//2, h//2

def connector_sym(x, y, label, r=18):
    """Соединитель — окружность (ГОСТ 3.4.1)"""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="white" {ST}/>\n'
            + txt(x, y, label, fs=13, bold=True)), r

# ─── Layout constants ────────────────────────────────────────────────────────

W   = 900          # canvas width
CX  = 440          # main vertical axis

LX1 = 58           # outermost left back-edge column
LX2 = 85           # middle left back-edge column
LX3 = 108          # innermost left back-edge column

RX1 = 730          # outer right bypass column (decision NO branches section 1)
RX2 = 755          # outer right bypass column (decision NO branches section 3)
RX3 = 720          # inner right bypass column

# ─── Y-coordinates (element centres) ────────────────────────────────────────

# Each row: name  → y
Y = {}

Y['start']    = 95
Y['adj_init'] = 155
Y['l1s']      = 218   # цикл 1 начало
Y['d_uneqv']  = 296   # u ≠ v ?
Y['adj_add']  = 374
Y['l1e']      = 435   # цикл 1 конец

Y['sort']     = 507   # предопред
Y['col_init'] = 572
Y['l2s']      = 636   # цикл 2 начало
Y['forbidden1']= 700
Y['col1']     = 760
Y['l3s']      = 823   # цикл 3 начало
Y['col_inc']  = 885
Y['l3e']      = 947   # цикл 3 конец
Y['col_set']  = 1007
Y['l2e']      = 1070  # цикл 2 конец
Y['conn_a1']  = 1135  # соединитель A (выход)

Y['conn_a2']  = 1210  # соединитель A (вход, продолжение)
Y['impr_t']   = 1270  # есть_улучшения = Истина
Y['l4s']      = 1335  # цикл 4 начало
Y['impr_f']   = 1395
Y['max_col']  = 1455
Y['l5s']      = 1518  # цикл 5 начало
Y['d_maxc']   = 1598  # colors[v]=max_color?
Y['forbid2']  = 1676
Y['d_exist']  = 1748  # ∃c < max_color : c ∉ forbidden?
Y['col_min']  = 1826
Y['l5e']      = 1896  # цикл 5 конец
Y['d_gone']   = 1972  # max_color ∉ colors?
Y['impr_t2']  = 2050  # есть_улучшения = Истина
Y['l4e']      = 2120  # цикл 4 конец

Y['sched_init']= 2200
Y['l6s']      = 2263  # цикл 6 начало
Y['sched_add'] = 2325
Y['l6e']      = 2388  # цикл 6 конец
Y['ncolors']  = 2448
Y['output']   = 2510
Y['end']      = 2570

H = Y['end'] + 60

# ─── Assemble SVG ────────────────────────────────────────────────────────────

buf = []

buf.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}">
<defs>
  <marker id="A" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
    <polygon points="0 0, 9 3.5, 0 7" fill="black"/>
  </marker>
</defs>
<rect width="{W}" height="{H}" fill="white"/>''')

# ── Title ──────────────────────────────────────────────────────────────────────
buf.append(txt(CX, 28, 'Алгоритм раскраски графа Welsh-Powell', fs=14, bold=True))
buf.append(txt(CX, 46, 'Вариант 4: Автоматическое составление расписания  |  ГОСТ 19.701-90', fs=10, fill='#555'))
buf.append(seg(40, 60, W-40, 60))

# ─────────────────── SECTION 1: Build adjacency graph ─────────────────────────
buf.append(lbl(40, 76, '1. Построение графа смежности', fs=9, italic=True, fill='#777'))

# НАЧАЛО
buf.append(terminal(CX, Y['start'], 'НАЧАЛО'))

buf.append(arr(CX, Y['start']+18, CX, Y['adj_init']-20))

# adj_init
buf.append(process(CX, Y['adj_init'], 'adj[v] = ∅   для всех v ∈ vertices', w=340, h=40))

buf.append(arr(CX, Y['adj_init']+20, CX, Y['l1s']-17))

# ЦИКЛ 1 начало
s, hw, hh = loop_beg(CX, Y['l1s'], 'ЦИКЛ:  для каждого ребра (u, v) ∈ edges', w=360, h=34)
buf.append(s)

buf.append(arr(CX, Y['l1s']+17, CX, Y['d_uneqv']-28))

# Решение u ≠ v?
s, dw, dh = decision(CX, Y['d_uneqv'], 'u ≠ v ?', w=200, h=56)
buf.append(s)
buf.append(lbl(CX+6,       Y['d_uneqv']+dh+4, 'ДА',  anchor='start', fs=10))
buf.append(lbl(CX+dw+6,    Y['d_uneqv']-6,    'НЕТ', anchor='start', fs=10))

# ДА: adj add
buf.append(arr(CX, Y['d_uneqv']+dh, CX, Y['adj_add']-24))
buf.append(process(CX, Y['adj_add'], ['adj[u].добавить(v)', 'adj[v].добавить(u)'], w=280, h=48))

buf.append(arr(CX, Y['adj_add']+24, CX, Y['l1e']-17))

# ЦИКЛ 1 конец
s, hw, hh = loop_end(CX, Y['l1e'], 'следующее ребро (u, v)', w=340, h=34)
buf.append(s)

# НЕТ branch: right bypass (u==v → skip to loop end)
buf.append(poly([
    (CX+100, Y['d_uneqv']),
    (RX1,    Y['d_uneqv']),
    (RX1,    Y['l1e']),
    (CX+170, Y['l1e']),
]))

# Loop 1 back-edge: loop_end left → LX1 → up → loop_beg left
buf.append(poly([
    (CX-170, Y['l1e']),
    (LX1,    Y['l1e']),
    (LX1,    Y['l1s']),
    (CX-180, Y['l1s']),
]))

# ──────────────── SECTION 2: Welsh-Powell greedy coloring ─────────────────────
buf.append(arr(CX, Y['l1e']+17, CX, Y['sort']-24))
buf.append(lbl(40, Y['sort']-34, '2. Жадная раскраска Welsh-Powell', fs=9, italic=True, fill='#777'))

# order = sort (предопред. процесс)
buf.append(predef(CX, Y['sort'],
           ['order = сортировка(vertices,',
            'ключ: (−степень(v), имя_v))'],
           w=360, h=48))

buf.append(arr(CX, Y['sort']+24, CX, Y['col_init']-20))

# colors = {}
buf.append(process(CX, Y['col_init'], 'colors = {}', w=240, h=40))

buf.append(arr(CX, Y['col_init']+20, CX, Y['l2s']-17))

# ЦИКЛ 2 начало
s, *_ = loop_beg(CX, Y['l2s'], 'ЦИКЛ:  для каждой вершины v ∈ order', w=360, h=34)
buf.append(s)

buf.append(arr(CX, Y['l2s']+17, CX, Y['forbidden1']-20))

# forbidden
buf.append(process(CX, Y['forbidden1'],
           'forbidden = { colors[u] | u ∈ adj[v], u уже покрашен }',
           w=380, h=40))

buf.append(arr(CX, Y['forbidden1']+20, CX, Y['col1']-20))

# color = 1
buf.append(process(CX, Y['col1'], 'color = 1', w=200, h=40))

buf.append(arr(CX, Y['col1']+20, CX, Y['l3s']-17))

# ЦИКЛ 3 начало (inner while loop)
s, *_ = loop_beg(CX, Y['l3s'], 'ЦИКЛ:  пока  color ∈ forbidden', w=340, h=34)
buf.append(s)

buf.append(arr(CX, Y['l3s']+17, CX, Y['col_inc']-20))

# color += 1
buf.append(process(CX, Y['col_inc'], 'color += 1', w=200, h=40))

buf.append(arr(CX, Y['col_inc']+20, CX, Y['l3e']-17))

# ЦИКЛ 3 конец
s, *_ = loop_end(CX, Y['l3e'], 'проверить color ∈ forbidden', w=330, h=34)
buf.append(s)

# Loop 3 back (inner): left side
buf.append(poly([
    (CX-165, Y['l3e']),
    (LX3,    Y['l3e']),
    (LX3,    Y['l3s']),
    (CX-170, Y['l3s']),
]))

buf.append(arr(CX, Y['l3e']+17, CX, Y['col_set']-20))

# colors[v] = color
buf.append(process(CX, Y['col_set'], 'colors[v] = color', w=270, h=40))

buf.append(arr(CX, Y['col_set']+20, CX, Y['l2e']-17))

# ЦИКЛ 2 конец (outer v loop)
s, *_ = loop_end(CX, Y['l2e'], 'следующая вершина v ∈ order', w=340, h=34)
buf.append(s)

# Loop 2 back: farther left
buf.append(poly([
    (CX-170, Y['l2e']),
    (LX1,    Y['l2e']),
    (LX1,    Y['l2s']),
    (CX-180, Y['l2s']),
]))

buf.append(arr(CX, Y['l2e']+17, CX, Y['conn_a1']-18))

# Соединитель A (выход из секции 1–2)
s, r = connector_sym(CX, Y['conn_a1'], 'A')
buf.append(s)

# ────────────────── SECTION 3: Optimization loop ─────────────────────────────
buf.append(lbl(40, Y['conn_a2']-30, '3. Локальная оптимизация (перекраска)', fs=9, italic=True, fill='#777'))

# Соединитель A (вход)
s, r = connector_sym(CX, Y['conn_a2'], 'A')
buf.append(s)

buf.append(arr(CX, Y['conn_a2']+18, CX, Y['impr_t']-20))

# есть_улучшения = Истина
buf.append(process(CX, Y['impr_t'], 'есть_улучшения = Истина', w=290, h=40))

buf.append(arr(CX, Y['impr_t']+20, CX, Y['l4s']-17))

# ЦИКЛ 4 начало (while улучшения)
s, *_ = loop_beg(CX, Y['l4s'], 'ЦИКЛ:  пока  есть_улучшения', w=340, h=34)
buf.append(s)

buf.append(arr(CX, Y['l4s']+17, CX, Y['impr_f']-20))

# есть_улучшения = Ложь
buf.append(process(CX, Y['impr_f'], 'есть_улучшения = Ложь', w=290, h=40))

buf.append(arr(CX, Y['impr_f']+20, CX, Y['max_col']-20))

# max_color
buf.append(process(CX, Y['max_col'], 'max_color = max( colors.values() )', w=330, h=40))

buf.append(arr(CX, Y['max_col']+20, CX, Y['l5s']-17))

# ЦИКЛ 5 начало (for v in vertices)
s, *_ = loop_beg(CX, Y['l5s'], 'ЦИКЛ:  для каждой вершины v ∈ vertices', w=370, h=34)
buf.append(s)

buf.append(arr(CX, Y['l5s']+17, CX, Y['d_maxc']-28))

# Решение colors[v] = max_color?
s, dw5, dh5 = decision(CX, Y['d_maxc'],
                       ['colors[v] = max_color ?'], w=300, h=56)
buf.append(s)
buf.append(lbl(CX+6,       Y['d_maxc']+dh5+4, 'ДА',  anchor='start', fs=10))
buf.append(lbl(CX+dw5+6,   Y['d_maxc']-6,    'НЕТ', anchor='start', fs=10))

# ДА ветка
buf.append(arr(CX, Y['d_maxc']+28, CX, Y['forbid2']-20))

# forbidden 2
buf.append(process(CX, Y['forbid2'],
           'forbidden = { colors[u] | u ∈ adj[v] }',
           w=360, h=40))

buf.append(arr(CX, Y['forbid2']+20, CX, Y['d_exist']-28))

# Решение ∃c < max_color, c ∉ forbidden?
s, dw6, dh6 = decision(CX, Y['d_exist'],
                       ['∃c : 1 ≤ c < max_color', 'и  c ∉ forbidden ?'],
                       w=310, h=64)
buf.append(s)
buf.append(lbl(CX+6,       Y['d_exist']+dh6+4, 'ДА',  anchor='start', fs=10))
buf.append(lbl(CX+dw6+6,   Y['d_exist']-6,    'НЕТ', anchor='start', fs=10))

# ДА: colors[v] = min c
buf.append(arr(CX, Y['d_exist']+32, CX, Y['col_min']-20))
buf.append(process(CX, Y['col_min'], 'colors[v] = наименьший такой c', w=300, h=40))

buf.append(arr(CX, Y['col_min']+20, CX, Y['l5e']-17))

# ЦИКЛ 5 конец
s, *_ = loop_end(CX, Y['l5e'], 'следующая вершина v ∈ vertices', w=360, h=34)
buf.append(s)

# НЕТ branch from d_maxc: bypass right to l5e
buf.append(poly([
    (CX+150, Y['d_maxc']),
    (RX2,    Y['d_maxc']),
    (RX2,    Y['l5e']),
    (CX+180, Y['l5e']),
]))

# НЕТ branch from d_exist: bypass right (shorter) to l5e
buf.append(poly([
    (CX+155, Y['d_exist']),
    (RX3,    Y['d_exist']),
    (RX3,    Y['l5e']),
    (CX+180, Y['l5e']),  # both NO paths merge at right side of l5e
]))

# Loop 5 back: left side
buf.append(poly([
    (CX-180, Y['l5e']),
    (LX2,    Y['l5e']),
    (LX2,    Y['l5s']),
    (CX-185, Y['l5s']),
]))

buf.append(arr(CX, Y['l5e']+17, CX, Y['d_gone']-28))

# Решение max_color ∉ colors.values() ?
s, dw7, dh7 = decision(CX, Y['d_gone'],
                       ['max_color ∉ colors.values() ?'], w=320, h=56)
buf.append(s)
buf.append(lbl(CX+6,       Y['d_gone']+dh7+4, 'ДА',  anchor='start', fs=10))
buf.append(lbl(CX+dw7+6,   Y['d_gone']-6,    'НЕТ', anchor='start', fs=10))

# ДА: есть_улучшения = Истина → l4e
buf.append(arr(CX, Y['d_gone']+28, CX, Y['impr_t2']-20))
buf.append(process(CX, Y['impr_t2'], 'есть_улучшения = Истина', w=290, h=40))
buf.append(arr(CX, Y['impr_t2']+20, CX, Y['l4e']-17))

# НЕТ branch from d_gone: right → down → l4e right
buf.append(poly([
    (CX+160, Y['d_gone']),
    (RX2,    Y['d_gone']),
    (RX2,    Y['l4e']),
    (CX+170, Y['l4e']),
]))

# ЦИКЛ 4 конец
s, *_ = loop_end(CX, Y['l4e'], 'проверить есть_улучшения', w=340, h=34)
buf.append(s)

# Loop 4 back: outermost left
buf.append(poly([
    (CX-170, Y['l4e']),
    (LX1,    Y['l4e']),
    (LX1,    Y['l4s']),
    (CX-170, Y['l4s']),
]))

# ─────────────────── SECTION 4: Build schedule ──────────────────────────────
buf.append(arr(CX, Y['l4e']+17, CX, Y['sched_init']-20))
buf.append(lbl(40, Y['sched_init']-30, '4. Построение расписания', fs=9, italic=True, fill='#777'))

# schedule = {}
buf.append(process(CX, Y['sched_init'], 'schedule = {}', w=240, h=40))

buf.append(arr(CX, Y['sched_init']+20, CX, Y['l6s']-17))

# ЦИКЛ 6 начало
s, *_ = loop_beg(CX, Y['l6s'], 'ЦИКЛ:  для каждой вершины v ∈ vertices', w=370, h=34)
buf.append(s)

buf.append(arr(CX, Y['l6s']+17, CX, Y['sched_add']-20))

# schedule add
buf.append(process(CX, Y['sched_add'],
           'schedule[ colors[v] ].добавить(v)',
           w=330, h=40))

buf.append(arr(CX, Y['sched_add']+20, CX, Y['l6e']-17))

# ЦИКЛ 6 конец
s, *_ = loop_end(CX, Y['l6e'], 'следующая вершина v', w=310, h=34)
buf.append(s)

# Loop 6 back
buf.append(poly([
    (CX-155, Y['l6e']),
    (LX3,    Y['l6e']),
    (LX3,    Y['l6s']),
    (CX-185, Y['l6s']),
]))

buf.append(arr(CX, Y['l6e']+17, CX, Y['ncolors']-20))

# num_colors
buf.append(process(CX, Y['ncolors'], 'num_colors = len( schedule )', w=290, h=40))

buf.append(arr(CX, Y['ncolors']+20, CX, Y['output']-20))

# Вывод
buf.append(process(CX, Y['output'],
           'Вернуть { num_colors, colors, schedule }',
           w=360, h=40))

buf.append(arr(CX, Y['output']+20, CX, Y['end']-18))

# КОНЕЦ
buf.append(terminal(CX, Y['end'], 'КОНЕЦ'))

buf.append('</svg>')

# ─── Write file ──────────────────────────────────────────────────────────────

out_path = os.path.join(
    os.path.dirname(__file__),
    'BottleWebProject_C326_TEAM_STEP',
    'static', 'content', 'coloring_flowchart.svg'
)
os.makedirs(os.path.dirname(out_path), exist_ok=True)

svg_text = '\n'.join(buf)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(svg_text)

print(f'SVG saved: {out_path}')
print(f'Canvas: {W} x {H} px')
