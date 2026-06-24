---
title: VSCode 拡張による koto シンタックスハイライト
status: active
draft_status: n/a
created_at: 2026-06-25
updated_at: 2026-06-25
references:
  - "_docs/intent/Tooling/vscode-koto-grammar/decision.md"
  - "_docs/qa/Tooling/vscode-koto-grammar/test-plan.md"
  - "_docs/standards/japanese-lang-design-memo.md"
  - "_docs/standards/japanese-lang-why-not.md"
related_issues: []
related_prs: []
---

# VSCode 拡張による koto シンタックスハイライト

## Overview

koto 言語の最初の開発ツールとして、VSCode 拡張一式を `tools/vscode-koto/` に作成する。設計メモ § 7「次のステップ」で最優先と明示された TextMate Grammar を中心に据え、拡張子 `.koto` の認識、ブラケット・コメント等のエディタ挙動、キーワード／記号／リテラル／助詞の色分けを提供する。トランスパイラ本体に先行して整備することで、設計メモ §1 にある「日本語で書くと思考フレームがどう変わるか」の観察を、目視的に支援できる書き味で開始できるようにする。

## Scope

- 拡張のスケルトン: `tools/vscode-koto/package.json`、`tools/vscode-koto/language-configuration.json`。
- TextMate Grammar: `tools/vscode-koto/syntaxes/koto.tmLanguage.json`。`scopeName` は `source.koto`。
- 拡張子 `.koto` を言語 ID `koto` に紐づける `languages` contribution。
- 設計メモ § 7 に列挙されたすべてのキーワード（宣言系・制御系・動作系・構文系）、記号 `「」（）。、`、リテラル（算用数字、`真`、`偽`、`無し`）の認識ルール。
- 分かち書きで囲まれた助詞（`の`、`が`、`に`、`を`、`から`、`で`）の専用 scope。識別子内に同じ字が混入しても誤検出しないよう、全角スペース境界で判定する。
- サンプル `.koto` ファイル: 設計メモ § 4 の例文集から「最大値」「未完了の取り出し」「タスク表の作成」を `tools/vscode-koto/tests/fixtures/` に配置。
- `tools/vscode-koto/README.md` に開発時のロード手順（VSCode `Extensions: Install from Location...` 相当）と既知の制限を記載。

## Non-Goals

- 言語サーバー（LSP）の実装。診断・自動補完・ホバー情報はパーサ完成後に着手する（TODO §優先度高 #2、開発ツール #12–#16 参照）。
- パーサ／型チェッカー／トランスパイラ本体。
- セマンティックハイライト（型・変数の意味に基づく色分け）。設計メモ § 7 開発ツール #13 に該当するが、これは LSP に依存するため後段。
- npm パッケージとしての公開、VSCode Marketplace への登録。
- コメント構文の確定。設計メモ未確定。本タスクでは未定義のまま grammar に登録しない。
- ジェネリクス・パターンマッチ・「たぶん〜」など、設計メモで未確定の構文。
- インデント／全角スペース幅の自動整形。
- ファイル末尾自動改行、保存時整形等の VSCode 既定挙動の上書き。

## Requirements

- **Functional**:
  - `.koto` ファイルを VSCode で開くと言語 `koto` として認識される。
  - 設計メモ § 7 の全キーワードが、それぞれの群に対応する scope でハイライトされる。
  - 単一文字助詞は分かち書きで囲まれた場合のみキーワード扱いになり、識別子の一部としては扱わない。
  - 多文字キーワード（`と同じ`、`と同種`、`そのもの`、`からなる`、`のいずれか`、`として`、`である`、`繰り返すと` 等）が一文字キーワードや助詞より優先的にマッチする。
  - 文字列リテラル `「...」`、関数呼び出しの全角括弧 `（）`、句点 `。`、読点 `、` がそれぞれ独立した scope を持つ。
  - 算用数字 `0–9` が数値リテラルとして識別される。漢数字は数値リテラル扱いにしない（熟語の一部として識別子に含まれる形は許す）。
  - `真`、`偽`、`無し` が `constant.language` 系の scope を持つ。
- **Non-Functional**:
  - grammar は単一の `.tmLanguage.json` で完結し、外部依存を持たない。
  - 既存の docs validator（`scripts/check-docs.sh`）が PASS する。
  - 拡張は VSCode の標準 manifest に準拠し、追加の build / bundler を必要としない。
  - JSON は手で読める粒度に整形し、各 pattern に `comment` を付けて意図を残す。

## Tasks

1. `tools/vscode-koto/package.json` を作成する。`contributes.languages` と `contributes.grammars` を定義する。
2. `tools/vscode-koto/language-configuration.json` を作成する。bracket / autoClosing / surrounding pairs を全角記号で定義する。
3. `tools/vscode-koto/syntaxes/koto.tmLanguage.json` を作成する。include 順序を「文字列 → リテラル → 多文字キーワード → 単文字助詞 → 数値 → 記号 → 識別子」とし、誤マッチを避ける。
4. `tools/vscode-koto/tests/fixtures/` に最大値・未完了の取り出し・タスク表の作成の例文を配置する。
5. `tools/vscode-koto/README.md` に開発時ロード手順・既知の制限・未定義事項を書く。
6. 標準ドキュメント（intent / test-plan）の references がリンク切れになっていないことを `scripts/check-docs.sh` で確認する。
7. VSCode でサンプルを開き、トークン scope を inspect（`Developer: Inspect Editor Tokens and Scopes`）で確認した結果を verification に残す。
8. `qa-review` skill で verdict を確認する。

## QA Plan

- QA document: `_docs/qa/Tooling/vscode-koto-grammar/test-plan.md`
- Risk level: Low
- Test strategy:
  - Unit: 該当なし（grammar はランタイムロジックを持たないため）。
  - Integration: VSCode 拡張をローカルロードし、`tests/fixtures/*.koto` を開く。
  - Manual QA: `Developer: Inspect Editor Tokens and Scopes` で代表トークンの scope を確認し、test-plan の Test Matrix に従って判定する。
  - Validator / static check: `scripts/check-docs.sh` で docs 整合性を確認する。`tools/vscode-koto/package.json` と `syntaxes/koto.tmLanguage.json` の JSON 構文を `deno run --allow-read --check` または `jq` で軽く検証する。
  - Diff review: 設計メモ § 7 のキーワード一覧と grammar の `name` 列が 1:1 で対応していること、未定義 keyword（コメント等）が混入していないことを diff で確認する。
- Acceptance criteria と intent-derived invariant は test-plan の Test Matrix に紐づける。

## Deployment / Rollout

開発者個人の VSCode に「Install from Location」でロードする運用とする。Marketplace 配布はしない。問題があれば拡張をアンインストールするだけでロールバック可能。今後 LSP を追加する際にも同じディレクトリ `tools/vscode-koto/` を拡張ポイントとして再利用する想定。
