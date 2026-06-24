---
title: Grammar v2 entity-name パターン設計判断
status: active
draft_status: n/a
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/plan/Tooling/vscode-koto-grammar-v2/plan.md"
  - "_docs/qa/Tooling/vscode-koto-grammar-v2/test-plan.md"
  - "_docs/intent/Tooling/vscode-koto-grammar/decision.md"
related_issues: []
related_prs: []
---

# Grammar v2 entity-name パターン設計判断

## Context

v1 grammar はキーワード・助詞・記号・リテラルを別 scope に分けたが、識別子は無着色のまま残した。Python の Pylance が提供する「関数名と型名とパラメータ名と変数名を別色化」レベルの richness が、koto では構文の固定性のおかげで TextMate Grammar のパターンマッチだけで相当部分まで届く。

ユーザーから「Python ほどの richness が欲しい。実現可能な範囲で」との要望があり、◯（多少誤検出リスクあり）と ◎（誤検出ほぼなし）の判定に分けて、◯ と ◎ までを v2 のスコープに含めることで合意した。△（フィールドアクセス・メソッド呼び出し・列挙値参照）は LSP の責務として明示的に除外する。

## Decision

- v1 の repository に `entity-names` エントリを追加する。8 個のパターンを置き、specificity 降順に並べる。
- top-level `patterns` の include 順を「strings → numerics → literals → keywords-multi → modifiers → storage-types → keywords-control → **entity-names** → particles → punctuation」に更新する。`entity-names` を keyword 群の後・particles の前に置く。
- すべてのパターンに、v1 と同じ語境界要件（`(?<=^|[　。、（）「」])` または lookbehind の最初のアンカー）を課す。半角スペースを境界として認めない原則は維持。
- scope 名は TextMate の標準命名規約に従い、theme の既存マッピングで色が付くようにする。具体的には:
  - `entity.name.function.koto` — 関数宣言名・関数呼び出し名・コンストラクタ呼び出し名
  - `entity.name.type.koto` — 型名（`である` の前、`を返す` の前、`配列`/`集合`/`辞書` で終わる識別子、オブジェクト宣言名）
  - `variable.parameter.koto` — 関数パラメータ名
  - `variable.other.koto` — 変数束縛名
- △（フィールドアクセス、メソッド呼び出し、列挙値参照、識別子のスコープ追跡）は **v2 で意図的に未実装**とする。INV-002（grammar が言語仕様を先取りしない）を維持しつつ、これらは LSP の semantic token で取り戻す。

### 個別パターンの判断

1. **オブジェクト型宣言名** `(?<=オブジェクト　として　)X(?=　は[、。])` → `entity.name.type.koto`。lookbehind 10 文字（固定長）。Oniguruma は固定長 lookbehind を支障なく扱う。
2. **関数／コンストラクタ呼び出し** `X(?=（)` → `entity.name.function.koto`。`タスク（…）` のようなコンストラクタ呼び出しも同じ scope に寄せる（callable という共通性）。
3. **関数宣言名（fallback）** `X(?=　は[、。])` → `entity.name.function.koto`。1 でカバーされない `関数 として ... 最大値 は、` 系統を拾う。`オブジェクト として ... タスク は、` は 1 が先に match する（specificity）ので type と区別される。
4. **パラメータ名** `(?<=である　)X(?=　を受け取る)` → `variable.parameter.koto`。
5. **変数束縛名** `(?<=である　)X(?=　を　)` → `variable.other.koto`。`を` の後に空白を要求することで `を受け取る` を排除し、4 と 5 を曖昧性なく分ける。
6. **型注釈前** `X(?=　である)` → `entity.name.type.koto`。
7. **戻り値型** `X(?=　を返す)` → `entity.name.type.koto`。
8. **組み込み型サフィックス** `X(?:配列|集合|辞書)(?=$|[　。、（）「」])` → `entity.name.type.koto`。`空配列`、`空辞書`、`空集合` も型扱いになるが、リテラル的な使い方でも視覚上「集合的なもの」と分かるので許容。

### 順序の決定

specificity 降順を原則とする。理由: 同じ位置で複数のパターンが match した場合、TextMate は patterns 配列の先頭側を優先する。より特定的なパターン（lookbehind や lookahead が多いもの）を先に置けば、誤って generic なパターンが先に発火するのを防げる。

具体例: `オブジェクト　として　タスク　は、` の `タスク`:
- パターン 1（specificity 高）が先に match → `entity.name.type.koto`
- パターン 3（fallback）は試されない

## Alternatives

- **identifier 全件を一律 `variable.other` で着色する**: あらゆる識別子に色が付くが、関数／型／パラメータの差が見えない。今回の目的（richness）に反する。
- **`entity.name.koto` を generic な fallback scope として使う**: 非標準 scope なので theme の色マッピングが不確実。`entity.name.function.koto` のような標準 scope を fallback に使うほうが theme 互換性が高い。
- **begin / end の複合パターンで宣言行全体をひと塊で match する**: より正確に書けるが、grammar の構造が大きく変わり、v1 との連続性が崩れる。v2 は v1 の延長線として patterns 追加に留め、構造変更は v3 以降に回す。
- **`定数 として X` を `variable.other.constant` に分ける**: lookbehind が長くなり保守性が落ちる。v2 では `定数` 系も `variable.other` に寄せ、必要なら LSP 段階で取り戻す。
- **フィールドアクセスを `〜　の　X(?=$|[　。、])` で取る**: 助詞 `の` の他用法と区別不能。誤検出が頻発する。意図的に未実装。
- **列挙値参照を `〜　が　X　と同じ` のパターンで取る**: パターンは書けるが、`X` が列挙値か単なる識別子かは型情報がないと判別不能。意図的に未実装。
- **メソッド呼び出しを `〜　の　X(?=（)` で取る**: 助詞 `の` の他用法と区別不能で、かつパターン 2 と競合する。意図的に未実装。

