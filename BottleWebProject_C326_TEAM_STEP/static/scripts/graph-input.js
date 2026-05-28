/**
 * graph-input.js — Dynamic form rows for graph algorithm practice pages.
 * Requires jQuery (already included via layout.tpl).
 */

/* ─────────────────────────────────────────────────────────────
   updateSelects(containerSelector)
   Rebuilds every .node-select on the page from current .node-input values.
   ───────────────────────────────────────────────────────────── */
function updateSelects(containerSelector) {
    // Collect current node values from ALL node-inputs on the page
    var values = [];
    $('.node-input').each(function () {
        var v = $(this).val().trim();
        if (v) values.push(v);
    });

    // Rebuild every select on the page
    $('.node-select').each(function () {
        var $sel = $(this);
        var prev = $sel.val();           // remember current selection
        $sel.empty();
        $.each(values, function (_, v) {
            $sel.append($('<option>').val(v).text(v));
        });
        // Restore previous selection if still available
        if (values.indexOf(prev) !== -1) {
            $sel.val(prev);
        }
    });
}

/* ─────────────────────────────────────────────────────────────
   addNodeRow(containerId, placeholder)
   Adds a vertex input row to #containerId.
   ───────────────────────────────────────────────────────────── */
function addNodeRow(containerId, placeholder) {
    var $input = $('<input>', {
        type: 'text',
        name: 'vertex[]',
        class: 'form-control node-input',
        placeholder: placeholder || 'Название узла'
    });

    // Update selects on every keystroke
    $input.on('input', function () {
        updateSelects();
    });

    var $row = $('<div>', { class: 'input-row node-row' })
        .append($input)
        .append(
            $('<button>', {
                type: 'button',
                class: 'btn btn-danger btn-xs remove-row',
                text: '✕'
            })
        );

    $('#' + containerId).append($row);
    updateSelects();
}

/* ─────────────────────────────────────────────────────────────
   addEdgeRow(containerId, directed, hasWeight, hasInf)
   Adds a directed/undirected edge row with optional weight / inf-checkbox.
   ───────────────────────────────────────────────────────────── */
function addEdgeRow(containerId, directed, hasWeight, hasInf) {
    var arrow = directed ? '→' : '—';

    var $from = $('<select>', { name: 'edge_from[]', class: 'form-control node-select' });
    var $to   = $('<select>', { name: 'edge_to[]',   class: 'form-control node-select' });

    var $row = $('<div>', { class: 'input-row edge-row' })
        .append($from)
        .append($('<span>', { class: 'edge-arrow', text: arrow }))
        .append($to);

    if (hasWeight) {
        var $w = $('<input>', {
            type: 'number',
            name: 'edge_weight[]',
            class: 'form-control edge-weight',
            min: '1',
            placeholder: 'Вес',
            value: '1'
        });
        $row.append($w);
    }

    if (hasInf) {
        var $chk = $('<input>', {
            type: 'checkbox',
            name: 'edge_inf[]',    // renamed per-row on submit by page script
            value: '1'
        });
        var $lbl = $('<label>', { class: 'inf-label' })
            .append($chk)
            .append(' недоступен (∞)');
        $row.append($lbl);
    }

    $row.append(
        $('<button>', {
            type: 'button',
            class: 'btn btn-danger btn-xs remove-row',
            text: '✕'
        })
    );

    $('#' + containerId).append($row);
    updateSelects();
}

/* ─────────────────────────────────────────────────────────────
   addTaskRow(containerId)   — CPM only
   Adds a task name + duration row.
   ───────────────────────────────────────────────────────────── */
function addTaskRow(containerId) {
    var $nameInput = $('<input>', {
        type: 'text',
        name: 'task_name[]',
        class: 'form-control node-input',
        placeholder: 'Название задачи'
    });

    $nameInput.on('input', function () {
        updateSelects();
    });

    var $dur = $('<input>', {
        type: 'number',
        name: 'task_dur[]',
        class: 'form-control',
        min: '0',
        placeholder: 'Длительность',
        value: '1',
        style: 'max-width:120px'
    });

    var $row = $('<div>', { class: 'input-row task-row' })
        .append($nameInput)
        .append($('<span>', { class: 'edge-arrow', text: ':' }))
        .append($dur)
        .append(
            $('<button>', {
                type: 'button',
                class: 'btn btn-danger btn-xs remove-row',
                text: '✕'
            })
        );

    $('#' + containerId).append($row);
    updateSelects();
}

/* ─────────────────────────────────────────────────────────────
   addDepRow(containerId)   — CPM only
   Adds a dependency A → B select row.
   ───────────────────────────────────────────────────────────── */
