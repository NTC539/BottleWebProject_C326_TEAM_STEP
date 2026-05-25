% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Мосты Тарьяна — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода
     ═══════════════════════════════════════════════════════════ -->
<div class="theory-section">
    <h3>Ввод данных</h3>
    <form method="POST" action="/bridges/practice">

        <div class="form-group">
            <label for="vertices">Список городов (каждый на новой строке)</label>
            <textarea id="vertices" name="vertices" rows="5"
                      class="form-control"
                      placeholder="Москва&#10;Тула&#10;Орёл&#10;Курск&#10;Белгород">{{vertices_raw}}</textarea>
        </div>

        <div class="form-group">
            <label for="edges">Дороги (формат: ГОРОД_А - ГОРОД_Б : ВЕС, каждая на новой строке)</label>
            <textarea id="edges" name="edges" rows="6"
                      class="form-control"
                      placeholder="Москва - Тула : 170&#10;Тула - Орёл : 180&#10;Москва - Орёл : 380&#10;Орёл - Курск : 150&#10;Курск - Белгород : 130">{{edges_raw}}</textarea>
        </div>

        <button type="submit" class="btn btn-primary">Анализировать сеть</button>
    </form>
</div>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 2: Ошибка
     ═══════════════════════════════════════════════════════════ -->
% if defined('error') and error:
<div class="alert alert-danger">{{error}}</div>
% end

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 3: Результат
     ═══════════════════════════════════════════════════════════ -->
% if defined('result') and result is not None:

<div class="panel panel-info">
    <div class="panel-heading"><strong>Общая статистика</strong></div>
    <div class="panel-body">
        <p>Суммарная длина кратчайших путей (исходная сеть):
           <strong>{{result["total_path_sum"]}}</strong></p>
        <p>Найдено мостов: <strong>{{len(result["bridges"])}}</strong></p>
    </div>
</div>

% if result["bridges"]:
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
        % for item in result["bridge_impact"]:
        %   u, v, w = item["edge"]
        %   delta = item["delta"]
        %   delta_str = 'Сеть разрывается (∞)' if delta is None else '+{:.1f}'.format(delta)
        %   row_cls = 'danger' if delta is None else 'warning'
        <tr class="{{row_cls}}">
            <td>{{u}} — {{v}}</td>
            <td>{{w}}</td>
            <td>{{delta_str}}</td>
        </tr>
        % end
    </tbody>
</table>
<div class="alert alert-warning">
    <strong>Красные строки</strong> — удаление полностью разрывает сеть.
    <strong>Жёлтые</strong> — связность сохраняется, но пути удлиняются.
</div>
% else:
<div class="alert alert-success">
    Мостов не найдено. Сеть устойчива — удаление любой одной дороги не нарушит связность.
</div>
% end

<h4>Матрица кратчайших путей (исходная сеть)</h4>
<div class="table-responsive">
<table class="table table-bordered table-condensed">
    <thead>
        <tr>
            <th></th>
            % for col in result["all_pairs"]:
            <th>{{col}}</th>
            % end
        </tr>
    </thead>
    <tbody>
        % for row in result["all_pairs"]:
        <tr>
            <td><strong>{{row}}</strong></td>
            % for col in result["all_pairs"]:
            %   if row == col:
            <td>0</td>
            %   elif result["all_pairs"][row][col] == float('inf'):
            <td>∞</td>
            %   else:
            %     val = result["all_pairs"][row][col]
            %     cell = int(val) if val == int(val) else val
            <td>{{cell}}</td>
            %   end
            % end
        </tr>
        % end
    </tbody>
</table>
</div>

% end
