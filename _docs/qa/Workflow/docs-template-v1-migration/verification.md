---
title: "QA Verification: Docs-driven template v1.0.0 migration"
status: active
draft_status: n/a
qa_status: verified
risk: High
qa_schema: 2
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration/reference.md"
related_issues: []
related_prs: []
---

# QA Verification: Docs-driven template v1.0.0 migration

## Summary

Legacy B、release U、clean checkpoint P の三方向 migration を隔離 worktree で実施した。compatibility gate と strict schema gate を分離し、Koto project content を保持したまま reusable v1 workflow を統合した。v1 CI の full Markdownlint に対しては、migration 中に 8-path ledger の presentation-only 互換化を追加した。migration checkpoint `f0f19606cd5061cb3c2c87572da71585cd0a253f` では、Koto grammar decision のインラインコード中の全角スペースに由来する MD038 が残存しており、これは migration 実装後に判明した既存負債だった。2026-07-22 の post-push baseline CI closure で表記だけを `Unicode U+3000` に置き換え、9 件目の project-local compatibility record として ledger に加えた。CI-equivalent full lint が 72 files / 0 issues であることを実測した。

## Verification Verdict

Verdict: PASS

### Compatibility migration

Verdict: PASS

- U validators を unchanged P export に対して実行し、frontmatter、TODO、links、legacy intent、legacy QA がすべて exit 0 だった。
- B→U / B→P union 130 path は apply 57、merge 15、keep 36、remove 18、defer/exclude 4 に一意分類され、未解決 path はない。
- template-only 11 records は exact B=P blob、U absent、project guidance refs なしを確認して除外した。P ですでに absent の 7 paths は absent のまま保持した。

### Strict schema migration

Verdict: PASS

- migration-created Intent/QA は `intent_schema: 2` / `qa_schema: 2` と必須 sections を持ち、strict validators を通過した。
- generic frontmatter は正しい schema marker を unknown warning にせず、真に未知の marker は warning しつつ exit 0 とする fixture が PASS した。
- 意味変更しない legacy project docs は U の明示的 compatibility horizon に従って一括変換していない。

## Commands Run

```bash
# Legacy baseline
bash scripts/check-docs.sh

# U validators against unchanged P export
deno run --allow-read --allow-env --allow-run=git "$WT/scripts/validate-frontmatter.mjs"
deno run --allow-read "$WT/scripts/validate-todo.mjs"
deno run --allow-read --allow-env --allow-run=git "$WT/scripts/validate-doc-links.mjs"
deno run --allow-read --allow-env --allow-run=git "$WT/scripts/validate-intent.mjs"
deno run --allow-read --allow-env --allow-run=git "$WT/scripts/validate-qa.mjs"

# Current unscoped/scoped workflow
./scripts/check-docs.sh
DD_SCOPE_PATHS="$SCOPE_PATHS" deno run --allow-read --allow-env --allow-run=git scripts/validate-frontmatter.mjs
DD_SCOPE_PATHS="$SCOPE_PATHS" deno run --allow-read --allow-env --allow-run=git scripts/validate-doc-links.mjs
DD_SCOPE_PATHS="$SCOPE_PATHS" deno run --allow-read --allow-env --allow-run=git scripts/validate-intent.mjs
DD_SCOPE_PATHS="$SCOPE_PATHS" deno run --allow-read --allow-env --allow-run=git scripts/validate-qa.mjs

# Full and changed-path markdownlint
npx --yes markdownlint-cli2@0.13.0 "_docs/**/*.md" "_evals/**/*.md" "README.md" "AGENTS.md" "TODO.md" "QUICKSTART.md" "!_docs/archives/**/*" "!_docs/standards/templates/**/*" --config .markdownlint.jsonc
npx --yes markdownlint-cli2 "${CHANGED_MD[@]}" --config .markdownlint.jsonc

# Project and provenance checks
npm pack --dry-run --json
git -C /home/penne/dev/tools/templates/docs_driven_dev_template rev-parse 'v1.0.0^{commit}'
git -C /home/penne/dev/tools/templates/docs_driven_dev_template remote get-url origin
```

## Automated Test Results

