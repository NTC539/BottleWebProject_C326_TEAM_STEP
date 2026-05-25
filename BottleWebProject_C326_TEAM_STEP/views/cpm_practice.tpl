% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Критический путь — Практика</h2>

<div class="theory-section">
    <h3>Ввод данных</h3>
    <form method="POST" action="/cpm/practice">
        <div class="form-group">
            <label for="tasks">Список задач (ИМЯ:ДЛИТЕЛЬНОСТЬ, каждая на новой строке)</label>
            <textarea id="tasks" name="tasks" rows="6" class="form-control"
                      placeholder="A:3&#10;B:2&#10;C:4&#10;D:1&#10;E:2">{{tasks_raw}}</textarea>
        </div>
        <div class="form-group">
            <label for="deps">Зависимости (ПРЕДШЕСТВЕННИК->ПОСЛЕДОВАТЕЛЬ, каждая на новой строке)</label>
            <textarea id="deps" name="deps" rows="6" class="form-control"
                      placeholder="A->C&#10;A->D&#10;B->D&#10;C->E&#10;D->E">{{deps_raw}}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">Рассчитать</button>
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
            <p>Общая длительность проекта: <strong>{{result['duration']}}</strong></p>
            <p>Критический путь: <strong>{{ ' → '.join(result['critical_path']) }}</strong></p>
        </div>
    </div>

    <h4>Таблица ранних сроков</h4>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>Задача</th>
                <th>Длительность</th>
                <th>Ранний старт (ES)</th>
                <th>Раннее окончание (EF)</th>
                <th>На крит. пути</th>
            </tr>
        </thead>
        <tbody>
            % for task_name, duration in result['tasks'].items():
            %   on_cp = 'Да' if task_name in result['critical_path'] else 'Нет'
            %   row_class = 'success' if task_name in result['critical_path'] else ''
            <tr class="{{row_class}}">
                <td>{{task_name}}</td>
                <td>{{duration}}</td>
                <td>{{result['es'][task_name]}}</td>
                <td>{{result['ef'][task_name]}}</td>
                <td>{{on_cp}}</td>
            </tr>
            % end
        </tbody>
    </table>
</div>
% end
