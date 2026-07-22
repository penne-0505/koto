---
title: Discord bot リマインダー手書き演習 観察ノート
status: proposed
draft_status: exploring
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/standards/japanese-lang-design-memo.md"
  - "_docs/draft/Lang/discord-bot-reminder/reminder.koto"
  - "_docs/archives/draft/Lang/discord-bot-handwrite/notes.md"
related_issues: []
related_prs: []
---

<!-- Canonical path: _docs/draft/Lang/discord-bot-reminder/notes.md -->
<!-- Phase C (Lang-Chore-16) の手書き演習観察ログ。Phase A/B で確定した spec を新題材で初回運用テスト。memo §5 未決着論点で実際に詰まる箇所を炙り出す。 -->

## Purpose

Phase A / Phase B で memo §3-1〜§3-26 に統合された spec の **初回運用テスト**。Discord bot 題材ながら、Phase A/B とは異なる axis (時間・永続化・catch 需要) を扱う題材で:

1. 書き手にとって spec が本当に自然か確認
2. memo §5 未決着論点 (catch / 辞書 literal / コメント / etc.) で具体的にどう詰まるかを記録
3. 見落とし・追加論点を発見

動作させることは目的ではない。

## Method

- 書く場所: `_docs/draft/Lang/discord-bot-reminder/reminder.koto`
- 書く人: プロジェクト author (ユーザー)
- 支援: assistant が memo / notes 参照、spec 未定義箇所の指摘、違和感のログ整理
- 書き終わったら本ノートを一緒にレビューし、memo §5 の優先論点 (Phase B → B の順序) を確定

## 題材

**リマインダー bot**。予約時刻に本文を通知する。

コマンド一覧:

- `!remind 2026-07-05 09:00 会議` — 予約する
- `!remind list` — 予約一覧を返信
- `!remind cancel <id>` — 指定 id の予約を削除

背景処理:

- 定期的に「期日到来した予約」を検出し、通知する (実装は仮の loop で OK)

永続化:

- 予約は JSON ファイル (`reminders.json` 仮定) に保存
- 起動時に読み込み、変更時に書き込み

## 想定する API shape

Phase A/B と同じ前提に加えて:

- `ディスコード の 返信する(内容 が 〜、返信先番号 が 〜)` — 返信 (Phase B と同じ)
- `現在日時（）` — 現在時刻取得 (sample-2 と同じ)
- `時刻文字列を日時に変換する(文字列 が 〜)` — 文字列 → 日時 (仮定、失敗しうる)
- `ファイル に 書き込む(パス が 〜、内容 が 〜)` — ファイル IO (仮定、失敗しうる)
- `ファイル から 読み込む(パス が 〜)` — 同上、戻り値 `文字列？`
- `JSON文字列に変換する(値 が 〜)` — 予約辞書 → JSON 文字列 (仮定)
- `JSON文字列から復元する(文字列 が 〜)` — 逆 (仮定、失敗しうる)

上記は「外部関数として宣言されている」前提。宣言ファイル自体は演習では書かない。

## 書きたい要素 (最小)

以下の要素を含む関数を 4〜5 個程度手書きする:

- **オブジェクト型定義**: `予約` オブジェクト (id 数値、予約時刻 日時、本文 文字列、ユーザー番号 文字列)
- **辞書**: `数値と予約の辞書` (id → 予約) — **memo §5 #38: 辞書 literal 未確定** で確実に詰まる想定
- **時刻の property access**: `予約 の 予約時刻 の 年` 等 (memo §3-16 の運用テスト)
- **match 構文**: dispatcher で 3 コマンドを分岐 (memo §3-22)
- **異常終了**: 時刻パース失敗 / ファイル I/O 失敗 → `〜 として終える。` / `〜 で終える。` (memo §3-19)
- **catch シナリオ**: ファイル書き込み失敗を受け止めて別処理へ — **memo §5 #26 catch 構文未確定** で確実に詰まる想定
- **比較演算**: `予約時刻 が 現在時刻 以下` (memo §3-7)
- **loop + 集合操作**: 予約群を走査して期日到来分を抽出 (memo §3-9 / 標準 lib 未設計)

## 進め方

Phase A/B と同じ:

