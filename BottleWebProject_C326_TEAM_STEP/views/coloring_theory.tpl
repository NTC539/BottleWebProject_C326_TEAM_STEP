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
