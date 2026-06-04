"""
tests/test_bridges_ui.py — UI-тест страницы /bridges/practice (Selenium).

Большой набор исходных данных (12 городов,
16 дорог) считывается из файла tests/data/bridges_ui_network.json и вводится в
форму, после чего проверяется генерация страницы с результатом анализа.

Тест аккуратно пропускается (SkipTest), если Selenium или драйвер браузера
не установлены, — чтобы не ломать общий прогон юнит-тестов на машинах без браузера.

Запуск: python -m unittest tests.test_bridges_ui -v
"""

import json
import os
import subprocess
import sys
import time
import unittest
import urllib.request
from pathlib import Path

from algorithms.bridges import analyze_network


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = Path(__file__).resolve().parent / "data" / "bridges_ui_network.json"

# Фиксированный порт тестового сервера. Если занят (например, остался висеть
# прошлый запуск) — сервер не поднимется и тесты будут пропущены: убей процесс.
SERVER_PORT = 5555

# Длительность пауз между этапами (сек), чтобы было видно глазами, что делает
# тест. Поставь больше — медленнее, 0 — без пауз.
STEP_PAUSE = 1.2


class BridgesPracticeUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
        except ImportError:
            raise unittest.SkipTest("Selenium is not installed")

        cls.webdriver = webdriver
        cls.By = By
        cls.EC = EC
        cls.WebDriverWait = WebDriverWait
        cls.server = None
        cls.driver = None

        cls.port = SERVER_PORT
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
                with urllib.request.urlopen(cls.base_url + "/bridges/practice", timeout=0.5):
                    return
            except OSError:
                time.sleep(0.2)

        raise unittest.SkipTest("Bottle server is not available")

    @classmethod
    def make_driver(cls):
        # Браузер всегда открывается видимым окном, чтобы было видно, что делает тест.
        errors = []

        chrome_options = cls.webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1280,900")
        chrome_options.add_argument("--disable-gpu")
        try:
            return cls.webdriver.Chrome(options=chrome_options)
        except Exception as exc:
            errors.append("Chrome: {}".format(exc))

        edge_options = cls.webdriver.EdgeOptions()
        edge_options.add_argument("--window-size=1280,900")
        edge_options.add_argument("--disable-gpu")
        try:
            return cls.webdriver.Edge(options=edge_options)
        except Exception as exc:
            errors.append("Edge: {}".format(exc))

        raise RuntimeError("; ".join(errors))

    # ── helpers ──────────────────────────────────────────────────────────────
    def pause(self, factor=1.0):
        """Пауза между этапами, чтобы было видно глазами, что делает тест.
        Длительность = STEP_PAUSE * factor."""
        if STEP_PAUSE > 0:
            time.sleep(STEP_PAUSE * factor)

    def wait_css(self, selector):
        return self.WebDriverWait(self.driver, 15).until(
            self.EC.presence_of_element_located((self.By.CSS_SELECTOR, selector))
        )

    def wait_until(self, check):
        return self.WebDriverWait(self.driver, 15).until(lambda driver: check(driver))

    def node_count(self):
        return self.driver.execute_script(
            "return document.querySelectorAll('input[name=\"node[]\"]').length;"
        )

    def edge_count(self):
        return self.driver.execute_script(
            "return document.querySelectorAll('input[name=\"edge_weight[]\"]').length;"
        )

    def fill_from_dataset(self, dataset):
        """Заполняет форму данными графа, вызывая JS-функции страницы."""
        self.driver.execute_script(
            """
            var data = arguments[0];
            clearBridgeNodes();
            clearBridgeEdges();
            data.nodes.forEach(function (n) { addBridgeNodeRow(n); });
            updateBridgeSelects();
            data.edges.forEach(function (e) { addBridgeEdgeRow(e[0], e[1], e[2]); });
            updateBridgeSelects();
            """,
            dataset,
        )

    # ── tests ────────────────────────────────────────────────────────────────
    def test_page_has_required_controls(self):
        self.driver.get(self.base_url + "/bridges/practice")
        self.pause()  # дать рассмотреть открывшуюся страницу

        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "form[action='/bridges/practice']"))
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "#bridge-nodes-body"))
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "#bridge-edges-body"))
        self.assertTrue(self.driver.find_elements(self.By.ID, "bridge-generate-btn"))
        self.assertTrue(self.driver.find_elements(self.By.ID, "bridge-gen-count"))
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "button[type='submit']"))

    def test_large_network_from_file_and_analysis(self):
        # Большой набор данных считывается из файла.
        with open(DATA_FILE, encoding="utf-8") as fh:
            dataset = json.load(fh)

        # Этап 1: открываем пустую страницу практики.
        self.driver.get(self.base_url + "/bridges/practice")
        self.pause()

        # Этап 2: заполняем форму городами и дорогами из файла.
        self.fill_from_dataset(dataset)

        # Форма заполнена в полном объёме.
        self.wait_until(lambda d: self.node_count() == len(dataset["nodes"]))
        self.assertEqual(self.node_count(), len(dataset["nodes"]))
        self.assertEqual(self.edge_count(), len(dataset["edges"]))
        self.pause(1.6)  # видно заполненные таблицы городов и дорог

        # Этап 2.5: правим вес одной дороги РУКАМИ (ручной ввод с клавиатуры).
        first_weight = self.driver.find_element(
            self.By.CSS_SELECTOR, "input[name='edge_weight[]']")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", first_weight)
        first_weight.clear()
        first_weight.send_keys("99")
        self.assertEqual(first_weight.get_attribute("value"), "99")
        self.pause(1.6)  # видно введённое вручную значение

        # Этап 3: запуск анализа и ожидание сгенерированной страницы результата.
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait_css("#state0")
        self.pause(1.6)  # видно результат: матрицы, вкладки и граф

        # На странице результата присутствуют сводка, матрицы и вкладки состояний.
        self.assertIn("Результат анализа", self.driver.page_source)
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, ".matrix-table"))

        # Сверяем РЕЗУЛЬТАТ с эталоном алгоритма: сколько мостов должно быть в этом
        # графе (мосты зависят только от структуры, поэтому ручная правка веса не влияет).
        expected_bridges = len(analyze_network(dataset["nodes"], dataset["edges"])["bridges"])

        # Тест читает число «Найдено мостов» прямо со страницы и сверяет с эталоном.
        shown_text = self.driver.find_element(
            self.By.XPATH,
            "//div[contains(@class, 'summary-chip')][contains(., 'Найдено мостов')]//strong"
        ).text
        self.assertEqual(int(shown_text), expected_bridges)

        # Вкладок ровно столько: исходная сеть + по одной на каждый найденный мост.
        tabs = self.driver.find_elements(self.By.CSS_SELECTOR, ".nav-tabs > li")
        self.assertEqual(len(tabs), expected_bridges + 1)

        # Граф исходной сети отрисован библиотекой vis.js.
        self.assertTrue(self.driver.find_elements(self.By.CSS_SELECTOR, "#state0 .state-graph"))
        self.pause()

    def test_random_generation_fills_tables(self):
        self.driver.get(self.base_url + "/bridges/practice")
        self.pause()

        count = self.driver.find_element(self.By.ID, "bridge-gen-count")
        count.clear()
        count.send_keys("7")
        self.pause()  # видно введённое число городов

        self.driver.find_element(self.By.ID, "bridge-generate-btn").click()
        # Генерация идёт запросом к /bridges/generate (сервер, Python).
        self.wait_until(lambda d: self.node_count() == 7)
        self.assertEqual(self.node_count(), 7)
        self.assertGreaterEqual(self.edge_count(), 6)  # связный граф: не менее n-1 рёбер
        self.pause(1.6)  # видно сгенерированные города и дороги


if __name__ == "__main__":
    unittest.main()
