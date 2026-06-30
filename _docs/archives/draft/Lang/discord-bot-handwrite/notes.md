---
title: Discord bot 手書き演習 観察ノート (archived)
status: archived
draft_status: n/a
created_at: 2026-06-25
updated_at: 2026-07-01
archived_at: 2026-07-01
references:
  - "_docs/standards/japanese-lang-design-memo.md"
  - "_docs/archives/draft/Lang/discord-bot-handwrite/handler.koto"
  - "_docs/archives/draft/Lang/discord-bot-handwrite/sample-1.koto"
  - "_docs/archives/draft/Lang/discord-bot-handwrite/sample-2.koto"
related_issues: []
related_prs: []
---

<!-- Canonical path: _docs/archives/draft/Lang/discord-bot-handwrite/notes.md -->
<!-- Archived: 2026-07-01 — Phase A/B 確定事項は `_docs/standards/japanese-lang-design-memo.md` §3-1〜§3-26 に統合済み。本ファイルは設計史を辿るための歴史資料。正本ではない。 -->

## ⚠️ Archive Notice (2026-07-01)

このファイルは **archive 済み** です。

- **Phase A/B (Lang-Chore-11 / Lang-Chore-12) の手書き演習で確定した spec 変更と未決着論点は、`_docs/standards/japanese-lang-design-memo.md` (§3-1〜§3-26、§5) に統合済み**
- 本ファイルは **設計史を辿るための歴史資料** として保存されている。正本ではない
- 現在の koto 仕様を参照する場合は、必ず memo 側を参照すること
- 同梱ファイル (`handler.koto`、`sample-1.koto`、`sample-2.koto`) も同じく歴史資料
- Phase A/B の議論経過 (なぜ各 spec がこの形になったか) を辿りたい場合のみ本ファイルを開く

---

<!-- 設計メモ §7「その後 1」に基づく手書き演習の観察ログ。動かないコードを書きながら、書き味の違和感・spec の欠落・思考フレームへの作用を記録する。-->

## Purpose

設計メモ §1 が掲げる主目的「日本語ドリブンでプログラムを書くと、思考フレームがどう変わるか」を、Discord bot コードを手書きすることで観察する。動作させることが目的ではない。

## Method

- Phase A: ハンドラ関数 1 個（`!ping` → `pong`）。コードは `handler.koto`。
- Phase A 拡張: 別文脈での手書き（架空サービスの `投稿する` 関数）。コードは `sample-1.koto`。Phase A の発見を踏まえてより踏み込んだ構文を試している。
- 書く人: プロジェクト author（ユーザー）
- 支援: assistant が設計メモ参照・spec 未定義箇所の指摘・違和感のログ整理を担当
- 書き終わったら本ノートを一緒にレビューし、Phase B / spec 詰め / parser 着手のどれに進むかを判断する

## 演習指示 (Phase A)

題材は「`!ping` メッセージを受け取ったら `pong` と返信する」ハンドラ関数 1 つ。書く場所は本ノートと同ディレクトリの `handler.koto`。動かす必要はないので、未定義の関数や型を仮の名前で参照しても構わない。

### 想定する API shape

discord.py / discord.js どちらの慣習でも構わない。ここでは shape の例として:

- `メッセージ` 型のオブジェクトが渡される
- `メッセージ の 内容` で送信文字列が取れる（文字列型）
- `メッセージ に [文字列] を返信して待つ` で返信できる（async）

これらが「外部 オブジェクト として」で宣言されている前提で扱ってよい（宣言ファイル自体は本演習では書かない）。

### 書きたい要素

- 非同期関数の宣言
- パラメータの型注釈
- 戻り値なし（何も返さない）
- フィールドアクセス
- 文字列比較
- 条件分岐
- await

## 演習指示 (Phase B)

題材は「`!ping` / `!echo X` / `!time` の 3 コマンドを 1 つの dispatcher で受ける Discord bot ハンドラ」。書く場所は `sample-2.koto`。動かす必要はないので、未定義の関数や型を仮の名前で参照して構わない。

### 想定する API shape

Phase A と同じ前提に加えて:

- `メッセージ の 内容` で送信文字列（文字列型）が取れる
- 文字列に対して以下が呼べる想定（仮定義、書きながら必要なら追加）:
  - `〜 が 〜 で 始まる`（boolean predicate）
  - `〜 の 〜 番目以降`（substring 抽出）
  - `〜 と 〜 の 連結`（concat）
- 現在時刻取得: `現在時刻（時差 が ..., フォーマット が ...）` のような free function（sample-1 で出現済み）

### 期待する動作

- `!ping` → `pong` を返信
- `!echo [text]` → `[text]` をそのまま返信（`!echo こんにちは` なら `こんにちは` を返信）
- `!time` → 現在時刻を文字列で返信
- 上記いずれにも該当しないメッセージ → 何もしない

### 観察したい要素（書きながら出てきそうな spec gap）

意図的に未定義のまま臨む。書く中で「これどう書くんだろう」と感じる箇所をそのまま記録する:

- パターン分岐: `もし...なら` の連鎖で書くか、何か match 風構文を期待するか
- 文字列の前方一致 predicate の自然な書き味
- 文字列の部分抽出構文
- コメント構文（`＃` 仮使用が続くか、別の何かが欲しくなるか）
- 辞書リテラル（コマンド名 → ハンドラの mapping を辞書で書きたくならないか）
- Optional 型と narrowing の実例（メッセージ内容が `null` の場合の扱い等）

### 進め方

Phase A と同じ。詰まったら言ってもらえれば、設計メモを照合しつつノートに整理する。

## Observations

時系列で並ぶ。書く本人の主観 + 議論で出てきた観察を混在。原文の ＃ コメントは `handler.koto` / `sample-1.koto` を参照。

### Phase A (handler.koto)

- 型名とパラメータ名に同じ語を選んでしまう（`インタラクション である インタラクション`）。日本語だと型と変数を別語にする摩擦が大きい（英語の大文字小文字での差別化がない）。**思考フレームへの作用の証拠**。
- カタカナ音写を躊躇なく採用（`ピン`、`ポン`、`インタラクション`）。設計メモ §6「概念は輸入品」を体現。和語化を強制していない。
- メソッド連鎖を `の` で自然に組み立ててしまった（`インタラクション の レスポンス の メッセージを送る`）。Python の `.` チェーンが日本語化されただけで、思考フレームは Python のまま。
- コメント構文が未定義のため、`＃`（全角）を私的に発明した。
- void return の終端形が不明。`である。` で閉じるイメージを持っていたが、メモには明示なし。

### Phase A 拡張 (sample-1.koto)

