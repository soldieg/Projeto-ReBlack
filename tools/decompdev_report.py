#!/usr/bin/env python3
"""Convert the scoped PS2 EE catalog into the objdiff v2 report for decomp.dev."""

import argparse
import json
import re
from datetime import date
from pathlib import Path


SCOPE = (
    "EE/R5900 provisional function catalog only; excludes IOP and VU/DVP; "
    "not global PS2 coverage"
)
NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.$@]*$")
ADDRESS_RE = re.compile(r"^0x[0-9A-Fa-f]{8}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


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
    if progress.get("schema") != 2:
        raise ValueError("unsupported progress schema")
    if progress.get("version") != "SLUS_213.76":
        raise ValueError("this report only supports SLUS_213.76")
    scope = progress.get("scope", "").strip()
    if scope != SCOPE:
        raise ValueError("this report requires the explicit EE/R5900 scope label")
    if progress.get("private_inputs_excluded") is not True:
        raise ValueError("private inputs must be excluded")

    inventory = progress.get("inventory")
    if not isinstance(inventory, dict):
        raise ValueError("inventory metadata is required")
    if inventory.get("source") != "Ghidra EE function dependency queue":
        raise ValueError("inventory must come from the Ghidra EE queue")
    if not SHA256_RE.fullmatch(str(inventory.get("source_sha256", ""))):
        raise ValueError("inventory source hash must be a SHA-256")
    if inventory.get("overlapping_intervals") != 0:
        raise ValueError("overlapping function intervals are not allowed")

    functions_data = progress.get("functions")
    if not isinstance(functions_data, list) or not functions_data:
        raise ValueError("the EE function inventory must not be empty")
    expected_count = inventory.get("function_count")
    expected_bytes = inventory.get("body_bytes")
    if (not isinstance(expected_count, int) or isinstance(expected_count, bool)
            or expected_count != len(functions_data)):
        raise ValueError("function count does not match the inventory")

    addresses = set()
    units = []
    total_code = matched_code = complete_code = 0
    total_functions = matched_functions = complete_units = 0

    for item in functions_data:
        if not isinstance(item, dict):
            raise ValueError("function rows must be objects")
        name = item.get("name")
        address = item.get("address")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            raise ValueError(f"invalid EE function name: {name!r}")
        if not isinstance(address, str) or not ADDRESS_RE.fullmatch(address):
            raise ValueError(f"{name}: address must be an 8-digit hexadecimal address")
        if address.lower() in addresses:
            raise ValueError(f"duplicate function address: {address}")
        addresses.add(address.lower())

        size = item.get("size")
        matched_bytes = item.get("matched_bytes")
        complete = item.get("complete")
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0
               for value in (size, matched_bytes)):
            raise ValueError(f"{name}: sizes and matched bytes must be non-negative integers")
        if size == 0 or matched_bytes > size:
            raise ValueError(f"{name}: invalid body size or matched-byte count")
        if not isinstance(complete, bool):
            raise ValueError(f"{name}: complete must be a boolean")
        if complete and matched_bytes != size:
            raise ValueError(f"{name}: exact match must cover the complete function")
        if not complete and matched_bytes == size:
            raise ValueError(f"{name}: full-byte match must be marked as an exact match")

        evidence = item.get("validation_evidence")
        if evidence is not None:
            if not isinstance(evidence, dict):
                raise ValueError(f"{name}: validation evidence must be an object")
            if not isinstance(evidence.get("id"), str) or not evidence["id"].strip():
                raise ValueError(f"{name}: validation evidence id is required")
            if not isinstance(evidence.get("method"), str) or not evidence["method"].strip():
                raise ValueError(f"{name}: validation evidence method is required")
            if not SHA256_RE.fullmatch(str(evidence.get("sha256", ""))):
                raise ValueError(f"{name}: validation evidence SHA-256 is invalid")
            validated_at = evidence.get("validated_at")
            if not isinstance(validated_at, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", validated_at):
                raise ValueError(f"{name}: validation evidence date is invalid")
            try:
                date.fromisoformat(validated_at)
            except ValueError as exc:
                raise ValueError(f"{name}: validation evidence date is invalid") from exc
            if not complete:
                raise ValueError(f"{name}: validation evidence requires an exact complete match")

        fuzzy_percent = _percentage(matched_bytes, size)
        full_code = size if complete else 0
        full_function = int(complete)
        measures = _measures(
            matched_bytes, size, full_function, 1,
            1, full_function, full_code,
        )
        unit_name = f"EE/{name}@{address}"
        virtual_address = int(address, 16)
        units.append({
            "name": unit_name,
            "measures": measures,
            "sections": [{
                "name": ".text",
                "size": size,
                "fuzzy_match_percent": fuzzy_percent,
            }],
            "functions": [{
                "name": name,
                "size": size,
                "fuzzy_match_percent": fuzzy_percent,
                "address": 0,
                "metadata": {"virtual_address": virtual_address},
            }],
            "metadata": {
                "complete": complete,
                "module_name": "EE",
                "source_path": "docs/decompdev/progress.json",
                "progress_categories": ["ee-r5900-provisional"],
                "auto_generated": True,
            },
        })
        total_code += size
        matched_code += matched_bytes
        complete_code += full_code
        total_functions += 1
        matched_functions += full_function
        complete_units += full_function

    if expected_bytes != total_code:
        raise ValueError("body-byte total does not match the inventory")
    if inventory.get("unique_start_count") != total_functions:
        raise ValueError("unique function-start count does not match the inventory")
    if inventory.get("synthetic_labels_excluded") != 141:
        raise ValueError("the 141 synthetic labels must remain excluded from the EE denominator")

    overall = _measures(
        matched_code, total_code, matched_functions, total_functions,
        len(units), complete_units, complete_code,
    )
    return {
        "version": 2,
        "measures": overall,
        "units": units,
        "categories": [{
            "id": "ee-r5900-provisional",
            "name": "EE/R5900 provisional function catalog only (not global PS2 coverage)",
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
    output.write_text(json.dumps(report, separators=(",", ":")) + "\n", encoding="utf-8")
    measures = report["measures"]
    print(
        f"decompdev-report: exact {measures['matched_functions']}/"
        f"{measures['total_functions']} functions, "
        f"{measures['complete_code']}/{measures['total_code']} exact bytes; "
        f"fuzzy {measures['matched_code']}/{measures['total_code']} bytes; "
        f"scope: {progress['scope']}; wrote {output}"
    )


if __name__ == "__main__":
    main()
