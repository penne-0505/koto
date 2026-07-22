---
title: koto TextMate Grammar 設計判断
status: active
draft_status: n/a
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/plan/Tooling/vscode-koto-grammar/plan.md"
  - "_docs/qa/Tooling/vscode-koto-grammar/test-plan.md"
  - "_docs/standards/japanese-lang-design-memo.md"
  - "_docs/standards/japanese-lang-why-not.md"
related_issues: []
related_prs: []
---

# koto TextMate Grammar 設計判断

## Context

koto はキーワードと識別子が同じ文字体系（漢字＋ひらがな）を共有する。英語ベース言語と異なり、空白記号や大文字・小文字の差で語境界が決まらない。設計メモ § 1 で「思考フレームへの作用」を主目的とすると宣言した以上、書き味の最初の印象を支える視覚分離は標準より重要になる。一方、パーサや LSP が存在しない段階の TextMate Grammar は純粋な正規表現マッチに依存するため、文法的正確さよりも「誤検出しない」を優先する必要がある。

加えて、設計メモにはまだ未確定の構文（コメント、ジェネリクス、パターンマッチ、Optional 型表記、宣言的 API の構文化）がある。grammar に未確定構文の予想を載せると、後の言語仕様が grammar に引きずられる、または grammar が早期に陳腐化する。

## Decision

- **scopeName** を `source.koto` とする。VSCode の慣習に準拠し、後続の LSP セマンティックハイライトと衝突しない名前空間を確保する。
- **拡張子は `.koto`** に固定する。設計メモ § 7 の候補 `.jp` / `.nihon` / `.koto` / `.nh` のうち、プロジェクト名と一致する `.koto` を採用する。
- **語境界判定は分かち書きを唯一の手がかりとする**。全角スペース（Unicode U+3000）、行頭・行末、句読点（`。`、`、`）、全角丸括弧（`（`、`）`）、鉤括弧（`「`、`」`）を語境界として扱う。半角スペースや欧文記号は境界として認めない。
- **キーワードの正規表現は前後の語境界をルックアラウンドで明示**する。これにより、識別子（裸書き）に同一字列が含まれていても誤検出しない。例: `(?<=[　。、（）「」]|^)関数(?=[　。、（）「」]|$)`。
- **多文字キーワード優先**: include 順序を「文字列 → リテラル → 多文字キーワード → 単文字助詞 → 数値 → 記号 → 識別子」とし、`と同じ` が `と` より先にマッチするよう保証する。
- **助詞は独立した scope** `keyword.operator.particle.koto` を与える。設計メモが「助詞が意味を運ぶ」と明示しているため、可視化として独立扱いする。ただし語境界要件は他のキーワードと同等に厳格にする。
- **未確定構文は grammar に登録しない**。コメント、ジェネリクス、Optional 型、パターンマッチは仕様確定後に追加する。「とりあえず `#` をコメントにしておく」のような暫定実装は採用しない。
- **`公開`、`非同期`、`外部` などの修飾語**は `storage.modifier.koto` を与え、`関数`、`オブジェクト` などの宣言キーワード `storage.type.koto` と視覚的に区別する。設計メモ § 3-13 が修飾語を分かち書きで前置すると規定しているため、grammar 上も別 scope で扱うほうが書き手の意図が見える。
- **`である` は宣言系（型注釈）と等価判定の両用**だが、grammar 段階では文脈解決しない。両用法ともに `keyword.operator.type-annotation.koto` 相当の単一 scope に寄せ、文脈別の意味づけはセマンティックハイライト（LSP）に委ねる。
- **トークン化テストは VSCode の Inspect Editor Tokens and Scopes** を一次手段とし、自動化（`vscode-tmgrammar-test` 等）は本タスクのスコープ外とする。導入コスト > 当面の便益と判断。

## Alternatives

- **scopeName を `source.kotolang`** にする: VSCode の慣習では拡張子と一致させなくてよいが、`koto` が他言語 `Koto`（Rust 製スクリプト言語）と衝突する懸念がある。それでも `source.koto` を選ぶのは、本プロジェクト内部での識別性を優先し、Marketplace への配布を Non-Goal にしているため衝突は実害を持たないため。
- **拡張子 `.nh` / `.jp`** を採用する: `.jp` は国名コード／TLD と視覚的に衝突し、`.nh` は意味が伝わりにくい。Why-not は設計メモ／回答時の AskUserQuestion で議論済み。
- **語境界を考慮せずキーワードをそのままマッチさせる**: 実装は簡単だが、識別子内の同一字列を誤って色付ける。例えば `関数` の `関` を含む識別子（仮想例: `関連タスク`）がキーワード扱いになる。誤検出は「日本語で書ける感じ」を直接損なうため不採用。
- **語境界に半角スペースも許す**: 設計メモが分かち書きを全角スペースに固定している。半角スペースを許すと grammar が仕様に先行して曖昧さを生むため不採用。
- **助詞を `punctuation.separator` にする**: 助詞は分離記号ではなく意味役割の運び手なので、`keyword.operator.particle` のほうが意味に近い。
- **未確定構文（コメント等）を暫定実装する**: 後で仕様が変わったとき、書かれた既存コードを書き換える必要が出る。grammar が「仕様の先取り」をすると言語設計が grammar の都合に引きずられるリスクがある。
- **`vscode-tmgrammar-test` で自動化する**: テストの再現性は高いが、npm 依存と CI 設定が増える。現段階の言語仕様が揺らいでいるため、自動化の維持コストが便益を上回ると判断。仕様が固まり次第、別タスクで再評価する（intentional omission として記録）。
- **JSON ではなく YAML / plist 形式の grammar**: VSCode は JSON が一次サポート。YAML は人間可読だが build step が必要。plist は古い形式で読みにくい。JSON が最少コスト。

