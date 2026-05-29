% rebase('layout.tpl', title='Критический путь (CPM) - Практика', year=year)

<h2>Критический путь — Практика</h2>

<form method="POST" action="/cpm/practice">
    <div>
        <h3>Шаг 1 — Задачи проекта</h3>
        <span>
            Введите задачи и их длительность (в любых единицах — днях, часах):
        </span>
        <div id="tasks-container"></div>
        <button type="button">
            + Добавить задачу
        </button>
    </div>

    <div>
        <h3>Шаг 2 — Зависимости</h3>
        <span>
            Укажите порядок выполнения: задача A должна завершиться до начала задачи B:
        </span>
        <div id="deps-container"></div>
        <button type="button">
            + Добавить зависимость
        </button>
    </div>

    <div>
        <span>Данные:</span>
        <button type="button">
            🎲 Случайные данные
        </button>
    </div>

    <div>
        <button type="submit">Рассчитать</button>
    </div>
</form>

<div>(Ошибка)</div>

<div>
    <h3>Результат</h3>

    <div>
        <div><strong>Итог</strong></div>
        <div>
            <p>Общая длительность проекта: <strong>(Длительность)</strong></p>
            <p>Критический путь: <strong>(Критический путь)</strong></p>
        </div>
    </div>

    <h4>Таблица ранних сроков</h4>
    <table>
        <thead>
            <tr>
                <th>Задача</th>
                <th>Длительность</th>
                <th>Ранний старт (ES)</th>
                <th>Раннее окончание (EF)</th>
                <th>На крит. пути</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
            <tr>
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
            <tr>
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
            <tr>
                <td>(Имя задачи)</td>
                <td>(Длительность)</td>
                <td>(ES Задачи)</td>
                <td>(EF Задачи)</td>
                <td>(На критическом пути?)</td>
            </tr>
        </tbody>
    </table>

    <div>
        <h4>Сетевой граф проекта</h4>
        <p>
            Красные узлы и стрелки — критический путь.
            В каждом узле: название задачи, длительность, ES и EF.
        </p>
        <div id="graph-canvas"></div>
    </div>
</div>