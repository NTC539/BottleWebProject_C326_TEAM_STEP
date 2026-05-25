import unittest
from algorithms.cpm import find_critical_path


class TestFindCriticalPath(unittest.TestCase):

    def test_linear_chain(self):
        """Линейная цепочка A→B→C — единственный путь."""
        tasks = {"A": 2, "B": 3, "C": 4}
        deps  = [("A", "B"), ("B", "C")]
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 9)
        self.assertEqual(result["critical_path"], ["A", "B", "C"])
        self.assertEqual(result["es"], {"A": 0, "B": 2, "C": 5})

    def test_diamond_two_branches(self):
        """Ромб: A→C→E (длина 9) длиннее A→D→E (6) и B→D→E (5)."""
        tasks = {"A": 3, "B": 2, "C": 4, "D": 1, "E": 2}
        deps  = [("A", "C"), ("A", "D"), ("B", "D"), ("C", "E"), ("D", "E")]
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 9)
        self.assertEqual(result["critical_path"], ["A", "C", "E"])

    def test_single_vertex(self):
        """Одна вершина без зависимостей."""
        tasks = {"X": 7}
        result = find_critical_path(tasks, [])

        self.assertEqual(result["duration"], 7)
        self.assertEqual(result["critical_path"], ["X"])
        self.assertEqual(result["es"], {"X": 0})

    def test_parallel_equal_paths(self):
        """S→A→F и S→B→F одинаковой длины — любой путь длиной 3 допустим."""
        tasks = {"S": 0, "A": 5, "B": 5, "F": 0}
        deps  = [("S", "A"), ("S", "B"), ("A", "F"), ("B", "F")]
        result = find_critical_path(tasks, deps)

        self.assertEqual(result["duration"], 5)
        self.assertEqual(len(result["critical_path"]), 3)
        path = result["critical_path"]
        self.assertEqual(path[0], "S")
        self.assertEqual(path[-1], "F")
        self.assertIn(path[1], ("A", "B"))

    def test_cycle_raises_value_error(self):
        """Цикл A→B→C→A должен вызывать ValueError с упоминанием цикла."""
        tasks = {"A": 1, "B": 1, "C": 1}
        deps  = [("A", "B"), ("B", "C"), ("C", "A")]
        with self.assertRaises(ValueError) as ctx:
            find_critical_path(tasks, deps)
        self.assertIn("цикл", str(ctx.exception).lower())

    def test_unknown_task_raises_value_error(self):
        """Ссылка на отсутствующую задачу должна вызывать ValueError."""
        with self.assertRaises(ValueError) as ctx:
            find_critical_path({"A": 1}, [("A", "Z")])
        self.assertIn("Z", str(ctx.exception))

    def test_independent_start_vertices(self):
        """Три независимые вершины — критическая та, что длиннее всех."""
        tasks = {"A": 1, "B": 3, "C": 2}
        result = find_critical_path(tasks, [])

        self.assertEqual(result["duration"], 3)
        self.assertEqual(result["critical_path"], ["B"])


if __name__ == "__main__":
    unittest.main()