- 「文の構造を運ぶ」感覚で書いてみた。具体的には `関数 として、 [parameters chained with 連用形 + 、]、戻り値型 を 返す 関数名 は、 [body]` という形が自然に出てきた。
- 関数本体内の statement が `。` で完結する一方、ヘッダ内の繰り返し（パラメータ列挙）は 連用形 + 、 で続く。`、` と `。` の使い分けに意味が出てきた。
- 多行版で書いていると 連用形 + 、 を反射的に入れてしまうが、`として` の後の 、 は文法的に不要だった（手癖）。視覚的にインデントを使えば事足りる。
- 関数の全体（特にシグネチャ）を「一つの日本語の文」として書きたくなる。一行版（`公開 関数 として 文字列 である X を受け取り、... 文字列 を 返す 投稿する は、 [body] である。`）が成立することは、構造の中核。
- 構文上 statement は数行で長くなることが多いので、二重インデントは現実的にきつい。「、 なし行は visual indent を閉じる」という規約で対応したい意図がある（実装はパーサが indent 非依存である限り、書き手側の運用慣習）。
- 比較表現（`より大きい`）が自然に出るが、メモには `と同じ` 系しかない。
- 辞書を直接リテラルで書きたい場面でフォーマットを思いつかない。
- IME 変換で `真` が出にくい。`はい` も意味が違うので、現状の `真` で固定。

## 確定した spec 変更

ここまでの議論で決まった事項。設計メモ更新時の入力になる。各項目に `(memo にすでにある／確認のみ)` `(memo にあるが今回変更)` `(memo にない、新規追加)` を付ける。

### 構造的ルール

- **句読点が節の状態を運ぶ**: 、 = 継続（次に何か続く）、 。 = 完結。 (新規追加)
- **動詞は対応する活用形を取る**: 、 の前は連用形（`受け取り`、`して`、`なら`、`繰り返すと`、`をして待つ`）、 。 の前は終止形（`受け取る`、`返す`、`例外として終える`、`である`、`保存する`）。 (新規追加)
- **`である` は活用形不変** で 2 役を担う: 型注釈マーカー（`〜 である 〜`）と節終結 copula（`である。`）。 (memo にあるが意味付けを補強)
- **、 の細分（列挙区切り vs 構造的遷移）は spec で分けない**。書き手の感覚に任せ、運用で必要が出たら線を引く。`として` 等の連用形が verbal か marker かの分類も同様に保留。 (新規追加)
- **インデントは視覚のみ**。メモ §3-1 を踏襲。単一行版が成立することは sample-1.koto line 84 で実証済み。 (memo にすでにある／確認のみ)
- **全角 space (U+3000) は token 区切りの唯一の正式 separator**: newline と indent は purely visual で、token を区切る semantic role を持たない。multi-line で書く場合も token 境界には全角 space を必ず維持する (trailing 全角 space を含む)。これにより単一行 ⇔ 多行の変換が機械的・無損失。lexer / parser は全角 space のみを separator として認識する。memo §3-1 (分かち書き) を厳密化。 (新規追加)
  - **canonical indent: tab**。tab 文字を indent に使う (半角 space ではなく tab)。全角 space (token separator) と tab (indent) を文字種で役割分離。
  - editor 設定上の含意: trailing 全角 space を消さないこと (`files.trimTrailingWhitespace: false` の `[koto]` scope 設定が必要)。VSCode extension に default として組み込む。
- **変数束縛の canonical 形**: `[Type 修飾] [Type] である [変数名] を [値] とする。` (`を` 形のみ canonical)。topic 形 `〜 は 〜 とする` は不採用 (vocabulary 固定原則、consistency)。既存の `〜 を 返す。` / `〜 を 受け取り、` / `〜 を Y として 取り込む。` 等と `を` で一貫。 (新規追加)
- **compound keyword は内部 space なし**: particle + verb が一塊で機能する koto の predicate / control-flow 関連 keyword は、内部に space を入れない (compound keyword として扱う)。 (新規追加)
  - 該当例: `として取り込む` / `を受け取り、` / `を返す` / `として終える` / `で終える` / `について` / `について繰り返すと` / `何もしない` / `と同じ` / `より大きい` / `のいずれか` / `に含まれる` / `である` 等
  - 「助詞で意識させる」目的は koto 全体の **token 間 space** (`X が Y` 形式) で既に実現されている。compound keyword 内の space は redundant
  - vocabulary 固定原則 (memo §3-1) と統合

### 関数シグネチャ

