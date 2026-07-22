---
title: Docs-driven template v1.0.0 migration decisions
status: active
draft_status: n/a
intent_schema: 2
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
  - "_docs/reference/Workflow/docs-template-v1-migration/reference.md"
related_issues: []
related_prs: []
---

# Docs-driven template v1.0.0 migration decisions

## Context

Koto は release lock 導入前の template commit B を基礎に project 固有文書と WIP を追加している。U の reusable workflow を wholesale replacement すると project customization を失い、逆に U の meta-work history まで持ち込むと downstream guidance と誤読される。

## Decisions

### DEC-001: B/U/P を固定した三方向 migration とする

- **What**: legacy B、immutable tag と full SHA の U、clean owner checkpoint P を別々の provenance として記録し、P から隔離 branch を作る。lock は compatibility PASS 後の最後の migration write とする。
- **Why**: moving tip、active checkout、post-cutoff work を混同せず、統合した upstream revision と project snapshot を再現できるようにするため。
- **Change freedom**: 同じ B/U/P tree と path classification を再現できる限り、inventory の生成・表示形式や検証 command の編成は変更できる。
- **Why not**: U の branch tip や Koto main の現在値をその場で比較すると、後から同じ migration input を再構成できない。

### DEC-002: reusable contract は pathwise merge し template-self history は除外する

- **What**: standards、templates、paired skills、hooks、validators、fixtures、CI、root guidance を path ごとに classify/merge する。lifecycle-self-audit と upstream 完了済み meta-work records は取り込まない。
- **Why**: downstream で運用に必要な規約と executable checks は採用しつつ、upstream 自身の履歴を Koto の active project guidance にしないため。
- **Change freedom**: reusable content の配置や表現は paired checks と downstream workflow が保たれる範囲で変更できる。

### DEC-003: P の project content と application behavior を不変にする

- **What**: TODO の既存 task、Lang/discord-bot-reminder/parser、runtime/language/compiler/source/tests/build/assets/project docs を保持する。full Markdownlint を導入する互換性補正は、reference の 8-path ledger に限り、Koto の tab、global task ID、設計上の文字列を保持する presentation-only edit として許容する。
- **Why**: template workflow 更新を Koto の設計・実装作業と混ぜず、checkpointed WIP の意味と再開可能性を保ちつつ、CI が検証する Markdown 表現だけを互換化するため。
- **Change freedom**: migration-created workflow docs、tooling、CI、template-shared root guidance は、project content を変えない範囲で更新できる。8-path ledger の修正は lint rule への局所適合だけに限り、Koto text、task ID、仕様・QA の意味を変更しない。

### DEC-004: compatibility と strict schema を別 gate とする

- **What**: 新 validator を legacy-compatible mode で unchanged P docs に先に通し、その後に migration-created/semantically changed docs の schema v2 marker と strict sections を検証する。legacy project docs は意味変更なしに一括変換しない。
- **Why**: validator 導入による regression と schema 移行の不備を区別し、現行文書の意味を metadata-only bulk edit で揺らさないため。
- **Change freedom**: compatibility と strict checks の command は、二段階の evidence が別々に残る限り変更できる。

### DEC-005: lifecycle hook は軽量な guardrail として採用する

- **What**: prompt 時は短い evidence/scope reminder、write/stop 時は非局所影響・恒久性・verification の監査を促し、恒久削除と credential-like path を block する hook を paired client configuration から利用する。
- **Why**: agent の判断を hook に代行させず、長い定型文を毎 prompt に注入せずに、破壊操作と closure omission を境界で検出するため。
- **Change freedom**: 同じ安全境界と unit/smoke evidence を保つ限り、hook client、文言、event ごとの粒度は変更できる。

## Consequences / Impact

- final diff は docs workflow/tooling と migration records に限定される。
- schema v2 は新規 migration records と今後の semantic edits に適用され、legacy docs は互換層で引き続き有効である。
- upstream provenance と downstream CI scope は別の値として記録される。

## Quality Implications

- blind replacement、branch mixing、premature lock、bulk schema edit を diff/fixture/provenance checks で検出する。
- hook は DEC-005 の軽量性・非破壊性・closure evidence を unit/smoke tests で確認する。
- obsolete deletion は blob equality、references、U state の三証拠を必要とする。
- project content の P tree hash/diff を final tree と比較する。

## Intent-derived Invariants

- INV-001 (from DEC-001): final lock は tag `v1.0.0` と full SHA `f71e9ab20466ea2972158334261f5ae2b2265754` の組を記録する。
- INV-002 (from DEC-003): project application/WIP paths は P と同一 content を保持し、8-path lint ledger は semantic content を同一に保つ。

## Enforced in (optional)

- INV-001: `docs-template.lock.json` と provenance verification command。
- INV-002: final preservation hash/diff checks と 8-path lint ledger review。

## Rollback / Follow-ups

- branch/worktree 内のみの変更なので、採用しない場合は P の active checkout に影響しない。
- U より新しい release は、この migration の lock を B とする別 migration で扱う。
