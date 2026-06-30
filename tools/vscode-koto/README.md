# vscode-koto

koto 言語の VSCode 用シンタックスハイライト拡張。`tools/vscode-koto/` 配下に拡張一式を置く。

- Plan: [_docs/plan/Tooling/vscode-koto-grammar/plan.md](../../_docs/plan/Tooling/vscode-koto-grammar/plan.md)
- Intent: [_docs/intent/Tooling/vscode-koto-grammar/decision.md](../../_docs/intent/Tooling/vscode-koto-grammar/decision.md)
- QA Test Plan: [_docs/qa/Tooling/vscode-koto-grammar/test-plan.md](../../_docs/qa/Tooling/vscode-koto-grammar/test-plan.md)

## ローカル開発でロードする

1. VSCode で `File: Open Folder...` から本リポジトリを開く。
2. コマンドパレットで `Developer: Install Extension from Location...` を選び、`tools/vscode-koto/` ディレクトリを指定する。
3. `.koto` ファイル（例: `tools/vscode-koto/tests/fixtures/max-value.koto`）を開く。
4. コマンドパレットで `Developer: Inspect Editor Tokens and Scopes` を起動し、トークンが期待通りの scope を持つことを確認する。

代替: 拡張ディレクトリを `~/.vscode/extensions/` 配下にシンボリックリンクしても同様にロードできる。

## 提供範囲

設計メモ § 7「次のステップ」のキーワード一覧をそのまま反映する。スコープ名は `source.koto` 配下に namespace 化する。

- 宣言系: `関数`、`オブジェクト`、`定数`、`可変`、`外部`、`公開`、`非同期`
- 制御系: `もし`、`なら`、`繰り返すと`、`である`、`からなる`、`のいずれか`
- 動作系: `返す`、`として終える`、`して待つ`、`取り込む`、`とする`、`を受け取る`、`を返す`
- 構文系: `として`、`である`、`の`、`が`、`に`、`を`、`から`、`で`、`と同じ`、`そのもの`、`と同種`
- 記号: 鉤括弧 `「」`、全角丸括弧 `（）`、句点 `。`、読点 `、`
- リテラル: 算用数字 `0-9`、`真`、`偽`、`無し`

スコープ名の詳細は [`syntaxes/koto.tmLanguage.json`](./syntaxes/koto.tmLanguage.json) を参照。

### v3: Phase B 確定構文のハイライト追加

Phase B 手書き演習 (Lang-Chore-12) で確定した新 keyword 群を追加。

| 追加カテゴリ | キーワード / 記号 | scope |
|---|---|---|
| 比較演算 | `より大きい` / `より小さい` / `以上` / `以下` / `と異なる` | `keyword.operator.comparison.*.koto` / `keyword.operator.equality.not-equal.koto` |
| 論理結合 | `かつ` / `または` / `ではない` | `keyword.operator.logical.{and,or,not}.koto` |
| 制御 (新) | `について` (match opener) / `について繰り返すと` (loop compound) / `何もしない` (no-op) / `で終える` (異常終了 explicit) | `keyword.control.{match,loop,noop,throw}.koto` |
| パラメータ (連用形) | `を受け取り` | `keyword.operator.signature.parameter.koto` (`を受け取る` と同 scope) |
| 集合 | `に含まれる` | `keyword.operator.set.contains.koto` |
| 終了型 (built-in) | `例外` / `警告` / `通知` | `support.type.builtin.terminal.{exception,warning,notice}.koto` |
| 型 postfix Optional | `？` | `keyword.operator.optional.koto` |
| 列挙記号 | 中点 `・` | `punctuation.separator.list.koto` |

設計メモ §3-19〜§3-26 の Phase B 確定事項に対応する。v1 / v2 の既存パターンに regression なし (boundary 要件を維持、既存スコープを退行させない)。

v3 では Phase B canonical の **tab indent** に合わせ、全パターンの語境界要件に `\t` を追加 (`(?<=^|[　。、（）「」\t])`)。tab 直後の keyword (`\tもし` 等) も正しくハイライトされる。

v3.1 amendment:

- `を返す` の scope を `keyword.operator.signature.return.koto` → **`keyword.control.return.koto`** に変更。`return` 相当の制御フローとして theme 側で control 色 (typically pink) が当たるようにする。`返す` 単独形と同 scope に揃える
- `である` を 2 つの scope に分割:
  - `である` + `。` (関数本体終端、`end` 相当) → **`keyword.control.end.koto`** (control 色、pink)
  - `である` + 全角 space / 他境界 (型注釈マーカー) → 既存の `keyword.operator.type-annotation.koto` (operator 色)
- entity-names の identifier 捕捉パターンから `\t` を除外 (`[^　。、（）「」\t]+`)。tab を識別子の一部として誤捕捉しないようにする

### v2: 識別子の文脈別着色

v2 では識別子も文脈に応じて別 scope で着色する。パーサ／LSP なしで TextMate Grammar のパターンマッチのみで到達できる範囲に限定（intent v2 INV-005）。

