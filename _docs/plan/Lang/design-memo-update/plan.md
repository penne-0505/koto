---
title: 設計メモ Phase A/B 統合更新
status: proposed
draft_status: n/a
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/intent/Lang/design-memo-update/decision.md"
  - "_docs/qa/Lang/design-memo-update/test-plan.md"
  - "_docs/standards/japanese-lang-design-memo.md"
  - "_docs/archives/draft/Lang/discord-bot-handwrite/notes.md"
related_issues: []
related_prs: []
---

<!-- Canonical path: _docs/plan/Lang/design-memo-update/plan.md -->

<!-- markdownlint-disable MD029 -->
<!-- Preserve global task IDs in ordered lists. -->

# 設計メモ Phase A/B 統合更新

## Overview

`_docs/standards/japanese-lang-design-memo.md` (以降 memo) を、Phase A/B 手書き演習 (Lang-Chore-11 / Lang-Chore-12) で確定した spec 変更で更新し、`_docs/draft/Lang/discord-bot-handwrite/notes.md` (以降 notes.md) を archive する。

これにより memo を **single source of truth** に戻し、parser 実装着手 (将来) と Tooling-Feat-14 (VSCode grammar v3) の前提を整える。

Phase A/B で notes.md に蓄積された確定事項は 20+ 件、新規未決着論点は 10+ 件。memo 現状 484 行 → 改訂後 700-900 行程度を想定。

## Scope

### 改訂対象セクション (memo §3 既存)

以下 11 セクションを Phase A/B 確定事項で改訂する:

| §       | 改訂方針                                                                                            |
|---------|-----------------------------------------------------------------------------------------------------|
| 3-1     | **強化** — 分かち書きを「全角 space は唯一の token separator、newline/indent は purely visual、tab indent canonical、compound keyword 内 space なし」へ |
| 3-2     | **拡張** — 関数シグネチャの形式 `[修飾] 関数 として [params] [returnT] を 返す [name] は、`         |
| 3-3     | **書き換え** — 「たぶん〜」候補を撤回、`T？` postfix Optional 採用、flow-sensitive narrowing 追加     |
| 3-5     | **拡張** — indexed accessor 4 形 (`N 番目` / `以降` / `以前` / `から〜まで`)、exclusive 不採用       |
| 3-7     | **拡張** — 比較演算 (`より大きい` / `より小さい` / `以上` / `以下` / `と異なる`) 追加、`未満`/`超える` 不採用 |
| 3-9     | **大幅拡張** — throw 部分を § 異常終了 へ分離、`である。` mid-body 早期終了、句読点ルール明文化       |
| 3-10    | **拡張** — 中点 `・`、`？` (型 postfix)、tab (indent) を追加                                         |
| 3-11    | **書き換え** — メソッド将来追加を撤回 (不採用確定)、`自身` 概念撤回                                  |
| 3-13    | **拡張** — alias import (`〜 を Y として 取り込む`)、`の` chain 深さ制限、type-as-namespace 1 段     |
| 3-16    | **再構成** — property access (immutable binding 上、built-in 型のみ)、built-in property 初版 list   |
| 3-18    | **軽更新** — 宣言形 map/filter の Phase B 持ち越し明記                                              |

### 新規セクション (memo §3 追加)

| §         | 内容                                                                              |
|-----------|-----------------------------------------------------------------------------------|
| 3-19 (新) | 異常終了 / 終了型 — `〜 で終える` / `〜 として終える` 両立形、終了型 marker、built-in `例外`/`警告`/`通知` |
| 3-20 (新) | predicate と comparison の区別 — comparison = built-in keyword、predicate = default function (particle 埋め込み命名規約) |
| 3-21 (新) | 集合 disjunction — `〜 のいずれか` 修飾形 / `〜 に 含まれる` 完結形、中点 `・` 列挙 |
| 3-22 (新) | match 構文 — `〜 について、` + 暗黙 field access、暗黙終端、default 不要、fall-through なし |
| 3-23 (新) | 型の postfix 修飾子合成 — `？` / `配列` を左→右に累積                              |
| 3-24 (新) | no-op 構文 — `何もしない。`                                                        |
| 3-25 (新) | `の` chain の意味論 — 3 役割 (field / module nav / type-as-namespace)、深さ制限、value method dispatch 禁止 |
| 3-26 (新) | 変数束縛 canonical 形 — `を` 形のみ、`は` 形不採用                                |

