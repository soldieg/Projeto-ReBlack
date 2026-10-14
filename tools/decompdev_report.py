#!/usr/bin/env python3
"""Convert audited progress counts into the objdiff v2 report read by decomp.dev."""

import argparse
import json
import re
from pathlib import Path


def _percentage(matched, total):
    return round(100.0 * matched / total, 4) if total else 0.0


def _measures(code_matched, code_total, functions_matched, functions_total,
              units_total=0, units_complete=0, complete_code=0):
    return {
        "fuzzy_match_percent": _percentage(code_matched, code_total),
        "total_code": code_total,
        "matched_code": code_matched,
        "matched_code_percent": _percentage(code_matched, code_total),
        "total_data": 0,
        "matched_data": 0,
        "matched_data_percent": 0.0,
        "total_functions": functions_total,
        "matched_functions": functions_matched,
        "matched_functions_percent": _percentage(functions_matched, functions_total),
        "complete_code": complete_code,
        "complete_code_percent": _percentage(complete_code, code_total),
        "complete_data": 0,
        "complete_data_percent": 0.0,
        "total_units": units_total,
        "complete_units": units_complete,
    }


def build_report(progress):
    if progress.get("schema") != 1:
        raise ValueError("unsupported progress schema")
    if progress.get("version") != "SLUS_213.76":
        raise ValueError("this pilot only supports SLUS_213.76")
    scope = progress.get("scope", "").strip()
    if scope != "EE single-function pilot; not global project coverage":
        raise ValueError("this pilot requires its exact single-function scope label")
    if progress.get("private_inputs_excluded") is not True:
        raise ValueError("private inputs must be excluded")
    units_data = progress.get("units")
    if not isinstance(units_data, list) or len(units_data) != 1:
        raise ValueError("this pilot requires exactly one unit")

    units = []
    all_code_matched = all_code_total = 0
    all_functions_matched = all_functions_total = 0
    complete_units = 0
    for item in units_data:
        name = item.get("name")
        if name != "EE/FUN_001ABEB8":
            raise ValueError("this pilot only supports EE/FUN_001ABEB8")
        code = item.get("code_bytes", {})
        functions = item.get("functions", {})
        if not name:
            raise ValueError("each unit needs a name")
        evidence = item.get("evidence")
        if not isinstance(evidence, dict):
            raise ValueError(f"{name}: evidence is required")
        for field in ("date", "comparison", "method", "reference_window_sha256"):
            if not isinstance(evidence.get(field), str) or not evidence[field].strip():
                raise ValueError(f"{name}: evidence {field} is required")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", evidence["reference_window_sha256"]):
            raise ValueError(f"{name}: evidence reference hash must be a SHA-256")
        values = (
            code.get("matched"), code.get("total"),
            functions.get("matched"), functions.get("total"),
        )
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0
               for value in values):
            raise ValueError(f"{name}: counts must be non-negative integers")
        code_matched, code_total, functions_matched, functions_total = values
        if code_matched > code_total:
            raise ValueError(f"{name}: matched code exceeds total")
        if functions_matched > functions_total:
            raise ValueError(f"{name}: matched functions exceeds total")
        if code_total == 0 or functions_total == 0:
            raise ValueError(f"{name}: total code and functions must be non-zero")

        complete = item.get("complete", False)
        if not isinstance(complete, bool):
            raise ValueError(f"{name}: complete must be a boolean")
        if complete and (code_matched != code_total or functions_matched != functions_total):
            raise ValueError(f"{name}: complete unit has unmatched code or functions")
        complete_units += int(complete)
        if code_total != 40 or functions_total != 1:
            raise ValueError(f"{name}: pilot requires one 40-byte function")
        if evidence.get("symbol") != "FUN_001ABEB8":
            raise ValueError(f"{name}: evidence symbol must be FUN_001ABEB8")
        try:
            virtual_address = int(evidence["linked_address"], 16)
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"{name}: evidence linked_address must be hexadecimal") from None
        measures = _measures(
            code_matched, code_total, functions_matched, functions_total,
            1, int(complete), code_total if complete else 0,
        )
        units.append({
            "name": name,
            "measures": measures,
            "sections": [{
                "name": ".text",
                "size": code_total,
                "fuzzy_match_percent": _percentage(code_matched, code_total),
            }],
            "functions": [{
                "name": evidence["symbol"],
                "size": code_total,
                "fuzzy_match_percent": _percentage(code_matched, code_total),
                "address": 0,
                "metadata": {"virtual_address": virtual_address},
            }],
            "metadata": {
                "complete": complete,
                "module_name": name.split("/", 1)[0],
                "source_path": "docs/decompdev/progress.json",
                "progress_categories": ["ee-pilot"],
                "auto_generated": False,
            },
        })
        all_code_matched += code_matched
        all_code_total += code_total
        all_functions_matched += functions_matched
        all_functions_total += functions_total
    if len(units) != 1 or len(units[0]["functions"]) != all_functions_total:
        raise ValueError("function rows must match the audited function count")

    overall = _measures(
        all_code_matched, all_code_total,
        all_functions_matched, all_functions_total,
        len(units), complete_units, sum(
            unit["measures"]["complete_code"] for unit in units
        ),
    )
    return {
        "version": 2,
        "measures": overall,
        "units": units,
        "categories": [{
            "id": "ee-pilot",
            "name": "EE single-function pilot (not global coverage)",
            "measures": overall.copy(),
        }],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="input_path", default="docs/decompdev/progress.json")
    parser.add_argument("--out", default="build/report.json")
    args = parser.parse_args()
    progress = json.loads(Path(args.input_path).read_text(encoding="utf-8"))
    report = build_report(progress)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    measures = report["measures"]
    print(
        f"decompdev-report: {measures['matched_functions']}/{measures['total_functions']} "
        f"functions; {measures['matched_code']}/{measures['total_code']} code bytes; "
        f"scope: {progress['scope']}; wrote {output}"
    )


if __name__ == "__main__":
    main()
