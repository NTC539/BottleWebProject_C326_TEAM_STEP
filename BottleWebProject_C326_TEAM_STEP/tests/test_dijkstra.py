import unittest
import random
from algorithms.dijkstra_utils import (
    parse_edges_from_lists,
    parse_edges_from_text,
    generate_random_graph,
    run_dijkstra_and_prepare_results,
    export_edges_to_string
)


class TestParseEdgesFromLists(unittest.TestCase):
    def test_valid_edges(self):
        edge_count = 3
        from_list = ['A', 'B', 'C']
        to_list = ['B', 'C', 'A']
        weight_list = ['5', 'inf', '10.5']
        edges_raw, edges_display, errors = parse_edges_from_lists(edge_count, from_list, to_list, weight_list)

        self.assertEqual(len(edges_raw), 3)
        self.assertEqual(edges_raw[0], ('A', 'B', 5.0))
        self.assertEqual(edges_raw[1], ('B', 'C', float('inf')))
        self.assertEqual(edges_raw[2], ('C', 'A', 10.5))
        self.assertEqual(edges_display, [('A', 'B', '5'), ('B', 'C', 'inf'), ('C', 'A', '10.5')])
        self.assertEqual(errors, [])

    def test_empty_fields(self):
        edge_count = 2
        from_list = ['A', '']
        to_list = ['B', 'C']
        weight_list = ['5', '']
        edges_raw, edges_display, errors = parse_edges_from_lists(edge_count, from_list, to_list, weight_list)

        self.assertEqual(edges_raw, [('A', 'B', 5.0)])
        self.assertEqual(len(errors), 1)
        self.assertIn('Ребро 2: все поля должны быть заполнены', errors[0])

    def test_invalid_weight(self):
        edge_count = 2
        from_list = ['A', 'B']
        to_list = ['B', 'C']
        weight_list = ['abc', '-5']
        edges_raw, edges_display, errors = parse_edges_from_lists(edge_count, from_list, to_list, weight_list)

        self.assertEqual(edges_raw, [])
        self.assertEqual(len(errors), 2)
        self.assertIn('вес "abc" не является числом', errors[0])
        self.assertIn('вес должен быть > 0, получено -5.0', errors[1])

    def test_vertex_name_too_long(self):
        edge_count = 1
        from_list = ['VeryLongName']
        to_list = ['B']
        weight_list = ['10']
        edges_raw, edges_display, errors = parse_edges_from_lists(edge_count, from_list, to_list, weight_list)

        self.assertEqual(edges_raw, [])
        self.assertEqual(len(errors), 1)
        self.assertIn('название вершины "VeryLongName" не должно превышать 10 символов', errors[0])

    def test_positive_weight(self):
        edge_count = 1
        from_list = ['A']
        to_list = ['B']
        weight_list = ['0.5']
        edges_raw, edges_display, errors = parse_edges_from_lists(edge_count, from_list, to_list, weight_list)

        self.assertEqual(len(edges_raw), 1)
        self.assertEqual(edges_raw[0][2], 0.5)
        self.assertEqual(errors, [])


class TestParseEdgesFromText(unittest.TestCase):
    def test_valid_content(self):
        content = "A,B,5\nB,C,inf\nC,A,10.5"
        edges, count, vertices, errors = parse_edges_from_text(content, max_edges=25)

        self.assertEqual(count, 3)
        self.assertEqual(edges, [('A', 'B', '5'), ('B', 'C', 'inf'), ('C', 'A', '10.5')])
        self.assertEqual(vertices, {'A', 'B', 'C'})
        self.assertEqual(errors, [])

    def test_comma_and_space_mix(self):
        content = "A B 5\nB,C,inf\nC A 10"
        edges, count, vertices, errors = parse_edges_from_text(content)

        self.assertEqual(count, 3)
        self.assertEqual(edges[0], ('A', 'B', '5'))
        self.assertEqual(edges[1], ('B', 'C', 'inf'))
        self.assertEqual(edges[2], ('C', 'A', '10'))
        self.assertEqual(errors, [])
 

    def test_exceed_max_edges(self):
        content = "\n".join([f"A,B,{i}" for i in range(30)])
        edges, count, vertices, errors = parse_edges_from_text(content, max_edges=25)

        self.assertEqual(count, 25)  
        self.assertEqual(len(edges), 25)
        self.assertEqual(len(errors), 1)
        self.assertIn('содержит более 25 рёбер', errors[0])

    def test_long_vertex_name(self):
        content = "VeryLongVertex,B,10"
        edges, count, vertices, errors = parse_edges_from_text(content)

        self.assertEqual(count, 0)
        self.assertEqual(edges, [])
        self.assertEqual(len(errors), 1)
        self.assertIn('название вершины слишком длинное', errors[0])


