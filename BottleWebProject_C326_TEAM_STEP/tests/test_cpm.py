import unittest
from algorithms.cpm import find_critical_path

class TestFindCriticalPath(unittest.TestCase):
    def test_linear_chain(self):
        # Линейная цепочка A→B→C — единственный путь.
        tasks = {"A": 2, "B": 3, "C": 4}
        deps  = [("A", "B"), ("B", "C")]
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 9)
        self.assertEqual(result["critical_paths"], [["A", "B", "C"]])
        self.assertEqual(result["es"], {"A": 0, "B": 2, "C": 5})

        # Ранние сроки
        self.assertEqual(result["es"], {"A": 0, "B": 2, "C": 5})
        self.assertEqual(result["ef"], {"A": 2, "B": 5, "C": 9})

        # Поздние сроки
        self.assertEqual(result["ls"], {"A": 0, "B": 2, "C": 5})
        self.assertEqual(result["lf"], {"A": 2, "B": 5, "C": 9})

        # Резервы (все нулевые — критический путь)
        self.assertEqual(result["total_float"], {"A": 0, "B": 0, "C": 0})

    def test_diamond_two_branches(self):
        # Ромб: A→C→E (длина 9) длиннее A→D→E (6) и B→D→E (5).
        tasks = {"A": 3, "B": 2, "C": 4, "D": 1, "E": 2}
        deps  = [("A", "C"), ("A", "D"), ("B", "D"), ("C", "E"), ("D", "E")]
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 9)
        self.assertEqual(result["critical_paths"], [["A", "C", "E"]])

    def test_single_vertex(self):
        # Одна вершина без зависимостей.
        tasks = {"X": 7}
        result = find_critical_path(tasks, [])

        self.assertEqual(result["duration"], 7)
        self.assertEqual(result["critical_paths"], [["X"]])
        self.assertEqual(result["es"], {"X": 0})

    def test_parallel_equal_paths(self):
        # Два независимых пути одинаковой длины
        tasks = {"A": 5, "B": 5}
        deps  = []   # без зависимостей — каждая задача сама по себе
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 5)
        # Обе задачи критические (обе дают длину проекта)
        self.assertIn(["A"], result["critical_paths"])
        self.assertIn(["B"], result["critical_paths"])
        self.assertEqual(result["critical_tasks"], {"A", "B"})

    def test_merge_equal_paths(self):
        # A→C и B→C имеют одинаковую длину → обе ветки критические
        tasks = {"A": 3, "B": 3, "C": 2}
        deps  = [("A", "C"), ("B", "C")]
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 5)
        self.assertIn(["A", "C"], result["critical_paths"])
        self.assertIn(["B", "C"], result["critical_paths"])
        self.assertEqual(result["critical_tasks"], {"A", "B", "C"})

    def test_cycle_raises_value_error(self):
        # Цикл A→B→C→A должен вызывать ValueError с упоминанием цикла.
        tasks = {"A": 1, "B": 1, "C": 1}
        deps  = [("A", "B"), ("B", "C"), ("C", "A")]
        with self.assertRaises(ValueError) as ctx:
            find_critical_path(tasks, deps)
        self.assertIn("цикл", str(ctx.exception).lower())

    def test_unknown_task_raises_value_error(self):
        # Ссылка на отсутствующую задачу должна вызывать ValueError.
        with self.assertRaises(ValueError) as ctx:
            find_critical_path({"A": 1}, [("A", "Z")])
        self.assertIn("Z", str(ctx.exception))

    def test_independent_start_vertices(self):
        # Три независимые вершины — критическая та, что длиннее всех.
        tasks = {"A": 1, "B": 3, "C": 2}
        result = find_critical_path(tasks, [])

        self.assertEqual(result["duration"], 3)
        self.assertEqual(result["critical_paths"], [["B"]])
        self.assertEqual(result["critical_tasks"], {"B"})      
        self.assertEqual(result["total_float"]["A"], 2)        
        self.assertEqual(result["total_float"]["B"], 0)        
        self.assertEqual(result["total_float"]["C"], 1)      
        
    def test_multiple_end_tasks(self):
        # A→B и A→C — два независимых завершающих пути
        tasks = {"A": 2, "B": 5, "C": 3}
        deps  = [("A", "B"), ("A", "C")]
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 7)           # A(2) + B(5) = 7
        self.assertEqual(result["critical_paths"], [["A", "B"]])
        self.assertEqual(result["critical_tasks"], {"A", "B"})
        self.assertNotIn("C", result["critical_tasks"])
        self.assertEqual(result["total_float"]["C"], 2)

if __name__ == '__main__':
    unittest.main()
