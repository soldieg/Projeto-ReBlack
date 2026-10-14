import unittest

from tools.decompdev_report import build_report


class DecompdevReportTests(unittest.TestCase):
    def setUp(self):
        self.progress = {
            "schema": 2,
            "version": "SLUS_213.76",
            "scope": "EE/R5900 provisional function catalog only; excludes IOP and VU/DVP; not global PS2 coverage",
            "private_inputs_excluded": True,
            "inventory": {
                "source": "Ghidra EE function dependency queue",
                "source_sha256": "a" * 64,
                "function_count": 3,
                "body_bytes": 28,
                "unique_start_count": 3,
                "overlapping_intervals": 0,
                "synthetic_labels_excluded": 141,
            },
            "functions": [
                {"name": "FUN_00100000", "address": "0x00100000", "size": 8, "matched_bytes": 8, "complete": True},
                {"name": "FUN_00100008", "address": "0x00100008", "size": 12, "matched_bytes": 3, "complete": False},
                {"name": "FUN_00100014", "address": "0x00100014", "size": 8, "matched_bytes": 0, "complete": False},
            ],
        }

    def test_builds_an_ee_scoped_report_with_exact_and_partial_matches(self):
        report = build_report(self.progress)

        self.assertEqual(report["version"], 2)
        measures = report["measures"]
        self.assertEqual(measures["total_functions"], 3)
        self.assertEqual(measures["matched_functions"], 1)
        self.assertEqual(measures["total_code"], 28)
        self.assertEqual(measures["matched_code"], 11)
        self.assertEqual(measures["complete_code"], 8)
        self.assertEqual(measures["complete_units"], 1)
        self.assertEqual(measures["fuzzy_match_percent"], 39.2857)
        self.assertEqual(measures["complete_code_percent"], 28.5714)
        self.assertEqual(len(report["units"]), 3)
        self.assertEqual(report["units"][0]["name"], "EE/FUN_00100000@0x00100000")
        self.assertEqual(report["units"][1]["functions"][0]["fuzzy_match_percent"], 25.0)
        self.assertEqual(report["categories"][0]["id"], "ee-r5900-provisional")
        self.assertIn("not global", report["categories"][0]["name"])

    def test_rejects_duplicate_function_addresses(self):
        duplicate = dict(self.progress["functions"][0], name="FUN_00100018")
        self.progress["functions"].append(duplicate)
        self.progress["inventory"]["function_count"] = 4
        self.progress["inventory"]["body_bytes"] = 36

        with self.assertRaisesRegex(ValueError, "duplicate function address"):
            build_report(self.progress)

    def test_rejects_inconsistent_inventory_totals(self):
        self.progress["inventory"]["body_bytes"] = 27

        with self.assertRaisesRegex(ValueError, "body-byte total"):
            build_report(self.progress)

    def test_rejects_an_unmarked_non_exact_match(self):
        self.progress["functions"][1]["matched_bytes"] = 12

        with self.assertRaisesRegex(ValueError, "exact match"):
            build_report(self.progress)

    def test_rejects_global_or_other_platform_scope(self):
        self.progress["scope"] = "PS2 global coverage"

        with self.assertRaisesRegex(ValueError, "EE/R5900 scope"):
            build_report(self.progress)

    def test_requires_private_inputs_to_be_excluded(self):
        self.progress["private_inputs_excluded"] = False

        with self.assertRaisesRegex(ValueError, "private inputs must be excluded"):
            build_report(self.progress)


if __name__ == "__main__":
    unittest.main()
