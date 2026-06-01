"""
tests/test_bridges.py — Unit tests for algorithms/bridges.py
Run: python -m pytest tests/test_bridges.py -v

Контракт (соответствует блок-схеме и ТЗ 2.2.1–2.2.4):
  • bridges — список мостов (Тарьян);
  • total_path_sum — сумма кратчайших путей ИСХОДНОГО графа (i < j, включая ∞);
  • states[0] — исходный граф (removed=None), далее по одному на каждый мост;
    в каждом состоянии: removed, edges и три матрицы weight / adj / dist.
"""

import unittest
from algorithms.bridges import analyze_network

INF = float('inf')


def _bridge_set(bridges):
    """Convert bridge list to a set of frozensets for order-independent comparison."""
    return {frozenset((u, v)) for u, v, w in bridges}


def _find_state(result, pair):
    """Return the state whose removed bridge connects the two vertices in `pair`."""
    target = frozenset(pair)
    for state in result['states']:
        if state['removed'] is not None and frozenset(state['removed'][:2]) == target:
            return state
    raise AssertionError(f"Нет состояния с удалённым мостом {pair}")


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

    def test_base_sum_pairs_i_lt_j(self):
        # Пары i<j: AB=1, AC=3, AD=6, BC=2, BD=5, CD=3 → 20.
        self.assertEqual(self.result['total_path_sum'], 20.0)

    def test_states_count(self):
        # Исходный граф + по одному на каждый мост.
        self.assertEqual(len(self.result['states']), 4)

    def test_first_state_is_original(self):
        original = self.result['states'][0]
        self.assertIsNone(original['removed'])
        self.assertEqual(len(original['edges']), 3)

    def test_original_dist_matrix(self):
        dist = self.result['states'][0]['dist']
        self.assertEqual(dist['A']['A'], 0.0)
        self.assertEqual(dist['A']['D'], 6.0)   # 1+2+3
        self.assertEqual(dist['B']['D'], 5.0)   # 2+3

    def test_original_adjacency_matrix(self):
        adj = self.result['states'][0]['adj']
        self.assertEqual(adj['A']['B'], 1)
        self.assertEqual(adj['B']['C'], 1)
        self.assertEqual(adj['A']['C'], 0)      # нет прямого ребра
        self.assertEqual(adj['A']['A'], 0)      # диагональ матрицы смежности

    def test_original_weight_matrix(self):
        weight = self.result['states'][0]['weight']
        self.assertEqual(weight['B']['C'], 2.0)
        self.assertEqual(weight['A']['A'], 0.0)
        self.assertEqual(weight['A']['C'], INF)  # нет прямого ребра

    def test_removing_bc_breaks_path(self):
        state = _find_state(self.result, {'B', 'C'})
        # B–C делит {A,B}|{C,D}: A→D становится недостижимым.
        self.assertEqual(state['dist']['A']['D'], INF)
        self.assertEqual(state['adj']['B']['C'], 0)   # ребро удалено
        self.assertEqual(state['adj']['A']['B'], 1)   # остальные на месте
        self.assertEqual(len(state['edges']), 2)

    def test_removing_ab_isolates_a(self):
        state = _find_state(self.result, {'A', 'B'})
        self.assertEqual(state['dist']['A']['B'], INF)
        self.assertEqual(state['dist']['B']['D'], 5.0)  # хвост связен


class TestTriangleNoBridges(unittest.TestCase):
    """Triangle A–B–C: no bridges (each edge part of a cycle)."""

    def setUp(self):
        self.vertices = ['A', 'B', 'C']
        self.edges = [('A', 'B', 1.0), ('B', 'C', 2.0), ('A', 'C', 3.0)]
        self.result = analyze_network(self.vertices, self.edges)

    def test_no_bridges(self):
        self.assertEqual(self.result['bridges'], [])

    def test_only_original_state(self):
        # Мостов нет → только исходный граф.
        self.assertEqual(len(self.result['states']), 1)
        self.assertIsNone(self.result['states'][0]['removed'])

    def test_total_path_sum_finite(self):
        # AB=1, BC=2, AC=min(3, 1+2)=3 → 1+2+3 = 6.
        self.assertEqual(self.result['total_path_sum'], 6.0)

    def test_adjacency_full(self):
        adj = self.result['states'][0]['adj']
        self.assertEqual(adj['A']['B'], 1)
        self.assertEqual(adj['A']['C'], 1)
        self.assertEqual(adj['B']['C'], 1)


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
        self.assertIn(frozenset({'C', 'D'}), _bridge_set(self.result['bridges']))

    def test_two_states(self):
        self.assertEqual(len(self.result['states']), 2)

    def test_base_sum_finite(self):
        # Исходный граф связен → база конечна.
        self.assertNotEqual(self.result['total_path_sum'], INF)

    def test_original_cross_distance(self):
        # A→D = A–C(1) + C–D(5) = 6.
        self.assertEqual(self.result['states'][0]['dist']['A']['D'], 6.0)
        self.assertEqual(self.result['states'][0]['adj']['C']['D'], 1)
        self.assertEqual(self.result['states'][0]['weight']['C']['D'], 5.0)

    def test_removed_bridge_disconnects(self):
        state = _find_state(self.result, {'C', 'D'})
        self.assertEqual(state['dist']['A']['D'], INF)   # сеть распалась
        self.assertEqual(state['adj']['C']['D'], 0)      # мост удалён
        self.assertEqual(state['weight']['C']['D'], INF)
        self.assertEqual(state['dist']['A']['C'], 1.0)   # треугольник 1 цел


class TestSingleVertex(unittest.TestCase):
    """Single vertex, no edges: trivial graph."""

    def setUp(self):
        self.result = analyze_network(['A'], [])

    def test_no_bridges(self):
        self.assertEqual(self.result['bridges'], [])

    def test_only_original_state(self):
        self.assertEqual(len(self.result['states']), 1)

    def test_total_path_sum_zero(self):
        self.assertEqual(self.result['total_path_sum'], 0.0)

    def test_matrices_diagonal(self):
        state = self.result['states'][0]
        self.assertEqual(state['dist']['A']['A'], 0.0)
        self.assertEqual(state['weight']['A']['A'], 0.0)
        self.assertEqual(state['adj']['A']['A'], 0)


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

    def test_three_states(self):
        self.assertEqual(len(self.result['states']), 3)

    def test_base_sum_infinite(self):
        # Исходный граф уже несвязен (A↔C недостижимы) → база = ∞.
        self.assertEqual(self.result['total_path_sum'], INF)

    def test_original_adjacency(self):
        adj = self.result['states'][0]['adj']
        self.assertEqual(adj['A']['B'], 1)
        self.assertEqual(adj['C']['D'], 1)
        self.assertEqual(adj['A']['C'], 0)

    def test_removing_ab_isolates_pair(self):
        state = _find_state(self.result, {'A', 'B'})
        self.assertEqual(state['dist']['A']['B'], INF)
        self.assertEqual(state['dist']['C']['D'], 2.0)   # вторая компонента цела


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
