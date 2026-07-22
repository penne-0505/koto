---
title: "QA Test Plan: Docs-driven template v1.0.0 migration"
status: active
draft_status: n/a
qa_status: planned
risk: High
qa_schema: 2
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration/reference.md"
related_issues: []
related_prs: []
---

# QA Test Plan: Docs-driven template v1.0.0 migration

## Source of Intent

- TODO: `Workflow-Chore-17`
- Plan: `_docs/plan/Workflow/docs-template-v1-migration/plan.md`
- Intent: `_docs/intent/Workflow/docs-template-v1-migration/decision.md`

## Quality Goal

Koto 固有 content と application behavior を変えず、reusable v1.0.0 workflow を provenance と path-level evidence が閉じた状態で統合する。

## Acceptance Criteria

- AC-001: B/U/P、isolation、tag resolution、final lock が一致する。
- AC-002: union inventory と migration ledger が final diff を未分類 0 で覆う。
- AC-003: unchanged P docs の compatibility と schema-marker/unknown-warning fixtures が成功する。
- AC-004: reusable paths が統合され template-self lifecycle/meta history が除外される。
- AC-005: CI scope が P + ACMR で、upstream provenance が明示的 `git -C` で検証される。
- AC-006: checkpointed project/WIP content と application behavior に差分がなく、8-path lint ledger は semantic content だけを保持する presentation-only edit である。
- AC-007: migration-specific closure checks と利用可能な Koto checks が成功し、CI-equivalent full markdownlint は 0 issues である。

## Decision Review Scope

- DEC-001: provenance と lock write order。
- DEC-002: pathwise merge、paired distribution、meta-work exclusion、deletion proof。
- DEC-003: project content preservation と no application behavior change。
- DEC-004: compatibility gate と strict schema gate の分離。
- DEC-005: lifecycle hook の軽量 guardrail、安全 block、closure evidence。

## Intent-derived Invariants

- INV-001: final lock の tag/full SHA 組。
- INV-002: project application/WIP paths の P content identity。

## Risk Assessment

- Risk level: High
- Risk rationale: migration、CI、validator、skill、documentation rule を同時に更新する。
- Regression risk: legacy docs rejection、project customization loss、CI scope omission、hook portability、template meta-history contamination。
- Data safety risk: active checkout と project WIP の上書き。隔離 worktree と P hash evidence で防ぐ。
- Security / privacy risk: 新 hook/script は secret を読まず、import 前 review と executable tests を行う。
- UX risk: agent guidance の過剰制約または schema の一括強制。
- Agent misbehavior risk: branch mixing、blind replacement、premature lock、bulk schema edits、実行していない command の verification 記載。

## Test Strategy

- Unit: validator fixtures、hook unit tests。
- Integration: unchanged P snapshot compatibility、unscoped/scoped docs wrapper、hook smoke。
- Manual QA: inventory/deletion/provenance/lock review。
- Validator/static check: markdownlint、Deno fmt/check、paired-skill cmp、JSON parsing。
- Diff review: P-preservation manifest、final diff ledger、forbidden path scan。

## Test Matrix

| ID | Source | Requirement / Optional Invariant | Test Type | Command / File | Expected Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 / INV-001 | TODO / intent | B/U/P と final lock | provenance | `git -C <upstream> rev-parse 'v1.0.0^{commit}'`; JSON assertion | U full SHA と lock が一致 | planned |
| AC-002 | TODO | inventory/ledger closure | diff review | union paths と `git diff --name-only P..HEAD` の照合 | unclassified 0 | planned |
| AC-003 | TODO | compatibility と schema marker/warning | validator | P snapshot に U validators; fixture runner | compatibility PASS、marker fixtures PASS | planned |
| AC-004 | TODO | reusable path integration/meta exclusion | static/diff | paired checks、forbidden meta path scan、deletion proof | expected paths only | planned |
| AC-005 | TODO | P + ACMR CI scope / upstream git -C | static/provenance | workflow inspection; `git -C` resolution | exact env と SHA | planned |
| AC-006 / INV-002 | TODO / intent | project content preservation | hash/diff | P export と final project paths の blob/hash comparison、8-path ledger review | ledger 外の unexpected changes 0; ledger は semantic preservation | planned |
| AC-007 | TODO | closure suite | integration | wrapper、scoped lint、hook/smoke/fixtures、Koto checks、CI-equivalent full lint | migration commands exit 0; full lint 0 issues | planned |
| DEC-001 | intent | premature lock/branch mixing をしない | agent misbehavior | write-order and branch diff review | lock final、parent P、single branch | planned |
| DEC-002 | intent | blind replacement/meta history をしない | agent misbehavior | shared-path 3-way review | customization preserved | planned |
| DEC-004 | intent | bulk schema edit をしない | agent misbehavior | legacy doc diff/schema scan | semantic target 以外は unchanged | planned |
| DEC-005 | intent | hook が軽量 guardrail に留まる | unit/smoke | `deno run --allow-read --allow-run=git scripts/test-agent-workflow-hook.mjs`; smoke | prompt/write/stop boundary と block が PASS | planned |

## Manual QA Checklist

- [ ] B/U/P と cutoff 時刻、worktree、branch ownership を verification に記録する。
- [ ] deletion candidate ごとに exact B=P、project refs、U absent/replaced を確認する。
- [ ] compatibility と strict-schema verdict を別々に記録する。
- [ ] final lock が最後の migration write だったことを diff/write order で確認する。

## Regression Checklist

- [ ] checkpointed TODO tasks の本文が P と同一である。
- [ ] Discord reminder/parser、Lang docs、tooling fixtures に migration 由来差分がない（8-path lint ledger を除く）。
- [ ] runtime/language/compiler/source/tests/build/assets path に差分がない。
- [ ] paired skills が byte-identical である。

## High-risk Checklist

- [x] Rollback/recovery は隔離 branch を採用しない方法で可能。
- [x] Data safety: P snapshot と active checkout を変更しない boundary を確認済み。
- [x] Security / privacy: imported hooks/scripts は secret を読まないことを実行前に review する。
- [x] failure mode は compatibility、strict schema、project regression に分けて報告する。

## Out of Scope

- application behavior change、legacy project docs の一括 schema conversion、remote update。

## Open Questions

- None
