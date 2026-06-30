---
title: "QA Test Plan: koto grammar v3 — Phase B 構文"
status: active
draft_status: n/a
qa_status: planned
risk: Low
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/intent/Tooling/vscode-koto-grammar-v3/decision.md"
  - "_docs/plan/Tooling/vscode-koto-grammar-v3/plan.md"
related_issues: []
related_prs: []
---

# QA Test Plan: `koto grammar v3 — Phase B 構文`

## Source of Intent

- TODO: `Tooling-Feat-14`
- Plan: `_docs/plan/Tooling/vscode-koto-grammar-v3/plan.md`
- Intent: `_docs/intent/Tooling/vscode-koto-grammar-v3/decision.md`

## Quality Goal

`.koto` ファイルで Phase B 新構文 (memo §3-19〜§3-26 等) がそれぞれ適切な scope で着色される。同時に v1 / v2 のハイライトに regression を出さない。

## Acceptance Criteria

- **AC-001**: 以下の Phase B 新 keyword / 記号がそれぞれ対応 scope でハイライトされる:
  - 比較演算: `より大きい` / `より小さい` / `以上` / `以下` / `と異なる` → `keyword.operator.comparison.*.koto` / `keyword.operator.equality.not-equal.koto`
  - 論理結合: `かつ` / `または` / `ではない` → `keyword.operator.logical.{and,or,not}.koto`
  - 制御 (新): `について` / `について繰り返すと` / `何もしない` / `で終える` → `keyword.control.{match,loop,noop,throw}.koto`
  - パラメータ (連用形): `を受け取り` → `keyword.operator.signature.parameter.koto`
  - 集合: `に含まれる` → `keyword.operator.set.contains.koto`
  - 終了型: `例外` / `警告` / `通知` → `support.type.builtin.terminal.{exception,warning,notice}.koto`
  - 型 postfix Optional: `？` → `keyword.operator.optional.koto`
  - 列挙記号 中点 `・` → `punctuation.separator.list.koto`
- **AC-002**: 既存ハイライト (v1 / v2 範囲) に regression なし。v1 / v2 fixture (entity-names / max-value / incomplete-pickup / task-table / half-width-boundary) で既存パターン挙動が維持される
- **AC-003**: 新規 fixture `phase-b.koto` が `tools/vscode-koto/tests/fixtures/` に追加されており、AC-001 の全 keyword / 記号を 1 回以上含む
- **AC-004**: `について繰り返すと` (compound) が単独 `について` より先に評価される (longer-first 原則)。compound 形が単独形に分裂しない
- **AC-005**: `を受け取り` 連用形のパラメータ名が entity-names で `variable.parameter.koto` として認識される (`を受け取る` 終止形と並列)

## Intent-derived Invariants

- INV-001: memo §3 で確定した keyword / 構文のみが対象 (memo に無いものを grammar 先取りしない、v2 INV-002 を継承)
- INV-002: v1 / v2 既存パターンに regression を出さない
- INV-003: 半角スペースを語境界として認めない原則を維持 (v1 INV-003 継承)
- INV-004: 新規パターンも `(?<=^|[　。、（）「」])` または同等以上の語境界要件を持つ (1 文字 operator `？` / `・` を除き — これらは context-free に発火)
- INV-005: compound keyword (`について繰り返すと`) が単独 keyword (`について`) より配列順で先 (longer-first)
- INV-006: 既存 scope 名を再利用 (`keyword.control.throw.koto`、`keyword.control.loop.koto`、`keyword.operator.signature.parameter.koto` 等) — 既存 theme との互換性維持

## Risk Assessment

- **Risk level**: Low
- **Risk rationale**: 拡張機能の視覚レイヤーのみに影響する。失敗時の影響は「期待 scope と違う色が付く」「期待外の場所が着色される」に留まり、ランタイム挙動・データには無影響。
- **Regression risk**: v1 / v2 で動作していた highlight が変わると書き味の信用が下がる。fixture 5 本 (entity-names / max-value / incomplete-pickup / task-table / half-width-boundary) で退行が無いことを確認する
- **Data safety risk**: なし
- **Security / privacy risk**: なし
- **UX risk**: `例外` / `警告` / `通知` がユーザー定義型と同名の場合に built-in 終了型 scope で誤着色される可能性。memo §3-19 で言語組み込みと明示されているので意図通り、ただし将来 user 定義 終了型 marker が確定したらルール再検討
- **Agent misbehavior risk**: 後続 agent が memo §5 #39 未確定のコメント構文を grammar に勝手に追加する可能性 (INV-001 で防ぐ)。または memo に無い構文を grammar 先取りする可能性 (同上)

## Test Strategy