## Rationale

koto は構文上、特定のキーワード／助詞の前後に識別子が現れる位置がほぼ決まっている。Python と異なり「左辺＝代入対象」のような汎用構造ではなく、`である`、`を受け取る`、`を返す`、`とする`、`は[、。]` のような明確なマーカーで囲まれているため、TextMate Grammar のパターンマッチでも識別子の意味分類を高い精度で取れる。

scope 名を `entity.name.function.koto` / `entity.name.type.koto` / `variable.parameter.koto` / `variable.other.koto` という TextMate 標準命名に揃えることで、theme の既存マッピングを利用できる。`entity.name.koto` のような非標準 scope を作ると、theme によっては色が付かない。

specificity 降順を採るのは、TextMate の「先勝ち」ルールに対する自然な対応。lookbehind / lookahead が多いほど match 条件が厳しいので、その厳しいパターンが先に当たれば、より一般的なパターンに落ちる前に正確な分類ができる。

△ を意図的に未実装にするのは v1 INV-002（grammar が言語仕様を先取りしない）の精神を継承するため。フィールドアクセスや列挙値参照のパターンを書こうとすると、必然的に「ここでは `の` を particle として扱わない」「この `X` は型推論で列挙値だと分かる」といった文脈情報が要る。grammar にそれを書き込むと、誤検出か仕様の先取りに陥る。

## Consequences / Impact

- v1 fixture を含むすべての `.koto` ファイルで識別子の richness が増す。退行はしない（パターンが追加されるだけで既存パターンに影響しない）。
- theme 依存で色が変わる。Dark Modern / Default Dark+ などの標準 theme では `entity.name.function` / `entity.name.type` / `variable.parameter` がそれぞれ別色になる想定。`variable.other` は theme によっては無色のまま（識別子と同等）。
- `空配列` / `空辞書` / `空集合` が型色になる。リテラル的な使われ方をするが、視覚上「集合的なもの」と理解できるので許容範囲とする。
- フィールドアクセス・メソッド呼び出し・列挙値参照は識別子色のまま。LSP 段階での補完待ち。これらの未着色は「ハイライトされない＝LSP 待ち or 仕様未確定」という v1 の運用方針と整合する。
- パターン数が 7 → 15 程度に増えるため、grammar ファイルが長くなる。各パターンに `comment` を付けて意図を残す。

## Quality Implications

- v1 INV-002（§7 キーワードのみ登録）は維持する。識別子の着色は §7 キーワード一覧の拡張ではなく、文脈ベースの分類なので独立。
- v1 INV-003（語境界要件）を継承する。新規パターンも語境界 lookbehind を必ず持つ。
- v1 INV-008（文字列内部はハイライト抑制）を継承する。新規パターンは string の begin/end の外でのみ発火する（include 順で `strings` が先頭なので、文字列内部は捕捉されない）。
- パターン追加によって既存トークンの scope が変わってはいけない（退行禁止）。各 fixture の v1 期待 scope を維持しつつ、新規 scope が加わるだけの形にする。

## Intent-derived Invariants

- INV-001: `entity-names` は v1 の `keywords-control` の後、`particles` の前に置かれる（include 順）。
- INV-002: `entity-names` 内のパターンは specificity 降順に並べられ、より特定的なパターンが先に評価される。
- INV-003: すべての `entity-names` パターンは語境界要件（`(?<=^|[　。、（）「」])` または lookbehind の最初に `である　` 等の固定アンカー）を持つ。
- INV-004: scope 名は TextMate 標準命名規約（`entity.name.function.*`、`entity.name.type.*`、`variable.parameter.*`、`variable.other.*`）の `.koto` 名前空間に従う。
- INV-005: フィールドアクセス、メソッド呼び出し、列挙値参照、識別子のスコープ追跡は v2 で grammar に追加されない。これらは LSP 段階の責務とする。
- INV-006: v1 の INV-001 〜 INV-008 はすべて維持される（v2 で退行させない）。

## Enforced in (optional)

- INV-001 / INV-002 / INV-003 / INV-004: `tools/vscode-koto/syntaxes/koto.tmLanguage.json` の `entity-names` repository と include 順。
- INV-005: 同 grammar ファイルに該当パターンが存在しないこと（grep / diff review）と、`tools/vscode-koto/README.md` の「既知の制限」節での明示。
- INV-006: 既存 fixture（`max-value.koto`、`incomplete-pickup.koto`、`task-table.koto`、`half-width-boundary.koto`）の v1 期待 scope が verification で再確認される。

## Rollback / Follow-ups

- Rollback: `entity-names` repository entry と include への参照を削除すれば v1 状態に戻る。
- Follow-ups:
  - LSP 着手時に、フィールドアクセス・メソッド呼び出し・列挙値参照・識別子のスコープ追跡をセマンティックトークンで補完する。
  - 多引数関数の構文が確定したら、パラメータ名パターンを拡張する。
  - `定数 として X` を独自 scope に分けるかは LSP 段階で再評価する。
