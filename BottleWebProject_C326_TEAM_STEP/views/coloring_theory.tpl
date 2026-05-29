% rebase('layout.tpl', title='Теория — Раскраска графа Welsh–Powell', year=year, active_page='coloring')
<link rel="stylesheet" type="text/css" href="/static/content/coloring_theory.css" />

<!-- СЕКЦИЯ 1: Навигация -->
<div class="ct-header">
    <h2>Раскраска графа &mdash; Welsh&ndash;Powell</h2>
    <a href="/coloring/practice" class="btn btn-primary btn-lg">К практике &rarr;</a>
</div>

<!-- СЕКЦИЯ 2: Ошибка -->
% if defined('error') and error:
<div class="alert alert-danger">{{error}}</div>
% end

<!-- СЕКЦИЯ 3: Содержание -->
<div class="row">

    <div class="col-md-6">
        <div class="theory-card">
            <div class="card-header">
                <span class="card-icon">&#127912;</span>
                <h4>Задача раскраски графа</h4>
            </div>
            <div class="card-body">
                <p>
                    <strong>Раскраска графа</strong> G&nbsp;=&nbsp;(V,&nbsp;E) &mdash;
                    отображение c:&nbsp;V&nbsp;&rarr;&nbsp;{1,&nbsp;2,&nbsp;&hellip;,&nbsp;k}
                    такое, что для каждого ребра {u,&nbsp;v}&nbsp;&isin;&nbsp;E
                    выполняется c(u)&nbsp;&ne;&nbsp;c(v).
                    Смежные вершины получают разные цвета.
                </p>
                <p>
                    Минимальное число цветов k называется
                    <strong>хроматическим числом</strong> &chi;(G).
                </p>
                <ul>
                    <li>Пустой граф (нет рёбер): &chi;&nbsp;=&nbsp;1</li>
                    <li>Дерево / двудольный граф: &chi;&nbsp;=&nbsp;2</li>
                    <li>Нечётный цикл: &chi;&nbsp;=&nbsp;3</li>
                    <li>Полный граф K<sub>n</sub>: &chi;&nbsp;=&nbsp;n</li>
                </ul>
                <p>Нахождение точного &chi;(G) &mdash; <strong>NP-полная</strong> задача.</p>
            </div>
        </div>
    </div>

    <div class="col-md-6">
        <div class="theory-card">
            <div class="card-header">
                <span class="card-icon">&#128203;</span>
                <h4>Алгоритм Welsh&ndash;Powell</h4>
            </div>
            <div class="card-body">
                <p>Жадная эвристика, хорошее приближение к &chi;(G) за
                <strong>O(V&sup2;&nbsp;+&nbsp;E)</strong>.</p>
                <ol>
                    <li>Упорядочить вершины по <em>убыванию степени</em>.</li>
                    <li>Взять первую неокрашенную вершину, назначить ей наименьший незанятый цвет.</li>
                    <li>
                        Пройти по остальным неокрашенным вершинам в том же порядке:
                        если вершина не конфликтует ни с одной уже окрашенной в текущий цвет &mdash;
                        назначить ей этот цвет.
                    </li>
                    <li>Увеличить номер цвета. Повторять шаги 2&ndash;3 до полной раскраски.</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="col-md-6">
        <div class="theory-card">
            <div class="card-header">
                <span class="card-icon">&#9878;&#65039;</span>
                <h4>Гарантии алгоритма vs оптимальность</h4>
            </div>
            <div class="card-body">
                <p>
                    Welsh&ndash;Powell <strong>не гарантирует</strong> оптимальной раскраски.
                    Результат зависит от порядка вершин и структуры графа.
                </p>
                <p>Гарантированная оценка числа используемых цветов k(WP):</p>
                <p style="text-align:center;font-size:16px;margin:12px 0;">
                    <code>&chi;(G) &le; k(WP) &le; &Delta;(G) + 1</code>
                </p>
                <p>где &Delta;(G) &mdash; максимальная степень вершины графа.</p>
                <p>
                    На практике алгоритм даёт близкий к оптимальному результат
                    для большинства реальных графов и работает значительно быстрее
                    точных методов полного перебора.
                </p>
            </div>
        </div>
    </div>

    <div class="col-md-6">
        <div class="theory-card">
            <div class="card-header">
                <span class="card-icon">&#128269;</span>
                <h4>Пример: граф из 6 вершин</h4>
            </div>
            <div class="card-body">
                <p>
                    Вершины: A, B, C, D, E, F.<br>
                    Рёбра: A&ndash;B, A&ndash;C, B&ndash;C, B&ndash;D,
                    C&ndash;E, D&ndash;E, D&ndash;F, E&ndash;F.
                </p>
                <p>
                    Степени: B=3, C=3, D=3, E=3, A=2, F=2.<br>
                    Порядок Welsh&ndash;Powell: <strong>B, C, D, E, A, F</strong>.
                </p>
                <p>Раскраска по шагам:</p>
                <p>
                    <span class="color-badge cb-red">B &mdash; Цвет&nbsp;1</span>
                    <span class="color-badge cb-red">E &mdash; Цвет&nbsp;1</span>
                </p>
                <p>
                    <span class="color-badge cb-green">C &mdash; Цвет&nbsp;2</span>
                    <span class="color-badge cb-green">D &mdash; Цвет&nbsp;2</span>
                    <span class="color-badge cb-green">F &mdash; Цвет&nbsp;2</span>
                </p>
                <p>
                    <span class="color-badge cb-blue">A &mdash; Цвет&nbsp;3</span>
                </p>
                <div class="chi-display">
                    3
                    <span class="chi-label">&chi;(G) = 3 цвета</span>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-12">
        <div class="theory-card">
            <div class="card-header">
                <span class="card-icon">&#128640;</span>
                <h4>Применение раскраски графов</h4>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-sm-4">
                        <p>
                            <strong>Расписания экзаменов</strong><br>
                            Распределение дисциплин по временным слотам без конфликтов:
                            смежные вершины (конфликтующие курсы) &mdash; разные слоты.
                        </p>
                    </div>
                    <div class="col-sm-4">
                        <p>
                            <strong>Распределение регистров</strong><br>
                            В компиляторах: назначение физических регистров процессора
                            переменным программы (конфликт = одновременное использование).
                        </p>
                    </div>
                    <div class="col-sm-4">
                        <p>
                            <strong>Телекоммуникации</strong><br>
                            Назначение частот в сотовой сети: соседние базовые станции
                            должны работать на разных частотах.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>
