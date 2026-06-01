"""
tests/test_bridges.py — Unit tests for algorithms/bridges.py
Run: python -m pytest tests/test_bridges.py -v

Контракт (Вариант A, соответствует блок-схеме и ТЗ 2.2.1–2.2.4):
  • суммы база/новая_сумма берутся по парам i < j и включают ∞;
  • удаление любого моста разрывает граф → delta = float('inf');
  • delta_rel = delta / база (тоже ∞ при разрыве).
"""

import unittest
from algorithms.bridges import analyze_network

INF = float('inf')


def _bridge_set(bridges):
    """Convert bridge list to a set of frozensets for order-independent comparison."""
    return {frozenset((u, v)) for u, v, w in bridges}


class TestPathAllBridges(unittest.TestCase):
    """Path graph A–B–C–D: every edge is a bridge."""

    def setUp(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [('A', 'B', 1.0), ('B', 'C', 2.0), ('C', 'D', 3.0)]
        self.result = analyze_network(self.vertices, self.edges)

    def test_bridge_count(self):
        self.assertEqual(len(self.result['bridges']), 3)

    def test_all_edges_are_bridges(self):
        expected = {frozenset({'A', 'B'}), frozenset({'B', 'C'}), frozenset({'C', 'D'})}
        self.assertEqual(_bridge_set(self.result['bridges']), expected)

    def test_all_deltas_infinite(self):
        # Удаление любого моста разрывает путь → delta = ∞.
        for item in self.result['bridge_impact']:
            self.assertEqual(item['delta'], INF,
                             f"Expected delta=inf for bridge {item['edge']}")

    def test_all_deltas_rel_infinite(self):
        for item in self.result['bridge_impact']:
            self.assertEqual(item['delta_rel'], INF)

    def test_impact_count_matches_bridges(self):
        self.assertEqual(len(self.result['bridge_impact']), 3)

    def test_base_sum_pairs_i_lt_j(self):
        # Пары i<j: AB=1, AC=3, AD=6, BC=2, BD=5, CD=3 → 20.
        self.assertEqual(self.result['total_path_sum'], 20.0)


class TestTriangleNoBridges(unittest.TestCase):
    """Triangle A–B–C: no bridges (each edge part of a cycle)."""

    def setUp(self):
        self.vertices = ['A', 'B', 'C']
        self.edges = [('A', 'B', 1.0), ('B', 'C', 2.0), ('A', 'C', 3.0)]
        self.result = analyze_network(self.vertices, self.edges)

    def test_no_bridges(self):
        self.assertEqual(self.result['bridges'], [])

    def test_bridge_impact_empty(self):
        self.assertEqual(self.result['bridge_impact'], [])

    def test_total_path_sum_finite(self):
        s = self.result['total_path_sum']
        self.assertNotEqual(s, INF)
        self.assertGreater(s, 0.0)


class TestTwoTrianglesOneBridge(unittest.TestCase):
    """
    Two triangles connected by a bridge:
    A–B:2, B–C:3, A–C:1  (triangle 1)
    D–E:4, D–F:2, E–F:3  (triangle 2)
    C–D:5                 (the only bridge)
    """

    def setUp(self):
        self.vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        self.edges = [
            ('A', 'B', 2.0), ('B', 'C', 3.0), ('A', 'C', 1.0),
            ('D', 'E', 4.0), ('D', 'F', 2.0), ('E', 'F', 3.0),
            ('C', 'D', 5.0),
        ]
        self.result = analyze_network(self.vertices, self.edges)

    def test_exactly_one_bridge(self):
        self.assertEqual(len(self.result['bridges']), 1)

    def test_correct_bridge(self):
        bs = _bridge_set(self.result['bridges'])
        self.assertIn(frozenset({'C', 'D'}), bs)

    def test_bridge_delta_infinite(self):
        # Removing C–D splits the graph → delta = ∞.
        self.assertEqual(self.result['bridge_impact'][0]['delta'], INF)

    def test_base_sum_finite(self):
        # Исходный граф связен → база конечна.
        self.assertNotEqual(self.result['total_path_sum'], INF)


class TestBridgeIsolatesLeaf(unittest.TestCase):
    """
    Star graph: A connected only to B, B also connected in a triangle B–C–D.
    Edge A–B is a bridge (removing it isolates A).
    """

    def setUp(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [
            ('A', 'B', 2.0),
            ('B', 'C', 1.0), ('C', 'D', 1.0), ('B', 'D', 1.0),
        ]
        self.result = analyze_network(self.vertices, self.edges)

    def test_one_bridge(self):
        self.assertEqual(len(self.result['bridges']), 1)

    def test_bridge_is_ab(self):
        bs = _bridge_set(self.result['bridges'])
        self.assertIn(frozenset({'A', 'B'}), bs)

    def test_delta_infinite_leaf_isolated(self):
        self.assertEqual(self.result['bridge_impact'][0]['delta'], INF)


class TestSingleVertex(unittest.TestCase):
    """Single vertex, no edges: trivial graph."""

    def setUp(self):
        self.result = analyze_network(['A'], [])

    def test_no_bridges(self):
        self.assertEqual(self.result['bridges'], [])

    def test_total_path_sum_zero(self):
        self.assertEqual(self.result['total_path_sum'], 0.0)

    def test_all_pairs_diagonal_zero(self):
        self.assertEqual(self.result['all_pairs']['A']['A'], 0.0)


class TestTwoDisconnectedComponents(unittest.TestCase):
    """
    Two separate edges (both bridges by definition):
    A–B:1  and  C–D:2  — no connection between the two pairs.
    """

    def setUp(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [('A', 'B', 1.0), ('C', 'D', 2.0)]
        self.result = analyze_network(self.vertices, self.edges)

    def test_two_bridges(self):
        self.assertEqual(len(self.result['bridges']), 2)

    def test_both_bridges_present(self):
        bs = _bridge_set(self.result['bridges'])
        self.assertIn(frozenset({'A', 'B'}), bs)
        self.assertIn(frozenset({'C', 'D'}), bs)

    def test_base_sum_infinite(self):
        # Исходный граф уже несвязен (A↔C недостижимы) → база = ∞.
        self.assertEqual(self.result['total_path_sum'], INF)

    def test_both_deltas_infinite(self):
        for item in self.result['bridge_impact']:
            self.assertEqual(item['delta'], INF)


class TestUnknownVertexRaises(unittest.TestCase):
    """Edge referencing a vertex not in the vertex list → ValueError."""

    def test_unknown_source(self):
        with self.assertRaises(ValueError) as ctx:
            analyze_network(['A', 'B'], [('Z', 'A', 1.0)])
        self.assertIn('Z', str(ctx.exception))

    def test_unknown_target(self):
        with self.assertRaises(ValueError) as ctx:
            analyze_network(['A', 'B'], [('A', 'Z', 1.0)])
        self.assertIn('Z', str(ctx.exception))


class TestInvalidWeightRaises(unittest.TestCase):
    """Edge with weight ≤ 0 → ValueError."""

    def test_zero_weight(self):
        with self.assertRaises(ValueError):
            analyze_network(['A', 'B'], [('A', 'B', 0)])

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            analyze_network(['A', 'B'], [('A', 'B', -1)])


if __name__ == '__main__':
    unittest.main()
