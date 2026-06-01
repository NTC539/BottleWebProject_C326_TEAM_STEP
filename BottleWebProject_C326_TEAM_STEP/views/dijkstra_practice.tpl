% rebase('layout.tpl', title='Практика — Алгоритм Дейкстры (OSPF)', year=year, active_page='practice')

<link rel="stylesheet" href="/static/content/dijkstra.css">
<script type="text/javascript" src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>

<h2>Практическое задание</h2>
<p class="text-muted">
  Введите количество рёбер → заполните таблицу и укажите источник → получите кратчайшие пути.
  <br>Вес можно указать как число (>0) или <code>inf</code> (недоступный канал).
</p>

<div class="row practice-container">
  <div class="col-md-5">
    <div class="input-panel">
      % if stage == 'input_count':
        <!-- ШАГ 1: только количество рёбер -->
        <form method="post" action="/dijkstra/practice">
          <input type="hidden" name="action" value="generate_count">
          <div class="form-group mb-3">
            <label for="edge_count">Количество рёбер</label>
            <input type="number" id="edge_count" name="edge_count" class="form-control" min="1" value="{{ edge_count if edge_count else 5 }}" required>
          </div>
          <!-- Скрытые поля для восстановления рёбер и источника, если были -->
          % for i, (from_val, to_val, weight_val) in enumerate(edges):
            <input type="hidden" name="from_{{ i }}" value="{{ from_val }}">
            <input type="hidden" name="to_{{ i }}" value="{{ to_val }}">
            <input type="hidden" name="weight_{{ i }}" value="{{ weight_val }}">
          % end
          <input type="hidden" name="source" value="{{ source }}">
          <button type="submit" class="btn-practice">Далее →</button>
        </form>

      % elif stage == 'input_edges':
        <!-- ШАГ 2: таблица рёбер + поле источника -->
        <form method="post" action="/dijkstra/practice">
          <input type="hidden" name="action" value="calculate">
          <input type="hidden" name="edge_count" value="{{ edge_count }}">
          
          <div class="form-group mb-3">
            <label for="source">Вершина-источник</label>
            <input type="text" id="source" name="source" class="form-control" value="{{ source }}" required>
          </div>

          <div class="form-group mb-3">
            <label>Таблица рёбер (от → до, вес)</label>
            <div class="table-responsive">
              <table class="table table-bordered table-sm">
                <thead>
                  <tr><th>#</th><th>От</th><th>До</th><th>Вес</th></tr>
                </thead>
                <tbody>
                  % for i in range(edge_count):
                    <%
                        from_val = edges[i][0] if i < len(edges) else ''
                        to_val = edges[i][1] if i < len(edges) else ''
                        weight_val = edges[i][2] if i < len(edges) else ''
                    %>
                    <tr>
                      <td>{{ i+1 }}</td>
                      <td><input type="text" name="from_{{ i }}" class="form-control" value="{{ from_val }}" ></td>
                      <td><input type="text" name="to_{{ i }}" class="form-control" value="{{ to_val }}" ></td>
                      <td><input type="text" name="weight_{{ i }}" class="form-control" value="{{ weight_val }}" placeholder="число или inf" ></td>
                    </tr>
                  % end
                </tbody>
              </table>
            </div>
          </div>
          
          <div class="action-buttons">
            <button type="submit" class="btn-practice">Рассчитать</button>
            <button type="submit" name="action" value="back_to_count" class="btn-secondary">← Назад</button>
            <button type="submit" name="action" value="random" class="btn-secondary">🎲 Случайный граф</button>
            <button type="submit" name="action" value="reset" class="btn-secondary">⟳ Сброс</button>
            <label for="fileUpload" class="btn btn-secondary" style="cursor:pointer;">📂 Загрузить файл</label>
            <input type="file" name="file" id="fileUpload" accept=".txt,.csv" style="display:none" onchange="this.form.action.value='upload'; this.form.submit();">
          </div>
          <small class="text-muted d-block mt-2">Файл: каждая строка "from,to,weight" (разделители запятая или пробел)</small>
        </form>
        <script>
          document.getElementById('fileUpload')?.addEventListener('change', function() {
            this.form.action.value = 'upload';
            this.form.submit();
          });
        </script>

      % elif stage == 'results':
        <!-- ШАГ 3: результаты (сообщение + таблица маршрутов слева) -->
        <div class="alert alert-success">
          <strong>✅ Маршруты построены</strong> – граф показан справа.
        </div>
        <form method="post" action="/dijkstra/practice" class="mb-3">
          <input type="hidden" name="action" value="back_to_edges">
          <input type="hidden" name="edge_count" value="{{ edge_count }}">
          <input type="hidden" name="source" value="{{ source }}">
          % for i, (from_val, to_val, weight_val) in enumerate(edges):
            <input type="hidden" name="from_{{ i }}" value="{{ from_val }}">
            <input type="hidden" name="to_{{ i }}" value="{{ to_val }}">
            <input type="hidden" name="weight_{{ i }}" value="{{ weight_val }}">
          % end
          <div class="action-buttons">
            <button type="submit" class="btn-secondary">← Назад к таблице</button>
            <button type="submit" name="action" value="reset" class="btn-secondary">⟳ Новый расчёт</button>
          </div>
        </form>

        % if results:
        <div class="results-panel">
          <h4>Результаты маршрутизации</h4>
          <div class="table-responsive">
            <table class="table table-bordered table-striped result-table">
              <thead>
                <tr><th>Узел</th><th>Задержка</th><th>Маршрут</th></tr>
              </thead>
              <tbody>
                % for node, data in results.items():
                <tr>
                  <td><strong>{{ node }}</strong></td>
                  <td>{{ data['dist_display'] }}</td>
                  <td>{{ data['path_display'] }}</td>
                </tr>
                % end
              </tbody>
            </table>
          </div>
        </div>
        % end
      % end

      % if errors:
      <div class="error-block mt-3">
        <strong>Ошибки:</strong>
        <ul class="mb-0 mt-2">
          % for err in errors:
            <li>{{ err }}</li>
          % end
        </ul>
      </div>
      % end
    </div>
  </div>

  <div class="col-md-7">
    <div class="graph-panel">
      % if stage == 'results':
        <!-- На этапе результатов показываем граф со всеми рёбрами -->
        <div id="graphContainer" class="graph-container"></div>
        <div class="graph-legend mt-2">
          <span class="legend-item"><span class="legend-color solid"></span> Доступный канал</span>
          <span class="legend-item"><span class="legend-color dashed"></span> Недоступный канал (∞)</span>
          <span class="legend-item"><span style="background:#e84855; width:16px; height:16px; display:inline-block; border-radius:50%;"></span> Источник</span>
          <span class="legend-item"><span style="background:#97c2e0; width:16px; height:16px; display:inline-block; border-radius:50%;"></span> Обычная вершина</span>
        </div>
      % else:
        <!-- На первых двух этапах показываем информационную заглушку -->
        <div class="graph-placeholder text-center p-5 bg-light rounded">
          <i class="fas fa-project-diagram fa-3x text-muted mb-3"></i>
          <h5 class="text-muted">Граф будет построен после расчёта</h5>
          <p class="small text-muted">Заполните данные слева и нажмите «Рассчитать»</p>
        </div>
      % end
    </div>
  </div>