- **シグネチャは「ヘッダ節」**として 1 つの日本語のまとまりを構成: `[修飾] 関数 として [パラメータ列挙] [戻り値型] を 返す [関数名] は、`。 (新規追加)
- **複数パラメータは `を受け取り、` で連結**。連用形 + 、。 (新規追加。memo §7 は `を受け取る` 終止形を辞書形として記載しているが、実用上はほぼ連用形）
- **戻り値型は必須**。void なら `無し を 返す` を明示（撤回: 「optional」とした暫定方針）。 (memo にない、新規追加)
- **`受け取る` 終止形は単独使用の場面が限定的**。dictionary form として残すが、grammar に連用形 `受け取り` を追加登録する必要あり。 (memo にあるが今回変更)

### 関数本体の終端 / 早期終了

- `である。` が正式（言語史的に唯一の終端だった）。 (新規追加: memo に正式採用と明記)
- `〜 を 返す。`（`無し を 返す。` 含む）も許容。 (memo にすでにある／確認のみ)
- 本体が継続節（〜、）で終わるなら `である。` で閉じる、return で終わるなら return の `。` で完結。 (新規追加)
- **早期終了 (early exit)**: (新規追加)
  - **戻り値なしの関数** (`無し を 返す` 関数): mid-body `である。` で関数を即終了させる。「ここで関数本体が終わる」という意味論を mid-body にも適用する。専用 keyword は導入しない。
  - **戻り値ありの関数**: mid-body `〜 を 返す。` で値付き早期 return。
- **`ここまで。` のような専用 early-exit keyword は不採用** (`である。` で十分、keyword の重複を避ける、vocabulary 固定原則)。

### メソッド・OOP

- **メソッドは採用しない、自由関数のみ**（メモ §3-11 の「将来追加」は不採用へ確定）。 (memo にあるが今回変更)
- `の` は field access と module navigation のみ。method dispatch では使わない。 (memo §3-16 を限定して明文化)

### 引数

- 位置引数と キーワード引数（`フィールド名 が 値`）の両対応。関数呼び出し・コンストラクタ呼び出しで共通形。 (memo §3-11 のフィールド初期化形を関数呼び出しにも一般化、新規追加)

### 型・リテラル

- `無し` = void 型。 (新規追加)
- **`無し` は unit 型の唯一の値**。void return（`無し を 返す`）も Optional の「無いほう」も同じ `無し` を使う。型システムが文脈を強制する（C 方針確定）。 (新規追加)
- **`T？` = Optional T**。`数値配列？`、`文字列？`、`タスク？` 等。`？` は全角 (U+FF1F)。memo §3-3 の `たぶん〜` 候補は撤回し、`〜？` 記号 suffix を採用。 (memo にあるが今回変更)
- **非 Optional 値の null 比較は型エラー**。`T である X` で `X が 無し と同じ` を書くと、型システムが拒否する（または warning）。 (新規追加)
- **flow-sensitive type narrowing 採用**。`もし X が 無し と同じ なら、〜 として終える。` の後、X は `T？` から `T` に narrow される（escape パターン）。「肯定 narrowing パターン」（条件式内で narrow する形）は構文未確定として保留。 (新規追加)
- `T？？` のような二重 Optional は禁止（無意味）。仕様 / 型チェッカーで防ぐ。 (新規追加)
- `？` は Optional 専用。述語関数名（`〜か`、`空である` 等）には使わない。Ruby / Clojure 流の `存在する？` のような identifier suffix は許さない。 (新規追加)

### 条件式の語彙

- **等価判定（`と〜` 族）**:
  - `X が Y と同じ` (==、memo 既存)
  - `X が Y と異なる` (!=、新規追加。compact form として常用)
  - `X が Y と同種` (same type、memo 既存)
  - `X が Y そのもの` (is、memo 既存。`と` を伴わない)
- **順序比較**:
  - `X が Y より大きい` (>) — sample-1 で出現、確定
  - `X が Y より小さい` (<) — symmetry で追加
  - `X が Y 以上` (≥) — 含む不等号
  - `X が Y 以下` (≤) — 含む不等号
  - `未満` / `超える`（同義語）は採用しない（memo §3-1 の語彙固定）
- **論理結合**:
  - `〜 かつ 〜` (AND)
  - `〜 または 〜` (OR)
  - `〜 ではない` (NOT、条件式末尾に付加する汎用否定。`である` の対の copula として一塊で扱う)
- **真偽値の比較は明示**: `もし X が 真 と同じ なら、〜` / `もし X が 偽 と同じ なら、〜`。暗黙の `もし X なら、〜` は採用しない。 (新規追加)

### 条件式の優先順位

優先順位（高→低）:

1. 比較演算（`と同じ` / `と異なる` / `と同種` / `そのもの` / `より大きい` / `より小さい` / `以上` / `以下`）
2. `ではない`（否定。直前の単一比較式に attach）
3. `かつ` (AND)
4. `または` (OR)

同レベル内は **左結合**（左から右に評価）。

- `A かつ B または C` → `(A かつ B) または C`
- `A かつ B かつ C` → `(A かつ B) かつ C`
- `A かつ B ではない` → `A かつ (B ではない)`
- `ではない` は単一比較に attach、複合全体への否定は採用しない（De Morgan で書き換えるか節分割）

### grouping 不採用（条件式の括弧）

`（A かつ B）または C` のような括弧グルーピングは **採用しない**（確定）。

理由:
- 自然日本語の話し言葉に grouping 記号がない（書き言葉の技術文書には存在するが、「読める」レベルで「流れるように読める」ではない。koto は後者を目指す）
- ネストするほど複雑な条件式はそもそも書くべきではない（書き手の意図が曖昧）
- 中間概念に名前を付けて節分割するか、De Morgan で書き換えるほうが Japanese flow に乗る
- `(A or B) and C` レベルでも `A か B のいずれか、なおかつ C` のような分解 / 書き換えのほうが読みやすい

複雑な条件が必要な場合:

```
# 節分割
もし 条件A ではない なら、〜 として終える。
もし 条件B なら、〜

# 中間の真偽値変数
真偽値 である 既登録ユーザー を　{ユーザー が 無し ではない かつ ユーザー の 状態 が 有効 と同じ}　とする。
もし 既登録ユーザー または 招待リンクからのアクセス なら、〜
```

（後者の `{ }` は仮表記。実際には変数束縛構文で書く）

### 論理結合 vocabulary (Phase B で確定)

Phase B 完了時点で以下を canonical 確定:

- **boolean 論理結合**: `かつ` (AND) / `または` (OR) / `ではない` (NOT) のみ canonical。`もしくは` / `なおかつ` 等の口語的 alternative は **不採用**。 (vocabulary 固定原則 memo §3-1)
- **value-level disjunction**: `〜 のいずれか` (修飾形) / `〜 に 含まれる` (predicate 完結形) を採用 (集合 disjunction の章を参照)。`または` を value 位置で使う形は **不採用**。

### import

- `〜 から X を 取り込む。` — 特定名 import。 (memo にすでにある／確認のみ)
- `〜 から X、Y を 取り込む。` — 複数名 import。 (memo にすでにある／確認のみ)
- `〜 を Y として 取り込む。` — モジュール別名 import（Python `import x as y` 相当）。 (新規追加)
- `〜 として 全て取り込む` は撤回。 (議論経過の記録: 一度提案したが、`〜 を Y として 取り込む` で必要を満たすと判断)

### `の` chain（field access / module navigation / type-as-namespace、深さ制限あり）

- **`の` の役割は 3 つ**: field access、module navigation、type-as-namespace（type を関数や定数の置き場として使う）。構文形は共通の `LHS の RHS [の RHS ...]`、LHS の種類で意味が決まる。 (新規追加)
- **深さ制限**: `の` chain は **module / type 境界を 1 回まで** しか跨げない。深く navigate したい場合は import を深くする。 (新規追加)
  - 例: `ディスコード の ギルド の 有効コマンド一覧(...)` ❌ → `「../ディスコード/ギルド」 を ギルド として 取り込む。` の上で `ギルド の 有効コマンド一覧(...)` ✅
  - 理由: import を「状況設定」として明示化、call site を短く保つ、`の` chain の意味論を単純化、依存追跡を明確化
- **意味論ルール** (parse 後の type check で enforce):
  - `value の field` → field access、OK
  - `value の field の field の ...` → 多段 field 鎖、OK（data structure を辿るのは自然、深さ制限の対象外）
  - `value の function(...)` → **instance method dispatch、禁止**
  - `module の function(...) / module の type / module の constant` → namespace lookup（1 回）、OK
  - `type の function(...) / type の constant` → associated free function / static constant（1 回）、OK（type を namespace として使う、Rust の `impl` 内 関連関数に近い）
  - `module の module の thing` → namespace lookup 2 回、❌ → import を深くする
  - `module の type の constant/function` → 同上、❌ → import を深くする
  - `namespace の field の function(...)` → 最終的に value から function 呼び出し、method dispatch なので ❌
- **判定表**:

| chain 形式                            | 判定 | 理由                                     |
|---------------------------------------|------|------------------------------------------|
| `value の field`                      | ✅   | field access                             |
| `value の field の field の ...`      | ✅   | data structure 鎖                        |
| `value の function(...)`              | ❌   | instance method dispatch                 |
| `module の function(...)`             | ✅   | namespace lookup (1 回)                  |
| `module の type`                      | ✅   | 同上                                     |
| `type の constant / function(...)`    | ✅   | 同上 (type-as-namespace)                 |
| `module の module の thing`           | ❌   | namespace lookup 2 回 → import を深く    |
| `module の type の constant`          | ❌   | 同上                                     |
| `namespace の field の function(...)` | ❌   | 最終 step が method dispatch             |

- **「メソッド不採用」の正確な定義**: instance に bound dispatch される形式（`value の function(...)`）のみを禁止。type が namespace として free function を公開するのは OK（ただし chain 深さ制限内）。memo §3-11 の「メソッド不採用」を狭く解釈する形で確定。 (新規追加)
- **典型例**:
  - `ギルド の 有効コマンド一覧（ギルド番号 が X）` — file-based module から free function 呼び出し（sample-2 line 19 の意図、import 側を深くするのが canonical）
  - `数値 の 最大値` — 型の静的定数
  - `メッセージ の 内容 の 長さ` — 多段 field 鎖
  - `メッセージ の 内容` — instance の field access
  - `メッセージ の 削除する（）` — ❌ instance method、書けない（自由関数 `メッセージを削除する（メッセージ が X）` 等に書き換え）
  - `ディスコード の ギルド の 有効コマンド一覧（...）` — ❌ namespace lookup 2 回（import 側を `「../ディスコード/ギルド」 を ギルド として取り込む。` に深めて 1 回にする）
- **namespace conflict 時の canonical 解法**: `「..」 を Y として 取り込む。` で alias 取り込み → `Y の 関数(...)` で qualify する。TypeScript / Rust / Python / Go 共通パターン。既存 import 構文で十分カバー。 (新規追加)
- **parse vs check の分業**: parse 時は `LHS の RHS [...]` を構文的に許容、type check で LHS の種類（value / module / type）、RHS の使われ方（field 参照 / function 呼び出し）、namespace 境界を跨ぐ回数を検証して illegal を拒否する。

### property access (immutable binding 上の field-syntax derived value)

- **適用範囲: built-in 型のみ**。user 定義型は宣言された field のみアクセス可能、派生値は free function を使う。user 定義型での derived property は未決着論点に保留 (Phase B 以降のニーズで再検討)。 (新規追加)
- **binding mutability の制約**: property syntax は **immutable binding 上でのみ** 使える。`可変 として` で宣言された binding には適用されず、free function `関数名(値)` を使う。 (新規追加)
  - 理由: mutable binding 上で `value の derived` を許すと、同一式内で derived 値が変化する surprise が起こる (`X の 長さ + X の 長さ` で X が変わると 2 値が異なる) 。immutable に限定することで構造的に防ぐ。
- **意味論**: 概念的には「定義時に派生値を計算してフィールドとして保持」。実装は lazy + memoize でも eager pre-compute でも、observable には同じ。 (新規追加)
- **アクセス syntax**: 通常の field access と区別なし。`X の 長さ` のように `の` chain で書ける。`の` chain の深さ制限 (前述) もそのまま適用 (field 鎖はいくらでも OK、namespace 境界 1 回まで)。 (新規追加)
- **「メソッド不採用」原則との関係**: property は parameterless / pure / 名詞句 で読める derived value。implicit self を取って args を持って dispatch される method とは別物。`の` chain ルール (value の field 形) の自然な拡張として扱う。本質的にメソッドではない、と整理。 (新規追加)
- **inclusion criteria** (built-in property を増やすときの目安):
  1. **常に定義される** (failure mode なし、Optional 返さない)
  2. **計算が conceptually trivial** (metadata 的、transformation ではない)
  3. **noun として読める** (`〜 の 長さ` は noun、`〜 を 大文字化` は verb)
  4. **戻り値型が原値より simple** (構造のメタ情報、子要素、子型、等)
- **built-in 型ごとの property 一覧 (初版 draft、実コード経験で追加 / 削除)**:

  | 型       | property | 戻り値型 |
  |----------|----------|----------|
  | 文字列   | 長さ     | 数値     |
  | 配列     | 要素数   | 数値     |
  | 日付     | 年       | 数値     |
  | 日付     | 月       | 数値     |
  | 日付     | 日       | 数値     |
  | 日付     | 曜日     | 列挙型   |
  | 時刻     | 時       | 数値     |
  | 時刻     | 分       | 数値     |
  | 時刻     | 秒       | 数値     |
  | 日時     | 日付部   | 日付     |
  | 日時     | 時刻部   | 時刻     |

  `空である` / `先頭文字` / `最後の要素` 等の failure mode を持つもの・predicate 系は property に含めず、predicate function / Optional 返り関数として実装。

- **mutable / 派生 / user 定義型での代替手段**: `要素数(配列)` / `長さ(文字列)` のような free function を使う。built-in 型でも mutable binding なら同じ。
- **vocabulary 補足**: 同じ概念に対して string は `長さ`、array は `要素数` と分ける (vocabulary 固定原則 memo §3-1 に従い、混同を避ける)。

### indexed accessor (配列・文字列の位置 access)

- **構文形**: `[配列 or 文字列] の [N 番目 / N 番目以降 / N 番目以前 / N 番目から M 番目まで]`。`の` chain 内の特別 form として parser が認識。 (新規追加)
- **インデックスは 1-indexed**: `1 番目` が先頭。`0 番目` は不採用 (人間的に自然な番号付け)。
- **inclusive のみ採用、exclusive 不採用**: 比較演算で `以上`/`以下` のみ採用し `未満`/`超える` を不採用とした方針と整合。exclusive 形 (`より後` / `より前`) は採用しない。表記揺れ問題も自動的に消える。 (vocabulary 固定原則 memo §3-1)
- **アクセサ一覧**:

  | form                          | 意味                       |
  |-------------------------------|----------------------------|
  | `〜 の N 番目`               | 単一要素 (1-indexed)        |
  | `〜 の N 番目以降`           | N 以降全部                  |
  | `〜 の N 番目以前`           | 1 から N まで (inclusive)   |
  | `〜 の N 番目から M 番目まで` | N から M まで (inclusive)   |

- **戻り値型**:
  - 単一要素 `N 番目`: 元要素の型 + `？` (Optional) — out-of-bounds は `無し`
  - 範囲アクセサ (`N 番目以降` 等): 元の collection 型 (配列 → 配列、文字列 → 文字列)。out-of-bounds は空 collection
- **適用範囲**: 文字列・配列 の built-in 機能。順序のない collection (辞書 / 集合 等は将来) では別 access 方法。
- **exclusive を書きたい場合**: operand を ±1 して inclusive 形に書き換える (`5 番目より後` → `6 番目以降`)。

### no-op (`何もしない。`)

- **構文形**: `何もしない。` — Python の `pass` 相当の no-op statement。 (新規追加)
- **使う場面**: if / match の body で「条件にマッチしたが何もせず通過させたい」とき。空 body よりも意図が明示される。
- **戻り値なし** (statement、expression ではない)。

### 型の postfix 修飾子合成

- **構文形**: 型修飾子は postfix で適用し、左→右に累積的に包む。 (新規追加)
- **修飾子 (現状確定)**:
  - `？` (Optional): `T？` = `Optional<T>`
  - `配列` (Array): `T配列` = `Array<T>`
- **合成例**:

  | 表記             | 意味                                  |
  |------------------|---------------------------------------|
  | `文字列`        | string                                |
  | `文字列？`      | Optional<string>                      |
  | `文字列？配列`  | Array<Optional<string>>               |
  | `文字列配列？`  | Optional<Array<string>> (順序で意味が変わる) |
  | `文字列配列？配列` | Array<Optional<Array<string>>> (3 段) |

- **任意 depth で合成可能**: 修飾子を後置するだけ。書かれた順序が型の包み構造を決める。
- **practical guidance**:
  - `配列？` (`Optional<Array>`): 「配列ごと存在しないかもしれない」 — 普通の use case (HTTP の optional クエリ、API の optional field 等)
  - `要素？配列` (`Array<Optional<要素>>`): 「配列はあるが個別要素が欠けている可能性」 — 稀。配列要素 への index access は自動で `Optional<T>` を返す (上述 indexed accessor の戻り値型) ため、明示的に `Array<Optional<T>>` を作る必要はほぼない
- **sample-2 line 52 の `文字列？配列 である 渡された引数ら` は spec ではなく書き手の判断ミス**: 引数が無い場合は **長さ 0 の `文字列配列`** で表現する方が筋。書き換え推奨。
- **将来追加予定の修飾子**: `辞書` / `集合` / `タプル` 等は登場時に追加。

### predicate / comparison の構文と実装方針

- **比較演算 (comparison)** は **built-in keyword** として実装。 (新規追加)
  - 対象: `と同じ` / `と異なる` / `と同種` / `そのもの` / `より大きい` / `より小さい` / `以上` / `以下`
  - 理由: 他言語の `=` / `>` / `<=` 等 operator に相当する基礎概念。言語組み込みの方が一貫性と効率の両面で適切
  - user 定義は不可
- **predicate function (述語関数)** は **default function** として実装。標準ライブラリ / user 定義のいずれも free function 形。 (新規追加)
  - 対象: `で始まる` / `で終わる` / `を含む` / `に含まれる` / `のいずれか` 等
  - 関数名に particle (`が` / `で` / `を` / `と` 等) を埋め込む命名規約
  - natural-language 呼び出し形: `[subject] [particle] [arg] [predicate-name]` が `predicate-name(subject, arg)` の syntactic sugar として parse される (Smalltalk keyword message / ObjC selector に類似)
  - 既存「メソッド不採用」「free function 中心」原則 (`の` chain の項) と整合
  - user は独自の predicate を同じ枠で定義可能
- **副次論点 (今後詰める、parser 着手 / standard library 設計時)**:
  - particle 埋め込み命名規約の formalization (declaration syntax の詳細、許される particle の種類)
  - predicate form が許される条件 (arg 数上限、戻り値型、命名形式の制約)
  - paren 形 `関数名(P が V, ...)` と predicate form `[subj] [part] [arg] [name]` の使い分け方針
  - 既存 `〜 のいずれか` / `〜 に 含まれる` (集合 disjunction) を predicate function として実装するか特別扱いするか

### 集合 disjunction（value-level OR、`〜 のいずれか` / `〜 に 含まれる`）

- **value 位置の `または` は不採用**: `または` は boolean レベルの結合専用。value 位置で disjunction を表現したい場合は集合構文を使う。 (新規追加)
- **修飾形 (predicate の引数位置)**: `LHS が V1・V2・... のいずれか [predicate]`。`〜 のいずれか` は集合 disjunction を構築する修飾形。 (新規追加)
  - 例: `もし X が 「!」・「！」 のいずれか で始まる なら、`
- **predicate 完結形 (集合メンバシップそのもの)**: `LHS が V1・V2・... に 含まれる`。集合メンバシップを述語として完結。 (新規追加)
  - 例: `もし X が 「ping」・「pong」・「time」 に 含まれる なら、`
- **列挙記号: 中点 `・` (U+30FB)**: 値の列挙には中点を使う。`、` は continuation 記号として温存し、value 列挙には使わない。日本語の伝統的な列挙記号 (人名・カテゴリ・選択肢) として自然。 (新規追加)
- **negation との合成は構造的に明確**: `〜 のいずれか で predicate ではない` / `〜 に 含まれる ではない` は「集合の要素すべてで predicate が成立しない」と一意に解釈される。De Morgan を読み手に強いない。 (新規追加)
  - 例: `もし X が 「!」・「！」 のいずれか で始まる ではない なら、` → 「!でも！でも始まらない」
- **値が 1 つの場合**: 通常の predicate (`X が V で始まる`) で書く。`〜 のいずれか` / `〜 に 含まれる` は集合 (2 値以上) に対して使う。
- **複数引数 predicate との合成**: 単項 predicate (subject + 1 arg) に限定。複数引数 predicate での lift は将来検討。
- **distribute の意味論**: 概念的には集合の各要素について predicate を適用、結果を OR 結合。subject は 1 回だけ評価して結果を再利用 (副作用ある関数呼び出しの重複評価を回避)。実装は hash set 最適化等の余地あり。
- **採用しなかった他案 (議論経過の記録)**:
  - (a) value 位置で `または` を distribute する案: edge case R2 (negation 合成での De Morgan 必要) が構造的問題。Raku junctions のみが (a) 採用、controversial。
  - (b) 冗長 boolean 形のみ許可: 書き味の負担が大きい、koto の「流れる日本語」goal と衝突。
  - 新記号 bracket (`〔〕` 等) 採用案: IME 入力負荷が高く、user が反対。
- **採用言語の前例**: SQL `IN (...)`、Python `x in (...)`、Ruby `[...].include?(x)`、Rust pattern `v1 | v2`、Kotlin `when` の case 列挙等、主要モダン言語の (c) 系統への収束的選択。

### 異常終了 (`〜 で終える` / `〜 として終える`、終了型 経由)

- **2 つの出口モデル**: 関数は **正常終了の出口 (`〜 を 返す。`)** と **異常終了の出口 (`〜 で終える。` / `〜 として終える。`)** の 2 つを持つ。宣言部の `〜 を 返す` は **正常終了の出口だけを縛る**。異常終了は別 channel として独立。 (新規追加)
- **終了型**: 異常終了で投げる値は **「終了型」と分類された型** でなければならない。 (新規追加)
  - **言語組み込み 終了型 (初版)**: `例外`、`警告`、`通知` (詳細仕様は今後)
  - **user 定義 終了型**: 何らかの marker で 終了型 として登録できる構文を将来詰める。built-in 3 つで実用の多くはカバー
- **2 つの書き方を許容 (両立形)**:
  - **explicit 形**: `例外(メッセージ が 「..」、コード が 〜) で終える。`
    - `例外(...)` は普通の関数呼び出し (引数を明示) → `で終える` keyword に渡して異常終了
    - 何が構築されているか **書かれた行から見える** (暗黙性なし)
    - 複雑な引数を取る場合に推奨
  - **sugar 形**: `「..」 を 例外 として終える。`
    - explicit 形の短縮形。`〜 を Type として終える。` は `Type（〜） で終える。` と等価
    - 終了型 が **単一引数 (典型的に メッセージ) のみで構築可能** な場合のみ使える
    - 軽量な場面で推奨
- **型制約**:
  - `で終える` の引数は **終了型 として分類された型** でなければならない
  - `「文字列」 で終える` のような無印値を直接投げる書き方は **型エラー**
  - `として終える` の sugar 適用条件は spec で限定 (詳細は後で正式化)
- **終了型同士の親子関係 (継承) は不採用**: `例外` `警告` `通知` 等は **横並びの独立した型** として並べる。継承による subtype catch は使わず、「どれかに当てはまる」を書きたい場合は `〜 のいずれか` 構文で `例外 ・ 警告 のいずれか として 捕まえる` 形で対応する (memo §3-1 vocabulary 固定原則 と前述「`の` chain 深さ制限」の方針との整合)。 (新規追加)
- **デザイン哲学**: 「メソッド不採用 + 自由関数中心」と整合。`例外(...)` は自由関数の呼び出し、`で終える` は独立した control-flow keyword。両者を **構築と終了の 2 道具に分離** することで、行頭で何が起きているか読み解ける。

### match 構文（`〜 について、`）

- **構文形**: `[subject] について、 [case なら、 [body]] [case なら、 [body]] ...`。switch / match 風のディスパッチ構文。 (新規追加)
- **case の condition は subject に対する省略が許される**:
  - `[X] と同じ なら、` → 暗黙に `subject が X と同じ なら、`
  - `[Type] と同種 ではない なら、` → subject の type 判定
  - **暗黙フィールドアクセス**: `[field名] が 〜 なら、` → `subject の [field名] が 〜 なら、`
- **暗黙フィールドアクセスの conflict 解決**: subject の field が優先。outer scope の同名識別子は隠される。外側変数を参照したい場合は明示 prefix で逃げる必要がある。 (新規追加)
- **適用範囲**: match 構文専用。汎用 scope opener (`について、` を任意 block に展開する) は将来検討。 (新規追加)
- **case body**: 1 文以上書ける。次の `[condition] なら、` 行で前 case が暗黙に閉じる。 (新規追加)
- **終端**: 暗黙終端。次の clause が `[condition] なら、` 形式でなければ match 全体が終わる。明示終端 keyword なし。 (新規追加)
- **default**: 不要、暗黙 noop。書きたければ最後に `その他 なら、〜` を書く (escape valve)。型システムによる exhaustiveness 強制は行わない。 (新規追加)
- **デザイン哲学**: 「`その他 なら、〜` を書きたくなったら設計を見直す」という signal を意図。網羅性の自動チェックではなく、書き手の判断に委ねる方針 (memo §1「思考フレームへの作用」主目的との整合)。 (新規追加)
- **fall-through なし**: matched case 実行後 match を抜ける。複数 case を同じ body で受けたい場合は condition の `または` 結合（B-2 議論待ち）または明示的な case 重複で対応。 (新規追加)
- **parser 着手時の caveat** (今は決めない、parser 着手時に詰める):
  - ネスト match のスコープ追跡（case body 内の別 match の case を外側 match の case と誤読しない手当て）
  - `もし X なら、` (if-statement) と match case の `[condition] なら、` の構文的区別 (`もし` 接頭の有無で判定する案が候補)

## Phase B 議論項目（in progress）

sample-2.koto を書いた後に表面化した論点の作業用一覧。順次 D→A→B→C→残り の順で議論し、決着したら「確定した spec 変更」「未決着論点」へ移送する。

### A. 新規構文（spec にない、sample-2 で発明された）

- ~~A-1: `〜 について、 [case なら、] [case なら、]` — switch / match 風構文（line 8-14, 34-44）~~ ✅ 解決 → 「確定した spec 変更」§ match 構文
- ~~A-2: `について、` で開いたスコープの中の **暗黙フィールドアクセス**（line 13: `内容 が` で `メッセージ の 内容` を指す）~~ ✅ 解決 → 同上
- ~~A-3: `〜 で 始まる` — 文字列 predicate（line 20）~~ ✅ 解決 → 「確定した spec 変更」§ predicate / comparison の構文と実装方針。比較演算 (`と同じ` 等) は built-in keyword、predicate function (`で始まる` 等) は default function (particle 埋め込み命名規約)
- ~~A-4: `〜 の 2番目以降` — 文字列の部分抽出（line 24）~~ ✅ 解決 → 「確定した spec 変更」§ indexed accessor。inclusive 4 形 (`N 番目` / `N 番目以降` / `N 番目以前` / `N 番目から M 番目まで`)、1-indexed
- ~~A-5: `何もしない。` — pass / no-op（line 30, 40）~~ ✅ 解決 → 「確定した spec 変更」§ no-op
- ~~A-6: `ここまで。` — 早期 return（line 77）~~ ✅ 解決 → 「確定した spec 変更」§ 関数本体の終端 / 早期終了。`ここまで。` は不採用、戻り値なし関数の mid-body `である。` で代替。sample-2 line 77 は書き換え推奨
- ~~A-7: `文字列？配列` — Optional と配列の合成型（line 52）~~ ✅ 解決 → 「確定した spec 変更」§ 型の postfix 修飾子合成。合成規則は general に維持。line 52 自体は書き手の判断ミス (`文字列配列` で長さ 0 表現が筋)、書き換え推奨
- ~~A-8: `A である B は C とする。` — 変数束縛の topic 形（line 16）の提案~~ ✅ 解決 → 「確定した spec 変更」§ 構造的ルール / 変数束縛の canonical 形。`を` 形のみ canonical、`は` 形は不採用

### B. 過去決定との競合（要確認）

- ~~B-1: line 19 `ディスコード の ギルド の 有効コマンド一覧(...)` — method dispatch に見える。`ギルド` を「サブモジュール」と解釈すれば module navigation で OK、「型」と解釈すれば method dispatch なので「メソッド不採用」決定と矛盾~~ ✅ 解決 → 「確定した spec 変更」§ `の` chain（深さ制限あり）。一度確定した case (a) の自由形は retract、「module/type 境界を 1 回まで、深く行きたければ import を深く」のルールで再確定。user の line 19 の書き方は discord.py 流の object chain の遺物で、koto canonical では `「../ディスコード/ギルド」 を ギルド として 取り込む。` の上で `ギルド の 有効コマンド一覧(...)` と書く
- ~~B-2: line 20 `「!」 または 「！」 で始まる` — `または` を value レベルで使用している。前回決めた優先順位は boolean レベルの結合のみで、value 列挙には対応していない~~ ✅ 解決 → 「確定した spec 変更」§ 集合 disjunction。value 位置の `または` は不採用、`V1・V2・... のいずれか` / `V1・V2・... に 含まれる` を採用
- ~~B-3: line 29 user 自身が `または` か `もしくは` か質問。語彙固定原則（memo §3-1）的にどちらか一方~~ ✅ 解決 → 「確定した spec 変更」§ 論理結合 vocabulary。`または` canonical、`もしくは` 不採用
- ~~B-4: import 構文 `として取り込む` (line 1, no space) — `を取り込む` の空白問題と同じ未決着（C-1 系）~~ ✅ 解決 → 「確定した spec 変更」§ 構造的ルール「compound keyword は内部 space なし」。`として取り込む` canonical (no space)

### C. 意味の確認が必要な点（user 自身がコメントで疑問提起）

- ~~C-1: line 10 `〜 を 例外 として終える` の semantic~~ ✅ 解決 → 「確定した spec 変更」§ 異常終了。(B-両立形) を採用: explicit 形 `例外(...) で終える` と sugar 形 `〜 を 例外 として終える` を両方許容、`で終える` は 終了型 marker で型制約、`返す` (正常終了) と 別 channel
- ~~C-2: line 13 暗黙フィールドアクセス案の是非（A-2 と表裏）~~ ✅ 解決 → 「確定した spec 変更」§ match 構文 (暗黙フィールドアクセス採用)

### D. typo / 命名揺れ（おそらく書き間違い、確認したい） ✅ 解決

- ~~D-1: line 18 で `存在するコマンドか` 宣言、line 25 で `存在するコマンド`（か なし）使用~~ typo 確定 (user 側で sample-2.koto を修正予定)
- D-2: line 86 関数名 `現在日時(...)` と変数名 `現在時刻` の不一致は **意図的**。関数名 = 元概念 (DateTime)、変数名 = 現在保持しているもの (時刻部分の文字列)、という命名スタイル。後の vocabulary 整理時に「関数命名規約」として再記録に値する観察として保留
- ~~D-3: line 87 末尾の `・`（中黒）→ `。`（句点）の typo？~~ typo 確定 (user 側で sample-2.koto を修正予定)

### E. ergonomics の苦言

- ~~E-1: line 63 `として` のあとのスペースを忘れる懸念（layout 変更時）~~ ✅ 解決 → 「確定した spec 変更」§ 構造的ルール (全角 space は唯一の token separator、multi-line でも維持。VSCode extension に trailing whitespace 保護設定を追加する別タスクを起票)
- ~~E-2: line 65, 74 `を受け取り、` / `を 受け取り、` の空白を統一したいという意思~~ ✅ 解決 → 「確定した spec 変更」§ 構造的ルール「compound keyword は内部 space なし」。`を受け取り、` canonical
- ~~E-3: line 74 `を返す` / `を 返す` の同上~~ ✅ 解決 → 同上。`を返す。` canonical
- ~~E-4: line 5「やはりインデントはタブがいい」再表明~~ ✅ 解決 → 「確定した spec 変更」§ 構造的ルール (canonical indent: tab。VSCode extension に `editor.insertSpaces: false` 等の設定を追加する別タスクを起票)

### F. 既存決定の確認（sample-2 で再使用、問題なく動いている）

- 多行 / 一行両様の関数シグネチャ
- `を受け取り、` 連結
- module alias import の形式
- `〜？` Optional
- `である。` で関数閉じ
- keyword 引数の `フィールド名 が 値`
- `か` がない、`または` 使用（boolean レベル）

### 議論順序

1. ✅ D（typo 確認）— 完了
2. ✅ A-1 / A-2 — 完了 → 「確定した spec 変更」§ match 構文
3. ✅ B-1（module 深い navigation vs method dispatch）— 完了 → 「確定した spec 変更」§ `の` chain
4. ✅ B-2（value レベル OR）— 完了 → 「確定した spec 変更」§ 集合 disjunction
5. ✅ A-3（`〜 で 始まる` — keyword vs default function）— 完了 → 「確定した spec 変更」§ predicate / comparison
6. ✅ プロパティアクセス・メソッド周り — 完了 → 「確定した spec 変更」§ property access (built-in only 採用、user 定義型は未決着論点に保留)
7. ✅ C-1（`例外 として終える` の意味論）— 完了 → 「確定した spec 変更」§ 異常終了
8. ✅ A-4〜A-8 残り — 完了 → 各「確定した spec 変更」 (indexed accessor / no-op / 早期終了 / 型合成 / 変数束縛 canonical 形)
9. ✅ B-3 / B-4 / E-2 / E-3（vocabulary 揺れ）— 完了 → 「確定した spec 変更」§ 構造的ルール / 論理結合 vocabulary
10. ✅ E-1 / E-4（ergonomics）— 完了 → 「確定した spec 変更」§ 構造的ルール (E-1: 全角 space 唯一 separator 厳格化、E-4: tab indent canonical)

**Phase B 議論項目すべて完了**。Decision after Phase B セクション参照。

## 未決着論点

順次 Phase B 等の実例で詰める。

### module / import 関連

- **個別名 alias の import 構文**: `〜 から X を Y として 取り込む。`（特定名を別名で取り込む）形式は spec 未定。Phase B では namespace conflict が出なかったので、実コードで必要が出てから決める。それまでは `〜 を Y として 取り込む。` (module alias) で qualify する canonical 解法で十分。

### property access 関連

- **user 定義 type の derived property**: 現状は不採用 (built-in 型のみ property syntax を許可)。user 定義型は宣言 field と free function だけで派生値を扱う。
  - 再検討のトリガ: Phase B 以降の実コードで「user 定義型に pure な derived property を持たせたい」cases が頻発するようになった時。
  - 採用時に決めるべきこと: 宣言構文 (型定義時に property 宣言を入れる文法)、純粋性の compiler enforcement、lazy vs eager 戦略、impurity (現在時刻等の外部依存) の扱い、メソッドとの境界明確化。
- **built-in property の追加判断**: 「inclusion criteria に通り、かつ実コードで頻出」が条件。投機的追加はしない。

### 異常終了 (catch / recover / 終了型) 関連

- **catch / recover 構文**: `〜 を 試して、 〜` 等の正式構文は Phase B 外として保留。実コードで「異常終了を捕まえて回復したい」cases が頻発したら設計に着手。
- **checked vs unchecked**: 関数宣言部に「投げうる終了型」を書くかどうかは当面 unchecked (書かない方針)。後で必要なら opt-in 形式で追加。
- **言語組み込み 終了型 の詳細仕様**: `例外` / `警告` / `通知` のフィールド構成、log integration の有無、それぞれの想定 use case の境界整理は別タスク。
- **user 定義 終了型 の marker 構文**: `終了型 として オブジェクト 〜 は 〜 からなる。` のような形式案あるが、正式化は user 定義 終了型 のニーズが出てから。
- **sugar 形 (`として終える`) が成立する条件の formalization**: 単一引数構築のみ許容 / default 引数のあるもの含む / 複数引数を kwarg で 1 つだけ指定する形 etc.、正式 spec が必要。Phase B 範囲外。

### Phase A 拡張で表面化

- **`を取り込む` の無スペース form**: `〜 を 取り込む` と `〜 を取り込む` のどちらも許可するか、片方に固定するか。
- **辞書リテラルの直接表記**: `{ k: v, ... }` 相当のリテラル構文。`空辞書` から差分を組むのか、専用構文を用意するのか。
- **コメント構文の確定**: `＃`（全角）を採用するか、`//` `--` `;` 等を選ぶか、または「コメントなし、`である` で空文」のような koto 独自方針を取るか。
- **`を 返す`（スペースあり）対応**: 現行 grammar pattern は `を返す`（無スペース）。書き手の自然な書字はスペースあり。grammar 側で両対応するか、書字側を統一するか。
- **ループ syntax の統一**: `要素を X として 〜 の 各要素について繰り返すと、` を `〜 について繰り返すと、` または `〜 の 各要素について繰り返すと、` にまとめるか。
- **インデントの tab 化**: 全角スペース運用が分かち書きと衝突しないか、tab に切り替えるべきかの議論。
- **`真` の IME 問題**: fix なし。観察として記録。

### 条件式・Optional 関連

- **論理結合の vocabulary**: canonical の `かつ` / `または` / `ではない` で固定するか、`〜 か 〜 のいずれか`、`なおかつ` 等の口語的 form も公式採用するか（暫定運用中、Phase B で判断）。
- **Optional 肯定 narrowing 構文**: `もし X が 無し と同じ ではない なら、〜` の中で X を `T？` から `T` に narrow する形は採用したいが、unwrap 専用構文を別途用意するかは未定。例えば `もし X が 値 として 取れたら、[V を 使って] 〜 そうでなければ 〜` のような pattern match 風。
- **Boolean を返す predicate の命名規約**: `〜か`、`空である`、`〜であるか` 等のうちどれを canonical にするか。
- **真偽値変数の中間束縛構文**: `真偽値 である X を {条件式} とする` のような形で、条件式を値として束縛する書き方の正式構文（暫定で `{ }` 表記しているが、本来は不要なはず）。

### grammar 側のフォロー

- v3（仮）で `を受け取り`（連用形）を grammar に追加。
- `である。`（行頭、indent あり）が正しくハイライトされるか実機検証。
- 比較演算子（`より大きい` / `より小さい` / `以上` / `以下`）を grammar に追加。
- `ではない` を `である` と並ぶ独立 keyword scope（`keyword.operator.negation.koto`）として追加。
- `？` を Optional 専用 scope（`keyword.operator.optional.koto`）として追加。
- `かつ` / `または` を論理結合 scope（`keyword.operator.logical.{and,or}.koto`）として追加。

## Decision after Phase B

Phase B 完了。sample-2.koto を起点に多くの spec 確定。次の進路:

### Phase B で追加確定した主な spec

- `の` chain (深さ制限あり) — module navigation / type-as-namespace は 1 段、field 鎖は任意 depth
- property access (immutable binding 上の field-syntax derived value、built-in 型のみ)
- predicate / comparison の構文と実装方針 (比較は built-in keyword、predicate function は default function)
- 集合 disjunction (`〜 のいずれか` / `〜 に 含まれる`、中点 `・` 列挙)
- 異常終了 (`〜 で終える` / `〜 として終える`、終了型 経由、両立形)
- match 構文 (`〜 について、` + 暗黙 field access)
- indexed accessor (1-indexed、inclusive 4 形)
- no-op (`何もしない。`)
- 型の postfix 修飾子合成 (`？` / `配列`)
- 変数束縛 canonical 形 (`を` のみ、`は` 不採用)
- 関数本体終端 / 早期終了 (mid-body `である。` で void 関数の早期 exit、専用 keyword `ここまで。` は不採用)
- compound keyword は内部 space なし (B-4 / E-2 / E-3 統合原則)
- 全角 space は唯一の token separator (E-1、分かち書き原則の厳格化、tab indent canonical)

### 次のステップ (TODO に起票)

1. **設計メモ更新** (`Lang-Doc-15`): Phase A/B 確定事項を `_docs/standards/japanese-lang-design-memo.md` に統合。本 notes.md は memo 更新後に archive
2. **VSCode extension default config 更新** (`Tooling-Chore-13`): tab indent + trailing 全角 whitespace 保護を `[koto]` scope の configurationDefaults に追加
3. **VSCode grammar v3** (`Tooling-Feat-14`): Phase B 新 keyword 群をハイライト対応
4. **parser / lexer 実装着手** (今後): memo 更新後、spec を基に parser のスケルトンを書く (Phase C 相当)

優先順は (1) → (2)・(3) 並走 → (4)。memo が更新されないと他の作業の正本がない。

### 未決着論点

本 notes.md の「未決着論点」セクション参照。Phase C 以降に持ち越し。主なもの:

- catch / recover 構文 (`〜 を 試して、 〜` 等の正式構文)
- checked vs unchecked (関数宣言部に投げうる終了型を書くか)
- user 定義 終了型 の marker 構文
- user 定義 type の derived property
- 個別名 alias の import 構文
- 辞書 / 集合 / タプル の literal 構文
- コメント構文 (`＃` 仮使用中)
- ループ syntax 統一
- `真` の IME 問題

## Decision after Phase A

Phase A と Phase A 拡張で出た材料は十分多い。次の進路:

- **採用**: notes.md（本書）で「確定した spec 変更」を記録 → Phase B（複数コマンド dispatch を題材）に進む。
- **理由**: 未決着論点のうち、比較演算・辞書リテラル・コメント構文・`を 返す` の grammar 衝突は、Phase B で実コードを書くと必ず再遭遇する。机上で先に決めるより、書いて詰まってから決めるほうが意思決定の精度が上がる。
- **保留**: 設計メモ自体の更新は別タスクとして起票（本ノートを入力に）。Phase B 完了後にまとめて反映する。

### 次のステップ

1. Phase B の題材を決める（`!echo X` と `!time` を 1 つの dispatcher で受ける、など）
2. 同じ流れで `sample-2.koto` 相当の手書き
3. 本 notes.md に観察を追記、未決着論点を順次解消
4. 全体決着後、設計メモを更新するタスクを起票
