% rebase('layout.tpl', title='Практика — Раскраска графа', year=year, active_page='coloring')
<link rel="stylesheet" type="text/css" href="/static/content/coloring_theory.css?v=11" />

<section class="practice-hero">
    <span class="page-label">Раскраска графа - практика</span>
    <h1>Расчёт расписания методом раскраски графа</h1>
    <p>
        Дисциплины являются вершинами графа, пары конфликтов - рёбрами. Алгоритм распределяет
        дисциплины по сменам так, чтобы связанные вершины не оказались в одной смене.
    </p>
    <div class="mode-switch">
        <span class="mode-current">Практика</span>
        <a href="/coloring" class="secondary">Вернуться к теории</a>
    </div>
</section>

% if errors:
<div class="alert alert-danger coloring-alert">
    <strong>Проверьте входные данные</strong>
    <ul>
    % for error in errors:
        <li>{{ error }}</li>
    % end
    </ul>
</div>
% end

<form method="POST" action="/coloring/practice" enctype="multipart/form-data" id="coloringForm">
    <input type="hidden" name="form_action" id="formAction" value="calculate">
    <div class="editor-grid">
        <section class="theory-section editor-panel">
            <h2>Дисциплины</h2>
            <div class="data-table-wrap">
                <table class="table data-table" id="subjectsTable">
                    <thead>
                        <tr>
                            <th style="width:48px">№</th>
                            <th>Дисциплина</th>
                            <th>Преподаватель</th>
                            <th style="width:44px"></th>
                        </tr>
                    </thead>
                    <tbody data-subject-body>
                    % for index, subject in enumerate(subjects, start=1):
                        % subject_color = result['colors'].get(subject.get('name', ''), '') if result else ''
                        <tr data-color="{{ subject_color }}">
                            <td data-row-number>{{ index }}</td>
                            <td><input type="text" name="subject[]" class="form-control subject-name" value="{{ subject.get('name', '') }}"></td>
                            <td><input type="text" name="teacher[]" class="form-control" value="{{ subject.get('teacher', '') }}"></td>
                            <td><button type="button" class="table-action" data-remove-subject aria-label="Удалить дисциплину">×</button></td>
                        </tr>
                    % end
                    </tbody>
                </table>
            </div>
            <div class="inline-add-row">
                <input type="text" id="newSubjectName" class="form-control" placeholder="Новая дисциплина">
                <input type="text" id="newSubjectTeacher" class="form-control" placeholder="Преподаватель">
                <button type="button" class="btn btn-primary" id="addSubjectBtn">Добавить</button>
            </div>
        </section>

        <section class="theory-section editor-panel">
            <h2>Конфликты</h2>
            <div class="conflict-builder">
                <select id="conflictFrom" class="form-control"></select>
                <span class="edge-arrow">-</span>
                <select id="conflictTo" class="form-control"></select>
                <button type="button" class="btn btn-primary" id="addConflictBtn">Добавить</button>
            </div>
            <div class="conflict-list" data-conflict-list>
            % for left, right in conflicts:
                <div class="conflict-item" data-conflict-from="{{ left }}" data-conflict-to="{{ right }}">
                    <span>{{ left }} - {{ right }}</span>
                    <input type="hidden" name="conflict_from[]" value="{{ left }}">
                    <input type="hidden" name="conflict_to[]" value="{{ right }}">
                    <button type="button" class="table-action" data-remove-conflict aria-label="Удалить конфликт">×</button>
                </div>
            % end
            </div>
        </section>
    </div>

    <section class="theory-section">
        <h2>Импорт и генерация данных</h2>
        <div class="form-grid">
            <div>
                <h3>Импорт из JSON</h3>
                <label class="input-section-label" for="jsonFile">JSON-файл</label>
                <div class="json-load-row">
                    <input id="jsonFile" type="file" name="json_file" class="form-control" accept=".json,application/json">
                    <button type="button" data-submit-action="load_json" class="btn btn-primary">Загрузить JSON</button>
                </div>
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
                        <input id="subjectCount" name="subject_count" type="number" class="form-control" value="{{ subject_count }}" min="1" max="20">
                    </div>
                    <div class="form-group">
                        <label for="density">Плотность графа</label>
                        <input id="density" name="density" type="number" class="form-control" value="{{ density }}" min="0" max="1" step="0.05">
                    </div>
                </div>
                <button type="button" data-submit-action="generate" class="btn btn-primary">Сгенерировать данные</button>
            </div>
        </div>
    </section>

    <div class="coloring-actions">
        <button type="submit" class="btn btn-primary btn-lg">Рассчитать расписание</button>
    </div>

    <section class="theory-section graph-section-wide">
        <h2>Граф конфликтов</h2>
        <div class="graph-toolbar">
            <button type="button" class="btn btn-default btn-sm" id="fitGraphBtn">Уместить</button>
            <button type="button" class="btn btn-default btn-sm" id="stabilizeGraphBtn">Расположить</button>
        </div>
        <div id="graph-canvas" class="graph-container future-graph-area interactive-graph"></div>
        <div class="graph-legend">
            <span><i class="legend-node neutral"></i>Дисциплина</span>
            <span><i class="legend-node colored"></i>Смена после расчёта</span>
            <span><i class="legend-line"></i>Конфликт</span>
        </div>
    </section>
</form>

% if result:
<section class="theory-section result-section">
    <h2>Результат</h2>
    <div class="result-summary">
        <div>
            <span class="result-number">{{ result['num_colors'] }}</span>
            <span>смен</span>
        </div>
        <div>
            <span class="result-number">{{ result['teacher_cost'] }}</span>
            <span>штраф по сменам преподавателей</span>
        </div>
        <div>
            <span class="result-number">{{ len(result['conflicts']) }}</span>
            <span>конфликтов в графе</span>
        </div>
    </div>

    <div class="result-layout">
        <div>
            <h3>Расписание по сменам</h3>
            <table class="table table-striped result-table">
                <thead>
                    <tr>
                        <th>Смена</th>
                        <th>Дисциплины</th>
                    </tr>
                </thead>
                <tbody>
                % for row in result['schedule']:
                    <tr>
                        <td><span class="shift-badge">Смена {{ row['shift'] }}</span></td>
                        <td>
                        % for subject in row['subjects']:
                            <span class="subject-chip">{{ subject['name'] }} <small>{{ subject['teacher'] }}</small></span>
                        % end
                        </td>
                    </tr>
                % end
                </tbody>
            </table>
        </div>

        <div>
            <h3>Смены преподавателей</h3>
            <table class="table table-striped result-table">
                <thead>
                    <tr>
                        <th>Преподаватель</th>
                        <th>Смены</th>
                    </tr>
                </thead>
                <tbody>
                % for row in result['teacher_shifts']:
                    <tr>
                        <td>{{ row['teacher'] }}</td>
                        <td>{{ ', '.join([str(shift) for shift in row['shifts']]) }}</td>
                    </tr>
                % end
                </tbody>
            </table>
        </div>
    </div>

    <h3>Порядок обработки Welsh-Powell</h3>
    <table class="table table-striped result-table">
        <thead>
            <tr>
                <th>Дисциплина</th>
                <th>Степень</th>
                <th>Итоговая смена</th>
            </tr>
        </thead>
        <tbody>
        % for subject_name in result['order']:
            <tr>
                <td>{{ subject_name }}</td>
                <td>{{ result['degrees'][subject_name] }}</td>
                <td>{{ result['colors'][subject_name] }}</td>
            </tr>
        % end
        </tbody>
    </table>
</section>
% end

<script src="/static/scripts/coloring_practice.js?v=20"></script>
