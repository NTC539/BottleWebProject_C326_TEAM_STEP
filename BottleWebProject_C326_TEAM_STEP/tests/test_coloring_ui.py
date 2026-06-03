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


if __name__ == "__main__":
    unittest.main()
