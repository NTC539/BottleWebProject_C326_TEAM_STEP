% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Мосты Тарьяна — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода (динамические строки)
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/bridges/practice">

<div class="theory-section">
    <h3>Шаг 1 — Города</h3>
    <span class="input-section-label">Добавьте города / узлы сети:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addNodeRow('nodes-container','Название города')">
        + Добавить город
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 — Дороги</h3>
    <span class="input-section-label">
        Добавьте дороги (неориентированные) с весом — длиной или временем:
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addEdgeRow('edges-container', false, true, false)">
        + Добавить дорогу
    </button>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Анализировать сеть</button>
</div>
</form>

<script>
$(function () {
    addNodeRow('nodes-container', 'Название города');
    addNodeRow('nodes-container', 'Название города');
    addNodeRow('nodes-container', 'Название города');
    addEdgeRow('edges-container', false, true, false);
    addEdgeRow('edges-container', false, true, false);
});
</script>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 2: Ошибка
     ═══════════════════════════════════════════════════════════ -->
% if defined('error') and error:
<div class="alert alert-danger" style="margin-top:16px">{{error}}</div>
% end

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 3: Результат (не трогать)
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
