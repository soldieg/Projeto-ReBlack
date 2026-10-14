# decomp.dev Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a clearly scoped, reproducible objdiff pilot from `soldieg/Projeto-ReBlack` to the native decomp.dev dashboard, without presenting it as global game coverage.

**Architecture:** Use objdiff's report as the sole progress data source. Generate the report in GitHub Actions and publish the artifact in the format decomp.dev expects; remove the old VU1 assembly map from the README and explain the pilot boundary in the repository docs. Task 2 can proceed even if no eligible pair exists. Creating a progress report and workflow is gated on finding a provenance-verified target/base object pair and confirming a safe way to make those inputs available to the workflow; if either is unavailable, stop before reporting.

**Tech Stack:** GitHub Actions, `objdiff.json`, `objdiff-cli`, decomp.dev native dashboard, Markdown.

**Spec:** `docs/superpowers/specs/2026-10-14-decompdev-pilot-design.md`

## Global Constraints

- Use only a pilot set with provenance and verifiable target/base object pairs.
- Keep units with no reconstruction source or valid comparison unbased; do not mark them complete.
- Do not publish a global percentage until the complete unit inventory and denominator are defined.
- Do not combine EE, IOP, and VU totals without an explicit unit and coverage rule.
- Keep the repository private during preparation and validation.
- Do not install the decomp.dev GitHub App, grant account-wide access, or change repository visibility as part of this plan.
- Do not commit ISO files, extracted game files, memory dumps, or derived pseudocode.

## Review Focus

- Missing target/base files: the report generation must fail clearly or leave the unit unbased; verify with an intentionally absent base path in the pilot config.
- Mismatched game version or object provenance: reject the candidate pair before adding it to the pilot; verify the manifest fields and recorded source evidence.
- Empty or incomplete pilot inventory: documentation must not show a numeric global percentage; verify the initial and no-go states.
- Workflow artifact naming or path mismatch: verify the artifact name is `SLUS_213.76_report` and contains `build/report.json` in the location consumed by decomp.dev.
- Private repository permissions: ensure workflow permissions are limited to required read/artifact operations and do not grant access to other repositories; verify the workflow manifest and app selection are scoped before any external setup.

---

### Task 1: Verify one eligible pilot comparison unit

**Files:**
- Read: local research artifacts under `F:\REBLACK\PS2` and repo evidence docs `EVIDENCIAS.md`, `STATUS.md`, `DECOMPDEV.md`
- Modify: `DECOMPDEV.md` to record the verified candidate or explicit no-go result

**Interfaces:**
- Produces: a written pilot candidate record containing game/build identity, target-object path and hash, reconstructed-source identity, base-object path and hash, toolchain/build command, and evidence that both objects are comparable.

- [ ] **Step 1: Inventory candidate target/base pairs** using the existing research artifacts and provenance records; do not create new binaries or infer pairs from Ghidra address lists, screenshots, or disassembly-only files.
- [ ] **Step 2: Verify candidate identities and hashes** against the documented game version and reconstruction source; record the exact evidence paths.
- [ ] **Step 3: Gate the pilot**: select one defensible pair and establish a safe, reproducible way for the workflow runner to access its inputs, or record which prerequisite is missing. Task 2 proceeds either way; Tasks 3–5 proceed only if both conditions are met.
- [ ] **Step 4: Review the record** for matching architecture, version, unit boundaries, a reproducible base build command, and confirmation that target/base binaries will not be uploaded as GitHub artifacts.

**Expected result:** one auditable pilot unit with workflow input-access method, or an explicit no-go with the missing prerequisites. No progress number is created in this task.

### Task 2: Remove the obsolete file map and document pilot status

**Files:**
- Modify: `README.md`
- Modify: `DECOMPDEV.md`
- Delete: `MAPA-PROGRESSO.svg`

**Interfaces:**
- Consumes: confirmed candidate record or no-go result from Task 1.
- Produces: README language that distinguishes the pilot from global coverage and documentation of the verified state.

