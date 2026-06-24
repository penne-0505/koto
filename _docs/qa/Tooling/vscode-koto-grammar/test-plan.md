---
title: "QA Test Plan: VSCode koto grammar"
status: active
draft_status: n/a
qa_status: planned
risk: Low
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/intent/Tooling/vscode-koto-grammar/decision.md"
  - "_docs/plan/Tooling/vscode-koto-grammar/plan.md"
related_issues: []
related_prs: []
---

# QA Test Plan: `VSCode koto grammar`

## Source of Intent

- TODO: `Tooling-Feat-9`
- Plan: `_docs/plan/Tooling/vscode-koto-grammar/plan.md`
- Intent: `_docs/intent/Tooling/vscode-koto-grammar/decision.md`

## Quality Goal

`.koto` ファイルを VSCode で開いたとき、設計メモ § 7 のキーワード・記号・リテラル・助詞が、書き手の意図に沿って色分けされる。同時に、識別子内に同一字列が含まれても誤検出せず、未確定構文を勝手に着色しない。「ハイライトされていない部分は仕様未確定」と読める信頼性を担保する。

## Acceptance Criteria

- AC-001: `tools/vscode-koto/` に `package.json`、`language-configuration.json`、`syntaxes/koto.tmLanguage.json` が存在し、拡張子 `.koto` を言語 `koto` に紐づけている。
- AC-002: 設計メモ § 7 の宣言系・制御系・動作系・構文系の各キーワードがすべて grammar に登録され、`source.koto` 配下の scope を持つ。
- AC-003: 文字列リテラル `「...」`、関数呼び出し用全角丸括弧 `（）`、句点 `。`、読点 `、`、算用数字、`真` / `偽` / `無し` がそれぞれ独立した scope で識別される。
- AC-004: 分かち書きで囲まれた一文字助詞（`の`、`が`、`に`、`を`、`から`、`で`）がキーワードとしてハイライトされ、識別子内に同じ字が含まれても誤検出しない。
- AC-005: `tools/vscode-koto/tests/fixtures/` に最大値・未完了の取り出し・タスク表の作成の 3 サンプルが存在し、目視またはトークン dump で期待 scope が確認できる。
- AC-006: `tools/vscode-koto/README.md` にインストール手順と既知の制限が記載されている。

## Intent-derived Invariants

- INV-001: `.koto` ファイルは VSCode に `source.koto` の言語として登録される。
- INV-002: 設計メモ § 7 のキーワード一覧に列挙された語のみが grammar に登録される。
- INV-003: すべてのキーワード／助詞のマッチには前後の語境界要件（全角スペース・行端・全角句読点・全角括弧・鉤括弧）が課され、半角スペースを語境界として認めない。
- INV-004: 多文字キーワードは単文字キーワード／助詞より先に評価される。
- INV-005: 修飾語と宣言キーワードは別 scope 群に分離される。
- INV-006: 漢数字は数値リテラル扱いにしない。
- INV-007: `真`、`偽`、`無し` は `constant.language.*.koto` 配下の scope を持つ。
- INV-008: 文字列リテラル `「...」` は `string.quoted.*.koto` を持ち、内部のキーワード字列はハイライトされない。

## Risk Assessment

- Risk level: Low
- Risk rationale: 拡張機能はエディタ視覚のみに影響する。ランタイム挙動・データ・セキュリティに影響しない。失敗した場合の最大影響は「色が出ない」「誤った色が出る」に留まる。
- Regression risk: 既存コードへの影響なし（新規ディレクトリ `tools/vscode-koto/`）。
- Data safety risk: なし。
- Security / privacy risk: なし。拡張は読み取り専用で、ネットワークアクセス・実行権限を要求しない。
- UX risk: 誤検出が起きた場合、書き味の信用が損なわれる。Manual QA でサンプル全文の scope 確認を必須とする。
- Agent misbehavior risk: 後続の agent が「ハイライトされていないから未実装」と誤解し、勝手に grammar を追記して言語仕様を先取りしてしまうリスク。intent INV-002 と README で防ぐ。

## Test Strategy

- Unit: 該当なし（grammar は宣言的データであり、ランタイムロジックを持たない）。
- Integration: VSCode で拡張をローカルロードし、`tests/fixtures/*.koto` を開く。
- Manual QA: `Developer: Inspect Editor Tokens and Scopes` で各サンプルの代表トークンの scope を Manual QA Checklist に従って記録する。
- Validator / static check: `scripts/check-docs.sh` で docs 整合性。`deno eval` または `node -e` で `JSON.parse` を通して JSON 妥当性。
- Diff review: 設計メモ § 7 と grammar の keyword 一覧を突き合わせ、過不足がないか確認する。include 順序が「文字列 → リテラル → 多文字キーワード → 単文字助詞 → 数値 → 記号 → 識別子」になっていることを確認する。

## Test Matrix

