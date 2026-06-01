/* ============================================================
   Мосты Тарьяна (bridges_practice): города и дороги
   ============================================================ */

function addBridgeNodeRow(name) {
    var $input = $('<input>', {
        type: 'text',
        name: 'node[]',
        class: 'form-control bridge-node-input',
        placeholder: 'Город',
        value: (name != null ? name : '')
    });
    // Запоминаем текущее имя города, чтобы при переименовании перенести
    // ссылки в дорогах со старого имени на новое (а не сбрасывать на первый город).
    $input.data('prev', name != null ? name : '');
    $input.on('input', function () {
        var $i = $(this);
        var newVal = $i.val().trim();
        // Поле временно пустое (город ещё дописывают) — списки не трогаем,
        // иначе дороги «соскочат» на первый город.
        if (newVal === '') { return; }
        updateBridgeSelects($i.data('prev'), newVal);
        $i.data('prev', newVal);
    });

    var $row = $('<tr>', { class: 'bridge-node-row' })
        .append($('<td>').append($input))
        .append($('<td>', { class: 'row-action' }).append(
            $('<button>', {
                type: 'button',
                class: 'btn btn-danger btn-xs remove-bridge-node',
                text: '✕'
            })
        ));

    $('#bridge-nodes-body').append($row);
    updateBridgeSelects();
}

function addBridgeEdgeRow(fromVal, toVal, weightVal) {
    var $from = $('<select>', { name: 'edge_from[]', class: 'form-control bridge-node-select' });
    var $to = $('<select>', { name: 'edge_to[]', class: 'form-control bridge-node-select' });
    var $weight = $('<input>', {
        type: 'number',
        name: 'edge_weight[]',
        class: 'form-control',
        min: '0',
        step: 'any',
        placeholder: 'Вес',
        value: (weightVal != null ? weightVal : '')
    });

    var $row = $('<tr>', { class: 'bridge-edge-row' })
        .append($('<td>').append($from))
        .append($('<td>', { class: 'edge-arrow-cell' }).append(
            $('<span>', { class: 'edge-arrow', text: '—' })))
        .append($('<td>').append($to))
        .append($('<td>').append($weight))
        .append($('<td>', { class: 'row-action' }).append(
            $('<button>', {
                type: 'button',
                class: 'btn btn-danger btn-xs remove-bridge-edge',
                text: '✕'
            })
        ));

    $('#bridge-edges-body').append($row);
    updateBridgeSelects();

    if (fromVal != null) { $from.val(fromVal); }
    if (toVal != null) { $to.val(toVal); }
}

function clearBridgeNodes() {
    $('#bridge-nodes-body').empty();
    updateBridgeSelects();
}

function clearBridgeEdges() {
    $('#bridge-edges-body').empty();
}

$(document).on('click', '.remove-bridge-node', function () {
    $(this).closest('tr').remove();
    updateBridgeSelects();
});

$(document).on('click', '.remove-bridge-edge', function () {
    $(this).closest('tr').remove();
});

// renameFrom/renameTo (необязательны): если город переименовали — переносит
// выбор дорог со старого имени на новое, чтобы рёбра не теряли ссылку.
function updateBridgeSelects(renameFrom, renameTo) {
    var values = [];
    $('.bridge-node-input').each(function () {
        var v = $(this).val().trim();
        if (v) values.push(v);
    });
    $('.bridge-node-select').each(function () {
        var $sel = $(this);
        var prev = $sel.val();
        // Если эта дорога указывала на переименованный город — следуем за новым именем.
        if (renameFrom != null && prev === renameFrom) {
            prev = renameTo;
        }
        $sel.empty();
        $.each(values, function (_, v) {
            $sel.append($('<option>').val(v).text(v));
        });
        if (values.indexOf(prev) !== -1) {
            $sel.val(prev);
        }
    });
}
