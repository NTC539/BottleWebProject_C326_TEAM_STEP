% rebase('layout.tpl', title=title, year=year, active_page='algorithms')

<h2>{{ title }}</h2>

<div class="theory-section">
    <h3>Описание задачи</h3>
    {{!task_description}}
</div>

<div class="theory-section">
    <h3>Теория</h3>
    {{!theory_content}}
</div>

<div class="theory-section">
    <h3>Алгоритм</h3>
    {{!algorithm_steps}}
</div>

<div class="btn-practice-wrap">
    <a href="{{ practice_url }}" class="btn-practice">
        Перейти к практике &raquo;
    </a>
</div>