| Command / Test | Result | Notes |
| --- | --- | --- |
| legacy `scripts/check-docs.sh` | PASS | P baseline: 6 docs and legacy fixtures passed |
| U validators on unchanged P | PASS | compatibility regression 0 |
| current `./scripts/check-docs.sh` | PASS | 2026-07-22: format, validators, fixtures, hook unit/smoke, paired contract checks |
| scoped docs wrapper and validators | PASS | 2026-07-22: CI と同じ `DD_SCOPE_BASE=6ad65726c93d729a5a84d29da6e67064c1594214` / `DD_SCOPE_DIFF_FILTER=ACMR` の wrapper、および remediation 対象 2 docs の明示 scope validator が exit 0 |
| validator fixtures | PASS | schema marker acceptance, unknown warning, ACMR, invalid-value checks included |
| hook unit/smoke | PASS | prompt/write/stop boundaries, destructive/sensitive blocks, paired client configs |
| paired skill comparison | PASS | 9 `.agents` / `.claude` skill pairs byte-identical |
| CI-equivalent full markdownlint | PASS | 2026-07-22: markdownlint-cli2 0.13.0、non-archive scope 72 files / 0 issues。f0 checkpoint で残った grammar decision の MD038 を semantic-preserving な Unicode 表記へ置換して解消 |
| changed-path markdownlint | PASS | 58 changed/new Markdown files, 0 issues before verification creation |
| JSON parse | PASS | hook configs, lock example, VS Code package/config/grammar parsed |
| `npm pack --dry-run --json` | PASS | `vscode-koto@0.1.0`, 10 package files |
| inventory resolution check | PASS | apply 57, merge 15, keep 36, remove 18, defer 4; total 130; six migration-created artifacts + nine lint compatibility records cover final P diff with unclassified 0 (first 8 migration edits, ninth post-push baseline CI closure) |
| P preservation hashes | PASS | 36 project-only paths identical to P; ledger 9 paths are reviewed as semantic-preserving presentation-only differences (first 8 migration edits, ninth post-push baseline CI closure) |
| application-path diff scan | PASS | runtime/language/compiler/source/src/tests/build/assets changes 0 |
| prospective lock and upstream `git -C` | PASS | source/tag/full SHA tuple matched exact U |

## Manual QA Results

| Checklist Item | Result | Notes |
| --- | --- | --- |
| branch/isolation | PASS | parent is P; active checkout/main/remote refs untouched |
| shared-path three-way review | PASS | TODO and two customized standards merged; other reusable paths applied or explicitly adapted |
| deletion authorization | PASS | 11 migration deletions satisfy all three owner conditions; already-absent paths unchanged |
| template-self exclusion | PASS | lifecycle-self-audit plan/intent/QA not imported; hook anchors retargeted to DEC-005 |
| schema staging | PASS | compatibility completed before strict live-doc checks and final lock write |
| Koto behavior boundary | PASS | runtime/application/WIP/task IDs/tooling semantics unchanged; only the ledger's nine Markdown presentation edits differ from P (first 8 migration edits, ninth post-push baseline CI closure) |

## Acceptance Criteria Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| AC-001 | PASS | inventory provenance, isolated branch, `git -C` tag resolution, final lock tuple |
| AC-002 | PASS | 130-path union inventory plus six migration artifacts and nine project-local lint records; closure has zero unclassified paths (first 8 migration edits, ninth post-push baseline CI closure) |
| AC-003 | PASS | unchanged P compatibility and schema-marker/unknown-warning fixture |
| AC-004 | PASS | reusable paths integrated; obsolete/self-history deletion/exclusion evidence |
| AC-005 | PASS | CI uses P `6ad657...` plus `ACMR`; upstream source/tag checked in explicit repository |
| AC-006 | PASS | 36 hashes, protected-path diff, application-path scan, and 9-path semantic-preservation ledger review (first 8 migration edits, ninth post-push baseline CI closure) |
| AC-007 | PASS | migration-specific suite and package dry-run PASS; CI-equivalent full lint 0 issues |

## Decision Conformance

| ID | Result | Why the implementation remains aligned |
| --- | --- | --- |
| DEC-001 | PASS | exact immutable B/U/P and isolated P-parent branch were used; lock was reserved for final write |
| DEC-002 | PASS | reusable contract was pathwise reconciled; template-self records were removed/excluded with evidence |
| DEC-003 | PASS | project application, Lang WIP, TODO tasks, and tooling semantics remain unchanged; only the documented 9-path Markdown presentation compatibility edits differ (first 8 migration edits, ninth post-push baseline CI closure) |
| DEC-004 | PASS | unchanged-P compatibility and live schema-v2 strict checks have separate evidence |
| DEC-005 | PASS | hook remains a tested guardrail; it does not mutate docs or authorize scope expansion |

## Invariant Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| INV-001 | PASS | prospective lock tuple check matched immutable U; final lock is the last write and receives a read-only closure check |
| INV-002 | PASS | 36 project-only hashes and protected-path scans matched P; 9-path ledger review confirms semantic preservation (first 8 migration edits, ninth post-push baseline CI closure) |

## Deferred / Not Covered

| ID | Reason | Follow-up |
| --- | --- | --- |
| f0 checkpoint の full-lint finding | Resolved | run 29891076422 で `_docs/intent/Tooling/vscode-koto-grammar/decision.md:28` の MD038 が残っていた。migration 実装後に判明した既存負債であり、2026-07-22 の remediation commit で文書表記のみを修正した。 |
| Automated grammar test | `tools/vscode-koto/package.json` defines no test/build scripts; README explicitly defers grammar-test tooling | None for this migration; package dry-run is the available automated package gate |

## Residual Risks

None

## Follow-up TODOs

None
