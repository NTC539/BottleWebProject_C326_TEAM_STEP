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
            <label class="input-section-label" for="subjectsText">Список дисциплин</label>
            <textarea id="subjectsText" name="subjects_text" class="form-control bulk-input" rows="9" spellcheck="false"
                      placeholder="Математика; Иванов
Физика; Петров
Информатика; Сидорова"></textarea>
        </section>

        <section class="theory-section">
            <h2>Конфликты</h2>
            <label class="input-section-label" for="conflictsText">Пары конфликтов</label>
            <textarea id="conflictsText" name="conflicts_text" class="form-control bulk-input" rows="9" spellcheck="false"
                      placeholder="Математика; Физика
Физика; Информатика
Математика; Информатика"></textarea>
        </section>
    </div>

    <section class="theory-section">
        <h2>Импорт и генерация данных</h2>
        <div class="form-grid">
            <div>
                <h3>Импорт из JSON</h3>
                <label class="input-section-label" for="jsonFile">JSON-файл</label>
                <input id="jsonFile" type="file" name="json_file" class="form-control" accept=".json,application/json">
                <h4 class="json-example-title">Пример структуры</h4>
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
        <div id="graph-canvas" class="graph-container future-graph-area"></div>
    </section>
</form>
