---
title: Grammar v3 — Phase B 新構文ハイライト 設計判断
status: proposed
draft_status: idea
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/plan/Tooling/vscode-koto-grammar-v3/plan.md"
  - "_docs/qa/Tooling/vscode-koto-grammar-v3/test-plan.md"
  - "_docs/intent/Tooling/vscode-koto-grammar-v2/decision.md"
  - "_docs/standards/japanese-lang-design-memo.md"
related_issues: []
related_prs: []
---

# Grammar v3 — Phase B 新構文ハイライト 設計判断

<!-- Stub: Lang-Doc-15 完了を受けて、grammar v3 の設計判断は実装着手時に詳細化する。本書は最低限の方向性を記録。 -->

## Context

Phase B 手書き演習で確定した新 keyword / 構文 (memo §3-19〜§3-26 等) は、現状 v1 / v2 grammar ではハイライトされない。書き手の体験を統一するために grammar 側も追従する。

## Decision

- v2 の `entity-names` repository 構造を保ちつつ、Phase B 新 keyword 群を既存 keyword 群 (`keywords-multi` 等) に追加する
- 中点 `・` (集合 disjunction の列挙記号) を新規 punctuation scope として追加
- `？` (型 postfix Optional) を新規 operator scope として追加
- 既存ハイライト (Phase A / v2 範囲) に regression を出さない

詳細な実装方針は着手時に詳細化。

## Alternatives

実装着手時に詳細化。

## Rationale

memo §3 を正本として grammar が追従する基本姿勢を維持する。

## Consequences / Impact

- 書き手は Phase B 構文を書いた直後から色付けで確認できる
- v2 の test fixture 4 本 + 新規 Phase B fixture で regression check を実施

## Intent-derived Invariants

- INV-001: memo §3 で確定した keyword / 構文のみを対象とする (memo に無いものを grammar 先取りしない、v2 INV-002 を継承)
- INV-002: v1 / v2 の既存パターンに regression を出さない
- INV-003: 半角スペースを語境界として認めない原則 (v1 INV-003) を維持

## Rollback / Follow-ups

- Rollback: 追加したパターンを削除すれば v2 状態に戻る
- Follow-ups: LSP セマンティックトークン (v2 範囲外の △ パターン) は別タスクで
