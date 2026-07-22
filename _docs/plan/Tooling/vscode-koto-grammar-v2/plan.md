---
title: Grammar v2 — entity-name パターン
status: active
draft_status: n/a
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/intent/Tooling/vscode-koto-grammar-v2/decision.md"
  - "_docs/qa/Tooling/vscode-koto-grammar-v2/test-plan.md"
  - "_docs/intent/Tooling/vscode-koto-grammar/decision.md"
  - "_docs/standards/japanese-lang-design-memo.md"
related_issues: []
related_prs: []
---

# Grammar v2 — entity-name パターン

## Overview

v1 で実装した `tools/vscode-koto/syntaxes/koto.tmLanguage.json` に、識別子レベルの richness を追加する。Python が Pylance を通じて提供している「関数名・型名・パラメータ名・変数名」の別色化を、パーサ／LSP なしで TextMate Grammar のパターンマッチのみで到達できる範囲に限って再現する。

koto は構文が固定の助詞・キーワードで囲まれているため、Python と比べてもパターンベースで取れる範囲が広い。識別子に追加される scope によって、書き手は「今書いているのが関数か型かパラメータか変数か」を視覚で支援される。

## Scope

`koto.tmLanguage.json` の `repository` に `entity-names` エントリを追加し、top-level `patterns` の include 順を「strings → numerics → literals → keywords-multi → modifiers → storage-types → keywords-control → **entity-names** → particles → punctuation」に更新する。

`entity-names` 内に以下のパターンを置く（順序は specificity 降順）:

1. オブジェクト型宣言名: `オブジェクト　として　[X]　は[、。]` の X → `entity.name.type.koto`
2. 関数／コンストラクタ呼び出し: `[X]（` の X → `entity.name.function.koto`
3. 関数宣言名: `[X]　は[、。]` の X（fallback。1 でカバーされない場合） → `entity.name.function.koto`
4. パラメータ名: `である　[X]　を受け取る` の X → `variable.parameter.koto`
5. 変数束縛名: `である`　`[X]`　`を`　の X → `variable.other.koto`
6. 型注釈前: `[X]　である` の X → `entity.name.type.koto`
7. 戻り値型: `[X]　を返す` の X → `entity.name.type.koto`
8. 組み込み型サフィックス: `…(配列|集合|辞書)` → `entity.name.type.koto`

新規 fixture `tools/vscode-koto/tests/fixtures/entity-names.koto` を追加し、各パターンが期待 scope を出すことを目視確認できるようにする。

## Non-Goals

設計メモ § 7「次のステップ」と v1 intent INV-002 を維持するため、以下は**今回手を出さない**。

- フィールドアクセス `〜　の　[X]`: 助詞 `の` の他用法（possession 等）と区別不能。LSP のセマンティックトークン待ち。
- メソッド呼び出し `〜　の　[X]（`: 上記の延長。
- 列挙値参照 `状態　が　[X]`: 型推論なしには `[X]` が列挙値か単なる識別子か判別できない。
- 識別子のスコープ追跡（宣言時と参照時の同名同色化）。LSP のセマンティックトークン待ち。
- `定数 として X` で定義された名前を `variable.other.constant` 等に細分すること。lookbehind が長くなり保守性が落ちる割に得るものが薄い。
- 設計メモで未確定の構文（コメント、ジェネリクス、Optional 型「たぶん〜」、パターンマッチ）への着色拡張。仕様確定待ち。

## Requirements

- **Functional**:
  - 8 パターンすべてが、対応する fixture トークンで期待 scope を出す。
  - v1 で動作していたキーワード・助詞・記号・リテラルの highlight は退行しない。
  - 識別子内に同字が含まれても誤検出しない（v1 INV-003 を継承）。
  - 半角スペース区切りは語境界として認めない（v1 INV-003 を継承）。
- **Non-Functional**:
  - 追加パターン数は 8 個以内。
  - すべての pattern に `(?<=^|[　。、（）「」])` または同等以上の語境界要件を持たせる。
  - `JSON.parse` を通る。
  - `scripts/check-docs.sh` が PASS する。

## Tasks

1. Plan / Intent / QA test-plan を作成する（本書 + intent + test-plan）。
2. `koto.tmLanguage.json` に `entity-names` repository を追加し、include 順を更新する。
3. `tools/vscode-koto/tests/fixtures/entity-names.koto` を追加する。
4. ECMAScript regex による positive / negative smoke test を verification に残す。
5. `tools/vscode-koto/README.md` に v2 の色分け対象を一節追記する。
6. VSCode で目視確認する（ユーザー作業）。
7. verification を完成させ、`qa-review` で verdict を確認する。

## QA Plan

- QA document: `_docs/qa/Tooling/vscode-koto-grammar-v2/test-plan.md`
- Risk level: Low
- Test strategy:
  - Unit: 該当なし。
  - Integration: VSCode で fixture をロードし scope を inspect。
  - Manual QA: `Developer: Inspect Editor Tokens and Scopes` で 8 パターン分の代表トークン scope を確認。
  - Validator / static check: `JSON.parse` で grammar 妥当性、`scripts/check-docs.sh` で docs 整合。
  - Diff review: include 順、各パターンの語境界要件、scope 名の theme 互換性を diff で確認。

## Deployment / Rollout

`tools/vscode-koto/` の grammar ファイルを更新するのみ。VSCode を `Developer: Reload Window` するか、拡張を Install from Location で再インストールすれば反映される。問題があれば該当 repository entry を削除すれば v1 状態に戻る。
