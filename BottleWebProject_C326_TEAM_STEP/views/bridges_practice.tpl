% rebase('layout.tpl', title='Практика — Мосты Тарьяна', year=year, active_page='bridges')
<link rel="stylesheet" type="text/css" href="/static/content/bridges_practice.css?v=5" />

<section class="practice-hero">
    <span class="page-label">Мосты Тарьяна — практика</span>
    <h1>Анализ устойчивости транспортной сети</h1>
    <p>
        Задайте города и дороги с весами. Будут найдены мосты (рёбра, разрывающие
        сеть), а для исходной сети и для каждого графа без моста выведены матрицы
        весов, смежности и кратчайших путей и сам граф.
    </p>
    <div class="mode-switch">
        <span class="mode-current">Практика</span>
        <a href="/bridges" class="secondary">Вернуться к теории</a>
    </div>
</section>

<!-- ═══════════════════════════════════════════════════════════
     СЕКЦИЯ 1: Форма ввода
     ═══════════════════════════════════════════════════════════ -->
<form method="POST" action="/bridges/practice">
    <div class="editor-grid">

        <section class="editor-panel">
            <h3>Города</h3>
            <p class="hint">Узлы транспортной сети.</p>
            <div class="input-table-wrap">
                <table class="table input-table">
                    <thead>
                        <tr>
                            <th>Город</th>
                            <th class="row-action"></th>
                        </tr>
                    </thead>
                    <tbody id="bridge-nodes-body"></tbody>
                </table>
            </div>
            <div class="row-actions-bar">
                <button type="button" class="btn btn-success btn-sm add-row-btn"
                        onclick="addBridgeNodeRow()">+ Добавить город</button>
                <button type="button" class="btn btn-default btn-sm"
                        onclick="clearBridgeNodes()">Очистить поля</button>
            </div>
        </section>

        <section class="editor-panel">
            <h3>Дороги</h3>
            <p class="hint">Неориентированные рёбра с весом (длиной / временем).</p>
            <div class="input-table-wrap">
                <table class="table input-table">
                    <thead>
                        <tr>
                            <th>Откуда</th>
                            <th class="edge-arrow-cell"></th>
                            <th>Куда</th>
                            <th class="col-weight">Вес</th>
                            <th class="row-action"></th>
                        </tr>
                    </thead>
                    <tbody id="bridge-edges-body"></tbody>
                </table>
            </div>
            <div class="row-actions-bar">
                <button type="button" class="btn btn-success btn-sm add-row-btn"
                        onclick="addBridgeEdgeRow()">+ Добавить дорогу</button>
                <button type="button" class="btn btn-default btn-sm"
                        onclick="clearBridgeEdges()">Очистить поля</button>
            </div>
        </section>
    </div>

    <div class="submit-bar">
        <button type="submit" class="btn btn-primary btn-lg">Анализировать сеть</button>
        <div class="gen-controls">
            <button type="button" id="bridge-generate-btn" class="btn btn-default">
                🎲 Сгенерировать случайные данные
            </button>
            <label for="bridge-gen-count" class="gen-count-label">
                Городов:
                <input type="number" id="bridge-gen-count" class="form-control gen-count-input"
                       min="2" max="15" value="6"
                       title="Сколько городов сгенерировать (2–15)">
            </label>
        </div>
    </div>
</form>

<script>
// Восстановление ввода формы (после отправки поля не очищаются)
var BR_NODES_INPUT = {{!nodes_input}};
var BR_EDGES_INPUT = {{!edges_input}};

