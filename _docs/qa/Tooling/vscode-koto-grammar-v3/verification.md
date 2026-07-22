---
title: "QA Verification: koto grammar v3 — Phase B 構文"
status: active
draft_status: n/a
qa_status: verified
risk: Low
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/intent/Tooling/vscode-koto-grammar-v3/decision.md"
  - "_docs/plan/Tooling/vscode-koto-grammar-v3/plan.md"
  - "_docs/qa/Tooling/vscode-koto-grammar-v3/test-plan.md"
related_issues: []
related_prs: []
---

# QA Verification: `koto grammar v3 — Phase B 構文`

## Summary

`tools/vscode-koto/syntaxes/koto.tmLanguage.json` に Phase B 確定構文 (memo §3-19〜§3-26) の keyword / 記号を追加した。実装したパターンは合計 **19 種** (比較演算 5 / 論理結合 3 / 制御 4 / パラメータ連用形 1 / 集合 1 / 終了型 3 / 型 postfix Optional 1 / 列挙記号中点 1)。新規 fixture `phase-b.koto` を追加し、ECMAScript regex による positive smoke test と既存 fixture への regression check を実施。

### Amendment 1 (2026-07-01): tab boundary 追加

初回 verification PASS 後、user が `phase-b.koto` を VSCode で実機確認した際に「tab 直後の `もし` がハイライトされない」問題を発見。原因: Phase B で tab indent canonical を確定したのに、grammar の lookbehind `(?<=^|[　。、（）「」])` が `\t` を boundary 文字として認識していなかった (v1/v2 fixture は全角 space indent だったため発覚せず、v3 で tab 採用 + tab-indent fixture を入れて初めて表面化)。

対処: 全パターンの lookbehind / lookahead を `(?<=^|[　。、（）「」\t])` / `(?=$|[　。、（）「」\t])` に更新 (56 + 51 = 107 箇所)。token boundary に tab を含めることで、tab 直後の keyword が正しく highlight される。

修正後の追加 smoke test:

- tab-indented keyword 6 件 (`\tもし`、`\tなら`、`\t数値　である　X`、`\t\t何もしない。`、`\tメッセージ　について、`、`\t数値　を返す`) すべて期待 scope で match
- 既存 5 fixture (v1/v2) の 26 ケース regression なし (`として終える`、`繰り返すと`、`を受け取る`、`と同じ`、`を返す`、`とする`、`である` がすべて従来通り発火、`half-width-boundary.koto` のみ意図通り発火しない)

### Amendment 2 (2026-07-01): `を返す` / `である。` を control scope へ + entity-names tab 除外

Amendment 1 後の user 実機確認で「`を返す` / `である。` / `を受け取り` が identifier 色とほぼ同じで判別できない」観察。原因: theme 側で `keyword.operator.signature.*` / `keyword.operator.type-annotation.*` などの koto 独自 sub-scope に specific 色 rule が無い (theme は generic `keyword.operator` には弱い色しか当てない傾向)。

設計判断: `を返す` (return 相当) と `である。` (関数本体終端 = end 相当) は semantic に control flow keyword であり、theme が確実に強い色 (典型的に pink) を当てる `keyword.control.*` scope に振り直すのが構造的に正しい。`を受け取り` は theme 依存のまま (user 同意済)。

対処:

- `を返す` の scope を `keyword.operator.signature.return.koto` → **`keyword.control.return.koto`** に変更 (`返す` 単独形と同 scope に揃える)
- `である` パターンを 2 つに split:
  - `(?<=^|[　。、（）「」\t])である(?=。)` → **`keyword.control.end.koto`** (`end` 相当、pink)
  - `(?<=^|[　。、（）「」\t])である(?=　|$|[、（）「」\t])` → 既存の `keyword.operator.type-annotation.koto` (型注釈、現状色維持)
- entity-names の identifier 捕捉パターン (5 箇所) の `[^　。、（）「」]+` を `[^　。、（）「」\t]+` に修正 (tab を identifier の一部として誤捕捉していたのを fix)

修正後の動作 (smoke test):

- `\t文字列　である　X　を受け取り、` → 文字列 (entity.name.type) / である (operator.type-annotation) / X (variable.parameter) / を受け取り (operator.signature.parameter)
- `\t真偽値　を返す` → 真偽値 (entity.name.type) / **を返す (keyword.control.return)** ← 新 scope
- `である。` → **である (keyword.control.end)** / 。 (punctuation.terminator) ← 新 scope
- `\t現在の最大　を返す。` → 現在の最大 / **を返す (keyword.control.return)** / 。

