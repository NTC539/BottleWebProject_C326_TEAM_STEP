% rebase('layout.tpl', title='Теория — Раскраска графа Welsh–Powell', year=year, active_page='coloring')
<!-- СЕКЦИЯ 1: Навигация -->
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px;">
    <h2 style="margin:0;border:none;padding:0;">Раскраска графа &mdash; Welsh&ndash;Powell</h2>
    <a href="/coloring/practice" class="btn btn-primary btn-lg">К практике &rarr;</a>
</div>
<!-- СЕКЦИЯ 2: Ошибка -->
% if defined('error') and error:
<div class="alert alert-danger">{{error}}</div>
% end
<!-- СЕКЦИЯ 3: Содержание -->
<div class="panel panel-primary">
    <div class="panel-heading"><h3 class="panel-title">Что такое раскраска графа?</h3></div>
    <div class="panel-body">
        <p>
            Раскраска графа G&nbsp;=&nbsp;(V,&nbsp;E) &mdash; отображение
            c:&nbsp;V&nbsp;&rarr;&nbsp;{1,&nbsp;2,&nbsp;&hellip;,&nbsp;k}
            такое, что для каждого ребра {u,&nbsp;v}&nbsp;&isin;&nbsp;E
            выполняется c(u)&nbsp;&ne;&nbsp;c(v). Смежные вершины получают разные цвета.
            Минимальное число цветов &chi;(G) называется <strong>хроматическим числом</strong>.
            Точное вычисление &chi;(G) &mdash; <strong>NP-полная</strong> задача.
        </p>
    </div>
</div>
<h4 style="color:#1a3a5c;">Хроматическое число: частные случаи</h4>
<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>Тип графа</th>
            <th>&chi;(G)</th>
            <th>Пример</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Пустой граф (нет рёбер)</td>
            <td>1</td>
            <td>Изолированные вершины</td>
        </tr>
        <tr>
            <td>Дерево / двудольный граф</td>
            <td>2</td>
            <td>Дорожная сеть без циклов</td>
        </tr>
        <tr>
            <td>Нечётный цикл</td>
            <td>3</td>
            <td>C<sub>5</sub> (пятиугольник)</td>
        </tr>
        <tr>
            <td>Полный граф K<sub>n</sub></td>
            <td>n</td>
            <td>K<sub>4</sub> &rarr; &chi;&nbsp;=&nbsp;4</td>
        </tr>
    </tbody>
</table>
<h4 style="color:#1a3a5c;">Алгоритм Welsh&ndash;Powell</h4>
<p>Жадная эвристика, хорошее приближение к &chi;(G) за <strong>O(V&sup2;&nbsp;+&nbsp;E)</strong>.</p>
<ol>
    <li style="margin-bottom:10px;">
        <strong>Сортировка по степени.</strong>
        Упорядочить все вершины по убыванию степени deg(v).
        При равной степени &mdash; в алфавитном порядке для детерминированности результата.
    </li>
    <li style="margin-bottom:10px;">
        <strong>Выбор первой неокрашенной вершины.</strong>
        Взять первую вершину из отсортированного списка, ещё не получившую цвет.
        Назначить ей наименьший свободный цвет c.
    </li>
    <li style="margin-bottom:10px;">
        <strong>Распространение цвета c.</strong>
        Просмотреть оставшиеся неокрашенные вершины в том же порядке.
        Если вершина <em>не конфликтует</em> ни с одной уже окрашенной в цвет c &mdash;
        назначить ей цвет c.
    </li>
    <li style="margin-bottom:10px;">
        <strong>Повтор.</strong>
        Увеличить номер цвета и вернуться к шагу&nbsp;2.
        Продолжать до тех пор, пока все вершины не получат цвет.
    </li>
</ol>
<h4 style="color:#1a3a5c;">Гарантии и оптимальность</h4>
<p>
    Welsh&ndash;Powell <strong>не гарантирует</strong> оптимальной раскраски &mdash;
    результат зависит от порядка вершин и структуры графа.
    Тем не менее алгоритм даёт результат, близкий к оптимальному,
    для большинства реальных задач и работает значительно быстрее методов полного перебора.