## Rationale

`koto` は仕様の確定度が「ハイライト可能」と「文脈解決が必要」の境界に座っている。grammar の役目を「視覚的な語境界の提示」と「キーワードのカテゴリ視認」に絞れば、未確定領域に手を出さずに済む。意味解析や型推論を必要とする判断（`である` の用法判別、列挙値の所属型推論、識別子の宣言／参照区別）は LSP で扱う。

語境界をルックアラウンドで明示するのは冗長だが、誤検出が一度でも起きると「全角スペースで区切れているのにキーワード色が漏れている」という違和感を生み、設計メモが約束した「日本語の特性が活きる」体験を直撃する。grammar の規則数が増えるコストよりも、誤検出ゼロのコストを優先する。

未確定構文を grammar に載せないのは、grammar が言語仕様のラフドラフトとして読まれてしまう副作用を避けるため。grammar に書かれた構文は「すでに決まったように」見える。設計メモが明示的に「未定」としている構文に対し、grammar が暗黙の既定値を埋めると、設計議論の自由度が下がる。

## Consequences / Impact

- 拡張子 `.koto` は確定する。今後変更すると拡張・ドキュメント・ファイルを横断して書き換えが発生する。
- 語境界を全角スペースに固定するため、書き手は分かち書きを徹底することが前提になる。これは設計メモ § 3-1 と整合し、強化される。
- 未登録キーワードや未確定構文は灰色（識別子と同じ色）で表示される。書き手は「ハイライトされない＝言語仕様が未確定」と認識できる。これは仕様の進捗を視覚的に追える副次効果になる。
- セマンティックハイライトを LSP に委ねるため、`である` の用法別の色分けや列挙値の所属型推論は本タスクの範囲外となり、LSP タスクで取り戻す。
- 拡張は `tools/vscode-koto/` に置き、今後の LSP も同ディレクトリの拡張ポイントとして合流させる前提とする。

## Quality Implications

- 識別子内の偶発的キーワード一致による誤検出は、書き味の信用を直接損なう。test-plan で識別子内字列の混入ケースを必ず検証する。
- 多文字キーワードと単文字キーワード／助詞の優先順序が破られると、`と同じ` が `と` と `同じ` に分裂してハイライトされる回帰が起きる。include 順序の固定は INV として扱う。
- 未確定構文を grammar に追加するときは、必ず本 intent を更新し、Alternatives セクションに why-not を残す。grammar が言語仕様より先行する事故を防ぐ。
- LSP セマンティックハイライトを後から重ねたとき、本 grammar の scope 名と衝突しないこと。`source.koto.*` 名前空間を予約する。

## Intent-derived Invariants

- INV-001: `.koto` ファイルは VSCode に `source.koto` の言語として登録され、`scopeName` は `source.koto` 固定である。
- INV-002: 設計メモ § 7 のキーワード一覧に列挙された語のみが grammar に登録される（コメント記法等、設計メモで未確定の構文は登録しない）。
- INV-003: すべてのキーワード／助詞のマッチには前後の語境界要件（全角スペース・行端・全角句読点・全角括弧・鉤括弧）が課される。半角スペースを語境界として認めない。
- INV-004: 多文字キーワードは単文字キーワード／助詞より先に評価される（grammar の include 順序および pattern 順序で保証する）。
- INV-005: 修飾語（`公開`、`非同期`、`外部`）と宣言キーワード（`関数`、`オブジェクト`、`定数`、`可変`）は別の scope 群（`storage.modifier.koto` と `storage.type.koto`）に分離される。
- INV-006: 漢数字は数値リテラル扱いにしない。算用数字 `0–9` のみを数値リテラルとして識別する。
- INV-007: `真`、`偽`、`無し` は `constant.language.*.koto` 配下の scope を持ち、識別子と区別される。
- INV-008: 文字列リテラル `「...」` は `string.quoted.*.koto` を持ち、内部のキーワード字列はハイライトされない。

## Enforced in (optional)

- INV-001: `tools/vscode-koto/package.json`、`tools/vscode-koto/syntaxes/koto.tmLanguage.json`。
- INV-002 – INV-008: `tools/vscode-koto/syntaxes/koto.tmLanguage.json` の repository 定義および include 順序。
- 検証は `tools/vscode-koto/tests/fixtures/*.koto` と verification の Manual QA で行う。

## Rollback / Follow-ups

- ロールバック: `tools/vscode-koto/` ディレクトリを削除すれば VSCode 拡張は消える。docs（plan / intent / qa）は historical record として残す。
- Follow-ups:
  - LSP 着手時にセマンティックハイライト・診断・補完を追加する（TODO 別タスク化予定）。
  - コメント構文が確定したら本 intent の Alternatives と grammar を同時更新する。
  - `vscode-tmgrammar-test` の導入是非を、仕様が一定固まった段階で再評価する。