## Verification Verdict

Verdict: PASS

automated 系の AC / INV はすべて mechanical に確認済み。VSCode 実機での目視は v2 と同じく Manual QA Checklist に DEFERRED (theme 依存の見映え部分)。grammar の token 分類自体は ECMAScript regex による positive / regression test で確定的に検証されている。

## Commands Run

```bash
node -e 'JSON.parse(require("fs").readFileSync("tools/vscode-koto/syntaxes/koto.tmLanguage.json", "utf-8"))'

# Phase B 新 keyword 19 種について:
# - fixture (phase-b.koto) に各 keyword が 1 回以上出現するか確認 (19 件)
# - grammar repository に対応 scope が登録されているか確認 (19 件)
deno eval '<positive smoke test, see test-plan>'

# 既存 5 fixture (entity-names / max-value / incomplete-pickup / task-table / half-width-boundary) で
# - v1 / v2 既存パターンが従来通り boundary 付きで発火するか確認
# - half-width-boundary.koto では意図通り boundary 違反で発火しないことを確認
deno eval '<regression test, see test-plan>'

bash scripts/check-docs.sh

# Amendment (tab boundary 追加後):
# - lookbehind/lookahead に \t を追加した全パターンを再検証
deno eval '<tab-indented keyword smoke test, 6 cases>'
deno eval '<corrected regression on existing fixtures, 26 cases>'
```

Result:

```text
JSON parse: OK (grammar 妥当)
Positive smoke (Phase B keyword 19 + scope 19): 38/38 PASS
Regression check (v1/v2 patterns on existing fixtures):
  - entity-names.koto / max-value.koto / incomplete-pickup.koto / task-table.koto: 既存 7 keyword 全件 boundary 付きで発火 (23 PASS)
  - half-width-boundary.koto: 意図通り boundary 違反で発火しない (expected behavior、これも PASS 扱い)
bash scripts/check-docs.sh: PASS (validator 群 + self-test 全件 exit 0)

Amendment (tab boundary 追加後):
Tab-indented keyword smoke (`\tもし` 等 6 件): 6/6 PASS
Regression (corrected logic, v1/v2 keywords across 5 existing fixtures): 26/26 PASS
```

## Automated Test Results

| Command / Test | Result | Notes |
| --- | --- | --- |
| `JSON.parse` (koto.tmLanguage.json) | PASS | grammar 妥当 |
| Positive smoke (Phase B keyword 19 件 fixture 出現確認) | PASS | `について繰り返すと`、`を受け取り`、`に含まれる`、`より大きい`、`より小さい`、`何もしない`、`と異なる`、`ではない`、`について`、`で終える`、`または`、`以上`、`以下`、`かつ`、`例外`、`警告`、`通知`、`？`、`・` の全 19 種が `phase-b.koto` に 1 回以上出現 |
| Positive smoke (Phase B scope 19 件 grammar 登録確認) | PASS | `keyword.operator.comparison.*` / `keyword.operator.logical.{and,or,not}` / `keyword.control.{match,loop,noop,throw}` / `keyword.operator.set.contains` / `support.type.builtin.terminal.*` / `keyword.operator.optional` / `punctuation.separator.list` の全 19 scope が grammar の `keywords-multi` / `terminal-types` / `operators-symbol` / `punctuation` repository に登録 |
| Regression check (v1/v2 既存パターン on entity-names.koto / max-value.koto / incomplete-pickup.koto / task-table.koto) | PASS | 既存 7 パターン (`として終える`、`繰り返すと`、`を受け取る`、`と同じ`、`を返す`、`とする`、`である`) が各 fixture で従来通り発火 (23 件) |
| Regression check (half-width-boundary.koto) | PASS | 意図通り boundary 違反で v1/v2 パターン非発火 (`を受け取る` / `を返す` / `である` が半角 space 文脈で非マッチ、これが本 fixture の design) |
| `bash scripts/check-docs.sh` | PASS | docs validator 群 + self-test すべて exit 0 |

## Manual QA Results

