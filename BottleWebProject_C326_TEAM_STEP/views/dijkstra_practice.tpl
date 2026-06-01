% rebase('layout.tpl', title='Практика — Алгоритм Дейкстры (OSPF)', year=year, active_page='practice')

<link rel="stylesheet" href="/static/content/dijkstra.css">
<script type="text/javascript" src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>

<h2>Практическое задание</h2>
<p class="text-muted">Введите ориентированный взвешенный граф, выберите источник — получите кратчайшие пути по алгоритму Дейкстры с фильтрацией недоступных каналов (∞).</p>

<div class="row practice-container">
    <div class="col-md-5">
        <div class="input-panel">
            <form method="post" action="/dijkstra/practice" id="dijkstraForm">
                <div class="form-group mb-3">
                    <label for="edgesInput">Рёбра графа (from,to,weight)</label>
                    <textarea id="edgesInput" name="edges" rows="8" class="form-control" placeholder="A,B,4
A,C,2
C,B,1
B,D,5
C,D,8
D,E,2
A,E,inf">{{ edges or '' }}</textarea>
                    <small class="text-muted">inf — недоступный канал. Каждое ребро с новой строки.</small>
                </div>

                <div class="form-group mb-3">
                    <label for="sourceInput">Вершина-источник</label>
                    <input type="text" id="sourceInput" name="source" class="form-control" value="{{ source or 'A' }}" placeholder="например, A">
                </div>

                <div class="action-buttons">
                    <a href="/dijkstra/random" class="btn-secondary">🎲 Случайный граф</a>
                    <span class="btn btn-secondary file-upload-btn">
                        📂 Загрузить файл
                        <input type="file" name="file" accept=".txt,.csv" formaction="/dijkstra/upload" formmethod="post" onchange="this.form.submit()">
                    </span>
                    <button type="submit" class="btn-practice" style="background:#1a3a5c;">Рассчитать</button>
                </div>
            </form>
        </div>
    </div>

    <div class="col-md-7">
        <div class="graph-panel">
            <div id="graphContainer" class="graph-container"></div>
            <div class="graph-legend mt-2">
                <span class="legend-item"><span class="legend-color solid"></span> Доступный канал</span>
                <span class="legend-item"><span style="background:#e84855; width:16px; height:16px; display:inline-block; border-radius:50%;"></span> Вершина-источник</span>
                <span class="legend-item"><span style="background:#97c2e0; width:16px; height:16px; display:inline-block; border-radius:50%;"></span> Обычная вершина</span>
            </div>
        </div>
    </div>
</div>

% if errors:
<div class="error-block mt-3">
    <strong>Ошибки в данных:</strong>
    <ul class="mb-0 mt-2">
    % for err in errors:
        <li>{{ err }}</li>
    % end
    </ul>
</div>
% end

% if prepared_edges:
<div class="graph-preview mt-3">
    <h4>Введённый граф (после фильтрации недоступных каналов)</h4>
    <div class="table-responsive">
        <table class="table table-bordered table-striped">
            <thead>
                <tr><th>От</th><th>К</th><th>Вес</th><th>Статус</th></tr>
            </thead>
            <tbody>
            % for (frm, to, weight_display, status) in prepared_edges:
                <tr>
                    <td>{{ frm }}</td>
                    <td>{{ to }}</td>
                    <td>{{ weight_display }}</td>
                    <td>{{ !status }}</td>   
                </tr>
            % end
            </tbody>
        </table>
    </div>
</div>
% end

% if prepared_results:
<div class="theory-section results-panel">
    <h3>Результаты маршрутизации от источника <code>{{ source }}</code></h3>
    <div class="table-responsive">
        <table class="table table-bordered table-striped result-table">
            <thead>
                <tr><th>Узел назначения</th><th>Минимальная задержка</th><th>Маршрут</th></tr>
            </thead>
            <tbody>
            % for node, data in prepared_results.items():
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

<script>
function drawGraph(edgesText, sourceVertex) {
    const lines = edgesText.trim().split(/\r?\n/);
    const edges = [];
    const verticesSet = new Set();
    for (let line of lines) {
        line = line.trim();
        if (line === '') continue;
        const parts = line.split(',');
        if (parts.length < 3) continue;
        const from = parts[0].trim();
        const to = parts[1].trim();
        const weightStr = parts[2].trim().toLowerCase();
        if (weightStr === 'inf') continue;
        const weight = parseFloat(weightStr);
        if (isNaN(weight)) continue;
        edges.push({ from, to, weight });
        verticesSet.add(from);
        verticesSet.add(to);
    }
    
    const vertices = Array.from(verticesSet);
    const nodes = vertices.map(v => ({
        id: v,
        label: v,
        color: v === sourceVertex ? '#e84855' : '#97c2e0',
        font: { color: 'white', size: 16 },
        size: 28
    }));
    const visEdges = edges.map(e => ({
        from: e.from,
        to: e.to,
        label: e.weight.toString(),
        arrows: { to: { enabled: true, scaleFactor: 0.7 } },
        font: { align: 'middle', size: 12 },
        color: { color: '#2e86ab' }
    }));
    
    const container = document.getElementById('graphContainer');
    const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(visEdges) };
    const options = {
        physics: false,
        interaction: {
            dragNodes: true,
            dragView: true,
            zoomView: true,
            minZoom: 0.5,
            maxZoom: 2.0
        },
        edges: { smooth: { type: 'continuous', roundness: 0.2 } }
    };
    if (window.network) window.network.destroy();
    window.network = new vis.Network(container, data, options);
}

window.addEventListener('DOMContentLoaded', () => {
    const edgesText = document.getElementById('edgesInput').value;
    const source = document.getElementById('sourceInput').value.trim();
    drawGraph(edgesText, source);
});
document.getElementById('edgesInput').addEventListener('input', function() {
    const source = document.getElementById('sourceInput').value.trim();
    drawGraph(this.value, source);
});
document.getElementById('sourceInput').addEventListener('input', function() {
    const edgesText = document.getElementById('edgesInput').value;
    drawGraph(edgesText, this.value.trim());
});
</script>

<div class="btn-practice-wrap mt-4 text-center">
    <a href="/dijkstra" class="btn-secondary" style="background:#6c757d;">← Вернуться к теории</a>
</div>