</p>
<div class="well text-center" style="font-size:16px;color:#1a3a5c;border-color:#2e86ab;">
    &chi;(G) &le; k(WP) &le; &Delta;(G) + 1
</div>
<p>
    где <strong>k(WP)</strong> &mdash; число цветов, использованных алгоритмом,
    а <strong>&Delta;(G)</strong> &mdash; максимальная степень вершины графа.
</p>
<h4 style="color:#1a3a5c;">Пример: граф из 6 вершин</h4>
<p>
    <strong>Вершины:</strong> A, B, C, D, E, F.<br>
    <strong>Рёбра:</strong> A&ndash;B, A&ndash;C, B&ndash;C, B&ndash;D,
    C&ndash;E, D&ndash;E, D&ndash;F, E&ndash;F.<br>
    <strong>Степени:</strong> B&nbsp;=&nbsp;3, C&nbsp;=&nbsp;3, D&nbsp;=&nbsp;3,
    E&nbsp;=&nbsp;3, A&nbsp;=&nbsp;2, F&nbsp;=&nbsp;2.<br>
    <strong>Порядок Welsh&ndash;Powell:</strong> B, C, D, E, A, F.
</p>
<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>Вершина</th>
            <th>Степень</th>
            <th>Назначенный цвет</th>
            <th>Причина</th>
        </tr>
    </thead>
    <tbody>
        <tr class="danger">
            <td>B</td><td>3</td>
            <td><span class="label label-danger">Смена&nbsp;1</span></td>
            <td>Первая вершина &mdash; цвет 1</td>
        </tr>
        <tr class="danger">
            <td>E</td><td>3</td>
            <td><span class="label label-danger">Смена&nbsp;1</span></td>
            <td>Нет ребра с B(1) &rarr; цвет 1</td>
        </tr>
        <tr class="success">
            <td>C</td><td>3</td>
            <td><span class="label label-success">Смена&nbsp;2</span></td>
            <td>Смежна с B(1) &rarr; новый цвет 2</td>
        </tr>
        <tr class="success">
            <td>D</td><td>3</td>
            <td><span class="label label-success">Смена&nbsp;2</span></td>
            <td>Смежна с B(1); нет ребра C&ndash;D &rarr; цвет 2</td>
        </tr>
        <tr class="info">
            <td>A</td><td>2</td>
            <td><span class="label label-info">Смена&nbsp;3</span></td>
            <td>Смежна с B(1) и C(2) &rarr; новый цвет 3</td>
        </tr>
        <tr class="info">
            <td>F</td><td>2</td>
            <td><span class="label label-info">Смена&nbsp;3</span></td>
            <td>Смежна с E(1) и D(2); нет ребра A&ndash;F &rarr; цвет 3</td>
        </tr>
    </tbody>
</table>
<p>
    Итоговая раскраска:
    <span class="label label-danger">B &mdash; Смена&nbsp;1</span>
    <span class="label label-danger">E &mdash; Смена&nbsp;1</span>
    <span class="label label-success">C &mdash; Смена&nbsp;2</span>
    <span class="label label-success">D &mdash; Смена&nbsp;2</span>
    <span class="label label-info">A &mdash; Смена&nbsp;3</span>
    <span class="label label-info">F &mdash; Смена&nbsp;3</span>
</p>
<div class="well text-center" style="font-size:3em;font-weight:bold;color:#1a3a5c;border-color:#2e86ab;">
    3
    <div style="font-size:0.35em;color:#2e86ab;font-weight:normal;">&chi;(G) = 3 цвета</div>
</div>
<h4 style="color:#1a3a5c;">Применение раскраски графов</h4>
<div class="row">
    <div class="col-sm-4">
        <p>
            <strong>Расписания экзаменов</strong><br>
            Распределение дисциплин по временным слотам без конфликтов:
            смежные вершины (конфликтующие дисциплины) &mdash; разные слоты.
        </p>
    </div>
</div>