1. 書きながら詰まったところ / 違和感 / spec 未定義箇所を Observations に追記
2. コード側にも `＃` 仮コメントで疑問を残す
3. 一段落したら本ノートを一緒にレビュー
4. Decision セクションで次の進路を決める (memo §5 のどの論点から詰めるか、直接 parser 着手か等)

## Observations

### 2026-07-07: 初回停止点の退避

現状 `reminder.koto` は実装を進める前の足場作りで止まっている。予約 / 一覧 / キャンセル / 期日到来検出の関数群はまだ書かれていないため、Phase C は未完了。

#### O-001: import compound のハイライト違和感

`reminder.koto` では次の形を書いた。

```koto
「../ディスコード」　を　ディスコード　として取り込む。
```

書いた時点で「`として取り込む。` がハイライトされていない」という観察が出ている。Phase B では compound keyword は内部 space なしを canonical としたため、`として取り込む` 自体は現在の設計に沿っている。一方、grammar / README 側の実装・説明がこの import compound を現在どこまで拾うかは、現物確認が必要。

この観察は、comment syntax とは別に、grammar v3 の import keyword カバレッジ確認として扱う。

#### O-002: `＃` コメントは仮使用で、grammar はまだコメント扱いしない

`reminder.koto` では `＃` をコメントとして使っている。

```koto
＃　コメントはコメントの色にしてほしい。
```

これは grammar bug ではなく、memo §5 のコメント構文未決定に接続する観察。現時点では `＃` は仮コメントであり、コメント色にするには、まず言語仕様としてコメント構文を確定し、その後 grammar に反映する必要がある。

Phase C では `＃` を観察ログの補助として使い続けてよいが、「コメントとして色が付かないこと」は既知の未決着論点として扱う。

#### O-003: Discord context object をそのまま持ち込むと API shape が肥大化する

`reminder.koto` では次のようなメモが出ている。

> 「ディスコード」の「メッセージ」は ctx を兼ねたようなものをイメージしている。content, guild, channel, author などが入っているイメージ。

さらに、`コマンド` オブジェクト案として次を仮置きした。

```koto
オブジェクト　として　コマンド　は、
	メッセージ　である　メッセージ、
	文字列　である　コマンド名、
	文字列と文字列の辞書？　である　引数ら、
からなる。
```

これは Discord API の ctx / message / interaction を koto 側でどう抽象化するかの論点。Discord bot 題材を続ける場合、言語構文だけでなく外部 API 宣言・adapter shape の設計に引っ張られやすい。

Phase C の目的は adapter を完成させることではないため、今後は必要なら未定義仮型・未定義仮関数として通し、API shape の細部へ深入りしすぎない。

#### O-004: 状態管理中心の題材は koto の不得意領域を露出させる

リマインダー bot は、長寿命の mutable state、event-driven な副作用、ファイル I/O、失敗回復を同時に要求する。これは koto の現時点の設計、特に不変デフォルト・自由関数中心・明示型・catch 未定義・辞書 literal 未定義と衝突しやすい。

この衝突は「失敗」ではなく、memo §1 の主目的である「日本語で書くと思考フレームがどう変わるか」の観察材料である。続ける場合は、きれいな Discord bot を完成させるのではなく、詰まった箇所を `＃` と Observations に残すことを優先する。

#### O-005: Discord bot 以外の題材候補が必要

Discord bot は user がオーガニックに書ける題材である一方、外部 API / mutable state / side effect に寄りすぎる。次に比較対象として、koto の得意そうな純粋処理・データ整形寄りの題材を試す価値がある。

候補:

- 文字列コマンドの parse / normalize / validate: 入力文字列を構造化し、エラーを返す。副作用が薄く、match / Optional / 終了型を試せる。
- CSV / Markdown 風データの整形: 配列・辞書・filter / map / sort の必要性が出る。標準ライブラリ設計に接続しやすい。
- 予定リストや課題一覧の集計: 日時 property access とコレクション処理を使うが、Discord adapter からは離れられる。
- 小さな pricing / tax / score 計算: 純粋関数として書きやすく、関数シグネチャ・型・比較・分岐の書き味を確認できる。

Discord bot を続ける価値は残っているが、続行するなら「状態管理の不得意さを記録する演習」として位置づける。言語の自然な書き味を確認したいなら、次は副作用の少ない題材へ移るのがよい。

## Decision after Phase C

(演習完了後にまとめる)
