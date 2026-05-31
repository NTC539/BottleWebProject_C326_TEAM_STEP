% rebase('layout.tpl', title='Алгоритм Дейкстры — OSPF маршрутизация', year=year, active_page='dijkstra')

<link rel="stylesheet" href="/static/content/dijkstra.css">
<style>
    .theory-section,
    .graph-metrics,
    .step-content,
    .context-note {
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }

    .theory-section:hover {
        box-shadow: none !important;
    }
</style>

<section class="theory-hero">
    <span class="page-label">Страница теории</span>
    <h1>Алгоритм Дейкстры</h1>
    <p>Коротко о поиске кратчайших путей во взвешенном графе.</p>
    <div class="mode-switch">
        <a href="/dijkstra" class="secondary">Теория</a>
        <a href="/dijkstra/practice">Перейти к практике</a>
    </div>
</section>

<!-- Блок 1 — Условие задачи (расширен) -->
<div class="theory-section">
    <h3>Условие задачи</h3>
    <p>
        Компьютерная сеть задана взвешенным ориентированным графом,
        где вершины — сетевые узлы (маршрутизаторы), дуги — каналы связи,
        вес дуги — задержка передачи данных (в миллисекундах).
        Некоторые каналы могут быть временно недоступны (вес = ∞).
        Требуется для заданного узла-источника найти маршрут с минимальной
        суммарной задержкой до каждого узла назначения сети.
    </p>
    <p>
        Алгоритм: Дейкстра с модификацией для учёта метрики OSPF
        (недоступные каналы игнорируются).
    </p>
    <div class="context-note">
        <strong>Контекст OSPF:</strong> Протокол OSPF (Open Shortest Path First)
        использует алгоритм Дейкстры как основу для вычисления таблиц маршрутизации.
        Каждый маршрутизатор строит полную карту сети (LSDB) и независимо
        вычисляет кратчайшие пути к каждой подсети.
    </div>
</div>

<!-- Блок 2 — Ориентированный взвешенный граф (расширен) -->
<div class="theory-section">
    <h3>Ориентированный взвешенный граф</h3>
    <p>
        Ориентированным графом называют пару G = (V, E), где E — множество
        упорядоченных пар (дуг). Дуга (u, v) означает: из узла u в узел v
        есть односторонний канал. В отличие от неориентированного графа,
        наличие дуги (u, v) не подразумевает наличие дуги (v, u).
    </p>
    <p>В сетевой модели OSPF (Open Shortest Path First):</p>
    <ul>
        <li>Каждый маршрутизатор знает топологию всей сети.</li>
        <li>Вес дуги — метрика: задержка, пропускная способность или стоимость.</li>
        <li>Дуга с весом ∞ означает временно недоступный канал (авария, перегрузка), такая дуга исключается из расчёта.</li>
        <li>Цель — найти путь с минимальной суммой весов от источника до каждого узла назначения.</li>
    </ul>
    <div class="graph-metrics">
        <h4>Способы задания метрик в OSPF</h4>
        <ul>
            <li><strong>Пропускная способность:</strong> cost = 10<sup>8</sup> / bandwidth (бит/с).</li>
            <li><strong>Задержка:</strong> суммарное время прохождения пакета (мс).</li>
            <li><strong>Надёжность:</strong> основанная на статистике ошибок.</li>
            <li><strong>Административная стоимость:</strong> вручную назначается администратором.</li>
        </ul>
    </div>
</div>

<!-- Блок 3 — Алгоритм Дейкстры (расширен) -->
<div class="theory-section">
    <h3>Алгоритм Дейкстры</h3>
    <p>
        Алгоритм Дейкстры находит кратчайшие пути от одной вершины-источника
        до всех остальных в графе с <strong>неотрицательными</strong> весами рёбер
        за время <code>O((V + E) log V)</code> с использованием приоритетной очереди.
    </p>
    <div class="algorithm-steps">
        <div class="step"><span class="step-number">1</span><div class="step-content"><strong>Инициализация:</strong> <code>dist[s] = 0</code> для источника s, <code>dist[v] = ∞</code> для всех остальных вершин v. Добавить все вершины в очередь с приоритетом по dist.</div></div>
        <div class="step"><span class="step-number">2</span><div class="step-content"><strong>Выбор текущей вершины:</strong> Извлечь из очереди вершину u с минимальным <code>dist[u]</code>.</div></div>
        <div class="step"><span class="step-number">3</span><div class="step-content"><strong>Релаксация дуг:</strong> Для каждой дуги (u, v) с весом w: <ul><li>если w = ∞ — пропустить (канал недоступен, модификация OSPF);</li><li>если <code>dist[u] + w &lt; dist[v]</code>: обновить <code>dist[v] = dist[u] + w</code>, запомнить <code>prev[v] = u</code> (для восстановления пути).</li></ul></div></div>
        <div class="step"><span class="step-number">4</span><div class="step-content"><strong>Повторение:</strong> Повторять шаги 2–3 до опустошения очереди.</div></div>
        <div class="step"><span class="step-number">5</span><div class="step-content"><strong>Восстановление пути:</strong> Для любой вершины v следовать по <code>prev[]</code> от v к s в обратном порядке.</div></div>
    </div>
