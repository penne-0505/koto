---
title: "QA Verification: VSCode koto grammar"
status: active
draft_status: n/a
qa_status: verified
risk: Low
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/intent/Tooling/vscode-koto-grammar/decision.md"
  - "_docs/plan/Tooling/vscode-koto-grammar/plan.md"
  - "_docs/qa/Tooling/vscode-koto-grammar/test-plan.md"
related_issues: []
related_prs: []
---

# QA Verification: `VSCode koto grammar`

## Summary

koto 言語の VSCode 拡張一式を `tools/vscode-koto/` に追加した。`package.json` で `.koto` を言語 `koto`（`scopeName: source.koto`）に紐づけ、`syntaxes/koto.tmLanguage.json` に設計メモ § 7 の全キーワード・記号・リテラルを登録した。語境界は全角スペース・行端・全角句読点・全角括弧・鉤括弧に限定し、半角スペースを境界として認めない。fixture を `tests/fixtures/` に 4 本配置（最大値、未完了の取り出し、タスク表の作成、半角スペース／識別子内同字の negative ケース）。

機械的検証は完了している（JSON 妥当性、§ 7 キーワード網羅 grep audit、ECMAScript regex による positive/negative 18 ケースの一致確認、`scripts/check-docs.sh` の docs 整合）。VSCode 上での実際のレンダリング確認（`Developer: Inspect Editor Tokens and Scopes` による scope 表示）はホスト環境に GUI VSCode がないため未実施で、ユーザー側に委ねる。

## Verification Verdict

Verdict: PASS

automated 系統の AC / INV はすべて mechanical に確認済み。さらに 2026-06-25 にユーザー環境（GUI VSCode）で `tools/vscode-koto/` を Install from Location でロードし、`incomplete-pickup.koto` を開いて目視確認した結果、storage.type / keyword.operator / keyword.control / particle / 識別子のカテゴリがそれぞれ別色で出ること、`未完了の取り出し` 内部の `の` や `各要素について` がハイライトされない（INV-002/INV-003 が効いている）ことを確認した。

実機ロードに伴って、VSCode 既定の `editor.unicodeHighlight.invisibleCharacters` が U+3000（全角スペース）を警告対象としてノイズを出すことが判明し、`package.json` の `contributes.configurationDefaults` で `[koto]` スコープに対して該当 3 設定（`invisibleCharacters` / `ambiguousCharacters` / `nonBasicASCII`）を `false` 既定として上書きする調整を加えた。判断根拠は README「エディタ既定設定」節に記載。

## Commands Run

```bash
deno eval 'JSON.parse(await Deno.readTextFile("tools/vscode-koto/package.json")); JSON.parse(await Deno.readTextFile("tools/vscode-koto/language-configuration.json")); JSON.parse(await Deno.readTextFile("tools/vscode-koto/syntaxes/koto.tmLanguage.json"));'

grep -oE '"name": "[^"]+"' tools/vscode-koto/syntaxes/koto.tmLanguage.json | sort -u
for kw in 関数 オブジェクト 定数 可変 外部 公開 非同期 もし なら 繰り返すと である からなる のいずれか 返す として終える して待つ 取り込む とする を受け取る を返す として の が に を から で と同じ そのもの と同種 真 偽 無し; do
  grep -q "])${kw}(?=" tools/vscode-koto/syntaxes/koto.tmLanguage.json && echo "OK $kw" || echo "MISS $kw"
done

# 40 個の regex を ECMAScript で構文検証し、fixture 上の positive / negative マッチを 18 ケース確認
deno eval '<smoke test script — see Test Matrix>'

bash scripts/check-docs.sh
```

Result:

```text
JSON parse: All 3 JSON files are valid.
keyword grep audit: 33/33 §7 keywords found in grammar.
regex syntax: 40/40 patterns ECMAScript-compatible.
smoke test: 14/14 positive matches succeed (max-value.koto の各行で期待キーワードが該当 regex で hit する).
negative test: 4/4 negative matches reject as expected (半角スペース挟みの 関数/として、関数記録 内の 関数、関連の数 内の の が unmatched).
scripts/check-docs.sh: exit 0（Tooling-Feat-9 の verification 不在エラーは本文書作成で解消）.
```

## Automated Test Results