| scope | 文脈例 |
|---|---|
| `entity.name.function.koto` | 関数宣言名（`を返す　[X]　は[、。]`）、関数／コンストラクタ呼び出し（`[X]（`） |
| `entity.name.type.koto` | 型注釈（`[X]　である`、`[X]　を返す`）、サフィックス（`〜配列`/`〜集合`/`〜辞書`）、オブジェクト宣言名（`オブジェクト　として　[X]　は[、。]`） |
| `variable.parameter.koto` | パラメータ名（`である　[X]　を受け取る`） |
| `variable.other.koto` | 変数束縛名（`である　[X]　を　…　とする`、`である　[X]　とする`、`）　を　[X]　とする`） |

v2 範囲外（LSP 待ち）:

- フィールドアクセス `〜　の　[X]` — 助詞 `の` の他用法と区別不能
- メソッド呼び出し `〜　の　[X]（` — 同上
- 列挙値参照 `〜　が　[X]　と同じ` — 型推論なしには列挙値と識別子を判別不能
- 識別子のスコープ追跡（宣言時と参照時の同名同色化）

## エディタ既定設定

`.koto` ファイルに対して、以下の VSCode 既定設定を `contributes.configurationDefaults` で `[koto]` スコープに適用する。`.koto` 以外のファイルには影響しない。

### 全角スペース・全角記号の警告抑制

- `editor.unicodeHighlight.invisibleCharacters: false`
- `editor.unicodeHighlight.ambiguousCharacters: false`
- `editor.unicodeHighlight.nonBasicASCII: false`
- `editor.renderWhitespace: "none"`

koto は分かち書き＝全角スペース U+3000 を構文の主軸に据える。VSCode の既定は U+3000 を「不可視文字」として警告し、`renderWhitespace` の既定値も全角スペースを中点風の記号で可視化するが、本言語ではすべての行に多数登場する正規構文要素であり、ノイズが大きい。同様に全角丸括弧・句読点・鉤括弧などの全角記号も `ambiguousCharacters` / `nonBasicASCII` に該当しうるため、まとめて抑制する。

全角スペースを視覚的に確認したくなった場合は、ユーザー側の settings で `[koto]` スコープを上書きする（`editor.renderWhitespace` を `boundary` 等に戻す）。

### インデント・空白保持 (Phase B 確定事項)

- `editor.insertSpaces: false` — インデントは tab 文字を使う
- `editor.detectIndentation: false` — 既存ファイルからの自動検出を無効化（tab で固定）
- `editor.tabSize: 4` — tab を 4 文字幅で render
- `files.trimTrailingWhitespace: false` — 行末の trailing whitespace を保存時に削除しない

koto では文字種で 2 つの役割を分離する:

- **全角スペース U+3000** = token separator（唯一の正式な token 区切り）
- **tab 文字** = indent（視覚レイアウト、semantic な役割なし）

trailing 全角 space は token 区切りとして意味を持つため、editor の「行末空白削除」機能で消されると syntax 上の意味が変わってしまう。これを防ぐため `files.trimTrailingWhitespace: false` を必須に設定する（多くの editor の trailing whitespace 削除は ASCII space 専用だが、念のため明示的に無効化）。

`editor.tabSize` の幅 (4) は表示の好みなので、ユーザー側 settings で `[koto]` スコープを上書きして変更してよい。

## 全角スペース可視化フォントとの相性

UDEV Gothic や HackGen 等、全角スペース U+3000 を点線枠などで可視化することを設計目的に含む系統のフォントを使用している場合、koto では分かち書き＝全角スペースが構文の主軸要素であるため、フォントの可視化機能が情報ノイズに転じる。

UDEV Gothic 系列では、可視化を行う variant の名前中の `NF`（Nerd Fonts）を `HS`（Hidden Space）に差し替えた variant が配布されており、全角スペースは他フォントと同様に通常描画になる。例:

- 可視化あり: `UDEV Gothic 35NFLG`
- 可視化なし: `UDEV Gothic 35HSLG`（`NF` の位置に `HS` が入る命名）

### 対処の選択肢

#### A. koto のときだけ可視化なし variant に切り替える（局所的）

他のコード（TypeScript・Dart 等、全角混入を視認したいファイル群）では従来の可視化を保ったまま、`.koto` だけ可視化なし variant に切り替える方法。ユーザー側の `settings.json` で `[koto]` スコープに `editor.fontFamily` を上書きする:

```jsonc
"editor.fontFamily": "'UDEV Gothic 35NFLG'",
"[koto]": {
  "editor.fontFamily": "'UDEV Gothic 35HSLG'"
}
```

primary が CJK 対応フォントになるため、日本語も primary で描かれ、fontconfig の fallback を経由しない。fontconfig の状態に依存せず確実に効く。

#### B. fontconfig の日本語 fallback を可視化なし variant にする（大域的）

Linux 環境で全 GUI アプリでの全角スペース可視化を一律に解除したい場合は、ユーザー fontconfig で日本語 fallback の先頭を HS variant に変える。`~/.config/fontconfig/fonts.conf`（既存ファイルがあれば追記）:

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <match target="pattern">
    <test name="lang" compare="contains"><string>ja</string></test>
    <edit name="family" mode="prepend"><string>UDEV Gothic 35HSLG</string></edit>
  </match>
  <alias>
    <family>monospace</family>
    <prefer><family>UDEV Gothic 35HSLG</family></prefer>
  </alias>