function addDepRow(containerId) {
    var $from = $('<select>', { name: 'dep_from[]', class: 'form-control node-select' });
    var $to   = $('<select>', { name: 'dep_to[]',   class: 'form-control node-select' });

    var $row = $('<div>', { class: 'input-row dep-row' })
        .append($from)
        .append($('<span>', { class: 'edge-arrow', text: '→' }))
        .append($to)
        .append(
            $('<button>', {
                type: 'button',
                class: 'btn btn-danger btn-xs remove-row',
                text: '✕'
            })
        );

    $('#' + containerId).append($row);
    updateSelects();
}

/* ─────────────────────────────────────────────────────────────
   Global remove-row handler
   ───────────────────────────────────────────────────────────── */
$(document).on('click', '.remove-row', function () {
    $(this).closest('.input-row').remove();
    updateSelects();
});

/* ═══════════════════════════════════════════════════════════
   ВСПОМОГАТЕЛЬНЫЕ УТИЛИТЫ ДЛЯ ЗАПОЛНЕНИЯ ФОРМ
   ═══════════════════════════════════════════════════════════ */

// Очищает контейнер узлов и добавляет строки из массива names
function fillNodes(containerNodes, names, placeholder) {
    $('#' + containerNodes).empty();
    names.forEach(function (n) {
        addNodeRow(containerNodes, placeholder);
        $('#' + containerNodes + ' .node-input').last().val(n).trigger('input');
    });
}

// Очищает контейнер рёбер и заполняет из массива [{from, to, weight?, inf?}]
function fillEdges(containerEdges, edgesArr, directed, hasWeight, hasInf) {
    $('#' + containerEdges).empty();
    edgesArr.forEach(function (e) {
        addEdgeRow(containerEdges, directed, hasWeight, hasInf);
        var $row = $('#' + containerEdges + ' .edge-row').last();
        $row.find('[name="edge_from[]"]').val(e.from);
        $row.find('[name="edge_to[]"]').val(e.to);
        if (hasWeight && e.weight !== undefined) {
            $row.find('[name="edge_weight[]"]').val(e.weight);
        }
        if (hasInf && e.inf) {
            $row.find('input[type="checkbox"]').prop('checked', true);
        }
    });
}

/* ═══════════════════════════════════════════════════════════
   ГЕНЕРАТОРЫ СЛУЧАЙНЫХ ДАННЫХ
   ═══════════════════════════════════════════════════════════ */

function randomDijkstra() {
    var n = 5, letters = 'ABCDEFGH'.slice(0, n).split('');
    var edges = [];
    for (var i = 0; i < n - 1; i++) {
        edges.push({ from: letters[i], to: letters[i + 1], weight: rnd(1, 30) });
    }
    for (var k = 0; k < 3; k++) {
        var u = letters[rnd(0, n - 2)], v = letters[rnd(1, n - 1)];
        if (u !== v) {
            edges.push({ from: u, to: v, weight: rnd(5, 50), inf: Math.random() < 0.2 });
        }
    }
    fillNodes('nodes-container', letters, 'Название узла');
    fillEdges('edges-container', edges, true, true, true);
    $('[name="source"]').val(letters[0]);
}

function randomBridges() {
    var names = ['Москва', 'СПб', 'Казань', 'Самара', 'Екатеринбург'];
    var n = names.length;
    var edges = [];
    for (var i = 1; i < n; i++) {
        edges.push({ from: names[0], to: names[i], weight: rnd(10, 300) });
    }
    edges.push({ from: names[1], to: names[2], weight: rnd(50, 200) });
    edges.push({ from: names[3], to: names[4], weight: rnd(50, 200) });
    fillNodes('nodes-container', names, 'Название города');
    fillEdges('edges-container', edges, false, true, false);
}

function randomCPM() {
    var taskNames = ['Анализ', 'Проектирование', 'Разработка', 'Тестирование', 'Документирование'];
    $('#tasks-container').empty();
    taskNames.forEach(function (name) {
        addTaskRow('tasks-container');
        var $row = $('#tasks-container .task-row').last();
        $row.find('[name="task_name[]"]').val(name).trigger('input');
        $row.find('[name="task_dur[]"]').val(rnd(2, 8));
    });
    var deps = [
        { from: taskNames[0], to: taskNames[1] },
        { from: taskNames[0], to: taskNames[2] },
        { from: taskNames[1], to: taskNames[3] },
        { from: taskNames[2], to: taskNames[3] },
        { from: taskNames[3], to: taskNames[4] }
    ];
    $('#deps-container').empty();
    deps.forEach(function (d) {
        addDepRow('deps-container');
        var $row = $('#deps-container .dep-row').last();
        $row.find('[name="dep_from[]"]').val(d.from);
        $row.find('[name="dep_to[]"]').val(d.to);
    });
}