### §4 例文集の更新

- 既存 6 例 (4-1〜4-6) を Phase A/B 仕様に書き直し
- 新規例 (match、異常終了、集合 disjunction、property access) を最小限追加
- 例文は新仕様の代表的 use case をカバーする目的で、網羅は狙わない

### §5 未決定事項の更新

- **解決済**: #2 メソッド構文 (不採用確定) / #4 エラーハンドリング throw 側 (確定、catch 側のみ持ち越し) / #9 Optional 型構文 (`T？` 確定) — 解決マーク + 撤回経緯記録
- **新規未決着論点 (Phase A/B 由来)** を §5 に転記:
  - catch / recover 構文
  - checked vs unchecked exception
  - user 定義 終了型 marker
  - user 定義 type の derived property
  - 個別名 alias import
  - 辞書 / 集合 / タプル literal
  - コメント構文 (`＃` 仮使用中)
  - ループ syntax 統一
  - 論理結合の口語的 form 試験運用結果
  - 真偽値中間束縛構文
  - 比較演算の `空である` 述語の正式採否
  - インスタンス property の lazy/eager 戦略
  - 部分型 / generic / pattern matching (型システム本格設計時)

### §7 次のステップの更新

- ✅ TextMate Grammar v1, v2 完了
- ✅ Discord bot 手書き演習 Phase A, B 完了
- 次: VSCode Grammar v3 (Tooling-Feat-14、起票済) / parser 実装着手 (未起票) / 標準ライブラリ設計 (未起票)

### notes.md の archive

- `_docs/draft/Lang/discord-bot-handwrite/notes.md` (sample-1.koto / sample-2.koto / handler.koto を含むディレクトリごと) を `_docs/archives/draft/Lang/discord-bot-handwrite/` へ `git mv`
- archive 時に notes.md 冒頭に「archive 完了マーク」を追記 (status: archived 等)

### 影響範囲

- **memo に依存する Tooling-Feat-14 (grammar v3)**: memo を読んで grammar に反映するため、memo 更新が先。Tooling-Feat-14 の前提
- **将来の parser 実装**: memo を仕様正本として参照するため、memo の正確さが parser の正しさを決める
- **既存 Intent / Plan ドキュメント**: notes.md への参照リンクを memo (or archive path) に張り替える必要があるか確認

## Non-Goals

- **設計議論の再開** — Phase A/B で確定したものをそのまま反映する。新たな議論や spec 修正は持ち込まない。改善点を発見したら新規 Issue / TODO として起票し、本タスクでは扱わない
- **新規 spec の追加** — memo に記録するのは Phase A/B で確定済みのもの + 既決事項のみ。投機的拡張は対象外
- **例文集の網羅的拡充** — 新規例は新仕様カバレッジ目的の最小限のみ。既存例の機械的な仕様適合のみで完了
- **parser 実装の準備物作成** — IR 設計、文法定義、tokenizer/lexer 仕様は別タスク (Phase C 相当)
- **VSCode Grammar v3 の実装** — Tooling-Feat-14 で別途
- **notes.md ディレクトリ全体の archive 整理** — sample-1.koto / sample-2.koto / handler.koto / notes.md を含むディレクトリ単位で archive。個別ファイルの再構成はしない
- **設計メモの構造再設計** — セクション番号付け (3-1, 3-2, ...) や全体構成は維持。改訂と追加のみ

## Requirements

- **Functional**:
  - 上記 Scope セクションで列挙した全 Phase A/B 確定事項が memo に反映されている
  - 全 未決着論点が memo §5 に転記されている
  - 既存 memo 内容との矛盾がない (撤回・置換は撤回経緯を残す)
  - notes.md と memo の参照関係が整合している (memo から notes.md への参照は archive path に張り替え or 削除)
  - notes.md が `_docs/archives/draft/Lang/discord-bot-handwrite/` へ git mv 済み
- **Non-Functional**:
  - vocabulary 固定原則を守る (canonical form の重複表記を作らない、撤回した form は明示)
  - section の論理構造 (3-1 など番号付け、見出し階層) が一貫している
  - markdown が render される (見出し階層、リスト構造、コードブロック等)
  - `scripts/check-docs.sh` 等の validator が PASS する
  - frontmatter の `updated_at` を更新する

## Tasks

Plan / Intent / QA test-plan 作成後、以下の phase 構成で memo 改訂を進める。

### Phase 0: 準備

