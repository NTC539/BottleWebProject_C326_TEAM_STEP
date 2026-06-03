import unittest

from algorithms.coloring import (
    ColoringInputError,
    MAX_SUBJECTS,
    check_input,
    generate_random_data,
    greedy_coloring,
    load_coloring_json,
    make_export_data,
    make_graph,
    sample_coloring_data,
    solve_coloring,
    sort_vertices,
)


def subject(name, teacher="T"):
    return {"name": name, "teacher": teacher}


def valid_coloring(test_case, result):
    colors = result["colors"]
    for left, right in result["conflicts"]:
        test_case.assertNotEqual(colors[left], colors[right])


class ColoringValidationTest(unittest.TestCase):
    def test_empty_rows_are_ignored_and_text_is_trimmed(self):
        subjects, conflicts, teachers = check_input(
            [subject(" A ", " T1 "), subject("", "")],
            [],
        )

        self.assertEqual(subjects, [subject("A", "T1")])
        self.assertEqual(conflicts, [])
        self.assertEqual(teachers, {"A": "T1"})

    def test_rejects_non_dict_subject_row(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input(["A"], [])

        self.assertIn("некорректно", context.exception.errors[0])

    def test_rejects_empty_subject_list(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input([], [])

        self.assertIn("Добавьте хотя бы одну дисциплину", context.exception.errors[0])

    def test_rejects_missing_subject_name(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input([subject("", "T1")], [])

        self.assertIn("не указана дисциплина", context.exception.errors[0])

    def test_rejects_missing_teacher(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input([subject("A", "")], [])

        self.assertIn("не указан преподаватель", context.exception.errors[0])

    def test_rejects_duplicate_subjects_case_insensitive(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input([subject("A"), subject("a")], [])

        self.assertIn("повторно", context.exception.errors[0])

    def test_rejects_too_many_subjects(self):
        subjects = [subject("S{}".format(i)) for i in range(MAX_SUBJECTS + 1)]

        with self.assertRaises(ColoringInputError) as context:
            check_input(subjects, [])

        self.assertIn("не должно превышать", context.exception.errors[0])

    def test_rejects_bad_conflict_format(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input([subject("A")], ["A"])

        self.assertIn("Конфликт №1 задан некорректно", context.exception.errors[0])

    def test_rejects_conflict_with_one_side(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input([subject("A")], [("A", "")])

        self.assertIn("должны быть две дисциплины", context.exception.errors[0])

    def test_rejects_conflict_with_unknown_subject(self):
        with self.assertRaises(ColoringInputError) as context:
            check_input([subject("A")], [("A", "B")])

        self.assertIn("Не найдена дисциплина", context.exception.errors[0])

    def test_ignores_empty_self_and_duplicate_conflicts(self):
        subjects = [subject("A"), subject("B")]

        good_subjects, conflicts, teachers = check_input(
            subjects,
            [("", ""), ("A", "A"), ("A", "B"), ("B", "A")],
        )

        self.assertEqual(good_subjects, subjects)
        self.assertEqual(conflicts, [("A", "B")])
        self.assertEqual(teachers, {"A": "T", "B": "T"})


class ColoringAlgorithmTest(unittest.TestCase):
    def test_graph_is_undirected(self):
        graph = make_graph(["A", "B", "C"], [("A", "B"), ("B", "C")])

        self.assertEqual(graph["A"], {"B"})
        self.assertEqual(graph["B"], {"A", "C"})
        self.assertEqual(graph["C"], {"B"})

    def test_vertices_are_sorted_by_degree_then_name(self):
        graph = make_graph(["B", "A", "C"], [("A", "B"), ("A", "C")])

        self.assertEqual(sort_vertices(["B", "A", "C"], graph), ["A", "B", "C"])

    def test_greedy_coloring_uses_lowest_available_color(self):
        graph = make_graph(["A", "B", "C"], [("A", "B"), ("B", "C")])

        colors = greedy_coloring(["A", "B", "C"], graph)

        self.assertEqual(colors, {"A": 1, "B": 2, "C": 1})

    def test_empty_conflict_graph_uses_one_shift(self):
        result = solve_coloring([subject("A"), subject("B"), subject("C")], [])

        self.assertEqual(result["num_colors"], 1)
        self.assertEqual(set(result["colors"].values()), {1})
        valid_coloring(self, result)

    def test_chain_graph_uses_two_shifts(self):
        result = solve_coloring(
            [subject("A"), subject("B"), subject("C"), subject("D")],
            [("A", "B"), ("B", "C"), ("C", "D")],
        )

        self.assertEqual(result["num_colors"], 2)
        valid_coloring(self, result)

    def test_triangle_graph_uses_three_shifts(self):
        result = solve_coloring(
            [subject("A"), subject("B"), subject("C")],
            [("A", "B"), ("B", "C"), ("A", "C")],
        )

        self.assertEqual(result["num_colors"], 3)
        valid_coloring(self, result)

    def test_complete_graph_uses_one_shift_per_subject(self):
        subjects = [subject("A"), subject("B"), subject("C"), subject("D")]
        conflicts = [
            ("A", "B"), ("A", "C"), ("A", "D"),
            ("B", "C"), ("B", "D"), ("C", "D"),
        ]

        result = solve_coloring(subjects, conflicts)

        self.assertEqual(result["num_colors"], 4)
        valid_coloring(self, result)

    def test_schedule_contains_all_subjects_once(self):
        subjects = [subject("A"), subject("B"), subject("C")]
        result = solve_coloring(subjects, [("A", "B")])

        scheduled = []
        for row in result["schedule"]:
            scheduled.extend(item["name"] for item in row["subjects"])

        self.assertEqual(sorted(scheduled), ["A", "B", "C"])

    def test_teacher_cost_counts_extra_teacher_shifts(self):
        subjects = [
            subject("A", "T1"),
            subject("B", "T1"),
            subject("C", "T2"),
        ]

        result = solve_coloring(subjects, [("A", "B")])

        self.assertEqual(result["teacher_cost"], 1)
        self.assertEqual(result["teacher_shifts"][0]["teacher"], "T1")
        self.assertEqual(result["teacher_shifts"][0]["shifts"], [1, 2])


class ColoringJsonTest(unittest.TestCase):
    def test_load_json_accepts_subjects_and_conflicts(self):
        data = {
            "subjects": [
                {"name": "Математика", "teacher": "Иванов"},
                {"name": "Физика", "teacher": "Петров"},
            ],
            "conflicts": [["Математика", "Физика"]],
        }

        subjects, conflicts = load_coloring_json(data)

        self.assertEqual(len(subjects), 2)
        self.assertEqual(conflicts, [("Математика", "Физика")])

    def test_load_json_ignores_result_field(self):
        data = {
            "subjects": [subject("A"), subject("B")],
            "conflicts": [["A", "B"]],
            "result": {"anything": "old result"},
        }

        subjects, conflicts = load_coloring_json(data)

        self.assertEqual(subjects, [subject("A"), subject("B")])
        self.assertEqual(conflicts, [("A", "B")])

    def test_load_json_rejects_non_object_root(self):
        with self.assertRaises(ColoringInputError) as context:
            load_coloring_json([])

        self.assertIn("JSON должен содержать объект", context.exception.errors[0])

    def test_load_json_rejects_missing_subject_list(self):
        with self.assertRaises(ColoringInputError) as context:
            load_coloring_json({"conflicts": []})

        self.assertIn("список subjects", context.exception.errors[0])

    def test_load_json_rejects_bad_conflict_list(self):
        with self.assertRaises(ColoringInputError) as context:
            load_coloring_json({"subjects": [], "conflicts": {}})

        self.assertIn("conflicts должно быть списком", context.exception.errors[0])

    def test_load_json_rejects_bad_subject_item(self):
        with self.assertRaises(ColoringInputError) as context:
            load_coloring_json({"subjects": ["A"], "conflicts": []})

        self.assertIn("должна быть объектом", context.exception.errors[0])

    def test_load_json_rejects_bad_conflict_item(self):
        with self.assertRaises(ColoringInputError) as context:
            load_coloring_json({"subjects": [subject("A")], "conflicts": ["A"]})

        self.assertIn("должен быть парой дисциплин", context.exception.errors[0])

    def test_export_json_can_be_imported_back(self):
        subjects = [
            subject("Математика", "Иванов"),
            subject("Физика", "Петров"),
            subject("Информатика", "Сидорова"),
        ]
        conflicts = [("Математика", "Физика"), ("Физика", "Информатика")]
        result = solve_coloring(subjects, conflicts)

        exported = make_export_data(result["subjects"], result["conflicts"], result)
        imported_subjects, imported_conflicts = load_coloring_json(exported)

        self.assertIn("result", exported)
        self.assertEqual(exported["result"]["algorithm"], "Welsh-Powell")
        self.assertEqual(imported_subjects, result["subjects"])
        self.assertEqual(imported_conflicts, result["conflicts"])


class ColoringRandomGenerationTest(unittest.TestCase):
    def test_random_generation_with_zero_density_has_no_conflicts(self):
        subjects, conflicts = generate_random_data(5, 0)

        self.assertEqual(len(subjects), 5)
        self.assertEqual(conflicts, [])
        self.assertEqual(subjects[0]["name"], "Дисциплина 1")

    def test_random_generation_with_full_density_has_all_conflicts(self):
        subjects, conflicts = generate_random_data(4, 1)

        self.assertEqual(len(subjects), 4)
        self.assertEqual(len(conflicts), 6)

    def test_random_generation_clamps_subject_count_to_maximum(self):
        subjects, conflicts = generate_random_data(100, 0)

        self.assertEqual(len(subjects), MAX_SUBJECTS)
        self.assertEqual(conflicts, [])

    def test_random_generation_clamps_subject_count_to_minimum(self):
        subjects, conflicts = generate_random_data(0, 1)

        self.assertEqual(len(subjects), 1)
        self.assertEqual(conflicts, [])

    def test_random_generation_clamps_density(self):
        subjects_low, conflicts_low = generate_random_data(4, -1)
        subjects_high, conflicts_high = generate_random_data(4, 2)

        self.assertEqual(len(subjects_low), 4)
        self.assertEqual(conflicts_low, [])
        self.assertEqual(len(subjects_high), 4)
        self.assertEqual(len(conflicts_high), 6)


class ColoringSampleDataTest(unittest.TestCase):
    def test_sample_data_returns_editable_copy(self):
        first_subjects, first_conflicts = sample_coloring_data()
        second_subjects, second_conflicts = sample_coloring_data()

        first_subjects[0]["name"] = "Changed"
        first_conflicts.clear()

        self.assertNotEqual(first_subjects[0]["name"], second_subjects[0]["name"])
        self.assertNotEqual(first_conflicts, second_conflicts)


if __name__ == "__main__":
    unittest.main()