function randomColoring() {
    var subjects = ['Математика', 'Физика', 'Химия', 'История', 'Биология', 'Информатика'];
    var n = subjects.length;
    var allPairs = [];
    for (var i = 0; i < n; i++) {
        for (var j = i + 1; j < n; j++) {
            allPairs.push({ from: subjects[i], to: subjects[j] });
        }
    }
    shuffle(allPairs);
    var edges = allPairs.slice(0, 7);
    fillNodes('nodes-container', subjects, 'Название дисциплины');
    fillEdges('edges-container', edges, false, false, false);
}

/* ═══════════════════════════════════════════════════════════
   ЗАГРУЗКА ИЗ JSON-ФАЙЛА
   ═══════════════════════════════════════════════════════════ */

function openJsonFile(callback) {
    var $inp = $('<input type="file" accept=".json">').hide();
    $('body').append($inp);
    $inp.on('change', function () {
        var file = this.files[0];
        if (!file) { $inp.remove(); return; }
        var reader = new FileReader();
        reader.onload = function (e) {
            try {
                var data = JSON.parse(e.target.result);
                callback(data);
            } catch (ex) {
                alert('Ошибка чтения файла: ' + ex.message);
            }
            $inp.remove();
        };
        reader.readAsText(file, 'utf-8');
    });
    $inp[0].click();
}

function loadFileDijkstra() {
    openJsonFile(function (d) {
        fillNodes('nodes-container', d.vertices || [], 'Название узла');
        fillEdges('edges-container', d.edges || [], true, true, true);
        if (d.source) $('[name="source"]').val(d.source);
    });
}

function loadFileBridges() {
    openJsonFile(function (d) {
        fillNodes('nodes-container', d.vertices || [], 'Название города');
        fillEdges('edges-container', d.edges || [], false, true, false);
    });
}

function loadFileCPM() {
    openJsonFile(function (d) {
        $('#tasks-container').empty();
        (d.tasks || []).forEach(function (t) {
            addTaskRow('tasks-container');
            var $row = $('#tasks-container .task-row').last();
            $row.find('[name="task_name[]"]').val(t.name).trigger('input');
            $row.find('[name="task_dur[]"]').val(t.duration);
        });
        $('#deps-container').empty();
        (d.deps || []).forEach(function (dep) {
            addDepRow('deps-container');
            var $row = $('#deps-container .dep-row').last();
            $row.find('[name="dep_from[]"]').val(dep.from);
            $row.find('[name="dep_to[]"]').val(dep.to);
        });
    });
}

function loadFileColoring() {
    openJsonFile(function (d) {
        fillNodes('nodes-container', d.vertices || [], 'Название дисциплины');
        var edges = (d.edges || []).map(function (e) {
            return Array.isArray(e) ? { from: e[0], to: e[1] } : e;
        });
        fillEdges('edges-container', edges, false, false, false);
    });
}

/* ═══════════════════════════════════════════════════════════
   СКАЧИВАНИЕ РЕЗУЛЬТАТА
   ═══════════════════════════════════════════════════════════ */

function downloadResult(page) {
    var data = (window._resultData || {})[page] || {};
    var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    var url  = URL.createObjectURL(blob);
    var a    = document.createElement('a');
    a.href   = url;
    a.download = page + '_result.json';
    a.click();
    URL.revokeObjectURL(url);
}

function downloadResultTxt(page) {
    var data  = (window._resultData || {})[page] || {};
    var lines = [page.toUpperCase() + ' — результат расчёта', ''];
    function walk(obj, indent) {
        Object.keys(obj).forEach(function (k) {
            var v = obj[k];
            if (typeof v === 'object' && v !== null && !Array.isArray(v)) {
                lines.push(indent + k + ':');
                walk(v, indent + '  ');
            } else {
                lines.push(indent + k + ': ' +
                    (Array.isArray(v) ? v.join(' → ') : v));
            }
        });
    }
    walk(data, '');
    var blob = new Blob([lines.join('\n')], { type: 'text/plain' });
    var a    = document.createElement('a');
    a.href   = URL.createObjectURL(blob);
    a.download = page + '_result.txt';
    a.click();
}

/* ═══════════════════════════════════════════════════════════
   МЕЛКИЕ УТИЛИТЫ
   ═══════════════════════════════════════════════════════════ */
function rnd(a, b) { return Math.floor(Math.random() * (b - a + 1)) + a; }
function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
        var j = rnd(0, i);
        var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
}
