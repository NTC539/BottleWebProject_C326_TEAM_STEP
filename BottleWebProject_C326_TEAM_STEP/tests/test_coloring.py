import unittest
from algorithms.coloring import color_graph


class TestColorGraph(unittest.TestCase):

    def assert_valid_coloring(self, vertices, edges, result):
        colors = result["colors"]
        # All vertices present
        for v in vertices:
            self.assertIn(v, colors, f"Вершина {v!r} отсутствует в colors")
        # No two adjacent vertices share a color
        for u, v in edges:
            self.assertNotEqual(
                colors[u], colors[v],
                f"Конфликт: вершины {u!r} и {v!r} имеют одинаковый цвет {colors[u]}"
            )
        # num_colors matches actual distinct colors used
        self.assertEqual(
            result["num_colors"],
            len(set(colors.values())),
            "num_colors не совпадает с числом уникальных цветов в colors"
        )

    # ------------------------------------------------------------------
    def test_no_edges(self):
        """Граф без рёбер — все вершины в одной смене."""
        vertices = ["А", "Б", "В"]
        edges = []
        result = color_graph(vertices, edges)
        self.assertEqual(result["num_colors"], 1)
        self.assertEqual(set(result["schedule"][1]), {"А", "Б", "В"})
        self.assert_valid_coloring(vertices, edges, result)

    def test_path_four_vertices(self):
        """Путь A-B-C-D — двудольный граф, достаточно 2 цветов."""
        vertices = ["A", "B", "C", "D"]
        edges = [("A", "B"), ("B", "C"), ("C", "D")]
        result = color_graph(vertices, edges)
        self.assertEqual(result["num_colors"], 2)
        self.assert_valid_coloring(vertices, edges, result)

    def test_triangle_k3(self):
        """Треугольник K3 — нечётный цикл, нужно ровно 3 цвета."""
        vertices = ["A", "B", "C"]
        edges = [("A", "B"), ("B", "C"), ("A", "C")]
        result = color_graph(vertices, edges)
        self.assertEqual(result["num_colors"], 3)
        self.assert_valid_coloring(vertices, edges, result)

    def test_complete_k4(self):
        """Полный граф K4 — нужно ровно 4 цвета."""
        vertices = ["A", "B", "C", "D"]
        edges = [
            ("A", "B"), ("A", "C"), ("A", "D"),
            ("B", "C"), ("B", "D"),
            ("C", "D"),
        ]
        result = color_graph(vertices, edges)
        self.assertEqual(result["num_colors"], 4)
        self.assert_valid_coloring(vertices, edges, result)

    def test_single_vertex(self):
        """Одна вершина без рёбер."""
        vertices = ["Математика"]
        edges = []
        result = color_graph(vertices, edges)
        self.assertEqual(result["num_colors"], 1)
        self.assertEqual(result["colors"], {"Математика": 1})
        self.assert_valid_coloring(vertices, edges, result)

    def test_schedule_example(self):
        """Пример из теории: 5 дисциплин, ожидаем не более 3 смен."""
        vertices = ["М", "Ф", "И", "Ис", "Х"]
        edges = [("М", "Ф"), ("М", "И"), ("Ф", "И"), ("Ф", "Ис"), ("И", "Х")]
        result = color_graph(vertices, edges)
        self.assertLessEqual(result["num_colors"], 3)
        self.assert_valid_coloring(vertices, edges, result)

    def test_even_cycle_c4(self):
        """Чётный цикл C4 — двудольный, достаточно 2 цветов."""
        vertices = ["A", "B", "C", "D"]
        edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
        result = color_graph(vertices, edges)
        self.assertEqual(result["num_colors"], 2)
        self.assert_valid_coloring(vertices, edges, result)

    def test_unknown_vertex_raises(self):
        """Неизвестная вершина в edges вызывает ValueError."""
        with self.assertRaises(ValueError) as ctx:
            color_graph(["A", "B"], [("A", "Z")])
        self.assertIn("Z", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
