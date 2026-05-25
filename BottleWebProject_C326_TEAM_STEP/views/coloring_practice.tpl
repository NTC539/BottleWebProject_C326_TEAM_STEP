% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Раскраска графа — Практика</h2>

<div class="theory-section">
    <h3>Ввод данных</h3>
    <form method="POST" action="/coloring/practice">
        <div class="form-group">
            <label for="vertices">Список дисциплин (каждая на новой строке)</label>
            <textarea id="vertices" name="vertices" rows="6" class="form-control"
                      placeholder="Математика&#10;Физика&#10;Информатика&#10;История&#10;Химия">{{vertices_raw}}</textarea>
        </div>
        <div class="form-group">
            <label for="edges">
                Конфликты — дисциплины, которые нельзя ставить в одну смену
                (формат: ДИСЦИПЛИНА_А - ДИСЦИПЛИНА_Б, каждый на новой строке)
            </label>
            <textarea id="edges" name="edges" rows="6" class="form-control"
                      placeholder="Математика - Физика&#10;Математика - Информатика&#10;Физика - Информатика&#10;Физика - История&#10;Информатика - Химия">{{edges_raw}}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">Составить расписание</button>
    </form>
</div>

% if error:
<div class="alert alert-danger">{{error}}</div>
% end

% if result:
<div class="theory-section">
    <h3>Результат</h3>

    <div class="panel panel-success">
        <div class="panel-heading"><strong>Итог</strong></div>
        <div class="panel-body">
            <p>Минимальное количество смен: <strong>{{result['num_colors']}}</strong></p>
        </div>
    </div>

    <h4>Расписание по сменам</h4>
    % for shift_num in sorted(result['schedule'].keys()):
    <div class="theory-section" style="border-left: 4px solid #2e86ab; padding: 12px 16px; margin-bottom: 12px">
        <h4 style="margin-top:0">Смена {{shift_num}}</h4>
        <p>{{ ', '.join(result['schedule'][shift_num]) }}</p>
    </div>
    % end

    <h4>Таблица назначений</h4>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>Дисциплина</th>
                <th>Смена</th>
            </tr>
        </thead>
        <tbody>
            % for discipline, shift in sorted(result['colors'].items(), key=lambda x: x[1]):
            <tr>
                <td>{{discipline}}</td>
                <td>Смена {{shift}}</td>
            </tr>
            % end
        </tbody>
    </table>
</div>
% end