1. Plan (本書) / Intent (`_docs/intent/Lang/design-memo-update/decision.md`) / QA test-plan (`_docs/qa/Lang/design-memo-update/test-plan.md`) を作成
2. ユーザー合意取得

### Phase 1: memo §3 既存セクションの改訂

3. §3-1 (語順・分かち書き) を強化
4. §3-2 (宣言の構文) を拡張
5. §3-3 (型の表現) を書き換え
6. §3-5 (インデックス) を拡張
7. §3-7 (等価判定) を拡張
8. §3-9 (制御フロー) を大幅拡張
9. §3-10 (記号の用途) を拡張
10. §3-11 (型定義) を書き換え
11. §3-13 (モジュール) を拡張
12. §3-16 (プロパティアクセス) を再構成
13. §3-18 (高階関数 / 宣言形) を軽更新

### Phase 2: memo §3 新規セクション追加

14. §3-19 異常終了 / 終了型
15. §3-20 predicate と comparison の区別
16. §3-21 集合 disjunction
17. §3-22 match 構文
18. §3-23 型の postfix 修飾子合成
19. §3-24 no-op 構文
20. §3-25 `の` chain の意味論
21. §3-26 変数束縛 canonical 形

### Phase 3: §4 例文集の更新

22. 既存 4-1〜4-6 を Phase A/B 仕様に書き直し
23. 新規例 (match、異常終了、集合 disjunction、property access の 4 例) を追加

### Phase 4: §5 未決定事項の更新

24. 解決済 (#2 / #4 / #9) に解決マーク + 撤回経緯記載
25. 新規未決着論点 (Phase A/B 由来 ~13 項目) を追加

### Phase 5: §7 次のステップの更新

26. 完了済 (Tooling-Feat-9 / -10、Lang-Chore-11 / -12) を ✅ マーク
27. 次の steps (Tooling-Feat-14、parser 実装、標準ライブラリ設計) を追記

### Phase 6: notes.md archive

28. `_docs/draft/Lang/discord-bot-handwrite/` を `_docs/archives/draft/Lang/discord-bot-handwrite/` へ `git mv`
29. archive notes.md 冒頭に archive マーク追記 (status: archived 等)
30. memo / 他 Intent / Plan からの notes.md 参照を archive path に張り替え

### Phase 7: 検証

31. `scripts/check-docs.sh` 等の validator 実行
32. manual review checklist で全確定事項のカバレッジ確認
33. cross-reference check (notes.md → memo の項目対応確認)
34. verification (`_docs/qa/Lang/design-memo-update/verification.md`) 完成
35. `qa-review` skill で verdict 確認

## QA Plan

- **QA document**: `_docs/qa/Lang/design-memo-update/test-plan.md`
- **Risk level**: Medium (memo は project の single source of truth、誤りは下流の Tooling / parser に伝播)
- **Test strategy**:
  - **Manual review (主)**: Phase A/B 確定事項のチェックリスト照合 (Plan の Scope 表をそのまま checklist として使う)
  - **Cross-reference check**: notes.md (archived) と memo の対応関係確認 (notes.md の確定事項が漏れなく memo に転記されているか)
  - **Link integrity**: memo 内 / Intent / Plan から memo / notes.md (archive) への参照リンクが断たれていない
  - **Markdown render check**: 見出し・リスト・コードブロックの render が崩れていない
  - **Validator**: `scripts/check-docs.sh` 等の docs validator が PASS する
  - **Diff review**: 撤回・置換が明示されている、新規追加と既存内容に矛盾がない
- **Acceptance criteria と invariant の紐づけ** (詳細は test-plan で):
  - AC-001 (確定事項反映) → manual review checklist + cross-reference check
  - AC-002 (未決着論点転記) → manual review checklist + cross-reference check
  - AC-003 (notes.md archive) → file existence check + git mv 履歴確認 + link integrity check
  - intent-derived INV (整合性、矛盾なし、vocabulary 固定維持) → diff review

## Deployment / Rollout

- memo 更新と notes.md archive は documentation のみの変更
- ロールバック: `git revert` で改訂前の memo / notes.md 状態に復帰可能
- archive は `git mv` で履歴維持、ロールバックも `git mv` で逆方向可能
- 並行作業ブランチ: 不要 (main / 作業ブランチで直接コミット、PR 単位で review)
- Phase 単位でコミット分割推奨 (review しやすさ + ロールバック単位の細分化)

<!-- markdownlint-enable MD029 -->
