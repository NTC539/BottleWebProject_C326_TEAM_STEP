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
