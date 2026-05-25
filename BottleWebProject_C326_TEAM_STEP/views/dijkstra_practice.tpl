% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Алгоритм Дейкстры — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода (динамические строки)
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/dijkstra/practice" id="form-dijkstra">
<input type="hidden" name="edge_count" id="edge-count" value="0">

<div class="theory-section">
    <h3>Шаг 1 — Узлы сети</h3>
    <span class="input-section-label">Добавьте маршрутизаторы / узлы:</span>
    <div id="nodes-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addNodeRow('nodes-container','Название узла (A, Router-1...)')">
        + Добавить узел
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 2 — Каналы связи</h3>
    <span class="input-section-label">
        Добавьте направленные каналы. Отметьте «недоступен» для временно
        отключённых каналов (вес = ∞):
    </span>
    <div id="edges-container"></div>
    <button type="button" class="btn btn-success btn-sm add-row-btn"
            onclick="addEdgeRow('edges-container', true, true, true)">
        + Добавить канал
    </button>
</div>

<div class="theory-section">
    <h3>Шаг 3 — Источник</h3>
    <span class="input-section-label">Выберите узел, от которого строить маршруты:</span>
    <select name="source" class="form-control node-select" style="max-width:250px"></select>
</div>

<div style="margin-top:16px">
    <button type="submit" class="btn btn-primary">Построить маршруты</button>
</div>
</form>

<script>
$(function () {
    // Добавить 3 узла и 2 канала по умолчанию
    addNodeRow('nodes-container', 'Название узла');
    addNodeRow('nodes-container', 'Название узла');
    addNodeRow('nodes-container', 'Название узла');
    addEdgeRow('edges-container', true, true, true);
    addEdgeRow('edges-container', true, true, true);

    // Перед отправкой: нумеруем checkbox-ы и фиксируем edge_count
    $('#form-dijkstra').on('submit', function () {
        var count = $('#edges-container .edge-row').length;
        $('#edge-count').val(count);
        $('#edges-container .edge-row').each(function (i) {
            $(this).find('input[type=checkbox]').attr('name', 'edge_inf_' + i);
        });
    });
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

% if result["skipped_edges"]:
<div class="alert alert-warning">
    <strong>Исключены недоступные каналы (∞):</strong>
    % for se_u, se_v, se_w in result["skipped_edges"]:
    {{se_u}}→{{se_v}}&nbsp;&nbsp;
    % end
</div>
% end

% if result["unreachable"]:
<div class="alert alert-danger">
    <strong>Недостижимые узлы:</strong> {{', '.join(result["unreachable"])}}
</div>
% end

<div class="theory-section">
    <h3>Таблица кратчайших маршрутов от узла {{source_val}}</h3>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>Узел назначения</th>
                <th>Задержка (мс)</th>
                <th>Маршрут</th>
            </tr>
        </thead>
        <tbody>
            % for v in result["distances"]:
            %   dist = result["distances"][v]
            %   path = result["paths"][v]
            %   if v == source_val:
            <tr class="active">
                <td><strong>{{v}}</strong> (источник)</td>
                <td>0</td>
                <td>{{v}}</td>
            </tr>
            %   elif dist == float('inf'):
            <tr class="danger">
                <td>{{v}}</td>
                <td>∞</td>
                <td>Недостижим</td>
            </tr>
            %   else:
            %     dist_display = int(dist) if dist == int(dist) else dist
            <tr>
                <td>{{v}}</td>
                <td>{{dist_display}}</td>
                <td>{{ ' → '.join(path) }}</td>
            </tr>
            %   end
            % end
        </tbody>
    </table>
</div>

% end