class TestGenerateRandomGraph(unittest.TestCase):
    def test_default_generation(self):
        for _ in range(10):
            edges, source = generate_random_graph()
            edge_count = len(edges)
            self.assertGreaterEqual(edge_count, 4)
            self.assertLessEqual(edge_count, 9)

            allowed_vertices = {'A', 'B', 'C', 'D', 'E', 'F'}
            for f, t, w in edges:
                self.assertIn(f, allowed_vertices)
                self.assertIn(t, allowed_vertices)
                self.assertNotEqual(f, t) 
                self.assertTrue(w == 'inf' or (w.isdigit() and int(w) > 0))

            all_vertices = {f for f, _, _ in edges} | {t for _, t, _ in edges}
            self.assertIn(source, all_vertices)

    def test_custom_vertex_set(self):
        vertices = ['X', 'Y', 'Z']
        for _ in range(5):
            edges, source = generate_random_graph(vertex_set=vertices, min_edges=2, max_edges=2)
            self.assertEqual(len(edges), 2)
            for f, t, _ in edges:
                self.assertIn(f, vertices)
                self.assertIn(t, vertices)
                self.assertNotEqual(f, t)
            self.assertIn(source, vertices)


class TestRunDijkstraAndPrepareResults(unittest.TestCase):
    def test_successful_run(self):
        # Простой граф без отрицательных весов
        edges_raw = [('A', 'B', 5.0), ('A', 'C', 2.0), ('C', 'B', 1.0)]
        results, graph_edges, errors = run_dijkstra_and_prepare_results(edges_raw, 'A')

        self.assertIsNotNone(results)
        self.assertEqual(results['A']['dist_display'], '0.0')
        self.assertEqual(results['B']['dist_display'], '3.0')   
        self.assertEqual(results['C']['dist_display'], '2.0')
        self.assertEqual(results['B']['path_display'], 'A → C → B')
        self.assertEqual(graph_edges, edges_raw)
        self.assertEqual(errors, [])

    def test_source_not_in_graph(self):
        edges_raw = [('A', 'B', 5.0)]
        results, graph_edges, errors = run_dijkstra_and_prepare_results(edges_raw, 'X')

        self.assertIsNone(results)
        self.assertIsNone(graph_edges)
        self.assertEqual(len(errors), 1)
        self.assertIn('Вершина-источник "X" не найдена', errors[0])

    def test_inf_distance(self):
        # Граф, где B недостижим из A
        edges_raw = [('A', 'C', 2.0), ('D', 'B', 1.0)]
        results, graph_edges, errors = run_dijkstra_and_prepare_results(edges_raw, 'A')

        self.assertIsNotNone(results)
        self.assertEqual(results['A']['dist_display'], '0.0')
        self.assertEqual(results['C']['dist_display'], '2.0')
        self.assertEqual(results['B']['dist_display'], '∞')
        self.assertEqual(results['B']['path_display'], '—')
        self.assertEqual(errors, [])


class TestExportEdgesToString(unittest.TestCase):
    def test_export_valid_edges(self):
        edges_display = [('A', 'B', '5'), ('B', 'C', 'inf'), ('C', 'A', '10')]
        content, ok = export_edges_to_string(edges_display)
        self.assertTrue(ok)
        expected = "A,B,5\nB,C,inf\nC,A,10"
        self.assertEqual(content, expected)

    def test_export_empty_edges(self):
        edges_display = []
        content, ok = export_edges_to_string(edges_display)
        self.assertFalse(ok)
        self.assertEqual(content, "")

    def test_export_with_empty_fields(self):
        edges_display = [('A', '', '5'), ('', 'B', 'inf')]
        content, ok = export_edges_to_string(edges_display)
        self.assertFalse(ok)  # нет полностью заполненных строк
        self.assertEqual(content, "")

        edges_display2 = [('A', 'B', '5'), ('', '', '')]
        content2, ok2 = export_edges_to_string(edges_display2)
        self.assertTrue(ok2)
        self.assertEqual(content2, "A,B,5")


if __name__ == '__main__':
    unittest.main()