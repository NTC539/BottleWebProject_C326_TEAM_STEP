% rebase('layout.tpl', title='Теория — Раскраска графа', year=year, active_page='coloring')
<link rel="stylesheet" type="text/css" href="/static/content/coloring_theory.css" />

<section class="theory-hero">
    <span class="page-label">Страница теории</span>
    <h1>Раскраска графа для расписания</h1>
    <p>
        Идея простая: дисциплины считаем вершинами, конфликты между ними — рёбрами.
        Дисциплины, соединённые ребром, нельзя поставить в одну смену.
    </p>
    <div class="mode-switch">
        <a href="/coloring" class="secondary">Теория</a>
        <a href="/coloring/practice">Перейти к практике</a>
    </div>
</section>

<section class="theory-layout">
    <div>
        <h2>Как это работает</h2>
        <div class="simple-steps">
            <div class="ct-step">
                <span class="ct-step-num">1</span>
                <p><strong>Собираем граф.</strong> Вершины — дисциплины, рёбра — пары, которые конфликтуют.</p>
            </div>
            <div class="ct-step">
                <span class="ct-step-num">2</span>
                <p><strong>Сортируем вершины.</strong> Сначала берём дисциплины с большим числом конфликтов.</p>
            </div>
            <div class="ct-step">
                <span class="ct-step-num">3</span>
                <p><strong>Назначаем смену.</strong> Выбираем первый свободный номер смены, где нет соседей-конфликтов.</p>
            </div>
            <div class="ct-step">
                <span class="ct-step-num">4</span>
                <p><strong>Улучшаем результат.</strong> Пробуем перенести дисциплины так, чтобы преподавателям было удобнее.</p>
            </div>
        </div>
    </div>

    <aside class="theory-note">
        <h3>Главное правило</h3>
        <p>
            Если две дисциплины соединены ребром, они всегда должны быть в разных сменах.
            Всё остальное — попытка сделать расписание компактнее.
        </p>
    </aside>
</section>

<section>
    <h2>Разобранный пример</h2>
    <p>
        Возьмём шесть дисциплин: A, B, C, D, E, F.
        Конфликты: A-B, A-C, B-C, B-D, C-E, D-E, D-F, E-F.
    </p>

    <div class="example-grid">
        <div class="example-graph" role="img" aria-label="Граф примера раскраски">
            <svg viewBox="0 0 420 260" class="graph-svg">
                <line x1="92" y1="58" x2="210" y2="44" />
                <line x1="92" y1="58" x2="160" y2="140" />
                <line x1="210" y1="44" x2="160" y2="140" />
                <line x1="210" y1="44" x2="278" y2="142" />
                <line x1="160" y1="140" x2="302" y2="214" />
                <line x1="278" y1="142" x2="302" y2="214" />
                <line x1="278" y1="142" x2="374" y2="90" />
                <line x1="302" y1="214" x2="374" y2="90" />

                <circle class="node-blue" cx="92" cy="58" r="24" />
                <circle class="node-red" cx="210" cy="44" r="24" />
                <circle class="node-green" cx="160" cy="140" r="24" />
                <circle class="node-green" cx="278" cy="142" r="24" />
                <circle class="node-red" cx="302" cy="214" r="24" />
                <circle class="node-blue" cx="374" cy="90" r="24" />

                <text x="92" y="64">A</text>
                <text x="210" y="50">B</text>
                <text x="160" y="146">C</text>
                <text x="278" y="148">D</text>
                <text x="302" y="220">E</text>
                <text x="374" y="96">F</text>
            </svg>
        </div>

        <div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Смена</th>
                        <th>Дисциплины</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="color-badge cb-red">1</span></td>
                        <td>B, E</td>
                    </tr>
                    <tr>
                        <td><span class="color-badge cb-green">2</span></td>
                        <td>C, D</td>
                    </tr>
                    <tr>
                        <td><span class="color-badge cb-blue">3</span></td>
                        <td>A, F</td>
                    </tr>
                </tbody>
            </table>
            <p>
                Получилось три смены. Внутри каждой смены нет дисциплин, которые соединены ребром.
            </p>
        </div>
    </div>
</section>

<section>
    <h2>Что делает оптимизация</h2>
    <div class="compact-points">
        <p><strong>Уменьшает число смен,</strong> если дисциплину можно безопасно перенести раньше.</p>
        <p><strong>Смотрит на преподавателей,</strong> чтобы один преподаватель не был разбросан по лишним сменам.</p>
        <p><strong>Не ломает расписание:</strong> конфликтующие дисциплины всё равно остаются в разных сменах.</p>
    </div>
</section>