</fontconfig>
```

保存後 `fc-cache -fv` を実行し、VSCode を**完全終了→再起動**（Reload Window ではなく）。Chromium のフォントキャッシュは reload では消えない。検証は:

```bash
fc-match :lang=ja                 # UDEV Gothic 35HSLG が返ればよい
fc-match 'monospace:lang=ja'      # 同上
```

VSCode の `editor.fontFamily` が DejaVu Serif や monospace のような欧文／alias であっても、日本語部分は fontconfig の fallback が拾うため、ここを HSLG に変えれば koto 含むすべてのファイルで全角スペース可視化が消える。

### 拡張側でフォントを既定しない理由

本拡張は `configurationDefaults` でフォントを指定しない。HS variant のインストール状況や、可視化フォントを使うかどうかはユーザー環境とポリシーの領域であり、拡張から前提を押し付けないため。

## 既知の制限

設計メモ § 7 に列挙されたキーワード「のみ」を登録する（intent INV-002）。grammar が言語仕様を先取りすると設計議論の自由度が下がるため、未確定の構文は意図的に未対応とする。

- **コメント構文は未定義**。`#`、`//`、`--` などは何の意味も持たない。設計メモで構文が確定したら追加する。
- **`は` 助詞は未登録**。`〜 は、` の `は` は識別子色のままになる。設計メモ § 5 未決定 #5「受動態の扱い／主題に意味を持たせるか」が決着するまで保留。
- **`と` 助詞は未登録**。`A　と　B　を　加える` の `と` は識別子色のまま。`と同じ`、`と同種`、`として` の構成要素としてのみ扱う。
- **`より大きい`、`より小さい` などの比較表現は未登録**。設計メモに正式な比較構文の記載がない。
- **`要素を`、`各要素について` は固定句として未登録**。設計メモ § 3-9 の繰り返し構文には言及があるが § 7 のキーワード一覧には載っていない。本拡張は § 7 に厳密準拠する。
- **`空配列`、`空辞書`、`空集合` はリテラル扱いにしない**。識別子として扱われる。設計メモ § 7 のリテラル一覧に含まれていない。
- **半角スペースは語境界として認めない**（intent INV-003）。設計メモ § 3-1「分かち書きは全角スペース」に従う。半角スペース区切りで書かれたキーワードはハイライトされない。
- **ジェネリクス・パターンマッチ・Optional 型（「たぶん〜」）は未登録**。仕様が未確定。
- **セマンティックハイライト（型・変数の意味別色分け）は提供しない**。LSP の責務とし、別タスクで扱う。

## 設計メモの例文との差異

設計メモ § 4 の例文の一部は § 3-1 の「分かち書きで単語を区切る」原則に対して内部空白が不足している箇所がある。たとえば:

- メモ表記: `を例外として終える。` → 本拡張で期待する表記: `を　例外　として終える。`
- メモ表記: `各要素について繰り返すと` → 本拡張で期待する表記: `各要素について　繰り返すと`
- メモ表記: `可変として` → 本拡張で期待する表記: `可変　として`

本拡張は § 3-1 原則に厳密準拠する。`tests/fixtures/*.koto` は正規化された分かち書きで書き直してある。設計メモ側を原則に合わせて改訂するか、メモの表記を仕様として正式採用するかは、言語設計の継続的課題として残す（intent の Open Questions を参照）。

## 手動検証ポイント

QA test-plan の Test Matrix と Manual QA Checklist を参照。特に以下を `Developer: Inspect Editor Tokens and Scopes` で確認する。

- `tests/fixtures/max-value.koto`: 宣言系・制御系・動作系・構文系の各群がそれぞれ異なる scope に配色される。
- `tests/fixtures/incomplete-pickup.koto`: 列挙値参照 `未完了` が単なる識別子として扱われ（型推論不要のため）、`と同じ` が等価判定 scope を持つ。
- `tests/fixtures/task-table.koto`: 複合名詞型 `文字列とタスクの辞書` が一塊の識別子として扱われ、内部の `と` / `の` がハイライトされない。
- `tests/fixtures/half-width-boundary.koto`: 半角スペース区切りでキーワードがハイライトされない、識別子内の同字（`関数記録`、`今の数`、`関連の数`）が誤検出されない、文字列リテラル内部のキーワード字列がハイライトされない。

## ロードマップ

- LSP 着手時にセマンティックハイライト・診断・補完・定義ジャンプを追加する。`source.koto.*` 名前空間は LSP との衝突を避けて予約済み。
- コメント・ジェネリクス・パターンマッチ等の仕様確定に応じて intent の Alternatives を更新し、grammar を追加する。
- 自動 grammar テスト（`vscode-tmgrammar-test` 等）の導入是非は言語仕様が一定固まった段階で再評価する。

## 配布方針

VSCode Marketplace への登録はしない。リポジトリ内の開発者が「Install from Location」でロードする運用とする。問題があれば拡張をアンインストールするだけでロールバック可能。