</div>

<!-- Блок 4 — Модификация для OSPF (расширен) -->
<div class="theory-section">
    <h3>Модификация для метрики OSPF</h3>
    <p>В протоколе OSPF маршрутизатор автоматически исключает недоступные каналы из расчёта маршрутов. Модификация алгоритма:</p>
    <ul>
        <li>Перед запуском: отфильтровать все дуги с весом = ∞.</li>
        <li>Если после фильтрации путь до узла назначения не существует — узел считается недостижимым, маршрут не строится.</li>
        <li>В отчёте отображать список недостижимых узлов и список отфильтрованных (недоступных) каналов отдельно.</li>
    </ul>
    <div class="ospf-note"><strong>Почему это важно в OSPF:</strong><br>В динамических сетях каналы могут периодически отключаться. Исключение недоступных рёбер позволяет избежать использования "сломанных" маршрутов и ускоряет сходимость после изменений топологии.</div>
</div>

<!-- Блок 5 — Пример маршрутизации (расширен) -->
<div class="theory-section">
    <h3>Пример маршрутизации</h3>
    <p>Сеть из 5 узлов: <strong>A</strong> (источник), B, C, D, E.<br>Каналы: A→B:4, A→C:2, C→B:1, B→D:5, C→D:8, D→E:2, A→E:∞ (недоступен).</p>
    <h4>Шаг 1: Фильтрация недоступных каналов</h4>
    <p>Дуга A→E имеет вес ∞ — исключается из графа перед запуском алгоритма.</p>
    <h4>Шаг 2: Работа алгоритма Дейкстры (упрощённая таблица расстояний)</h4>
    <div class="example-table-wrapper"><table class="table table-bordered table-striped"><thead><tr><th>Итерация</th><th>Текущая вершина</th><th>Расстояния (A,B,C,D,E)</th><th>Предшественники</th></tr></thead><tbody>
    <tr><td>0</td><td>A</td><td>[0, ∞, ∞, ∞, ∞]</td><td>[-1,-1,-1,-1,-1]</td></tr>
    <tr><td>1</td><td>A</td><td>[0, 4, 2, ∞, ∞]</td><td>[-1, A, A, -1, -1]</td></tr>
    <tr><td>2</td><td>C</td><td>[0, 3, 2, 10, ∞]</td><td>[-1, C, A, C, -1]</td></tr>
    <tr><td>3</td><td>B</td><td>[0, 3, 2, 8, ∞]</td><td>[-1, C, A, B, -1]</td></tr>
    <tr><td>4</td><td>D</td><td>[0, 3, 2, 8, 10]</td><td>[-1, C, A, B, D]</td></tr>
    </tbody></table></div>
    <h4>Финальные кратчайшие маршруты</h4>
    <table class="table table-bordered table-striped"><thead><tr><th>Узел назначения</th><th>Минимальная задержка</th><th>Маршрут</th></tr></thead><tbody>
    <tr><td>B</td><td>3</td><td>A → C → B</td></tr>
    <tr><td>C</td><td>2</td><td>A → C</td></tr>
    <tr><td>D</td><td>8</td><td>A → C → B → D</td></tr>
    <tr><td>E</td><td>10</td><td>A → C → B → D → E</td></tr>
    </tbody></table>
</div>

<!-- Блок 6 — Переход к практике -->
<div class="btn-practice-wrap">
    <a href="/dijkstra/practice" class="btn-practice">Перейти к практике →</a>
</div>
