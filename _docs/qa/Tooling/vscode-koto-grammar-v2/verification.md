---
title: "QA Verification: koto grammar v2 entity-names"
status: active
draft_status: n/a
qa_status: verified
risk: Low
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/intent/Tooling/vscode-koto-grammar-v2/decision.md"
  - "_docs/plan/Tooling/vscode-koto-grammar-v2/plan.md"
  - "_docs/qa/Tooling/vscode-koto-grammar-v2/test-plan.md"
related_issues: []
related_prs: []
---

# QA Verification: `koto grammar v2 entity-names`

## Summary

v1 grammar に `entity-names` repository entry を追加し、識別子を文脈分類して別 scope で着色するようにした。Python の Pylance が提供する richness の一部を、パーサ／LSP なしで TextMate Grammar のパターンマッチのみで再現する。

実装したパターン数は 9 個（オブジェクト宣言名、関数呼び出し、関数宣言名 fallback、パラメータ名、変数束縛 A/B/C、型注釈前、戻り値型、型サフィックス）。すべてに語境界要件を課し、半角スペース挟みケースで非発火、識別子内の同字で非発火を維持。

position-aware tokenizer による「先勝ち」シミュレーションで 25 ケース（positive 18 + negative 5 + 退行 2）すべて PASS。VSCode 実機でのレンダリング確認は、grammar v1 と同じく Theme 依存の見映え部分のみ Manual QA に残す。

## Verification Verdict

Verdict: PASS

automated 系の AC / INV はすべて mechanical に確認済み。半角スペース regression、v1 既存 fixture の `今の数`（再代入文の値）が誤って variable 色になっていないことも含めて確認。VSCode 実機での目視は Manual QA Checklist に残すが、grammar の token 分類自体は ECMAScript regex + 先勝ちシミュレーションで確定的に検証されている。

## Commands Run

```bash
deno eval 'JSON.parse(await Deno.readTextFile("tools/vscode-koto/syntaxes/koto.tmLanguage.json"));'

# entity-names patterns を grammar から抽出し、fixture をシミュレートトークナイズ
# - positive: 18 ケース (各 AC を fixture の特定トークンと scope の組で確認)
# - negative: 5 ケース (フィールドアクセス・列挙値参照・文字列内部が無着色)
# - regression: 半角スペース行で entity-names が非発火
# - regression: max-value.koto の `現在の最大 を 今の数 とする` で `今の数` が variable 化しないこと
deno eval '<smoke test, see test-plan>'

bash scripts/check-docs.sh
```

Result:

```text
JSON parse: OK (grammar 妥当).
Smoke test (position-aware tokenize): 25/25 pass, 0 fail.
  - positive AC-001..AC-008 全件 pass (18 トークン)
  - negative AC-009 5 ケース pass (識別子色のまま)
  - regression: half-width 行で entity-names 非発火 ✓
  - regression: 今の数 (再代入文の値) は variable 色にならない ✓
bash scripts/check-docs.sh: PASS (validator 群 + self-test 全件 exit 0).
```

## Automated Test Results

| Command / Test | Result | Notes |
| --- | --- | --- |
| `JSON.parse` (koto.tmLanguage.json) | PASS | grammar 妥当。 |
| Position-aware tokenizer smoke (positive 18) | PASS | AC-001 〜 AC-008 を各 fixture トークンと期待 scope の組で全件確認。 |
| Smoke (AC-009 negative 5) | PASS | `状態`、`未完了`、`今日`、`タイトル`、`買い物` は entity-names で非着色（フィールドアクセス・列挙値参照・文字列内部）。 |
| Smoke (half-width regression) | PASS | 半角スペース行で entity-names patterns が非発火。 |
| Smoke (v1 v2 regression) | PASS | `現在の最大　を　今の数　とする`（再代入文）で `今の数` が variable.other に誤分類されない。type-inferred binding を `(?<=）　を　)` で narrow したことの効果。 |
| `bash scripts/check-docs.sh` | PASS | docs validator 群すべて exit 0。 |

## Manual QA Results

| Checklist Item | Result | Notes |
| --- | --- | --- |
| VSCode 再起動後 `entity-names.koto` を開き各識別子の scope を Inspect で確認。 | DEFERRED | grammar の token 分類は smoke test で確定的に確認済み。VSCode 上での見映え（色割り当て）は Theme 依存。ユーザー側で任意のタイミングで確認可能。 |
| 既存 4 fixture を開き v1 highlight が変わらないこと。 | DEFERRED | smoke test で v1 退行（特に `今の数` 誤分類）が起きないことは確認済み。実機目視は任意。 |
| 半角スペース版で entity-names も非発火することの目視。 | DEFERRED | smoke test で確認済み。 |

