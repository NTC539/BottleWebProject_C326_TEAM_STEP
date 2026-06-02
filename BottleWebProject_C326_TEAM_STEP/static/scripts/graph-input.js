var MAX_TASKS = 20;

function addTaskRow(containerId, name, dur) {
    if ($('#' + containerId + ' .task-row').length >= MAX_TASKS) {
        alert('Нельзя добавить больше ' + MAX_TASKS + ' задач');
        return;
    }
    var $nameInput = $('<input>', {
        type: 'text',
        name: 'task_name[]',
        class: 'form-control node-input',
        placeholder: 'Название задачи',
        value: (name != null ? name : '')
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
        value: (dur != null && dur !== '' ? dur : '1'),
        style: 'max-width:120px'
    });

    var $row = $('<div>', { class: 'input-row task-row' })
        .append($nameInput)
        .append($('<span>', { class: 'edge-arrow', text: ':' }))
        .append($dur)
        .append(
            $('<button>', {
                type: 'button',
                class: 'btn-danger btn-xs remove-row',
                text: '✕'
            })
        );

    $('#' + containerId).append($row);
    updateSelects();
}
function addDepRow(containerId, fromVal, toVal) {
    var $from = $('<select>', { name: 'dep_from[]', class: 'form-control node-select' });
    var $to = $('<select>', { name: 'dep_to[]', class: 'form-control node-select' });

    var $row = $('<div>', { class: 'input-row dep-row' })
        .append($from)
        .append($('<span>', { class: 'edge-arrow', text: '→' }))
        .append($to)
        .append(
            $('<button>', {
                type: 'button',
                class: 'btn-danger btn-xs remove-row',
                text: '✕'
            })
        );

    $('#' + containerId).append($row);
    updateSelects();

    // Восстановление выбранных значений (если опции уже добавлены updateSelects).
    if (fromVal != null) { $from.val(fromVal); }
    if (toVal != null) { $to.val(toVal); }
}

$(document).on('click', '.remove-row', function () {
    $(this).closest('.input-row').remove();
    updateSelects();
});

function updateSelects(containerSelector) {
    // Собирает все названия задач из полей ввода
    var values = [];
    $('.node-input').each(function () {
        var v = $(this).val().trim();
        if (v) values.push(v);
    });

    // Обновляет все выпадающие списки
    $('.node-select').each(function () {
        var $sel = $(this);
        var prev = $sel.val();  // запоминает текущий выбор
        $sel.empty();           // очищает список
        $.each(values, function (_, v) {
            $sel.append($('<option>').val(v).text(v));  // добавляет опции
        });
        // Восстанавливает предыдущий выбор, если он ещё существует
        if (values.indexOf(prev) !== -1) {
            $sel.val(prev);
        }
    });
}

/* ============================================================
   Мосты Тарьяна (bridges_practice): города и дороги
   ============================================================ */

// Добавляет строку города в таблицу #bridge-nodes-body
function addBridgeNodeRow(name) {
    var $input = $('<input>', {
        type: 'text',
        name: 'node[]',
        class: 'form-control bridge-node-input',
        placeholder: 'Город',
        value: (name != null ? name : '')
    });
    $input.on('input', updateBridgeSelects);

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

// Добавляет строку дороги (откуда → куда + вес) в таблицу #bridge-edges-body
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

$(document).on('click', '.remove-bridge-node', function () {
    $(this).closest('tr').remove();
    updateBridgeSelects();
});

$(document).on('click', '.remove-bridge-edge', function () {
    $(this).closest('tr').remove();
});

// Наполняет списки «откуда/куда» именами городов из полей ввода
function updateBridgeSelects() {
    var values = [];
    $('.bridge-node-input').each(function () {
        var v = $(this).val().trim();
        if (v) values.push(v);
    });
    $('.bridge-node-select').each(function () {
        var $sel = $(this);
        var prev = $sel.val();
        $sel.empty();
        $.each(values, function (_, v) {
            $sel.append($('<option>').val(v).text(v));
        });
        if (values.indexOf(prev) !== -1) {
            $sel.val(prev);
        }
    });
}