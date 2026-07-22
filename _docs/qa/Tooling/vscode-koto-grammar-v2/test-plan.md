---
title: "QA Test Plan: koto grammar v2 entity-names"
status: active
draft_status: n/a
qa_status: planned
risk: Low
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/intent/Tooling/vscode-koto-grammar-v2/decision.md"
  - "_docs/plan/Tooling/vscode-koto-grammar-v2/plan.md"
related_issues: []
related_prs: []
---

# QA Test Plan: `koto grammar v2 entity-names`

## Source of Intent

- TODO: `Tooling-Feat-10`
- Plan: `_docs/plan/Tooling/vscode-koto-grammar-v2/plan.md`
- Intent: `_docs/intent/Tooling/vscode-koto-grammar-v2/decision.md`

## Quality Goal

`.koto` ファイルの識別子が、文脈に応じて関数名・型名・パラメータ名・変数名として別 scope で着色される。同時に、v1 のキーワード・助詞・記号・リテラルの highlight は退行しない。v2 範囲外（フィールドアクセス・メソッド呼び出し・列挙値参照）は識別子色のまま残る（INV-005 を維持）。

## Acceptance Criteria

- AC-001: `[X]　は[、。]` の X が `entity.name.function.koto` で着色される（`オブジェクト として ... X は、` のケースを除く）。
- AC-002: `[X]（` の X が `entity.name.function.koto` で着色される（関数／コンストラクタ呼び出し）。
- AC-003: `[X]　である` の X が `entity.name.type.koto` で着色される。
- AC-004: `[X]　を返す` の X が `entity.name.type.koto` で着色される。
- AC-005: `〜配列` / `〜集合` / `〜辞書` で終わる識別子が `entity.name.type.koto` で着色される。
- AC-006: `である　[X]　を受け取る` の X が `variable.parameter.koto` で着色される。
- AC-007: `である`　`[X]`　`を`　の X が `variable.other.koto` で着色される。
- AC-008: `オブジェクト　として　[X]　は[、。]` の X が `entity.name.type.koto` で着色される（AC-001 より specificity が高く優先される）。
- AC-009: v2 範囲外（フィールドアクセス `〜の[X]`、メソッド呼び出し `〜の[X]（`、列挙値参照 `〜が[X]と同じ`）の `[X]` は識別子色のまま（着色されない）。

## Intent-derived Invariants

- INV-001: `entity-names` は include 順で `keywords-control` の後、`particles` の前。
- INV-002: `entity-names` 内パターンは specificity 降順。
- INV-003: 全 `entity-names` パターンが語境界要件を持つ。
- INV-004: scope 名は TextMate 標準命名規約に従う。
- INV-005: フィールドアクセス／メソッド呼び出し／列挙値参照／スコープ追跡は grammar に未実装。
- INV-006: v1 INV-001〜INV-008 は退行しない。

## Risk Assessment

- Risk level: Low
- Risk rationale: 拡張機能の視覚レイヤーのみに影響する。失敗時の影響は「期待 scope と違う色が付く」「期待外の場所が着色される」に留まり、ランタイム挙動・データには無影響。
- Regression risk: v1 で動作していた highlight が変わると書き味の信用が下がる。fixture 4 本（v1）で退行が無いことを確認する。
- Data safety risk: なし。
- Security / privacy risk: なし。
- UX risk: `空配列` / `空辞書` / `空集合` が型色になる挙動は受容範囲だが、ユーザーに違和感を与える可能性がある。intent と README で明示する。
- Agent misbehavior risk: 後続 agent が「ハイライトされていないから未実装」と誤解して、フィールドアクセス等の grammar 拡張を勝手に追加し、INV-005 を破る可能性。intent INV-005 と README で防ぐ。

## Test Strategy

- Unit: 該当なし（grammar は宣言的データ）。
- Integration: VSCode で `entity-names.koto` および既存 4 fixture をロード。
- Manual QA: `Developer: Inspect Editor Tokens and Scopes` で 9 ケース分の代表トークンを確認。
- Validator / static check: `JSON.parse` で grammar 妥当性、`scripts/check-docs.sh` で docs 整合。ECMAScript regex による positive / negative smoke test。
- Diff review: include 順、語境界要件、scope 名、v1 既存パターンの不変性を diff で確認。

## Test Matrix

