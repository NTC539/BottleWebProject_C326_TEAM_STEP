% rebase('layout.tpl', title='Практика — Раскраска графа', year=year, active_page='coloring')

<section class="practice-hero">
    <span class="page-label">Страница практики</span>
    <h1>Форма ввода данных для раскраски графа</h1>
    <p>
        Здесь можно подготовить данные для алгоритма: дисциплины, преподавателей и пары конфликтов.
        Логика расчёта не подключена, форма нужна как интерфейсный макет.
    </p>
    <div class="mode-switch">
        <a href="/coloring" class="secondary">Вернуться к теории</a>
        <a href="/coloring/practice">Практика</a>
    </div>
</section>

<form method="POST" action="/coloring/practice">
    <div class="form-grid">
        <section class="theory-section">
            <h2>Дисциплины</h2>
            <p class="input-section-label">Название дисциплины и преподаватель</p>
            <div class="input-row">
                <input type="text" name="subject[]" class="form-control" placeholder="Математика">
                <input type="text" name="teacher[]" class="form-control" placeholder="Иванов">
            </div>
            <div class="input-row">
                <input type="text" name="subject[]" class="form-control" placeholder="Физика">
                <input type="text" name="teacher[]" class="form-control" placeholder="Петров">
            </div>
            <div class="input-row">
                <input type="text" name="subject[]" class="form-control" placeholder="Информатика">
                <input type="text" name="teacher[]" class="form-control" placeholder="Сидорова">
            </div>
            <button type="button" class="btn btn-default btn-sm">Добавить дисциплину</button>
        </section>

        <section class="theory-section">
            <h2>Конфликты</h2>
            <p class="input-section-label">Пары дисциплин, которые нельзя ставить вместе</p>
            <div class="input-row">
                <input type="text" name="conflict_a[]" class="form-control" placeholder="Математика">
                <span class="edge-arrow">—</span>
                <input type="text" name="conflict_b[]" class="form-control" placeholder="Физика">
            </div>
            <div class="input-row">
                <input type="text" name="conflict_a[]" class="form-control" placeholder="Физика">
                <span class="edge-arrow">—</span>
                <input type="text" name="conflict_b[]" class="form-control" placeholder="Информатика">
            </div>
            <div class="input-row">
                <input type="text" name="conflict_a[]" class="form-control" placeholder="Математика">
                <span class="edge-arrow">—</span>
                <input type="text" name="conflict_b[]" class="form-control" placeholder="Информатика">
            </div>
            <button type="button" class="btn btn-default btn-sm">Добавить конфликт</button>
        </section>
    </div>

    <section class="theory-section">
        <h2>Дополнительные параметры</h2>
        <div class="form-row-grid">
            <div class="form-group">
                <label for="maxSubjects">Максимум дисциплин</label>
                <input id="maxSubjects" type="number" class="form-control" value="20" min="1" max="50">
            </div>
            <div class="form-group">
                <label for="density">Плотность случайного графа</label>
                <input id="density" type="number" class="form-control" value="0.35" min="0" max="1" step="0.05">
            </div>
            <div class="form-group">
                <label for="format">Формат загрузки</label>
                <select id="format" class="form-control">
                    <option>JSON</option>
                    <option>CSV</option>
                </select>
            </div>
        </div>
        <div class="mode-switch">
            <button type="button" class="btn btn-default">Сгенерировать пример</button>
            <button type="button" class="btn btn-default">Загрузить файл</button>
            <button type="submit" class="btn btn-primary">Рассчитать</button>
        </div>
    </section>
</form>
