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

Legacy B、release U、clean checkpoint P の三方向 migration を隔離 worktree で実施した。compatibility gate と strict schema gate を分離し、Koto project content を保持したまま reusable v1 workflow を統合した。v1 CI の full Markdownlint に対しては、8-path ledger の presentation-only 互換化を追加し、0 issues で閉じた。

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
npx --yes markdownlint-cli2 "_docs/**/*.md" "_evals/**/*.md" "README.md" "AGENTS.md" "TODO.md" "QUICKSTART.md" "!_docs/archives/**/*" "!_docs/standards/templates/**/*" --config .markdownlint.jsonc
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
| current `./scripts/check-docs.sh` | PASS | format, validators, fixtures, hook unit/smoke, paired contract checks |
| scoped validators | PASS | 13 changed/new docs in pre-verification run |
| validator fixtures | PASS | schema marker acceptance, unknown warning, ACMR, invalid-value checks included |
| hook unit/smoke | PASS | prompt/write/stop boundaries, destructive/sensitive blocks, paired client configs |
| paired skill comparison | PASS | 9 `.agents` / `.claude` skill pairs byte-identical |
| CI-equivalent full markdownlint | PASS | non-archive scope: 72 files, 0 issues; P inherited 92 issues / 8 paths を 8-path ledger で解消 |
| changed-path markdownlint | PASS | 58 changed/new Markdown files, 0 issues before verification creation |
| JSON parse | PASS | hook configs, lock example, VS Code package/config/grammar parsed |
| `npm pack --dry-run --json` | PASS | `vscode-koto@0.1.0`, 10 package files |
| inventory resolution check | PASS | apply 57, merge 15, keep 36, remove 18, defer 4; total 130; six migration-created artifacts + eight lint compatibility records cover final P diff with unclassified 0 |
| P preservation hashes | PASS | 36 project-only paths identical to P; ledger 8 paths are reviewed as semantic-preserving presentation-only differences |
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
| Koto behavior boundary | PASS | runtime/application/WIP/task IDs/tooling semantics unchanged; only the ledger's eight Markdown presentation edits differ from P |

## Acceptance Criteria Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| AC-001 | PASS | inventory provenance, isolated branch, `git -C` tag resolution, final lock tuple |
| AC-002 | PASS | 130-path union inventory plus six migration artifacts and eight project-local lint records; closure has zero unclassified paths |
| AC-003 | PASS | unchanged P compatibility and schema-marker/unknown-warning fixture |
| AC-004 | PASS | reusable paths integrated; obsolete/self-history deletion/exclusion evidence |
| AC-005 | PASS | CI uses P `6ad657...` plus `ACMR`; upstream source/tag checked in explicit repository |
| AC-006 | PASS | 36 hashes, protected-path diff, application-path scan, and 8-path semantic-preservation ledger review |
| AC-007 | PASS | migration-specific suite and package dry-run PASS; CI-equivalent full lint 0 issues |

## Decision Conformance

| ID | Result | Why the implementation remains aligned |
| --- | --- | --- |
| DEC-001 | PASS | exact immutable B/U/P and isolated P-parent branch were used; lock was reserved for final write |
| DEC-002 | PASS | reusable contract was pathwise reconciled; template-self records were removed/excluded with evidence |
| DEC-003 | PASS | project application, Lang WIP, TODO tasks, and tooling semantics remain unchanged; only the documented 8-path Markdown presentation compatibility edits differ |
| DEC-004 | PASS | unchanged-P compatibility and live schema-v2 strict checks have separate evidence |
| DEC-005 | PASS | hook remains a tested guardrail; it does not mutate docs or authorize scope expansion |

## Invariant Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| INV-001 | PASS | prospective lock tuple check matched immutable U; final lock is the last write and receives a read-only closure check |
| INV-002 | PASS | 36 project-only hashes and protected-path scans matched P; 8-path ledger review confirms semantic preservation |

## Deferred / Not Covered

| ID | Reason | Follow-up |
| --- | --- | --- |
| Existing full-lint findings | None | CI-equivalent full Markdownlint is 0 issues after the 8-path compatibility ledger |
| Automated grammar test | `tools/vscode-koto/package.json` defines no test/build scripts; README explicitly defers grammar-test tooling | None for this migration; package dry-run is the available automated package gate |

## Residual Risks

None

## Follow-up TODOs

None
