import unittest

from tools.decompdev_report import build_report


class DecompdevReportTests(unittest.TestCase):
    def setUp(self):
        self.progress = {
            "schema": 1,
            "version": "SLUS_213.76",
            "scope": "EE single-function pilot; not global project coverage",
            "units": [
                {
                    "name": "EE/FUN_001ABEB8",
                    "code_bytes": {"matched": 40, "total": 40},
                    "functions": {"matched": 1, "total": 1},
                    "complete": True,
                    "evidence": {
                        "date": "2026-10-14",
                        "symbol": "FUN_001ABEB8",
                        "linked_address": "0x001ABEB8",
                        "comparison": "objdiff-cli 3.8.2",
                        "method": "Both linked windows match the original reference hash.",
                        "reference_window_sha256": "b072a1104192ced915e82243dedc5fc3547bd3e62d6b174ef97254d07d2e9182",
                    },
                }
            ],
            "private_inputs_excluded": True,
        }

    def test_builds_a_scoped_report_from_evidence_counts(self):
        report = build_report(self.progress)

        self.assertEqual(report["version"], 2)
        self.assertEqual(report["measures"]["matched_code"], 40)
        self.assertEqual(report["measures"]["total_code"], 40)
        self.assertEqual(report["measures"]["matched_functions"], 1)
        self.assertEqual(report["measures"]["total_functions"], 1)
        self.assertEqual(report["units"][0]["name"], "EE/FUN_001ABEB8")
        function = report["units"][0]["functions"][0]
        self.assertEqual(function["name"], "FUN_001ABEB8")
        self.assertEqual(function["size"], 40)
        self.assertEqual(function["fuzzy_match_percent"], 100.0)
        self.assertEqual(function["metadata"]["virtual_address"], 0x001ABEB8)
        self.assertEqual(
            set(report["units"][0]["metadata"]),
            {
                "complete",
                "module_name",
                "source_path",
                "progress_categories",
                "auto_generated",
            },
        )
        self.assertIn("not global", self.progress["scope"])
        self.assertIn("reference_window_sha256", self.progress["units"][0]["evidence"])
        self.assertEqual(report["categories"][0]["id"], "ee-pilot")

    def test_incomplete_unit_does_not_count_as_complete_code(self):
        self.progress["units"][0]["complete"] = False
        report = build_report(self.progress)

        self.assertEqual(report["measures"]["matched_code"], 40)
        self.assertEqual(report["measures"]["complete_code"], 0)
        self.assertEqual(report["measures"]["complete_code_percent"], 0.0)

    def test_rejects_a_different_game_version(self):
        self.progress["version"] = "OTHER_VERSION"

        with self.assertRaisesRegex(ValueError, "only supports SLUS_213.76"):
            build_report(self.progress)

    def test_rejects_duplicate_or_out_of_scope_units(self):
        self.progress["units"].append(dict(self.progress["units"][0]))
        with self.assertRaisesRegex(ValueError, "exactly one unit"):
            build_report(self.progress)

        self.progress["units"] = [self.progress["units"][0]]
        self.progress["units"][0]["name"] = "IOP/FUN_001ABEB8"
        with self.assertRaisesRegex(ValueError, "only supports EE/FUN_001ABEB8"):
            build_report(self.progress)

    def test_rejects_counts_that_exceed_their_denominator(self):
        self.progress["units"][0]["code_bytes"]["matched"] = 41

        with self.assertRaisesRegex(ValueError, "matched code exceeds total"):
            build_report(self.progress)

    def test_rejects_an_unlabeled_scope(self):
        self.progress["scope"] = ""

        with self.assertRaisesRegex(ValueError, "scope label"):
            build_report(self.progress)

    def test_requires_auditable_evidence_and_private_inputs_excluded(self):
        del self.progress["units"][0]["evidence"]

        with self.assertRaisesRegex(ValueError, "evidence is required"):
            build_report(self.progress)

        self.setUp()
        self.progress["private_inputs_excluded"] = False
        with self.assertRaisesRegex(ValueError, "private inputs must be excluded"):
            build_report(self.progress)


if __name__ == "__main__":
    unittest.main()