| ID | Source | Requirement / Invariant | Test Type | Command / File | Expected Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | TODO | 拡張スケルトンと grammar が存在し、`.koto` が言語 `koto` に登録される。 | manual QA | `tools/vscode-koto/package.json` | `contributes.languages` に `extensions: [".koto"]`、`contributes.grammars` に `language: "koto"`、`scopeName: "source.koto"`。 | planned |
| AC-002 | TODO | § 7 の全キーワードが登録されている。 | diff review | `tools/vscode-koto/syntaxes/koto.tmLanguage.json` vs 設計メモ § 7 | 4 群（宣言系・制御系・動作系・構文系）の語が repository に存在。 | planned |
| AC-003 | TODO | 記号・リテラルが独立 scope で識別される。 | manual QA | `tests/fixtures/*.koto` の Inspect Token | `「...」` → `string.quoted`、`（）` → `punctuation.section`、`。` → `punctuation.terminator`、`真`/`偽`/`無し` → `constant.language`、数字 → `constant.numeric`。 | planned |
| AC-004 | TODO | 助詞は語境界を満たした場合のみキーワード。 | manual QA | `tests/fixtures/*.koto` + 識別子内に `の`/`が`/`を` を含む確認用片 | 助詞は `keyword.operator.particle`、識別子内の同字は識別子色のまま。 | planned |
| AC-005 | TODO | 3 サンプルが存在し scope 確認可能。 | diff review + manual QA | `tools/vscode-koto/tests/fixtures/` | `max-value.koto`、`incomplete-pickup.koto`、`task-table.koto` の 3 ファイルが存在し、設計メモ § 4 の例文を再現する。 | planned |
| AC-006 | TODO | README に手順と制限がある。 | diff review | `tools/vscode-koto/README.md` | インストール手順（Install from Location）、コメント等の未確定構文の注記、Marketplace 配布なしの明示。 | planned |
| INV-001 | intent | `source.koto` を `scopeName` とする。 | diff review | `koto.tmLanguage.json` | top-level `"scopeName": "source.koto"`。 | planned |
| INV-002 | intent | § 7 以外のキーワードを登録しない。 | diff review | `koto.tmLanguage.json` | コメント・ジェネリクス等の予想キーワードが含まれない。 | planned |
| INV-003 | intent | 語境界要件は全角境界に限る。半角スペースを語境界としない。 | manual QA | `tests/fixtures/half-width-boundary.koto`（半角スペース挟みで `関数` を置く） | 半角スペース挟みの `関数` はキーワードでなく識別子として扱われる。 | planned |
| INV-004 | intent | 多文字キーワード優先。 | manual QA | `tests/fixtures/*.koto` 内の `と同じ` トークン | 単一の `keyword.operator.equality` で着色され、`と` と `同じ` に分裂しない。 | planned |
| INV-005 | intent | 修飾語と宣言キーワードが別 scope。 | manual QA | `tests/fixtures/*.koto` 内の `公開 関数 として` | `公開` → `storage.modifier`、`関数` → `storage.type`。 | planned |
| INV-006 | intent | 漢数字を数値扱いしない。 | manual QA | `tests/fixtures/*.koto` 内の漢数字を含む識別子 / 文字列 | 漢数字は `constant.numeric` を持たない。 | planned |
| INV-007 | intent | `真`/`偽`/`無し` が定数色。 | manual QA | `tests/fixtures/*.koto` 内の `無し` | `constant.language.null.koto` 等の scope。 | planned |
| INV-008 | intent | 文字列内部はハイライト抑制。 | manual QA | `tests/fixtures/*.koto` 内の `「対象らが無し。」` | 文字列内の `無し` はキーワード色を持たない。 | planned |

## Manual QA Checklist

- [ ] VSCode で `tools/vscode-koto` を `Extensions: Install from Location` でロードする。
- [ ] `tests/fixtures/max-value.koto` を開き、宣言系・制御系キーワード、助詞、識別子が異なる色になっていることを確認する。
- [ ] 同ファイルで `Developer: Inspect Editor Tokens and Scopes` を開き、`関数` / `として` / `数値配列` / `である` / `対象ら` / `を受け取る` / `数値` / `を返す` / `最大値` / `もし` / `なら` / `1番目の要素` / `繰り返すと` / `である。` の scope を記録する。
- [ ] `tests/fixtures/incomplete-pickup.koto` を開き、`未完了` 列挙値と `状態` フィールド、`と同じ` 等価判定の scope を確認する。
- [ ] `tests/fixtures/task-table.koto` を開き、辞書型 `文字列とタスクの辞書` の scope を確認する。
- [ ] `tests/fixtures/half-width-boundary.koto` を開き、半角スペース挟みの `関数` が識別子色になることを確認する。
- [ ] サンプル内の文字列リテラル `「対象らが無し。」` 内部の `無し` がキーワード色になっていないことを確認する。
- [ ] サンプル内の `現在の最大` のような複合識別子（`の` を含む）が、識別子色のままでハイライトされていないことを確認する。

## Regression Checklist

- [ ] `scripts/check-docs.sh` が PASS する。
- [ ] `koto.tmLanguage.json` と `package.json` が `JSON.parse` を通る。
- [ ] 設計メモ § 7 のキーワード一覧と grammar の repository キーが過不足なく対応する。

## High-risk Checklist

該当なし（Risk Low）。

## Out of Scope

- LSP（診断・補完・ホバー・定義ジャンプ・セマンティックハイライト）。
- 自動化テスト（`vscode-tmgrammar-test` 等）。
- VSCode Marketplace への配布。
- Cursor / Zed / Sublime Text 等への移植。
- Theme による色の指定。色は使用者の Theme に従う。

## Open Questions

- コメント構文は設計メモで未確定。確定次第、Intent の Alternatives セクションを更新したうえで grammar を追加する。
- ジェネリクス（ユーザー定義の型コンストラクタ）の構文確定後、`数値配列` 形式の複合名詞型と整合させる必要がある。
