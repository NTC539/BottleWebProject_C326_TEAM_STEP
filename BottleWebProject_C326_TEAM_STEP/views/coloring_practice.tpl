% rebase('layout.tpl', title='Практика — Раскраска графа', year=year, active_page='coloring')

<section class="practice-hero">
    <span class="page-label">Страница практики</span>
    <h1>Форма ввода данных для раскраски графа</h1>
    <p>
        Укажите дисциплины, преподавателей и пары конфликтов. Эти данные используются
        для распределения дисциплин по сменам.
    </p>
    <div class="mode-switch">
        <span class="mode-current">Практика</span>
        <a href="/coloring" class="secondary">Вернуться к теории</a>
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
        <h2>Импорт и генерация данных</h2>
        <div class="form-grid">
            <div>
                <h3>Импорт из JSON</h3>
                <p class="input-section-label">Файл со списком дисциплин, преподавателей и конфликтов</p>
                <input type="file" name="json_file" class="form-control" accept=".json,application/json">
                <p class="text-muted">Файл должен содержать дисциплины и пары конфликтов.</p>
                <pre class="json-example"><code>{
  "subjects": [
    { "name": "Математика", "teacher": "Иванов" },
    { "name": "Физика", "teacher": "Петров" },
    { "name": "Информатика", "teacher": "Сидорова" }
  ],
  "conflicts": [
    ["Математика", "Физика"],
    ["Физика", "Информатика"]
  ]
}</code></pre>
            </div>

            <div>
                <h3>Случайная генерация</h3>
                <div class="form-row-grid">
                    <div class="form-group">
                        <label for="subjectCount">Количество дисциплин</label>
                        <input id="subjectCount" type="number" class="form-control" value="12" min="1" max="50">
                    </div>
                    <div class="form-group">
                        <label for="density">Плотность графа</label>
                        <input id="density" type="number" class="form-control" value="0.35" min="0" max="1" step="0.05">
                    </div>
                </div>
                <button type="button" class="btn btn-primary">Сгенерировать данные</button>
            </div>
        </div>
    </section>

    <section class="theory-section">
        <h2>Граф конфликтов</h2>
        <p class="text-muted">
            Здесь будет отображаться граф после импорта JSON или генерации случайных данных.
        </p>
        <div id="graph-canvas" class="graph-container future-graph-area"></div>
    </section>
</form>