- **Unit**: 該当なし (grammar は宣言的データ)
- **Integration**: VSCode で `phase-b.koto` と既存 fixture をロード
- **Manual QA**: `Developer: Inspect Editor Tokens and Scopes` で AC-001 の全 keyword / 記号の代表トークン scope を確認 (DEFERRED — v2 と同じく theme 依存の見映えは任意確認)
- **Automated validator**:
  - `JSON.parse` で grammar 妥当性
  - `scripts/check-docs.sh` で docs 整合
  - ECMAScript regex による positive smoke test (keyword 出現 + scope 登録)
  - ECMAScript regex による regression test (v1 / v2 既存パターンが既存 fixture で従来通り発火)
- **Diff review**: 新規パターンの語境界要件、scope 名、include 順、v1 / v2 既存パターンの不変性

## Test Matrix

| ID | Source | Requirement / Invariant | Test Type | Command / File | Expected Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | TODO | Phase B 新 keyword 全部 (19 種) がそれぞれ対応 scope でハイライトされる | regex smoke + 手動 review | `phase-b.koto` + grammar | 各 keyword が fixture に出現、scope が grammar に登録 | planned |
| AC-002 | TODO | v1 / v2 既存ハイライト regression なし | regex regression test | 既存 5 fixture + grammar | v1 / v2 パターンが従来通り発火 | planned |
| AC-003 | TODO | `phase-b.koto` fixture 追加 | file existence | `tools/vscode-koto/tests/fixtures/phase-b.koto` | ファイル存在、AC-001 keyword を全部含む | planned |
| AC-004 | TODO | compound `について繰り返すと` が単独 `について` より先 | grammar 配列順確認 | `keywords-multi.patterns` 配列 | `について繰り返すと` の index が `について` より小 | planned |
| AC-005 | TODO | `を受け取り` 連用形のパラメータ名が認識される | regex smoke | `phase-b.koto` の `である X を受け取り` | `entity-names` の対応パターンが match | planned |
| INV-001 | intent | memo §3 で確定した keyword のみ | diff review | grammar 全体 | memo に無いものを追加していない | planned |
| INV-002 | intent | v1 / v2 既存パターン退行なし | AC-002 と同じ | (同上) | (同上) | planned |
| INV-003 | intent | 半角スペースを語境界として認めない | regex smoke | `half-width-boundary.koto` | 新規パターンも boundary 違反で発火しない | planned |
| INV-004 | intent | 新規パターンも語境界要件 | grammar review | grammar 各 regex | 全 multi-char パターンに lookbehind/lookahead あり (1 文字 `？` `・` を除く) | planned |
| INV-005 | intent | longer-first 原則 | AC-004 と同じ | (同上) | (同上) | planned |
| INV-006 | intent | 既存 scope 名再利用 | grammar review | scope 名一覧 | 共有可能なものは再利用 (throw / loop / signature.parameter 等) | planned |

## Manual QA Checklist

- [ ] VSCode 再起動後、`tools/vscode-koto/tests/fixtures/phase-b.koto` を開く
- [ ] AC-001 の各 keyword で `Developer: Inspect Editor Tokens and Scopes` を実行、期待 scope を確認 (DEFERRED 可、theme 依存)
- [ ] `について繰り返すと` (line 38) が 1 トークンとして compound 認識されているか確認
- [ ] `を受け取り` (line 2, 3, 18, 33) のパラメータ名 (`X`、`接頭辞`、`メッセージ`、`対象ら`) が `variable.parameter.koto` か確認
- [ ] 既存 fixture (entity-names / max-value / incomplete-pickup / task-table / half-width-boundary) で v1 / v2 highlight に regression がないか目視

## Regression Checklist

- [ ] `bash scripts/check-docs.sh` PASS
- [ ] `koto.tmLanguage.json` が `JSON.parse` を通る
- [ ] v1 / v2 fixture で既存パターンが従来通り発火 (`として終える`、`繰り返すと`、`を受け取る`、`と同じ`、`を返す`、`とする`、`である`)
- [ ] `half-width-boundary.koto` で新規パターンも boundary 違反で発火しないことを確認

## Out of Scope

- 識別子の文脈別着色拡張 (v2 範囲外の △ パターン — フィールドアクセス、メソッド呼び出し、列挙値参照、スコープ追跡)
- LSP セマンティックトークン
- コメント構文への着色 (`＃` 仮使用中、memo §5 #39 で未確定)
- 位置 access (`N 番目` / `N 番目以降` 等) の専用ハイライト (数値 + `番目` 系列は v3 範囲外、将来 v4 で検討)
- ユーザー定義 終了型 marker (未確定、memo §5 #28)

## Open Questions

- `？` / `・` の 1 文字 operator は context-free に発火するため、文字列以外の文脈でも色が付く可能性 (例: 識別子内に `？` を含むケース — 仕様で禁止だが grammar 側では制御しない)。実機で違和感が出たら lookbehind/lookahead 追加検討
- `例外` / `警告` / `通知` をユーザーが自分の型名として再利用した場合の挙動 (built-in scope が優先される)。memo §5 #28 (user 定義 終了型 marker) の方針確定後に再評価
