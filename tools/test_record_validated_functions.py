import copy
import unittest

from tools.record_validated_functions import ValidationError, apply_validations


class RecordValidatedFunctionsTests(unittest.TestCase):
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
                {"name": "FUN_00100000", "address": "0x00100000", "size": 8, "matched_bytes": 0, "complete": False},
                {"name": "FUN_00100008", "address": "0x00100008", "size": 12, "matched_bytes": 3, "complete": False},
                {"name": "FUN_00100014", "address": "0x00100014", "size": 8, "matched_bytes": 8, "complete": True},
            ],
        }
        self.record = {
            "schema": 1,
            "validated_at": "2026-10-14",
            "evidence": {
                "id": "EXEC-519",
                "method": "objdiff-cli exact byte comparison",
            },
            "functions": [
                {"name": "FUN_00100008", "address": "0x00100008", "size": 12},
            ],
        }

    def test_promotes_validated_function_and_attaches_only_evidence_reference(self):
        updated = apply_validations(self.progress, self.record, "b" * 64)

        function = updated["functions"][1]
        self.assertEqual(function["matched_bytes"], 12)
        self.assertTrue(function["complete"])
        self.assertEqual(function["validation_evidence"], {
            "id": "EXEC-519",
            "method": "objdiff-cli exact byte comparison",
            "sha256": "b" * 64,
            "validated_at": "2026-10-14",
        })
        self.assertNotIn("path", function["validation_evidence"])
        self.assertEqual(self.progress["functions"][1]["matched_bytes"], 3)

    def test_accepts_a_dependency_group_as_one_atomic_record(self):
        self.record["functions"] = [
            {"name": "FUN_00100000", "address": "0x00100000", "size": 8},
            {"name": "FUN_00100008", "address": "0x00100008", "size": 12},
        ]

        updated = apply_validations(self.progress, self.record, "b" * 64)

        self.assertEqual([item["matched_bytes"] for item in updated["functions"]], [8, 12, 8])
        self.assertEqual(updated["functions"][0]["validation_evidence"]["id"], "EXEC-519")
        self.assertEqual(updated["functions"][1]["validation_evidence"]["id"], "EXEC-519")

    def test_rejects_unknown_function_without_mutating_input(self):
        original = copy.deepcopy(self.progress)
        self.record["functions"].append(
            {"name": "FUN_00100020", "address": "0x00100020", "size": 8}
        )

        with self.assertRaisesRegex(ValidationError, "not in the audited inventory"):
            apply_validations(self.progress, self.record, "b" * 64)

        self.assertEqual(self.progress, original)

    def test_rejects_size_or_name_mismatch(self):
        self.record["functions"][0]["size"] = 16

        with self.assertRaisesRegex(ValidationError, "does not match the inventory"):
            apply_validations(self.progress, self.record, "b" * 64)

    def test_rejects_invalid_evidence_reference_and_already_complete_function(self):
        with self.assertRaisesRegex(ValidationError, "SHA-256"):
            apply_validations(self.progress, self.record, "not-a-hash")

        self.record["functions"] = [
            {"name": "FUN_00100014", "address": "0x00100014", "size": 8}
        ]
        with self.assertRaisesRegex(ValidationError, "already marked complete"):
            apply_validations(self.progress, self.record, "b" * 64)


if __name__ == "__main__":
    unittest.main()
