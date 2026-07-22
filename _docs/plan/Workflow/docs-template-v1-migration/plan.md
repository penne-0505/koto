---
title: Docs-driven template v1.0.0 migration plan
status: active
draft_status: n/a
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration/reference.md"
related_issues: []
related_prs: []
---

# Docs-driven template v1.0.0 migration plan

## Overview

Koto が最後に採用した legacy template commit B から release v1.0.0 の U までを、owner-approved project checkpoint P と三方向比較して統合する。互換モードと schema v2 の strict verification を分離し、互換確認後の最後の migration write として provenance lock を作成する。

## Scope

- B `e6dc4331a81af21494208610b22ef2d9ecdce885` から U tag `v1.0.0` / `f71e9ab20466ea2972158334261f5ae2b2265754` までの reusable template delta。
- P `6ad65726c93d729a5a84d29da6e67064c1594214` から作成した `/tmp/docs-template-v1-rollout/koto` の隔離 branch。
- standards、templates、paired skills、hooks、validators、fixtures、docs CI、root guidance の pathwise merge。
- union inventory、migration-created artifact ledger、8-path project-local Markdownlint compatibility ledger、compatibility / strict-schema verification、provenance lock。

## Non-Goals

- Koto の runtime、language、compiler、source、tests、build、assets、VS Code grammar、Lang design docs、Discord reminder/parser WIP の機能変更。8-path ledger に記録した Markdown presentation-only edit は除く。
- upstream template 自身の lifecycle/self-audit および完了済み meta-work history の持ち込み。
- legacy project docs の意味を伴わない一括 schema v2 変換。
- main 更新、push、remote ref 更新。

## Requirements

- **Functional**: final tree が U の reusable workflow contract を備え、P の project content を保持し、`docs-template.lock.json` が正確な U を指す。
- **Non-Functional**: 全 path を inventory と ledger で説明でき、互換性、schema、provenance、削除条件、application behavior 不変性が再検証可能であり、CI-equivalent full Markdownlint は 0 issues である。
- **Isolation**: checkpoint 後の並行変更や別 branch を混入させない。
- **Deletion**: template-only path は exact B=P blob、project reference/changes なし、U absent/replaced の三条件を満たす場合だけ削除する。

## Pre-implementation Audit

- Evidence: B→U は `validate-intent`、schema v2、agent hooks、provenance lock を追加する一方、P には同等 path が存在せず reusable shared paths の大半は B と同一だった。
- Plausible disconfirming explanation: Koto が別 path に同等の validator/hook/provenance 機能を独自実装済みなら upstream import は重複する。P の tracked tree、scripts、CI、root guidance を検索したが同等実装は確認できなかった。
- Non-local effects: docs の validator input、CI scope、agent lifecycle、将来の template update provenance に影響する。Koto application の data flow、runtime、language tooling は呼び出さず、preservation diff の対象にする。
- Durable/compatibility boundary: schema v2 を durable target とし、legacy compatibility は既存 doc の semantic edit 時まで維持する。意味変更のない bulk conversion は行わない。

## Tasks

1. baseline status、B/U tag resolution、P tree、legacy validator 結果を固定する。
2. B→U / B→P union を二軸分類し、一意の resolution と rationale を与える。
3. validator/fixtures を compatibility mode で導入し、P snapshot の unchanged docs を検証する。
4. shared paths を三方向で review し、U の reusable content と P customization を merge する。
5. schema markers、unknown-marker warnings、CI `ACMR` scope、paired skill / hook contracts を検証する。
6. compatibility PASS 後に final lock を作成する。
7. P 由来の 8 Markdown path を局所的に lint 互換化し、semantic preservation と full Markdownlint 0 issues を確認する。
8. verification と final diff ledger を完成し、migration task を TODO から除く。

## QA Plan

- QA document: `_docs/qa/Workflow/docs-template-v1-migration/test-plan.md`
- Risk level: High
- Validator/static: unscoped/scoped docs wrapper、validator fixtures、hook unit/smoke、paired skill comparison、provenance checks。
- Regression: CI-equivalent full markdownlint 0 issues、Koto package test/build discovery と利用可能な command、P content hash/diff preservation（8-path presentation-only ledger を除く）。
- Manual/diff review: inventory closure、template-self exclusions、deletion proof、DEC-001〜DEC-004 conformance。

## Deployment / Rollout

- local single commit のみ。push、main update、remote ref update は行わない。
- rollback は migration branch/worktree を採用しないことで行える。P と active checkout は変更しない。
