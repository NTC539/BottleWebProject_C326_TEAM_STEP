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
function addDepRow(containerId) {
    var $from = $('<select>', { name: 'dep_from[]', class: 'form-control node-select' });
    var $to = $('<select>', { name: 'dep_to[]', class: 'form-control node-select' });

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