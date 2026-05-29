% rebase('layout.tpl', title='Практика — Мосты Тарьяна', year=year, active_page='bridges')

<h2>Мосты Тарьяна &mdash; Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/bridges/practice">

<div class="theory-section">
    <h3>Шаг 1 &mdash; Города</h3>
    <span class="input-section-label">Добавьте города / узлы сети:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn">
        + Добавить город
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 &mdash; Дороги</h3>
    <span class="input-section-label">
        Добавьте дороги (неориентированные) с весом &mdash; длиной или временем:
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn">
        + Добавить дорогу
    </button>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Анализировать сеть</button>
</div>
</form>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 2: Ошибка
     ═══════════════════════════════════════════════════════════ -->
% if defined('error') and error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 3: Результат
     ═══════════════════════════════════════════════════════════ -->

<div style="margin-bottom:12px; margin-top:20px">
    <button type="button" class="btn btn-default btn-sm">
        💾 Скачать результат (JSON)
    </button>
    <button type="button" class="btn btn-default btn-sm">
        📄 Скачать результат (TXT)
    </button>
</div>

<div class="panel panel-info">
    <div class="panel-heading"><strong>Общая статистика</strong></div>
    <div class="panel-body">
        <p>Суммарная длина кратчайших путей (исходная сеть):
           <strong>60</strong></p>
        <p>Найдено мостов: <strong>2</strong></p>
    </div>
</div>

<h4>Критические дороги (мосты)</h4>
<table class="table table-bordered table-striped table-hover">
    <thead>
        <tr>
            <th>Дорога</th>
            <th>Вес</th>
            <th>Прирост суммарных путей при удалении</th>
        </tr>
    </thead>
    <tbody>
        <tr class="danger">
            <td>C &mdash; D</td>
            <td>5</td>
            <td>Сеть разрывается (&infin;)</td>
        </tr>
        <tr class="danger">
            <td>D &mdash; E</td>
            <td>4</td>
            <td>Сеть разрывается (&infin;)</td>
        </tr>
    </tbody>
</table>
<div class="alert alert-warning">
    <strong>Красные строки</strong> &mdash; удаление полностью разрывает сеть.
    <strong>Жёлтые</strong> &mdash; связность сохраняется, но пути удлиняются.
</div>

<h4>Матрица кратчайших путей (исходная сеть)</h4>
<div class="table-responsive">
<table class="table table-bordered table-condensed">
    <thead>
        <tr>
            <th></th>
            <th>A</th><th>B</th><th>C</th><th>D</th><th>E</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>A</strong></td>
            <td>0</td><td>2</td><td>1</td><td>6</td><td>10</td>
        </tr>
        <tr>
            <td><strong>B</strong></td>
            <td>2</td><td>0</td><td>3</td><td>8</td><td>12</td>
        </tr>
        <tr>
            <td><strong>C</strong></td>
            <td>1</td><td>3</td><td>0</td><td>5</td><td>9</td>
        </tr>
        <tr>
            <td><strong>D</strong></td>
            <td>6</td><td>8</td><td>5</td><td>0</td><td>4</td>
        </tr>
        <tr>
            <td><strong>E</strong></td>
            <td>10</td><td>12</td><td>9</td><td>4</td><td>0</td>
        </tr>
    </tbody>
</table>
</div>

<div class="theory-section">
    <h4>Граф транспортной сети</h4>
    <p class="text-muted" style="font-size:13px">
        Красные жирные рёбра &mdash; мосты (критические дороги).
        Серые &mdash; обычные дороги.
    </p>
    <div id="graph-canvas" style="height:450px;border:1px solid #ddd;
         border-radius:4px;background:#fafafa;margin-top:8px"></div>
</div>