</div>

<script>
function drawGraphFromEdges(edgesList, sourceVertex) {
    if (!edgesList || edgesList.length === 0) return;
    const verticesSet = new Set();
    const regularEdges = [];
    const infEdges = [];
    for (let e of edgesList) {
        const from = e[0];
        const to = e[1];
        let weight = e[2];
        verticesSet.add(from);
        verticesSet.add(to);
        if (weight === 'inf' || weight === Infinity) {
            infEdges.push({ from, to, label: '∞' });
        } else {
            const weightNum = parseFloat(weight);
            if (isNaN(weightNum)) continue;
            regularEdges.push({ from, to, weight: weightNum });
        }
    }
    const vertices = Array.from(verticesSet);
    const nodes = vertices.map(v => ({
        id: v,
        label: v,
        color: v === sourceVertex ? '#e84855' : '#97c2e0',
        font: { color: 'white', size: 16 },
        size: 28
    }));
    
    // Обычные рёбра (доступные)
    const visEdges = regularEdges.map(e => ({
        from: e.from,
        to: e.to,
        label: e.weight.toString(),
        arrows: { to: { enabled: true, scaleFactor: 0.7 } },
        font: { align: 'middle', size: 12 },
        color: { color: '#2e86ab' }
    }));
    
    // Рёбра с inf (недоступные) – пунктирные, серые
    const infVisEdges = infEdges.map(e => ({
        from: e.from,
        to: e.to,
        label: 'inf',
        arrows: { to: { enabled: true, scaleFactor: 0.7 } },
        font: { align: 'middle', size: 12, color: '#888' },
        color: { color: '#aaaaaa' },
        dashes: true,
        width: 1.5
    }));
    
    const allEdges = visEdges.concat(infVisEdges);
    const container = document.getElementById('graphContainer');
    if (!container) return;
    const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(allEdges) };
    const options = {
        physics: false,
        interaction: { dragNodes: true, dragView: true, zoomView: true },
        edges: { smooth: { type: 'continuous', roundness: 0.2 } }
    };
    if (window.network) window.network.destroy();
    window.network = new vis.Network(container, data, options);
}

window.addEventListener('DOMContentLoaded', function() {
    var graphEdges = {{ !json.dumps(graph_edges_json) if graph_edges_json else 'null' }};
    var sourceVertex = "{{ source }}";
    if (graphEdges && document.getElementById('graphContainer')) {
        drawGraphFromEdges(graphEdges, sourceVertex);
    }
});
</script>

<div class="btn-practice-wrap mt-4 text-center">
  <a href="/dijkstra" class="btn-secondary" style="background:#6c757d;">← Вернуться к теории</a>
</div>