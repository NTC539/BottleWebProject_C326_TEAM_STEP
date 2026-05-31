% rebase('layout.tpl', title='Главная', year=year, active_page='home')

<section class="home-hero">
    <div>
        <span class="page-label">Главная страница</span>
        <h1>Задачи на графах</h1>
        <p>
            Четыре алгоритма для работы с графами: маршруты, устойчивость сети,
            критический путь и раскраска расписания.
        </p>
    </div>
    <a class="hero-link" href="/graph_theory">Общая теория</a>
</section>

<section class="task-grid">
    <article class="task-card task-card-blue">
        <span class="task-owner">Садеков</span>
        <h2>Алгоритм Дейкстры</h2>
        <p>Кратчайшие пути во взвешенном графе с недоступными каналами.</p>
        <div class="task-actions">
            <a href="/dijkstra">Теория</a>
            <a href="/dijkstra/practice">Форма ввода</a>
        </div>
    </article>

    <article class="task-card task-card-green">
        <span class="task-owner">Тигранян</span>
        <h2>Мосты Тарьяна</h2>
        <p>Поиск слабых мест сети и оценка изменения маршрутов.</p>
        <div class="task-actions">
            <a href="/bridges">Теория</a>
            <a href="/bridges/practice">Форма ввода</a>
        </div>
    </article>

    <article class="task-card task-card-yellow">
        <span class="task-owner">Езерский</span>
        <h2>Критический путь</h2>
        <p>План задач, зависимости и минимальная длительность проекта.</p>
        <div class="task-actions">
            <a href="/cpm">Теория</a>
            <a href="/cpm/practice">Форма ввода</a>
        </div>
    </article>

    <article class="task-card task-card-red">
        <span class="task-owner">Петренко</span>
        <h2>Раскраска графа</h2>
        <p>Распределение дисциплин по сменам без конфликтов.</p>
        <div class="task-actions">
            <a href="/coloring">Теория</a>
            <a href="/coloring/practice">Форма ввода</a>
        </div>
    </article>
</section>