$(function () {
    if (BR_NODES_INPUT && BR_NODES_INPUT.length) {
        BR_NODES_INPUT.forEach(function (n) { addBridgeNodeRow(n); });
    } else {
        addBridgeNodeRow();
        addBridgeNodeRow();
    }
    updateBridgeSelects();

    if (BR_EDGES_INPUT && BR_EDGES_INPUT.length) {
        BR_EDGES_INPUT.forEach(function (e) { addBridgeEdgeRow(e[0], e[1], e[2]); });
    }
    updateBridgeSelects();

    // Генерация случайных данных (граф приходит с сервера, Python)
    $('#bridge-generate-btn').on('click', function () {
        var cnt = parseInt($('#bridge-gen-count').val(), 10);
        var url = '/bridges/generate';
        if (!isNaN(cnt)) { url += '?cities=' + cnt; }   // сколько городов сгенерировать
        $.getJSON(url, function (data) {
            $('#bridge-nodes-body').empty();
            $('#bridge-edges-body').empty();
            data.nodes.forEach(function (n) { addBridgeNodeRow(n); });
            updateBridgeSelects();
            data.edges.forEach(function (e) { addBridgeEdgeRow(e[0], e[1], e[2]); });
            updateBridgeSelects();
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
     СЕКЦИЯ 3: Результат
     ═══════════════════════════════════════════════════════════ -->
% if defined('result') and result:
<h3 style="margin-top:24px">Результат анализа</h3>

<div class="result-summary">
    <div class="summary-chip">
        Сумма кратчайших путей (исходная сеть)
        <strong>{{ result['total_path_sum'] }}</strong>
    </div>
    <div class="summary-chip">
        Найдено мостов
        <strong>{{ result['bridge_count'] }}</strong>
    </div>
</div>

% if result['bridge_count'] == 0:
<div class="alert alert-success">Мостов нет — сеть устойчива.</div>
% end

<div style="margin: 4px 0 14px">
    <button type="button" id="bridge-download-btn" class="btn btn-default btn-sm">
        💾 Скачать результат (JSON)
    </button>
</div>

<!-- Вкладки: исходная сеть + по одной на каждый мост -->
<ul class="nav nav-tabs" role="tablist">
    % for idx, st in enumerate(result['states']):
    <li class="{{ 'active' if idx == 0 else '' }}">
        <a href="#state{{idx}}" data-toggle="tab" role="tab">{{ st['title'] }}</a>
    </li>
    % end
</ul>

<div class="tab-content">
    % for idx, st in enumerate(result['states']):
    <div class="tab-pane {{ 'active' if idx == 0 else '' }}" id="state{{idx}}" role="tabpanel">

        <div class="matrix-grid">
            % mats = [('Матрица весов', st['weight_rows'], True), ('Матрица смежности', st['adj_rows'], False)]
            % for mtitle, rows, mark_inf in mats:
            <div class="matrix-card">
                <h5>{{ mtitle }}</h5>
                <table class="table matrix-table">
                    <thead>
                        <tr>
                            <th></th>
                            % for v in result['vertices']:
                            <th>{{ v }}</th>
                            % end
                        </tr>
                    </thead>
                    <tbody>
                        % for ri, rv in enumerate(result['vertices']):
                        <tr>
                            <th>{{ rv }}</th>
                            % for cell in rows[ri]:
                            <td class="{{ 'inf' if mark_inf and cell == result['inf_label'] else '' }}">{{ cell }}</td>
                            % end
                        </tr>
                        % end
                    </tbody>
                </table>
            </div>
            % end
        </div>

        <p class="graph-hint">
            Красные рёбра — мосты (критические дороги). Серые — обычные дороги.
            Колесо мыши — масштаб, перетаскивание — перемещение.
        </p>

        <!-- Кратчайшие пути — на одном уровне с графом -->
        <div class="graph-row">
            <div class="matrix-card dist-card">
                <h5>Кратчайшие пути</h5>
                <table class="table matrix-table">
                    <thead>
                        <tr>
                            <th></th>
                            % for v in result['vertices']:
                            <th>{{ v }}</th>
                            % end
                        </tr>
                    </thead>
                    <tbody>
                        % for ri, rv in enumerate(result['vertices']):
                        <tr>
                            <th>{{ rv }}</th>
                            % for cell in st['dist_rows'][ri]:
                            <td class="{{ 'inf' if cell == result['inf_label'] else '' }}">{{ cell }}</td>
                            % end
                        </tr>
                        % end
                    </tbody>
                </table>
            </div>
            <div class="state-graph" id="graph-{{idx}}"></div>
        </div>
    </div>
    % end
</div>

<script>
var BR_BRIDGES = {{!result['gbridges']}};
var BR_STATES = [
    % for idx, st in enumerate(result['states']):
    { idx: {{idx}}, V: {{!st['gv']}}, E: {{!st['ge']}} },
    % end
];

(function () {
    var bridgeSet = {};
    BR_BRIDGES.forEach(function (p) { bridgeSet[p[0] + '|' + p[1]] = true; });

    function keyOf(a, b) { return a < b ? a + '|' + b : b + '|' + a; }

    var nets = {};

    function buildNet(s) {
        var container = document.getElementById('graph-' + s.idx);
        if (!container || typeof vis === 'undefined') { return; }

        var nodes = s.V.map(function (n) {
            return {
                id: n, label: n, shape: 'ellipse',
                color: { background: '#e8f4fb', border: '#2e86ab' },
                font: { color: '#1a3a5c', size: 16 }
            };
        });

        var edges = s.E.map(function (e) {
            var isBridge = bridgeSet[keyOf(e[0], e[1])];
            return {
                from: e[0], to: e[1], label: String(e[2]),
                font: { align: 'top', size: 12, color: '#526173' },
                width: isBridge ? 3 : 1,
                color: { color: isBridge ? '#e84855' : '#9bb8cc' },
                smooth: { type: 'continuous' }
            };
        });

        var data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
        var options = {
            physics: { enabled: true, stabilization: true },
            interaction: { dragNodes: true, dragView: true, zoomView: true }
        };
        var net = new vis.Network(container, data, options);
        net.once('afterDrawing', function () { net.fit({ animation: false }); });
        nets[s.idx] = net;
    }

    $(function () {
        if (BR_STATES.length) { buildNet(BR_STATES[0]); }

        // Граф рисуется лениво при открытии вкладки (скрытый canvas нельзя fit)
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            var idx = parseInt($(e.target).attr('href').replace('#state', ''), 10);
            if (!nets[idx]) {
                var s = BR_STATES.filter(function (x) { return x.idx === idx; })[0];
                if (s) { buildNet(s); }
            } else {
                nets[idx].fit({ animation: false });
            }
        });
    });
})();

// Экспорт результата анализа в .json
(function () {
    var payload = {{!result['gdownload']}};
    var btn = document.getElementById('bridge-download-btn');
    if (!btn) { return; }
    btn.addEventListener('click', function () {
        var text = JSON.stringify(payload, null, 2);
        var blob = new Blob([text], { type: 'application/json' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'bridges_result.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
})();
</script>
% end