| ID | Source | Requirement / Invariant | Test Type | Command / File | Expected Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | TODO | `[X] は、` が関数名扱い | regex smoke test + manual QA | `entity-names.koto` line N | `最大値` が `entity.name.function.koto`。 | planned |
| AC-002 | TODO | `[X]（` が関数呼び出し扱い | regex smoke + manual QA | `entity-names.koto` 末尾 | `最大値`、`タスク` がそれぞれ `entity.name.function.koto`。 | planned |
| AC-003 | TODO | `[X] である` が型扱い | regex smoke + manual QA | `entity-names.koto` 各所 | `数値配列`、`数値`、`文字列` 等が `entity.name.type.koto`。 | planned |
| AC-004 | TODO | `[X] を返す` が型扱い | regex smoke + manual QA | `entity-names.koto` | `数値` が `entity.name.type.koto`。 | planned |
| AC-005 | TODO | サフィックスが型扱い | regex smoke + manual QA | `entity-names.koto` | `空配列`、`空辞書` 等が `entity.name.type.koto`。 | planned |
| AC-006 | TODO | パラメータ名識別 | regex smoke + manual QA | `entity-names.koto` | `対象ら` が `variable.parameter.koto`。 | planned |
| AC-007 | TODO | 変数束縛名識別 | regex smoke + manual QA | `entity-names.koto` | `現在の最大`、`結果`、`新しいタスク` が `variable.other.koto`。 | planned |
| AC-008 | TODO | オブジェクト宣言名識別 | regex smoke + manual QA | `entity-names.koto` | `タスク` が `entity.name.type.koto`（pattern 1 が pattern 3 に勝つ）。 | planned |
| AC-009 | TODO | v2 範囲外の識別子は無着色 | manual QA | `entity-names.koto` | `今のタスク の 状態` の `状態` がそのまま、`〜 が 未完了 と同じ` の `未完了` がそのまま。 | planned |
| INV-001 | intent | include 順 | diff review | `koto.tmLanguage.json` top-level patterns | `entity-names` が `keywords-control` の後・`particles` の前。 | planned |
| INV-002 | intent | specificity 降順 | diff review | `koto.tmLanguage.json` `entity-names` 内 | lookbehind 付き → lookbehind 無し、より具体的 → より一般的の順序。 | planned |
| INV-003 | intent | 語境界要件 | diff review + regex smoke | `koto.tmLanguage.json` 各 entity-names regex | すべてに語境界 lookbehind/lookahead が存在。半角スペース挟みケースで非一致。 | planned |
| INV-004 | intent | TextMate 標準命名 | diff review | `koto.tmLanguage.json` scope 名 | `entity.name.function.koto`、`entity.name.type.koto`、`variable.parameter.koto`、`variable.other.koto` のみ。 | planned |
| INV-005 | intent | △ 範囲は未実装 | diff review + grep | `koto.tmLanguage.json` 全体 | フィールドアクセス／メソッド呼び出し／列挙値参照を意図したパターンが存在しない。 | planned |
| INV-006 | intent | v1 退行禁止 | manual QA + regex smoke | 既存 4 fixture | v1 で確認した keyword / particle / 記号 / リテラルの scope が維持される。 | planned |

## Manual QA Checklist

- [ ] VSCode 再起動後、`tools/vscode-koto/tests/fixtures/entity-names.koto` を開く。
- [ ] 各識別子に Inspect Editor Tokens and Scopes を当て、AC-001〜AC-008 で期待する scope が出ているか確認。
- [ ] `entity-names.koto` 内のフィールドアクセス `今のタスク の 状態` の `状態` が無着色であることを確認（AC-009）。
- [ ] 列挙値参照 `状態 が 未完了 と同じ` の `未完了` が無着色であることを確認（AC-009）。
- [ ] 既存 4 fixture（v1）を開き、v1 で確認した highlight が変わっていないことを確認（INV-006）。
- [ ] 半角スペース版（`half-width-boundary.koto`）で entity-names パターンも発火しないことを確認。

## Regression Checklist

- [ ] `scripts/check-docs.sh` が PASS する。
- [ ] `koto.tmLanguage.json` が `JSON.parse` を通る。
- [ ] v1 fixture 4 本で v1 patterns の挙動が変わらない。
- [ ] include 順が要件通り。
- [ ] v2 で追加したパターンが、v1 で着色していた箇所の scope を奪わない（identifier 色だった箇所のみ新規 scope を付ける）。

## High-risk Checklist

該当なし（Risk Low）。

## Out of Scope

- LSP セマンティックトークン（フィールドアクセス／メソッド呼び出し／列挙値参照／識別子スコープ追跡）。
- `定数 として X` 専用 scope。
- 多引数関数のパラメータ着色（仕様未確定）。
- 自動 grammar テスト（`vscode-tmgrammar-test` 等）— v1 と同じく未導入。

## Open Questions

- フィールドアクセスのパターンを「`の` の用法を分かち書きや前後文脈で判別できる範囲だけ」着色する妥協案があり得るか。当面は LSP 待ちで放置するが、書き手の体験次第で再評価。
