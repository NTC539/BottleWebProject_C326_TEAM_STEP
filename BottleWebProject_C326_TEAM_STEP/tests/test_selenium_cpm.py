import json
import time
import unittest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_separator(title):
    """Выводит разделитель с названием теста."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


class TestCPMUILargeData(unittest.TestCase):
    """Автоматизированный тест интерфейса расчёта критического пути с большими данными."""

    @classmethod
    def setUpClass(cls):
        test_dir = Path(__file__).parent
        data_dir = test_dir / 'data'
        instructions = load_json(data_dir / 'test_cpm_instructions.json')
        cls.base_url = instructions['base_url']
        test_data_file = instructions['test_data_file']
        test_data = load_json(data_dir / test_data_file)
        cls.tasks = test_data['tasks']
        cls.deps = test_data['deps']
        print(f"[ПОЛОЖИТЕЛЬНЫЙ ТЕСТ] Загружено {len(cls.tasks)} задач и {len(cls.deps)} зависимостей.")

    def setUp(self):
        options = webdriver.EdgeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = Service(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        if self.driver:
            time.sleep(2)
            self.driver.quit()

    def test_fill_large_data_and_calculate(self):
        """Позитивный сценарий: заполнение формы 20 задачами и проверка результата."""
        print_separator("ТЕСТ 1: ПОЛОЖИТЕЛЬНЫЙ СЦЕНАРИЙ (большие данные)")

        driver = self.driver
        wait = self.wait

        # 1. Открыть страницу
        print("[1/7] Открытие страницы практики...")
        driver.get(f"{self.base_url}/cpm/practice")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))

        # 2. Подготовка контейнера задач
        tasks_container = driver.find_element(By.ID, 'tasks-container')
        initial_rows = tasks_container.find_elements(By.CLASS_NAME, 'task-row')
        if not initial_rows:
            add_task_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[onclick*=\"addTaskRow('tasks-container')\"]")))
            add_task_btn.click()
            initial_rows = tasks_container.find_elements(By.CLASS_NAME, 'task-row')

        # 3. Заполнение задач (компактный лог)
        print(f"[2/7] Ввод {len(self.tasks)} задач...")
        add_task_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[onclick*=\"addTaskRow('tasks-container')\"]")))
        total_tasks = len(self.tasks)
        progress_step = max(1, total_tasks // 4)  # показывать прогресс 4 раза

        for idx, task in enumerate(self.tasks):
            if idx == 0:
                row = initial_rows[0]
            else:
                add_task_btn.click()
                row = tasks_container.find_elements(By.CLASS_NAME, 'task-row')[-1]

            name_input = row.find_element(By.NAME, 'task_name[]')
            name_input.clear()
            name_input.send_keys(task['name'])
            driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", name_input)
            dur_input = row.find_element(By.NAME, 'task_dur[]')
            dur_input.clear()
            dur_input.send_keys(str(task['dur']))

            # Прогресс каждые 25%
            if (idx + 1) % progress_step == 0 or idx == total_tasks - 1:
                print(f"   Прогресс: {idx + 1}/{total_tasks} задач")
            time.sleep(0.15)

        # 4. Заполнение зависимостей (компактный лог)
        print(f"[3/7] Ввод {len(self.deps)} зависимостей...")
        add_dep_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[onclick*=\"addDepRow('deps-container')\"]")))
        deps_container = driver.find_element(By.ID, 'deps-container')
        total_deps = len(self.deps)
        progress_step = max(1, total_deps // 4)

        for idx, dep in enumerate(self.deps):
            add_dep_btn.click()
            dep_rows = deps_container.find_elements(By.CLASS_NAME, 'dep-row')
            last_row = dep_rows[-1]
            from_select = last_row.find_element(By.NAME, 'dep_from[]')
            to_select = last_row.find_element(By.NAME, 'dep_to[]')
            WebDriverWait(last_row, 5).until(
                lambda row: len(Select(row.find_element(By.NAME, 'dep_from[]')).options) > 0)
            Select(from_select).select_by_visible_text(dep[0])
            Select(to_select).select_by_visible_text(dep[1])

            if (idx + 1) % progress_step == 0 or idx == total_deps - 1:
                print(f"   Прогресс: {idx + 1}/{total_deps} зависимостей")
            time.sleep(0.1)

        # 5. Запуск расчёта
        print("[4/7] Запуск расчёта...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 6. Прокрутка к итогу
        print("[5/7] Прокрутка к сводке (длительность, критический путь)...")
        summary = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h3[contains(text(),'Результат')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", summary)
        self.assertTrue(summary.is_displayed(), "Блок с результатами не отобразился")
        time.sleep(4.2)

        # 7. Прокрутка к таблице
        print("[6/7] Прокрутка к таблице сроков и резервов...")
        table = driver.find_element(By.CSS_SELECTOR, "table.table")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", table)
        self.assertTrue(table.is_displayed(), "Таблица с результатами не отобразилась")
        time.sleep(4.2)

        # 8. Прокрутка к графу
        print("[7/7] Прокрутка к графу проекта...")
        graph = driver.find_element(By.ID, "graph-canvas")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", graph)
        self.assertTrue(graph.is_displayed(), "Граф не отобразился")
        time.sleep(4.2)

        print("   ПОЛОЖИТЕЛЬНЫЙ ТЕСТ ПРОЙДЕН УСПЕШНО")


class TestCPMUIErrorHandling(unittest.TestCase):
    """Тесты обработки ошибок в интерфейсе CPM."""

    @classmethod
    def setUpClass(cls):
        test_dir = Path(__file__).parent
        data_dir = test_dir / 'data'
        instructions = load_json(data_dir / 'test_cpm_instructions.json')
        cls.base_url = instructions['base_url']
        error_data_file = data_dir / 'test_cpm_data_error.json'
        error_data = load_json(error_data_file)
        cls.tasks = error_data['tasks']
        cls.deps = error_data['deps']
        print(f"[НЕГАТИВНЫЙ ТЕСТ] Загружено {len(cls.tasks)} задач и {len(cls.deps)} зависимостей.")

    def setUp(self):
        options = webdriver.EdgeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = Service(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        if self.driver:
            time.sleep(5)
            self.driver.quit()

    def test_error_message_displayed(self):
        """Заполнение формы данными с ошибкой и проверка появления сообщения об ошибке."""
        print_separator("ТЕСТ 2: НЕГАТИВНЫЙ СЦЕНАРИЙ (цикл)")

        driver = self.driver
        wait = self.wait

        # 1. Открыть страницу
        print("[1/4] Открытие страницы...")
        driver.get(f"{self.base_url}/cpm/practice")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))

        # Очистить старые данные
        clear_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Очистить всё')]")
        for btn in clear_buttons:
            try:
                btn.click()
            except:
                pass
        time.sleep(1)

        # 2. Заполнить задачи
        print(f"[2/4] Ввод {len(self.tasks)} задач...")
        tasks_container = driver.find_element(By.ID, 'tasks-container')
        initial_rows = tasks_container.find_elements(By.CLASS_NAME, 'task-row')
        if not initial_rows:
            add_task_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[onclick*=\"addTaskRow('tasks-container')\"]")))
            add_task_btn.click()
            initial_rows = tasks_container.find_elements(By.CLASS_NAME, 'task-row')

        add_task_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[onclick*=\"addTaskRow('tasks-container')\"]")))
        for idx, task in enumerate(self.tasks):
            if idx == 0:
                row = initial_rows[0]
            else:
                add_task_btn.click()
                row = tasks_container.find_elements(By.CLASS_NAME, 'task-row')[-1]
            name_input = row.find_element(By.NAME, 'task_name[]')
            name_input.clear()
            name_input.send_keys(task['name'])
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                  name_input)
            dur_input = row.find_element(By.NAME, 'task_dur[]')
            dur_input.clear()
            dur_input.send_keys(str(task['dur']))
            time.sleep(0.15)

        # 3. Заполнить зависимости
        print(f"[3/4] Ввод {len(self.deps)} зависимостей...")
        add_dep_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[onclick*=\"addDepRow('deps-container')\"]")))
        deps_container = driver.find_element(By.ID, 'deps-container')
        for dep in self.deps:
            add_dep_btn.click()
            dep_rows = deps_container.find_elements(By.CLASS_NAME, 'dep-row')
            last_row = dep_rows[-1]
            from_select = last_row.find_element(By.NAME, 'dep_from[]')
            to_select = last_row.find_element(By.NAME, 'dep_to[]')
            WebDriverWait(last_row, 5).until(
                lambda row: len(Select(row.find_element(By.NAME, 'dep_from[]')).options) > 0)
            Select(from_select).select_by_visible_text(dep[0])
            Select(to_select).select_by_visible_text(dep[1])
            time.sleep(0.1)

        # 4. Отправить форму и проверить ошибку
        print("[4/4] Отправка формы и проверка ошибки...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        error_div = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".alert-danger")))
        self.assertTrue(error_div.is_displayed(), "Сообщение об ошибке не отобразилось")
        error_text = error_div.text
        print(f"   Получено сообщение: {error_text}")
        self.assertIn("цикл", error_text.lower(), "Текст ошибки не содержит 'цикл'")
        print("   НЕГАТИВНЫЙ ТЕСТ ПРОЙДЕН УСПЕШНО")


if __name__ == '__main__':
    unittest.main()