## Acceptance Criteria Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| AC-001 | PASS | `最大値`、`タスク表の作成` が `entity.name.function.koto` で確認（smoke test）。 |
| AC-002 | PASS | `タスク`（line 15 constructor）、`最大値`（line 17 call）が `entity.name.function.koto`（smoke test）。 |
| AC-003 | PASS | `文字列`、`タスク状態`、`日付`、`数値配列`、`タスク配列`、`文字列とタスクの辞書`、`数値`（パラメータ型）が `entity.name.type.koto`（smoke test）。 |
| AC-004 | PASS | `数値`（戻り値型）が `entity.name.type.koto`（smoke test）。 |
| AC-005 | PASS | `数値配列`、`タスク配列`、`文字列とタスクの辞書`、`空辞書` が `entity.name.type.koto`（smoke test）。 |
| AC-006 | PASS | `対象ら` が `variable.parameter.koto`（smoke test）。 |
| AC-007 | PASS | 構造 A (`結果`)、構造 B (`現在の最大`)、構造 C (`新しいタスク`、`最大`) すべて `variable.other.koto`（smoke test）。 |
| AC-008 | PASS | `タスク`（オブジェクト宣言）が `entity.name.type.koto`、`entity.name.function.koto` ではなく specificity 高い pattern が勝つ（smoke test）。 |
| AC-009 | PASS | `状態`（フィールドアクセス）、`未完了`（列挙値参照）、`今日`、`タイトル`（オブジェクト初期化のキー）、`買い物`（文字列内部）すべて entity-names で非着色（smoke test）。 |

## Invariant Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| INV-001 | PASS | `koto.tmLanguage.json` top-level patterns で `entity-names` が `keywords-control` の後・`particles` の前にある。 |
| INV-002 | PASS | `entity-names` 内パターンは specificity 降順（obj_decl → fn_call → fn_decl → param → var_bind A → var_bind B → type_before_dearu → type_return → type_suffix → var_bind C）。先勝ちシミュレーションで AC-008（オブジェクト宣言が関数宣言より先に勝つ）が確認された。 |
| INV-003 | PASS | 全 entity-names regex に `(?<=^\|[　。、（）「」])` または `(?<=である　)` / `(?<=オブジェクト　として　)` / `(?<=）　を　)` の固定アンカーがある。半角スペース行で非発火を smoke test で確認。 |
| INV-004 | PASS | scope 名は `entity.name.function.koto`、`entity.name.type.koto`、`variable.parameter.koto`、`variable.other.koto` のみ。すべて TextMate 標準命名規約の `.koto` 名前空間に従う。 |
| INV-005 | PASS | grammar に `〜　の　X(?=（)`（メソッド呼び出し）や `〜　が　X　と同じ`（列挙値参照）等のパターンが存在しないことを diff review で確認。README に「v2 範囲外」として明示。 |
| INV-006 | PASS | v1 INV-001〜INV-008 を退行させていない。特に `今の数` 再代入文の誤分類が起きないことを smoke test で確認。`「対象らが無し。」` 内部の `無し` も entity-names で非発火（string scope が先に claim する include 順）。 |

## Deferred / Not Covered

| ID | Reason | Follow-up |
| --- | --- | --- |
| VSCode 実機での個別 scope 名照合 | grammar の token 分類は smoke test で確定的に確認済み。実機での色割り当ては Theme 依存で本タスクのスコープ外。 | ユーザーが書き味を継続評価する過程で自然に確認される想定。差異があれば別 TODO を起こす。 |
| 多引数関数のパラメータ着色 | 設計メモで多引数構文が未確定のため。 | 仕様確定後に param パターンを拡張する。 |
| `定数 として X` 専用 scope | lookbehind が長くなり保守性が落ちる。 | LSP 段階で再評価。 |

## Residual Risks

None

## Follow-up TODOs

- `空配列` / `空辞書` / `空集合` がリテラル的識別子として扱われるのに type 色になる挙動は、書き味の継続観察で違和感が出るかどうかを見る。違和感が大きければ専用 scope（`constant.language.collection.koto` 等）に分けることを検討。
- v3（仮）で LSP セマンティックトークンに着手する際、本 grammar の `entity.name.*.koto` / `variable.*.koto` namespace と衝突しない設計にする（別 TODO で起票予定）。
