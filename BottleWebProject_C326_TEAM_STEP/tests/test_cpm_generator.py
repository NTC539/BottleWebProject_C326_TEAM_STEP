import unittest
from algorithms.cpm_generator import generate_random_cpm
from algorithms.cpm import find_critical_path

class TestGenerateRandomCPM(unittest.TestCase):
    def test_result_structure(self):
        # Результат — словарь с ключами 'tasks' и 'deps' правильного формата
        data = generate_random_cpm()
        self.assertIn("tasks", data)
        self.assertIn("deps", data)
        for task in data["tasks"]:
            self.assertIn("name", task)
            self.assertIn("dur", task)
            self.assertIsInstance(task["dur"], int)
        for dep in data["deps"]:
            self.assertEqual(len(dep), 2)

    def test_task_count_in_range(self):
        # Число задач в пределах [min_tasks, max_tasks]
        data = generate_random_cpm(min_tasks=5, max_tasks=8)
        self.assertGreaterEqual(len(data["tasks"]), 5)
        self.assertLessEqual(len(data["tasks"]), 8)

    def test_names_unique_and_alphabetic(self):
        # Имена — уникальные буквы от A
        data = generate_random_cpm(min_tasks=3, max_tasks=3)
        names = [t["name"] for t in data["tasks"]]
        self.assertEqual(names, ["A", "B", "C"])

    def test_durations_in_range(self):
        # Длительности в [min_dur, max_dur] и положительные
        data = generate_random_cpm(min_dur=3, max_dur=10)
        for task in data["tasks"]:
            self.assertGreaterEqual(task["dur"], 3)
            self.assertLessEqual(task["dur"], 10)

    def test_deps_are_valid(self):
        # Зависимости ссылаются на существующие задачи, без дубликатов и петель
        for _ in range(10):
            data = generate_random_cpm()
            names = {t["name"] for t in data["tasks"]}
            seen = set()
            for u, v in data["deps"]:
                self.assertIn(u, names)
                self.assertIn(v, names)
                self.assertNotEqual(u, v, f"Петля: {u}→{v}")
                self.assertNotIn((u, v), seen, f"Дубликат: {u}→{v}")
                seen.add((u, v))

    def test_graph_is_acyclic(self):
        # Сгенерированный граф не содержит циклов
        for _ in range(10):
            data = generate_random_cpm()
            tasks_dict = {t["name"]: t["dur"] for t in data["tasks"]}
            deps_tuples = [(d[0], d[1]) for d in data["deps"]]
            try:
                find_critical_path(tasks_dict, deps_tuples)
            except ValueError as e:
                if "цикл" in str(e).lower():
                    self.fail("Генератор создал граф с циклом")

    def test_respects_max_in_degree(self):
        # Число входящих рёбер не превышает max_in_degree
        for _ in range(10):
            data = generate_random_cpm(max_in_degree=2)
            in_deg = {t["name"]: 0 for t in data["tasks"]}
            for u, v in data["deps"]:
                in_deg[v] += 1
            for deg in in_deg.values():
                self.assertLessEqual(deg, 2)

    def test_at_least_one_start_task(self):
        # Всегда есть хотя бы одна задача без предшественников
        for _ in range(10):
            data = generate_random_cpm()
            names = {t["name"] for t in data["tasks"]}
            has_pred = {v for _, v in data["deps"]}
            self.assertGreater(len(names - has_pred), 0)

    def test_multiple_start_tasks_possible(self):
        # При start_prob > 0 могут появиться несколько стартовых задач
        found = False
        for _ in range(30):
            data = generate_random_cpm(start_prob=0.5, min_tasks=5, max_tasks=8)
            names = {t["name"] for t in data["tasks"]}
            has_pred = {v for _, v in data["deps"]}
            if len(names - has_pred) > 1:
                found = True
                break
        self.assertTrue(found, "Не появилось несколько стартовых задач")

    def test_density_controls_edge_count(self):
        # Число рёбер примерно равно n * density
        data = generate_random_cpm(min_tasks=10, max_tasks=10,
                                   density=1.5, start_prob=0.0)
        n = len(data["tasks"])
        expected = int(n * 1.5)
        self.assertAlmostEqual(len(data["deps"]), expected, delta=max(3, n * 0.3))

    def test_produces_valid_cpm_input(self):
        # Выход генератора принимается функцией find_critical_path
        for _ in range(5):
            data = generate_random_cpm()
            tasks_dict = {t["name"]: t["dur"] for t in data["tasks"]}
            deps_tuples = [(d[0], d[1]) for d in data["deps"]]
            result = find_critical_path(tasks_dict, deps_tuples)
            self.assertIn("critical_paths", result)

    def test_raises_on_too_many_tasks(self):
        # Более 26 задач — ValueError
        with self.assertRaises(ValueError):
            generate_random_cpm(min_tasks=27, max_tasks=30)


if __name__ == '__main__':
    unittest.main()