| Command / Test | Result | Notes |
| --- | --- | --- |
| `JSON.parse` × 3 (package.json / language-configuration.json / koto.tmLanguage.json) | PASS | すべて妥当な JSON。 |
| `grep` による § 7 キーワード網羅監査 | PASS | 33 語すべてが grammar 内で語境界 lookbehind 付きで見つかる。 |
| ECMAScript `new RegExp(...)` 検証（40 patterns） | PASS | すべて構文エラーなく compile。Oniguruma は ECMAScript の superset なので同等以上の挙動が見込める。 |
| Positive smoke test（max-value.koto 上の 14 トークン） | PASS | 関数 / として / を受け取る / を返す / もし / と同じ / 無し / なら / として終える / 数字 / とする / 繰り返すと / である / 返す が該当 regex で一致。 |
| Negative smoke test（half-width-boundary.koto 上の 4 ケース） | PASS | 半角スペース挟みの 関数 / として、識別子 関数記録 内の 関数、識別子 関連の数 内の の がすべて非一致。 |
| `bash scripts/check-docs.sh` | PASS | docs validator 群 + self-test がすべて exit 0。 |

## Manual QA Results

| Checklist Item | Result | Notes |
| --- | --- | --- |
| VSCode で `tools/vscode-koto` を `Extensions: Install from Location` でロードする。 | PASS | 2026-06-25 にユーザー環境でロード成功。`.koto` が言語 `koto` として認識された。 |
| `incomplete-pickup.koto` を開き各群キーワードが異なる色になることを確認。 | PASS | storage.type（橙系: `関数`、`可変`）、keyword.operator（黄系: `として`、`である`、`を受け取る`、`を返す`、`とする`、`と同じ`、`繰り返すと`）、keyword.control（黄系: `もし`、`なら`、`返す`）、particle、識別子（無色）が分離して描画されることを目視確認。 |
| `Developer: Inspect Editor Tokens and Scopes` で個別 scope 名照合。 | DEFERRED | カテゴリ分離は実機確認済み。個別 scope 名までの照合は未実施だが、AC / INV 充足には十分。 |
| `incomplete-pickup.koto` の `未完了`、`状態`、`と同じ` の scope 確認。 | PASS | `未完了` / `状態` は識別子色のまま（§7 未登録のため意図通り）、`と同じ` は等価判定の黄系で描画されることを目視確認。 |
| `task-table.koto` の `文字列とタスクの辞書` 内部の `と`/`の` がハイライトされないことを確認。 | DEFERRED | 機構上は INV-003 で抑制される構造。ユーザーが書き味を継続評価する過程で自然に確認される想定。 |
| `half-width-boundary.koto` の半角スペース版 `関数` が識別子色のままであることを確認。 | DEFERRED | Negative smoke test で regex レベルでは確認済み。実機目視は任意のフォローアップ。 |
| `「対象らが無し。」` 内部の `無し` がキーワード色にならないことを確認。 | DEFERRED | string scope は内部再帰しない構造。実機目視は任意のフォローアップ。 |
| 識別子 `未完了の取り出し` / `各要素について` の内部 `の` が識別子色のままであることを確認。 | PASS | 実機スクリーンショットで、これらの語の内部 `の` がハイライトされないことを確認。INV-003 が効いている。 |
| `.koto` ファイルに対して全角スペース U+3000 の Unicode Highlight 警告が抑制される。 | PASS | `package.json` の `contributes.configurationDefaults` で `[koto]` スコープに `editor.unicodeHighlight.invisibleCharacters: false` 等を既定として設定。実機確認で問題提起された noise への対応。 |

## Acceptance Criteria Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| AC-001 | PASS | `tools/vscode-koto/{package.json, language-configuration.json, syntaxes/koto.tmLanguage.json}` が存在。package.json の `contributes.languages[0].extensions` に `".koto"`、`contributes.grammars[0]` に `language: "koto"` と `scopeName: "source.koto"`。 |
| AC-002 | PASS | grep audit で § 7 の 33 キーワード全てが grammar に登録され、scope は `source.koto` 配下に名前空間化されていることを確認（`storage.*.koto`、`keyword.*.koto`、`constant.*.koto` のいずれか）。 |
| AC-003 | PASS | `string.quoted.other.koto`、`punctuation.section.parens.{begin,end}.koto`、`punctuation.terminator.statement.koto`、`punctuation.separator.koto`、`constant.numeric.decimal.koto`、`constant.language.{boolean.true,boolean.false,null}.koto` が独立 scope として定義されている。 |
| AC-004 | PASS | 単文字助詞は語境界 lookbehind / lookahead `(?<=^\|[　。、（）「」])` `(?=$\|[　。、（）「」])` を要求する。negative smoke test で識別子内の同字（`関連の数` の `の`）が非一致になることを確認。 |
| AC-005 | PASS | `tests/fixtures/` に `max-value.koto`、`incomplete-pickup.koto`、`task-table.koto`、`half-width-boundary.koto` の 4 本。最初の 3 本は設計メモ § 4 の例文を分かち書き正規化して再現。 |
| AC-006 | PASS | `tools/vscode-koto/README.md` にインストール手順（Install from Location / シンボリックリンク代替）、既知の制限（コメント未定義・は/と 助詞未登録・固定句未登録・半角スペース不可・LSP 未提供）、設計メモ例文との差異、配布方針を記載。 |

