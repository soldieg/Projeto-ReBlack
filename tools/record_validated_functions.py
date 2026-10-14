#!/usr/bin/env python3
"""Record exact function validations and submit a metadata-only GitHub PR."""

import argparse
import copy
import hashlib
import json
import re
import secrets
import subprocess
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

from tools.decompdev_report import ADDRESS_RE, NAME_RE, SHA256_RE, build_report


class ValidationError(ValueError):
    """Raised when a validation record does not match the audited catalog."""


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def apply_validations(progress, record, evidence_sha256):
    """Return a copy of progress with an exact, evidence-referenced batch applied."""
    if not isinstance(record, dict) or record.get("schema") != 1:
        raise ValidationError("unsupported validation record schema")
    if not isinstance(evidence_sha256, str) or not SHA256_RE.fullmatch(evidence_sha256):
        raise ValidationError("evidence file must have a SHA-256 reference")

    validated_at = record.get("validated_at")
    if not isinstance(validated_at, str) or not DATE_RE.fullmatch(validated_at):
        raise ValidationError("validated_at must use YYYY-MM-DD")
    try:
        date.fromisoformat(validated_at)
    except ValueError as exc:
        raise ValidationError("validated_at must be a real calendar date") from exc

    evidence = record.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence reference is required")
    evidence_id = evidence.get("id")
    method = evidence.get("method")
    if not isinstance(evidence_id, str) or not evidence_id.strip():
        raise ValidationError("evidence id is required")
    if not isinstance(method, str) or not method.strip():
        raise ValidationError("validation method is required")

    requested = record.get("functions")
    if not isinstance(requested, list) or not requested:
        raise ValidationError("at least one validated function is required")

    updated = copy.deepcopy(progress)
    rows = updated.get("functions")
    if not isinstance(rows, list):
        raise ValidationError("the audited function inventory is missing")
    by_address = {row.get("address", "").lower(): row for row in rows if isinstance(row, dict)}
    seen = set()
    evidence_ref = {
        "id": evidence_id.strip(),
        "method": method.strip(),
        "sha256": evidence_sha256.lower(),
        "validated_at": validated_at,
    }

    for function in requested:
        if not isinstance(function, dict):
            raise ValidationError("function records must be objects")
        name = function.get("name")
        address = function.get("address")
        size = function.get("size")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            raise ValidationError(f"invalid function name: {name!r}")
        if not isinstance(address, str) or not ADDRESS_RE.fullmatch(address):
            raise ValidationError(f"{name}: address must be an 8-digit hexadecimal value")
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            raise ValidationError(f"{name}: size must be a positive integer")
        key = address.lower()
        if key in seen:
            raise ValidationError(f"duplicate function address in validation batch: {address}")
        seen.add(key)

        row = by_address.get(key)
        if row is None:
            raise ValidationError(f"{name}@{address} is not in the audited inventory")
        if row.get("name") != name or row.get("size") != size:
            raise ValidationError(f"{name}@{address} does not match the inventory name and size")
        if row.get("complete") is True:
            raise ValidationError(f"{name}@{address} is already marked complete")

        row["matched_bytes"] = size
        row["complete"] = True
        row["validation_evidence"] = evidence_ref.copy()

    # Reuse the report's checks before any file is written or pushed.
    build_report(updated)
    return updated


def _run_git(repo, *args, capture=False):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        capture_output=capture,
    )
    if result.returncode:
        detail = result.stderr.strip() if capture else ""
        raise RuntimeError(f"git {' '.join(args)} failed" + (f": {detail}" if detail else ""))
    return result.stdout.strip() if capture else ""


def _github_repo(remote_url):
    match = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", remote_url)
    return match.groups() if match else (None, None)


def publish_record(repo, record, evidence_file):
    """Build and push a clean metadata-only branch based on the current origin/main."""
    repo = Path(repo).resolve()
    evidence_file = Path(evidence_file).resolve()
    if not evidence_file.is_file() or evidence_file.stat().st_size == 0:
        raise ValidationError("evidence file is missing or empty")
    evidence_hash = hashlib.sha256(evidence_file.read_bytes()).hexdigest()

    root = Path(_run_git(repo, "rev-parse", "--show-toplevel", capture=True)).resolve()
    remote_url = _run_git(root, "remote", "get-url", "origin", capture=True)
    owner, repository = _github_repo(remote_url)
    if not owner:
        raise RuntimeError("origin must be a GitHub repository")

    branch = "decompdev/validated-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    worktree_path = Path(tempfile.mkdtemp(prefix="ps2-decompdev-")).resolve()
    worktree_created = False
    pushed = False
    try:
        _run_git(root, "fetch", "origin", "main")
        _run_git(root, "worktree", "add", "--quiet", "-b", branch, str(worktree_path), "origin/main")
        worktree_created = True

        progress_path = worktree_path / "docs" / "decompdev" / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        updated = apply_validations(progress, record, evidence_hash)
        progress_path.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        subprocess.run(
            [sys.executable, "-m", "unittest", "tools.test_decompdev_report", "tools.test_record_validated_functions", "-v"],
            cwd=worktree_path,
            check=True,
        )
        report_path = worktree_path / "build" / "report.json"
        subprocess.run(
            [sys.executable, "tools/decompdev_report.py", "--in", str(progress_path), "--out", str(report_path)],
            cwd=worktree_path,
            check=True,
        )
        _run_git(worktree_path, "add", "--", "docs/decompdev/progress.json")
        _run_git(worktree_path, "commit", "-m", f"decompdev: record {len(record['functions'])} validated PS2 function(s)")
        _run_git(worktree_path, "push", "--set-upstream", "origin", branch)
        pushed = True
    finally:
        if worktree_created:
            _run_git(root, "worktree", "remove", "--force", str(worktree_path))
            _run_git(root, "branch", "-D", branch)
        elif worktree_path.exists():
            worktree_path.rmdir()

    if pushed:
        return f"https://github.com/{owner}/{repository}/pulls?q=is%3Apr+is%3Aopen+head%3A{owner}%3A{branch}"
    raise RuntimeError("the validated progress branch was not pushed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", required=True, help="local JSON validation batch; never uploaded")
    parser.add_argument("--evidence-file", required=True, help="local evidence file; only its SHA-256 is recorded")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()

    record = json.loads(Path(args.record).read_text(encoding="utf-8"))
    pull_request_search = publish_record(args.repo, record, args.evidence_file)
    print("Validation metadata pushed. GitHub Actions will open a PR and validate the report.")
    print(f"PR search: {pull_request_search}")
    print("After review and merge, the main workflow publishes the updated decomp.dev report.")


if __name__ == "__main__":
    main()
