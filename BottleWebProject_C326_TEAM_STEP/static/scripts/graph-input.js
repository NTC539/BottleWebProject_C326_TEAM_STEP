var MAX_TASKS = 20;
/**
 * Добавляет строку ввода новой задачи в указанный контейнер.
 *
 * @param {string} containerId - ID HTML-элемента (div), куда будет добавлена строка
 * @param {string} [name]      - начальное значение названия задачи (для восстановления формы после отправки)
 * @param {number|string} [dur] - начальное значение длительности (для восстановления)
 */
function addTaskRow(containerId, name, dur) {
    // Проверка лимита задач
    if ($('#' + containerId + ' .task-row').length >= MAX_TASKS) {
        alert('Нельзя добавить больше ' + MAX_TASKS + ' задач');
        return; // Прекращаем выполнение, новую строку не добавляем
    }

    // Создание поля ввода названия задачи
    var $nameInput = $('<input>', {
        type: 'text',   // Текстовое поле
        name: 'task_name[]',    // Имя для отправки формы (массив)
        class: 'form-control node-input',   // CSS-классы
        placeholder: 'Название задачи',     // Подсказка внутри поля
        value: (name != null ? name : '')   // Значение, если восстанавливаем форму
    });

    // При изменении названия задачи обновляем выпадающие списки зависимостей
    $nameInput.on('input', function () {
        updateSelects();
    });

    // Создание поля ввода длительности ──
    var $dur = $('<input>', {
        type: 'number',         // Только числа
        name: 'task_dur[]',     // имя для отправки формы (массив)
        class: 'form-control',  // CSS-классы
        min: '0',               // Минимальное значение
        placeholder: 'Длительность',    // Подсказка внутри поля
        value: (dur != null && dur !== '' ? dur : '1'), // Значение по умолчанию или если восстанавливаем форму
        style: 'max-width:120px'    // Ограничение ширины поля
    });

    // Сборка строки
    var $row = $('<div>', { class: 'input-row task-row' })
        .append($nameInput)     // Поле названия
        .append($('<span>', { class: 'edge-arrow', text: ':' }))    // Разделитель ":"
        .append($dur)           // Поле длительности
        .append(
            $('<button>', {     // Кнопка удаления строки "✕"
                type: 'button',
                class: 'btn-danger btn-xs remove-row',
                text: '✕'
            })
        );

    // Добавление строки в контейнер
    $('#' + containerId).append($row);

    // Обновляем выпадающие списки, чтобы новая задача появилась в них
    updateSelects();
}

/**
 * Добавляет строку выбора зависимости (предшественник → последователь) в контейнер.
 *
 * @param {string} containerId - ID HTML-элемента (div), куда добавить строку
 * @param {string} [fromVal]   - начальное значение для выбора предшественника
 * @param {string} [toVal]     - начальное значение для выбора последователя
 */
function addDepRow(containerId, fromVal, toVal) {
    // Создание пустых выпадающих списков
    var $from = $('<select>', {
        name: 'dep_from[]',     // Имя для отправки формы (массив)
        class: 'form-control node-select'   // CSS-классы
    });
    var $to = $('<select>', {
        name: 'dep_to[]',       // Имя для отправки формы (массив)
        class: 'form-control node-select'   // CSS-классы
    });

    // Сборка строки
    var $row = $('<div>', { class: 'input-row dep-row' })
        .append($from)      // Выпадающий список "От"
        .append($('<span>', {   // Стрелка "→"
            class: 'edge-arrow',
            text: '→'
        }))
        .append($to)        // Выпадающий список "К"
        .append(
            $('<button>', { // Кнопка удаления "✕"
                type: 'button',
                class: 'btn-danger btn-xs remove-row',
                text: '✕'
            })
        );

    // Добавление строки в контейнер
    $('#' + containerId).append($row);

    // Наполнение выпадающих списков 
    updateSelects();

    // Восстановление выбранных значений
    // Только того, как updateSelects() добавил <option> в select,
    // можно установить ранее сохранённые значения (для восстановления формы после отправки)
    if (fromVal != null) { $from.val(fromVal); }
    if (toVal != null) { $to.val(toVal); }
}

$(document).on('click', '.remove-row', function () {
    // Находим ближайший родительский элемент с классом .input-row и удаляем его со страницы
    $(this).closest('.input-row').remove();
    updateSelects();
});

function updateSelects(containerSelector) {
    // Собираеvмвсе названия задач из полей ввода
    var values = [];
    $('.node-input').each(function () {
        var v = $(this).val().trim();
        if (v) values.push(v);
    });

    // Обновляет все выпадающие списки
    $('.node-select').each(function () {
        var $sel = $(this);
        var prev = $sel.val();  // Запоминает текущий выбор
        $sel.empty();           // Очищает список
        $.each(values, function (_, v) {
            $sel.append($('<option>').val(v).text(v));  // Добавляет опции
        });
        // Восстанавливает предыдущий выбор, если он ещё существует
        if (values.indexOf(prev) !== -1) {
            $sel.val(prev);
        }
    });
}