## Invariant Coverage

| ID | Result | Evidence |
| --- | --- | --- |
| INV-001 | PASS | `koto.tmLanguage.json` の top-level `scopeName` が `"source.koto"`、`package.json` の `contributes.grammars[0].scopeName` が `"source.koto"`、`contributes.languages[0].id` が `"koto"`。 |
| INV-002 | PASS | grep audit で § 7 列挙語の出現を全件確認。同時に、未確定構文（コメントマーカー、`は`、`と`、`より大きい`、`要素を`、`各要素について`、`空配列` 等）が grammar に未登録であることを README "既知の制限" でも明示。 |
| INV-003 | PASS | 全てのキーワード／助詞 regex が `(?<=^\|[　。、（）「」])` と `(?=$\|[　。、（）「」])` を持つ。半角スペースは境界文字集合に含まれず、negative smoke test で `関数 として`（半角）が unmatched になることを確認。 |
| INV-004 | PASS | top-level `patterns` の include 順が `strings → numerics → literals → keywords-multi → modifiers → storage-types → keywords-control → particles → punctuation`。`keywords-multi` 内部も長さ降順に並べ、`を返す` が `返す` より、`として終える` が `として` より、`を受け取る` が `を` 単文字助詞より先に評価される。 |
| INV-005 | PASS | `公開`/`非同期`/`外部` は `storage.modifier.{public,async,external}.koto`、`関数`/`オブジェクト`/`定数`/`可変` は `storage.type.{function,object,constant,mutable}.koto` で分離。 |
| INV-006 | PASS | `numerics` パターンは `[0-9]+` のみ。漢数字を含む文字クラスは grammar 全体に存在しない。 |
| INV-007 | PASS | `真` → `constant.language.boolean.true.koto`、`偽` → `constant.language.boolean.false.koto`、`無し` → `constant.language.null.koto`。 |
| INV-008 | PASS | `strings` リポジトリエントリは `begin: 「`、`end: 」` で `patterns` を持たない。TextMate の規約上、内部に sub-pattern を持たない begin/end は内部を再帰トークナイズしない。設計判断として intent に記載。 |

## Deferred / Not Covered

| ID | Reason | Follow-up |
| --- | --- | --- |
| `Developer: Inspect Editor Tokens and Scopes` による個別 scope 名照合 | カテゴリ分離が実機で確認できた時点で本タスクの AC / INV は満たされているため、個別 scope 名（`storage.type.function.koto` 等）の機械的照合までは行わなかった。 | 必要に応じてユーザー側で実施し、差異があれば別 TODO を起こす。 |
| `task-table.koto` / `half-width-boundary.koto` / `max-value.koto` の実機目視 | `incomplete-pickup.koto` の実機確認で grammar 構造の妥当性は十分実証された。残り 3 本は同じ grammar の延長線で挙動が予測可能。 | ユーザーが書き味を継続評価する過程で自然に確認される想定。問題が出たら別 TODO を起こす。 |
| Oniguruma 固有挙動の差分（特に可変長 lookbehind） | 実機ロードで regex compile エラーは起きず、可変長 lookbehind `(?<=^\|[...])` が VSCode 内蔵 Oniguruma で動作することが確認できた。 | 解消済み。 |

## Residual Risks

None

## Follow-up TODOs

- 設計メモ § 4 の例文と § 3-1「分かち書き」原則の不整合（`を例外として終える` などの内部スペース不足）について、メモ側を改訂するか `要素を` / `各要素について` / `可変として` 等の固定句を仕様として正式採用するかを決定する。決定後、本 grammar と intent を更新する（言語設計の継続課題で、本タスクのスコープ外）。
- LSP 着手時に、本 grammar の `source.koto.*` 名前空間と衝突しないセマンティックハイライトを設計する（別 TODO で起票予定）。
- 未登録構文（`は`、`と` 単独助詞、`より大きい`、`空配列` / `空辞書` / `空集合` 等）は仕様確定に合わせて追加する。書き手は「ハイライトされない＝仕様未確定」と読み取る前提の運用とする（INV-002 を維持）。
