import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:5555/dijkstra/practice"  

def read_edges_from_file(filename):
    """Читает рёбра из файла, возвращает список кортежей (from, to, weight)."""
    edges = []
    with open("data/"+ filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) >= 3:
                from_v = parts[0].strip()
                to_v = parts[1].strip()
                weight = parts[2].strip()
                edges.append((from_v, to_v, weight))
    return edges

class DijkstraSeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Edge()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # Дадим небольшую задержку перед закрытием, чтобы можно было увидеть финальное состояние
        time.sleep(2)
        cls.driver.quit()

    def take_screenshot(self, name):
        """Делает скриншот при ошибке."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot_{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Скриншот сохранён: {filename}")

    def go_to_table(self, edge_count):
        """Переход на страницу практики, ввод количества рёбер, переход к таблице."""
        self.driver.get(BASE_URL)
        # Ждём поле ввода количества рёбер
        edge_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "edge_count"))
        )
        edge_input.clear()
        edge_input.send_keys(str(edge_count))
        # Нажимаем "Далее"
        next_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Далее')]")
        next_btn.click()
        # Ждём появления таблицы
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
        )

    def fill_table(self, edges):
        """Заполняет таблицу рёбер из списка кортежей (from, to, weight)."""
        for i, (from_v, to_v, weight) in enumerate(edges):
            from_input = self.driver.find_element(By.NAME, f"from_{i}")
            to_input = self.driver.find_element(By.NAME, f"to_{i}")
            weight_input = self.driver.find_element(By.NAME, f"weight_{i}")
            from_input.clear()
            from_input.send_keys(from_v)
            to_input.clear()
            to_input.send_keys(to_v)
            weight_input.clear()
            weight_input.send_keys(weight)

    def test_large_graph(self):
        """Тест 1: большой граф (25 рёбер) – проверка успешного расчёта."""
        print("\n=== Тест 1: Большой граф (25 рёбер) ===")
        edges = read_edges_from_file("data_valid_large.txt")
        self.assertEqual(len(edges), 25, "Файл должен содержать ровно 25 рёбер")

        self.go_to_table(25)
        self.fill_table(edges)

        # Указать источник (первая вершина первого ребра)
        source = edges[0][0]
        source_input = self.driver.find_element(By.ID, "source")
        source_input.clear()
        source_input.send_keys(source)

        # Нажать "Рассчитать"
        calc_btn = self.driver.find_element(By.XPATH, "//button[@value='calculate']")
        calc_btn.click()

        # Ожидаем появления таблицы результатов
        try:
            result_table = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result-table"))
            )
            rows = result_table.find_elements(By.TAG_NAME, "tr")
            self.assertGreater(len(rows), 1, "Таблица результатов пуста")
            print("✅ Расчёт выполнен, таблица результатов отобразилась")
            # Задержка для визуального контроля результата
            print("⏳ Пауза 5 секунд для просмотра результатов...")
            time.sleep(5)
        except Exception as e:
            self.take_screenshot("large_graph_fail")
            self.fail(f"Не удалось получить результаты: {e}")

    def test_validation(self):
        """Тест 2: валидация некорректных данных."""
        print("\n=== Тест 2: Валидация ошибок ===")
        edges = read_edges_from_file("data_invalid.txt")
        edges = edges[:5]

        self.go_to_table(len(edges))
        self.fill_table(edges)

        # Источник
        source_input = self.driver.find_element(By.ID, "source")
        source_input.clear()
        source_input.send_keys("A")

        # Нажать "Рассчитать"
        calc_btn = self.driver.find_element(By.XPATH, "//button[@value='calculate']")
        calc_btn.click()

        # Ожидаем появления блока ошибок
        try:
            error_block = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-block"))
            )
            error_text = error_block.text
            expected_errors = [
                "вес должен быть > 0",
                "все поля должны быть заполнены",
                "не является числом или \"inf\""
            ]
            for expected in expected_errors:
                self.assertIn(expected.lower(), error_text.lower(),
                              f"Не найдено сообщение: {expected}")
            print("✅ Все ожидаемые ошибки присутствуют")
            # Задержка для визуального просмотра блока ошибок
            print("⏳ Пауза 5 секунд для просмотра сообщений об ошибках...")
            time.sleep(5)
        except Exception as e:
            self.take_screenshot("validation_fail")
            self.fail(f"Блок ошибок не появился или сообщения неверны: {e}")

if __name__ == "__main__":
    unittest.main()