% rebase('layout.tpl', title=title, year=year, active_page=active_page)

<h2>Алгоритм Дейкстры — Практика</h2>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода
     ═══════════════════════════════════════════════════════════ -->
<div class="theory-section">
    <h3>Ввод данных</h3>
    <form method="POST" action="/dijkstra/practice">

        <div class="form-group">
            <label for="vertices">Список узлов / маршрутизаторов (каждый на новой строке)</label>
            <textarea id="vertices" name="vertices" rows="5"
                      class="form-control"
                      placeholder="A&#10;B&#10;C&#10;D&#10;E">{{vertices_raw}}</textarea>
        </div>

        <div class="form-group">
            <label for="edges">Каналы (формат: УЗЕЛ_А -&gt; УЗЕЛ_Б : ЗАДЕРЖКА,
                задержка = число или inf если канал недоступен)</label>
            <textarea id="edges" name="edges" rows="7"
                      class="form-control"
                      placeholder="A -> B : 4&#10;A -> C : 2&#10;C -> B : 1&#10;B -> D : 5&#10;C -> D : 8&#10;D -> E : 2&#10;A -> E : inf">{{edges_raw}}</textarea>
        </div>

        <div class="form-group">
            <label for="source">Узел-источник (от которого строить маршруты)</label>
            <input id="source" type="text" name="source"
                   class="form-control" style="max-width:200px"
                   placeholder="A"
                   value="{{source_raw}}" />
        </div>

        <button type="submit" class="btn btn-primary">Построить маршруты</button>
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
    <h3>Таблица кратчайших маршрутов от узла {{source_raw}}</h3>
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
            %   if v == source_raw:
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
