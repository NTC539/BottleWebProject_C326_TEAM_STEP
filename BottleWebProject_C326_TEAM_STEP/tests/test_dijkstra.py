"""
tests/test_dijkstra.py — Unit tests for algorithms/dijkstra.py
Run: python -m pytest tests/test_dijkstra.py -v
"""

import math
import unittest
from algorithms.dijkstra import route_network

INF = float('inf')


class TestDirectPath(unittest.TestCase):
    """Test 1 — direct shortest path through intermediate node."""

    def setUp(self):
        self.result = route_network(
            vertices=["A", "B", "C"],
            edges=[("A", "B", 4), ("A", "C", 2), ("C", "B", 1)],
            source="A",
        )

    def test_distances(self):
        d = self.result["distances"]
        self.assertEqual(d["A"], 0)
        self.assertEqual(d["B"], 3)
        self.assertEqual(d["C"], 2)

    def test_path_to_b(self):
        self.assertEqual(self.result["paths"]["B"], ["A", "C", "B"])

    def test_path_to_c(self):
        self.assertEqual(self.result["paths"]["C"], ["A", "C"])

    def test_path_to_source(self):
        self.assertEqual(self.result["paths"]["A"], ["A"])

    def test_no_unreachable(self):
        self.assertEqual(self.result["unreachable"], [])

    def test_no_skipped_edges(self):
        self.assertEqual(self.result["skipped_edges"], [])


class TestInfEdgeForcesDetour(unittest.TestCase):
    """Test 2 — ∞ edge is skipped; detour is found."""

    def setUp(self):
        self.result = route_network(
            vertices=["A", "B", "C", "D"],
            edges=[
                ("A", "B", INF),
                ("A", "C", 3),
                ("C", "B", 2),
                ("B", "D", 1),
            ],
            source="A",
        )

    def test_distance_b(self):
        self.assertEqual(self.result["distances"]["B"], 5)

    def test_path_b(self):
        self.assertEqual(self.result["paths"]["B"], ["A", "C", "B"])

    def test_one_skipped_edge(self):
        self.assertEqual(len(self.result["skipped_edges"]), 1)

    def test_skipped_edge_is_ab(self):
        u, v, w = self.result["skipped_edges"][0]
        self.assertEqual(u, "A")
        self.assertEqual(v, "B")
        self.assertTrue(math.isinf(w))


class TestUnreachableVertices(unittest.TestCase):
    """Test 3 — vertex C has no incoming edges from source side."""

    def setUp(self):
        self.result = route_network(
            vertices=["A", "B", "C"],
            edges=[("A", "B", 1)],
            source="A",
        )

    def test_c_distance_inf(self):
        self.assertTrue(math.isinf(self.result["distances"]["C"]))

    def test_c_in_unreachable(self):
        self.assertIn("C", self.result["unreachable"])

    def test_c_path_empty(self):
        self.assertEqual(self.result["paths"]["C"], [])


class TestAllEdgesInf(unittest.TestCase):
    """Test 4 — every edge has weight ∞; all non-source nodes unreachable."""

    def setUp(self):
        self.result = route_network(
            vertices=["A", "B", "C"],
            edges=[("A", "B", INF), ("A", "C", INF)],
            source="A",
        )

    def test_b_inf(self):
        self.assertTrue(math.isinf(self.result["distances"]["B"]))

    def test_c_inf(self):
        self.assertTrue(math.isinf(self.result["distances"]["C"]))

    def test_two_unreachable(self):
        self.assertEqual(len(self.result["unreachable"]), 2)

    def test_two_skipped(self):
        self.assertEqual(len(self.result["skipped_edges"]), 2)


class TestSingleNodeNoEdges(unittest.TestCase):
    """Test 5 — trivial graph: one vertex, no edges."""

    def setUp(self):
        self.result = route_network(
            vertices=["A"],
            edges=[],
            source="A",
        )

    def test_distance_zero(self):
        self.assertEqual(self.result["distances"], {"A": 0.0})

    def test_no_unreachable(self):
        self.assertEqual(self.result["unreachable"], [])

    def test_path_is_source(self):
        self.assertEqual(self.result["paths"], {"A": ["A"]})


class TestEqualLengthPaths(unittest.TestCase):
    """Test 6 — two paths of equal length; either is acceptable."""

    def setUp(self):
        self.result = route_network(
            vertices=["A", "B", "C", "D"],
            edges=[
                ("A", "B", 2),
                ("A", "C", 2),
                ("B", "D", 3),
                ("C", "D", 3),
            ],
            source="A",
        )

    def test_distance_d(self):
        self.assertEqual(self.result["distances"]["D"], 5)

    def test_path_d_is_valid(self):
        valid = [["A", "B", "D"], ["A", "C", "D"]]
        self.assertIn(self.result["paths"]["D"], valid)


class TestUnknownSourceRaises(unittest.TestCase):
    """Test 7 — source not in vertices → ValueError."""

    def test_raises(self):
        with self.assertRaises(ValueError) as ctx:
            route_network(
                vertices=["A", "B"],
                edges=[],
                source="Z",
            )
        self.assertIn("Z", str(ctx.exception))


class TestNegativeWeightRaises(unittest.TestCase):
    """Test 8 — negative weight → ValueError."""

    def test_negative(self):
        with self.assertRaises(ValueError):
            route_network(
                vertices=["A", "B"],
                edges=[("A", "B", -1)],
                source="A",
            )

    def test_zero(self):
        with self.assertRaises(ValueError):
            route_network(
                vertices=["A", "B"],
                edges=[("A", "B", 0)],
                source="A",
            )

    def test_unknown_vertex_in_edge(self):
        with self.assertRaises(ValueError) as ctx:
            route_network(
                vertices=["A", "B"],
                edges=[("A", "X", 1)],
                source="A",
            )
        self.assertIn("X", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
