---
title: Grammar v3 — Phase B 新構文のハイライト追加
status: proposed
draft_status: idea
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/intent/Tooling/vscode-koto-grammar-v3/decision.md"
  - "_docs/qa/Tooling/vscode-koto-grammar-v3/test-plan.md"
  - "_docs/standards/japanese-lang-design-memo.md"
related_issues: []
related_prs: []
---

<!-- Canonical path: _docs/plan/Tooling/vscode-koto-grammar-v3/plan.md -->
<!-- Stub: Lang-Doc-15 (memo Phase A/B 統合) 完了を受けて grammar v3 で対応する範囲の draft。実装着手時に Phases / Tasks / QA Plan を詳細化する。 -->

# Grammar v3 — Phase B 新構文のハイライト追加

## Overview

VSCode 拡張の TextMate Grammar (v1 / v2) を、Phase B 手書き演習 (Lang-Chore-12) で確定した新 keyword / 構文に対応させる。memo §3-1〜§3-26 が正本。

## Scope

memo §3 の Phase B 確定事項を grammar に反映する。具体的範囲は実装着手時に詳細化するが、最低限:

- `を受け取り、` (連用形)
- 比較演算: `より大きい` / `より小さい` / `以上` / `以下` / `と異なる` / `そのもの`
- 論理結合: `ではない` / `かつ` / `または`
- Optional & 集合: `？` (型 postfix 修飾子) / `配列` / `に含まれる` / `のいずれか` / 中点 `・`
- 制御: `について` / `について繰り返すと` / `なら、` / `である。` (mid-body 含む) / `何もしない。`
- 異常終了: `として終える` / `で終える` / 終了型名 (`例外` / `警告` / `通知`)
- 位置 access: `N 番目` / `N 番目以降` / `N 番目以前` / `N 番目から M 番目まで`

## Non-Goals

- 識別子の文脈別着色拡張 (v2 範囲外の △ パターン)
- LSP セマンティックトークン
- コメント構文への着色 (`＃` 仮使用中、未確定)

## Requirements

実装着手時に詳細化。

## Tasks

実装着手時に詳細化。

## QA Plan

- QA document: `_docs/qa/Tooling/vscode-koto-grammar-v3/test-plan.md`
- Risk level: Low
- Test strategy 詳細は実装着手時に詰める。

## Deployment / Rollout

`tools/vscode-koto/` の grammar / fixture を更新。`Developer: Reload Window` で反映。
