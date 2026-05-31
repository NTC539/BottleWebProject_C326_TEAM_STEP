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
    <div class="editor-grid">
        <section class="theory-section editor-panel">
            <h2>Дисциплины</h2>
            <div class="data-table-wrap">
                <table class="table data-table">
                    <thead>
                        <tr>
                            <th style="width:48px">№</th>
                            <th>Дисциплина</th>
                            <th>Преподаватель</th>
                            <th style="width:44px"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td><input type="text" name="subject[]" class="form-control" value="Математика"></td>
                            <td><input type="text" name="teacher[]" class="form-control" value="Иванов"></td>
                            <td><button type="button" class="table-action" aria-label="Удалить дисциплину">×</button></td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td><input type="text" name="subject[]" class="form-control" value="Физика"></td>
                            <td><input type="text" name="teacher[]" class="form-control" value="Петров"></td>
                            <td><button type="button" class="table-action" aria-label="Удалить дисциплину">×</button></td>
                        </tr>
                        <tr>
                            <td>3</td>
                            <td><input type="text" name="subject[]" class="form-control" value="Информатика"></td>
                            <td><input type="text" name="teacher[]" class="form-control" value="Сидорова"></td>
                            <td><button type="button" class="table-action" aria-label="Удалить дисциплину">×</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="inline-add-row">
                <input type="text" class="form-control" placeholder="Новая дисциплина">
                <input type="text" class="form-control" placeholder="Преподаватель">
                <button type="button" class="btn btn-primary">Добавить</button>
            </div>
        </section>

        <section class="theory-section editor-panel">
            <h2>Конфликты</h2>
            <div class="conflict-builder">
                <select name="conflict_from" class="form-control">
                    <option>Математика</option>
                    <option>Физика</option>
                    <option>Информатика</option>
                </select>
                <span class="edge-arrow">—</span>
                <select name="conflict_to" class="form-control">
                    <option>Физика</option>
                    <option>Информатика</option>
                    <option>Математика</option>
                </select>
                <button type="button" class="btn btn-primary">Добавить</button>
            </div>
            <div class="conflict-list">
                <div class="conflict-item">
                    <span>Математика — Физика</span>
                    <button type="button" class="table-action" aria-label="Удалить конфликт">×</button>
                </div>
                <div class="conflict-item">
                    <span>Физика — Информатика</span>
                    <button type="button" class="table-action" aria-label="Удалить конфликт">×</button>
                </div>
                <div class="conflict-item">
                    <span>Математика — Информатика</span>
                    <button type="button" class="table-action" aria-label="Удалить конфликт">×</button>
                </div>
            </div>
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