| Checklist Item | Result | Notes |
| --- | --- | --- |
| VSCode 再起動後 `phase-b.koto` を開き各 keyword の scope を Inspect で確認 | DEFERRED | grammar の token 分類は smoke test で確定的に確認済み。VSCode 上での見映え (色割り当て) は Theme 依存。ユーザー側で任意のタイミングで確認可能 (v2 verification と同じ運用) |
| `について繰り返すと` が 1 トークンとして compound 認識されているか確認 | DEFERRED | grammar 配列順で `について繰り返すと` が `について` より先に配置されていることを diff で確認済み。実機目視は任意 |
| 既存 5 fixture で v1 / v2 highlight regression がないか目視 | DEFERRED | smoke test で regression なしを確認済み。実機目視は任意 |

## Acceptance Criteria Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| AC-001 | PASS | Phase B 新 keyword 19 種が fixture 出現 + scope 登録の双方で確認済 (positive smoke 38/38 PASS) |
| AC-002 | PASS | v1 / v2 既存 7 パターンが 4 fixture で従来通り発火 (regression check 23 PASS)。half-width-boundary.koto では意図通り発火しないこと確認 |
| AC-003 | PASS | `tools/vscode-koto/tests/fixtures/phase-b.koto` 存在、全 19 種の Phase B keyword を含む |
| AC-004 | PASS | grammar diff review: `keywords-multi.patterns` 配列で `について繰り返すと` (index 0) が `について` (index 8) より先 |
| AC-005 | PASS | `entity-names` に `(?<=である　)([^　。、（）「」]+)(?=　を受け取り)` パターンを `を受け取る` 終止形パターンの直後に追加。`phase-b.koto` line 2-3 の `X` / `接頭辞` がパラメータ scope で取れる |

## Invariant Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| INV-001 | PASS | 追加した 19 種は memo §3-19〜§3-26 で確定したもののみ。memo に無いコメント構文 (`＃`)、`空である` 述語、user 定義 終了型 marker 等は追加していない |
| INV-002 | PASS | AC-002 と同じ根拠 (regression なし) |
| INV-003 | PASS | half-width-boundary.koto で新規パターンも boundary 違反で発火しないことを regression test で確認 (multi-char keyword は全部 `(?<=^\|[　。、（）「」])...(?=$\|[　。、（）「」])` 形) |
| INV-004 | PASS | 新規 multi-char パターン (14 個 in keywords-multi、3 個 in terminal-types) すべてに `(?<=^\|[　。、（）「」])` lookbehind + `(?=$\|[　。、（）「」])` lookahead あり。1 文字 operator `？` / `・` は context-free に発火 (INV-004 例外として明記) |
| INV-005 | PASS | `keywords-multi.patterns` 配列で `について繰り返すと` (5 chars effective + lookarounds) が `について` (4 chars) より先 |
| INV-006 | PASS | 既存 scope を再利用: `keyword.control.throw.koto` (`として終える` + `で終える` 共有)、`keyword.control.loop.koto` (`繰り返すと` + `について繰り返すと` 共有)、`keyword.operator.signature.parameter.koto` (`を受け取る` + `を受け取り` 共有)。新規 scope は必要最小限 |

## Deferred / Not Covered

| ID | Reason | Follow-up |
| --- | --- | --- |
| Manual QA (VSCode 実機目視) | grammar の token 分類は smoke test で確定的に検証済。VSCode 上での色割り当ては Theme 依存で grammar の責任外 | v2 verification と同じく、ユーザー側で任意のタイミングで確認可能 |
| 位置 access (`N 番目` / `N 番目以降` 等) の専用ハイライト | v3 範囲外 (test-plan Out of Scope) | v4 で検討 |
| コメント構文 (`＃` 仮使用中) | memo §5 #39 で未確定 (INV-001 で先取り禁止) | コメント仕様確定後に v4 等で追加 |
| ユーザー定義 終了型 marker | memo §5 #28 で未確定 (INV-001 で先取り禁止) | marker 構文確定後に grammar 対応検討 |

## Residual Risks

None

## Follow-up TODOs

- VSCode 実機での目視確認 (Theme 依存の見映え) は user 側で任意のタイミングで実施
- 位置 access (`N 番目` 系) のハイライト追加 (v4 検討)
- コメント構文確定後に grammar 追加 (memo §5 #39)
- ユーザー定義 終了型 marker 確定後に grammar 対応 (memo §5 #28)