- [ ] **Step 1: Update README map section** to remove the VU1 treemap image and its “Mapa de arquivos” description; retain VU1 counts only under the technical status section as dismantling evidence.
- [ ] **Step 2: Add an honest dashboard status**: before registration, state that the pilot is being prepared (or blocked by missing verified pairs) and that global coverage has no percentage; after successful registration, include the verified decomp.dev project link.
- [ ] **Step 3: Update `DECOMPDEV.md`** with the candidate evidence or no-go reason, explicit pilot scope, and current integration state.
- [ ] **Step 4: Check the documentation** with `git diff --check` and search README for the old SVG reference and any claim that VU1 dismantling equals decompilation progress.
- [ ] **Step 5: Commit** as `docs: replace VU1 map with decompilation pilot status`.

### Task 3: Configure and validate the objdiff pilot report

**Files:**
- Create: `objdiff.json`
- Create: `build/report.json` as a generated local output (do not commit unless the repository convention requires it)
- Modify: `DECOMPDEV.md`

**Interfaces:**
- Consumes: Task 1's candidate record.
- Produces: an objdiff v2 configuration with a single scoped comparison unit and a generated `build/report.json`.

- [ ] **Step 1: Define the pilot unit** in `objdiff.json` with exact target and base object paths, game/version metadata, and the matching unit identifier from Task 1.
- [ ] **Step 2: Keep non-reconstructed units unbased**; do not add synthetic or placeholder objects to inflate the report denominator.
- [ ] **Step 3: Generate the report** with `objdiff-cli report generate` using the repository root config.
- [ ] **Step 4: Validate the report**: check that it parses as the expected report schema, names only the pilot scope, and that the known matching/non-matching state agrees with an independent objdiff comparison.
- [ ] **Step 5: Record the exact objdiff-cli version, command, report scope, and validation evidence** in `DECOMPDEV.md`.
- [ ] **Step 6: Commit** as `build: add scoped objdiff pilot report` only if the generated configuration is reproducible and no game-derived binaries are staged.

### Task 4: Publish the report from GitHub Actions

**Files:**
- Create: `.github/workflows/decompdev-report.yml`
- Modify: `DECOMPDEV.md`

**Interfaces:**
- Consumes: `objdiff.json`, pilot objects, and `objdiff-cli` version/configuration from Task 3.
- Produces: a successful default-branch workflow run with artifact named `SLUS_213.76_report` containing `build/report.json`.

- [ ] **Step 1: Add a workflow** triggered on pushes to the default branch and manual dispatch; pin third-party actions to reviewed versions/SHAs and install the same objdiff-cli version recorded in Task 3.
- [ ] **Step 2: Set least-privilege workflow permissions** needed to check out code and upload an artifact; do not add write access to issues or pull requests.
- [ ] **Step 3: Generate the report** using the checked-in config and upload it under the decomp.dev artifact naming convention `SLUS_213.76_report`.
- [ ] **Step 4: Validate workflow syntax and artifact contents** with a real default-branch run; verify it contains the report file at the expected path and does not expose private game-derived files.
- [ ] **Step 5: Record the run URL, artifact name, and report hash** in `DECOMPDEV.md`.
- [ ] **Step 6: Commit** as `ci: publish objdiff pilot report artifact`.

### Task 5: Register and verify the native decomp.dev dashboard

**Files:**
- Modify: `DECOMPDEV.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: successful default-branch report artifact from Task 4.
- Produces: verified native dashboard URL and recorded synchronization evidence.

- [ ] **Step 1: Confirm decomp.dev can discover the report artifact** on the default branch and that the project form accepts the repository.
- [ ] **Step 2: If private-repository app installation is required, stop before installation** and request a separate explicit approval that names `soldieg/Projeto-ReBlack` and the displayed permissions; select only that repository.
- [ ] **Step 3: Register the project** only after its report appears in the service and the project metadata clearly labels the limited pilot scope.
- [ ] **Step 4: Verify the dashboard** against the uploaded report, including the number/scope of units and the displayed matching status; record date and evidence link.
- [ ] **Step 5: Add the verified decomp.dev dashboard link** to README and update `DECOMPDEV.md` to synced only after the dashboard is actually visible.
- [ ] **Step 6: Commit** as `docs: link verified decomp.dev pilot dashboard`.

## Handoff boundary

After Task 5, review the pilot results and remaining prerequisites for global coverage. Repository visibility is a separate decision and is not included in this plan.


