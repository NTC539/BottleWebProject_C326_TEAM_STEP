import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]
    finally:
        sock.close()


class ColoringPracticeUiTest(unittest.TestCase):
    TEST_HISTORY_NAME_SETS = [
        {"Algebra", "Physics", "History", "Literature"},
    ]

    @classmethod
    def setUpClass(cls):
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import Select
            from selenium.webdriver.support.ui import WebDriverWait
        except ImportError:
            raise unittest.SkipTest("Selenium is not installed")

        cls.webdriver = webdriver
        cls.By = By
        cls.EC = EC
        cls.Select = Select
        cls.WebDriverWait = WebDriverWait
        cls.server = None
        cls.driver = None

        cls.port = free_port()
        cls.base_url = "http://127.0.0.1:{}".format(cls.port)
        env = os.environ.copy()
        env["SERVER_HOST"] = "127.0.0.1"
        env["SERVER_PORT"] = str(cls.port)

        cls.server = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=str(PROJECT_ROOT),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cls.wait_for_server()

        try:
            cls.driver = cls.make_driver()
        except Exception as exc:
            cls.tearDownClass()
            raise unittest.SkipTest("Browser driver is not available: {}".format(exc))

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "driver", None):
            cls.driver.quit()
            cls.driver = None

        if getattr(cls, "server", None):
            cls.server.terminate()
            try:
                cls.server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                cls.server.kill()
            cls.server = None

    @classmethod
    def wait_for_server(cls):
        for _ in range(60):
            if cls.server.poll() is not None:
                raise unittest.SkipTest("Bottle server did not start")
            try:
                with urllib.request.urlopen(cls.base_url + "/coloring/practice", timeout=0.5):
                    return
            except OSError:
                time.sleep(0.2)

        raise unittest.SkipTest("Bottle server is not available")

    @classmethod
    def make_driver(cls):
        errors = []

        chrome_options = cls.webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1280,900")
        chrome_options.add_argument("--disable-gpu")
        try:
            return cls.webdriver.Chrome(options=chrome_options)
        except Exception as exc:
            errors.append("Chrome: {}".format(exc))

        edge_options = cls.webdriver.EdgeOptions()
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--window-size=1280,900")
        edge_options.add_argument("--disable-gpu")
        try:
            return cls.webdriver.Edge(options=edge_options)
        except Exception as exc:
            errors.append("Edge: {}".format(exc))

        raise RuntimeError("; ".join(errors))

    def tearDown(self):
        self.clean_test_history()

    def clean_test_history(self):
        history_path = PROJECT_ROOT / "data" / "coloring_history.json"
        if not history_path.exists():
            return

        try:
            with history_path.open("r", encoding="utf-8") as file:
                history = json.load(file)
        except (OSError, json.JSONDecodeError):
            return

        if not isinstance(history, list):
            return

        clean_history = []
        for entry in history:
            subjects = entry.get("input", {}).get("subjects", [])
            names = {item.get("name") for item in subjects if isinstance(item, dict)}
            if names in self.TEST_HISTORY_NAME_SETS:
                continue
            clean_history.append(entry)

        if len(clean_history) == len(history):
            return

        with history_path.open("w", encoding="utf-8") as file:
            json.dump(clean_history, file, ensure_ascii=False, indent=2)

    def wait_css(self, selector):
        return self.WebDriverWait(self.driver, 10).until(
            self.EC.presence_of_element_located((self.By.CSS_SELECTOR, selector))
        )

    def wait_until(self, check):
        return self.WebDriverWait(self.driver, 10).until(lambda driver: check(driver))

    def subject_values(self):
        return self.driver.execute_script(
            "return Array.from(document.querySelectorAll('.subject-name')).map(function(input) { return input.value; });"
        )

    def conflict_count(self):
        return self.driver.execute_script(
            "return document.querySelectorAll('input[name=\"conflict_from[]\"]').length;"
        )

    def test_page_has_required_controls(self):
        self.driver.get(self.base_url + "/coloring/practice")

        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "#subjectsTable"))
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "[data-conflict-list]"))
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "#jsonFile"))
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "#graph-canvas"))
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "[data-submit-action='generate']"))

    def test_json_import_manual_edit_and_calculation(self):
        data = {
            "subjects": [
                {"name": "Algebra", "teacher": "Ivanov"},
                {"name": "Physics", "teacher": "Petrov"},
                {"name": "History", "teacher": "Ivanov"},
            ],
            "conflicts": [["Algebra", "Physics"], ["Physics", "History"]],
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as file:
            json.dump(data, file, ensure_ascii=False)
            json_path = file.name
        self.addCleanup(lambda: os.path.exists(json_path) and os.remove(json_path))

        self.driver.get(self.base_url + "/coloring/practice")
        self.driver.find_element(self.By.ID, "jsonFile").send_keys(json_path)
        self.driver.find_element(self.By.CSS_SELECTOR, "[data-submit-action='load_json']").click()

        self.wait_until(lambda driver: self.subject_values() and self.subject_values()[0] == "Algebra")

        self.driver.find_element(self.By.ID, "newSubjectName").send_keys("Literature")
        self.driver.find_element(self.By.ID, "newSubjectTeacher").send_keys("Sidorov")
        self.driver.find_element(self.By.ID, "addSubjectBtn").click()
        self.wait_until(lambda driver: len(self.subject_values()) == 4)

        self.Select(self.driver.find_element(self.By.ID, "conflictFrom")).select_by_visible_text("Literature")
        self.Select(self.driver.find_element(self.By.ID, "conflictTo")).select_by_visible_text("Physics")
        self.driver.find_element(self.By.ID, "addConflictBtn").click()
        self.wait_until(lambda driver: self.conflict_count() == 3)

        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css("#coloring-result")

        self.assertIn("Literature", self.driver.page_source)
        self.assertIn("Physics", self.driver.page_source)
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "#graph-canvas canvas"))
        self.assertGreater(self.driver.find_element(self.By.ID, "graph-canvas").size["height"], 250)

    def test_random_generation_updates_subject_table(self):
        self.driver.get(self.base_url + "/coloring/practice")

        subject_count = self.driver.find_element(self.By.ID, "subjectCount")
        subject_count.clear()
        subject_count.send_keys("6")

        density = self.driver.find_element(self.By.ID, "density")
        density.clear()
        density.send_keys("0")

        self.driver.find_element(self.By.CSS_SELECTOR, "[data-submit-action='generate']").click()
        self.wait_until(
            lambda driver: len(self.subject_values()) == 6
            and self.subject_values()[0] == "Дисциплина 1"
        )

        first_name = self.subject_values()[0]
        self.assertEqual(first_name, "Дисциплина 1")
        self.assertEqual(self.conflict_count(), 0)

    def test_too_many_subjects_show_validation_error(self):
        self.driver.get(self.base_url + "/coloring/practice")

        rows = []
        for index in range(1, 22):
            rows.append(
                """
                <tr>
                    <td data-row-number>{index}</td>
                    <td><input type="text" name="subject[]" class="form-control subject-name" value="Extra {index}"></td>
                    <td><input type="text" name="teacher[]" class="form-control" value="Teacher {index}"></td>
                    <td></td>
                </tr>
                """.format(index=index)
            )

        self.driver.execute_script(
            """
            document.querySelector('[data-subject-body]').innerHTML = arguments[0];
            document.querySelector('[data-conflict-list]').innerHTML = '';
            document.getElementById('formAction').value = 'calculate';
            """,
            "".join(rows),
        )

        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css(".coloring-alert")

        self.assertIn("Количество дисциплин не должно превышать 20", self.driver.page_source)
        self.assertFalse(self.driver.find_elements(self.By.CSS_SELECTOR, "#coloring-result"))


    # ── Full-pipeline tests ───────────────────────────────────────────────────

    def test_full_manual_pipeline(self):
        """Полный пайп: ручной ввод → конфликты → расчёт → таблица смен → Welsh-Powell."""
        self.driver.get(self.base_url + "/coloring/practice")

        # Очищаем форму: убираем все строки дисциплин
        self.driver.execute_script(
            """
            document.querySelector('[data-subject-body]').innerHTML = '';
            document.querySelector('[data-conflict-list]').innerHTML = '';
            """
        )

        # Добавляем три дисциплины через поля «Новая дисциплина»
        subjects = [
            ("Математика", "Иванов"),
            ("Физика", "Петров"),
            ("Информатика", "Сидоров"),
        ]
        for name, teacher in subjects:
            self.driver.find_element(self.By.ID, "newSubjectName").clear()
            self.driver.find_element(self.By.ID, "newSubjectName").send_keys(name)
            self.driver.find_element(self.By.ID, "newSubjectTeacher").clear()
            self.driver.find_element(self.By.ID, "newSubjectTeacher").send_keys(teacher)
            self.driver.find_element(self.By.ID, "addSubjectBtn").click()

        self.wait_until(lambda d: len(self.subject_values()) == 3)

        # Добавляем конфликт Математика–Физика
        self.Select(self.driver.find_element(self.By.ID, "conflictFrom")).select_by_visible_text("Математика")
        self.Select(self.driver.find_element(self.By.ID, "conflictTo")).select_by_visible_text("Физика")
        self.driver.find_element(self.By.ID, "addConflictBtn").click()
        self.wait_until(lambda d: self.conflict_count() == 1)

        # Добавляем конфликт Физика–Информатика
        self.Select(self.driver.find_element(self.By.ID, "conflictFrom")).select_by_visible_text("Физика")
        self.Select(self.driver.find_element(self.By.ID, "conflictTo")).select_by_visible_text("Информатика")
        self.driver.find_element(self.By.ID, "addConflictBtn").click()
        self.wait_until(lambda d: self.conflict_count() == 2)

        # Рассчитать расписание
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css("#coloring-result")

        # Таблица расписания по сменам
        schedule_rows = self.driver.find_elements(
            self.By.CSS_SELECTOR, "#coloring-result .result-table tbody tr"
        )
        self.assertGreater(len(schedule_rows), 0, "Таблица расписания должна содержать строки")

        # Таблица смен преподавателей
        for teacher_name in ("Иванов", "Петров", "Сидоров"):
            self.assertIn(teacher_name, self.driver.page_source)

        # Таблица Welsh-Powell
        self.assertIn("Welsh-Powell", self.driver.page_source)
        wp_rows = self.driver.find_elements(
            self.By.CSS_SELECTOR, "table.result-table tbody tr"
        )
        self.assertGreater(len(wp_rows), 0)

    def test_random_generation_then_calculate_pipeline(self):
        """Пайп: генерация → расчёт → результат содержит корректные данные."""
        self.driver.get(self.base_url + "/coloring/practice")

        subject_count = self.driver.find_element(self.By.ID, "subjectCount")
        subject_count.clear()
        subject_count.send_keys("5")

        density = self.driver.find_element(self.By.ID, "density")
        density.clear()
        density.send_keys("0.5")

        self.driver.find_element(self.By.CSS_SELECTOR, "[data-submit-action='generate']").click()
        self.wait_until(lambda d: len(self.subject_values()) == 5)

        # После генерации дисциплины появились в таблице
        names = self.subject_values()
        self.assertEqual(len(names), 5)
        self.assertTrue(all(n.startswith("Дисциплина") for n in names))

        # Рассчитать
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css("#coloring-result")

        # Блок результата присутствует
        result_section = self.driver.find_element(self.By.ID, "coloring-result")
        self.assertTrue(result_section.is_displayed())

        # Счётчик смен — число ≥ 1
        num_colors_text = self.driver.find_element(
            self.By.CSS_SELECTOR, "#coloring-result .result-number"
        ).text
        self.assertTrue(num_colors_text.isdigit() and int(num_colors_text) >= 1)

    def test_json_import_calculate_and_history_saved(self):
        """Пайп: импорт JSON → расчёт → история сохранилась в файле."""
        data = {
            "subjects": [
                {"name": "Algebra", "teacher": "Ivanov"},
                {"name": "Physics", "teacher": "Petrov"},
                {"name": "History", "teacher": "Sidorov"},
                {"name": "Literature", "teacher": "Smirnova"},
            ],
            "conflicts": [
                ["Algebra", "Physics"],
                ["Physics", "History"],
                ["History", "Literature"],
            ],
        }

        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as f:
            json.dump(data, f, ensure_ascii=False)
            json_path = f.name
        self.addCleanup(lambda: os.path.exists(json_path) and os.remove(json_path))

        self.driver.get(self.base_url + "/coloring/practice")
        self.driver.find_element(self.By.ID, "jsonFile").send_keys(json_path)
        self.driver.find_element(self.By.CSS_SELECTOR, "[data-submit-action='load_json']").click()

        self.wait_until(lambda d: self.subject_values() and self.subject_values()[0] == "Algebra")
        self.assertEqual(len(self.subject_values()), 4)
        self.assertEqual(self.conflict_count(), 3)

        # Рассчитать
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css("#coloring-result")

        # Все четыре дисциплины видны в результате
        for subj in ("Algebra", "Physics", "History", "Literature"):
            self.assertIn(subj, self.driver.page_source)

        # Запись появилась в истории
        history_path = PROJECT_ROOT / "data" / "coloring_history.json"
        self.assertTrue(history_path.exists(), "Файл истории должен существовать после расчёта")
        with history_path.open("r", encoding="utf-8") as file:
            history = json.load(file)
        names_in_history = [
            {s.get("name") for s in entry.get("input", {}).get("subjects", [])}
            for entry in history
        ]
        self.assertIn({"Algebra", "Physics", "History", "Literature"}, names_in_history)

    def test_export_json_button_appears_after_calculation(self):
        """Кнопка «Скачать JSON» появляется только после успешного расчёта."""
        self.driver.get(self.base_url + "/coloring/practice")

        # До расчёта кнопки нет
        self.assertFalse(
            self.driver.find_elements(self.By.CSS_SELECTOR, ".export-json-btn"),
            "Кнопка экспорта не должна быть видна до расчёта",
        )

        # Рассчитать с данными по умолчанию
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css("#coloring-result")

        # После расчёта кнопка появилась
        self.assertTrue(
            self.driver.find_elements(self.By.CSS_SELECTOR, ".export-json-btn"),
            "Кнопка экспорта должна появиться после расчёта",
        )

    def test_add_and_remove_conflict_updates_count(self):
        """Добавление и удаление конфликта корректно обновляет счётчик."""
        self.driver.get(self.base_url + "/coloring/practice")

        initial_count = self.conflict_count()

        # Добавляем конфликт между первыми двумя дисциплинами по умолчанию
        from_select = self.Select(self.driver.find_element(self.By.ID, "conflictFrom"))
        options = [o.text for o in from_select.options]
        if len(options) < 2:
            self.skipTest("Недостаточно дисциплин для теста конфликтов")

        from_select.select_by_index(0)
        self.Select(self.driver.find_element(self.By.ID, "conflictTo")).select_by_index(1)
        self.driver.find_element(self.By.ID, "addConflictBtn").click()
        self.wait_until(lambda d: self.conflict_count() > initial_count)

        after_add = self.conflict_count()

        # Удаляем только что добавленный конфликт
        remove_buttons = self.driver.find_elements(
            self.By.CSS_SELECTOR, "[data-conflict-list] [data-remove-conflict]"
        )
        self.assertTrue(remove_buttons, "Должны быть кнопки удаления конфликтов")
        remove_buttons[-1].click()
        self.wait_until(lambda d: self.conflict_count() < after_add)

        self.assertEqual(self.conflict_count(), initial_count)

    def test_empty_subjects_shows_validation_error(self):
        """Отправка пустой таблицы дисциплин возвращает ошибку валидации."""
        self.driver.get(self.base_url + "/coloring/practice")

        self.driver.execute_script(
            """
            document.querySelector('[data-subject-body]').innerHTML = '';
            document.querySelector('[data-conflict-list]').innerHTML = '';
            document.getElementById('formAction').value = 'calculate';
            """
        )

        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css(".coloring-alert")

        self.assertIn("дисциплин", self.driver.page_source.lower())
        self.assertFalse(self.driver.find_elements(self.By.CSS_SELECTOR, "#coloring-result"))

    def test_result_section_structure(self):
        """Раздел результата содержит все три блока: смены, преподаватели, Welsh-Powell."""
        self.driver.get(self.base_url + "/coloring/practice")

        # Используем данные по умолчанию — просто рассчитываем
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css("#coloring-result")

        page = self.driver.page_source

        # Блок «Расписание по сменам»
        self.assertIn("Смена", page)
        # Блок «Смены преподавателей»
        self.assertIn("Преподаватель", page)
        # Таблица порядка Welsh-Powell
        self.assertIn("Welsh-Powell", page)
        # Сводка результата: num_colors, teacher_cost, conflicts count
        numbers = self.driver.find_elements(self.By.CSS_SELECTOR, "#coloring-result .result-number")
        self.assertEqual(len(numbers), 3, "Должны быть три числовых показателя в сводке")
        for el in numbers:
            self.assertTrue(el.text.isdigit(), "Каждый показатель должен быть числом")


if __name__ == "__main__":
    unittest.main()
