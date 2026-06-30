---
title: "QA Test Plan: 設計メモ Phase A/B 統合更新"
status: active
draft_status: n/a
qa_status: planned
risk: Medium
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/intent/Lang/design-memo-update/decision.md"
  - "_docs/plan/Lang/design-memo-update/plan.md"
  - "_docs/standards/japanese-lang-design-memo.md"
  - "_docs/archives/draft/Lang/discord-bot-handwrite/notes.md"
related_issues: []
related_prs: []
---

# QA Test Plan: 設計メモ Phase A/B 統合更新

## Source of Intent

- TODO: `Lang-Doc-15`
- Plan: `_docs/plan/Lang/design-memo-update/plan.md`
- Intent: `_docs/intent/Lang/design-memo-update/decision.md`

## Quality Goal

`_docs/standards/japanese-lang-design-memo.md` が **Phase A/B 手書き演習 (Lang-Chore-11 / Lang-Chore-12) で確定した全 spec 変更と全未決着論点を反映** し、project の **single source of truth として再び機能する**。同時に `_docs/draft/Lang/discord-bot-handwrite/` ディレクトリ全体が `_docs/archives/draft/Lang/discord-bot-handwrite/` に archive され、link integrity が保たれる。

更新後の memo を読めば、Phase A/B の議論経過を辿らなくても現在の koto 仕様が正しく理解できる状態にする。並行作業 (Tooling-Feat-14、将来の parser 実装) の前提を整える。

## Acceptance Criteria

- **AC-001**: Phase A/B で notes.md に記録された全 **確定 spec 変更** が memo に反映されている。具体的には:
  - 構造的ルール (句読点、動詞活用、`である`、全角 space separator、tab indent、compound keyword 無 space、変数束縛 canonical)
  - 関数シグネチャ (1 まとまり化、戻り値型必須、複数パラメータ連結)
  - 関数本体終端 / 早期終了 (`である。`、`〜 を 返す。`、mid-body `である。`、`ここまで。` 不採用)
  - メソッド・OOP (不採用確定、`の` 用途限定)
  - 引数 (位置 / キーワード両対応)
  - 型・リテラル (`無し`、`T？` Optional、null 比較型エラー、flow narrowing、`T？？` 禁止、`？` Optional 専用)
  - 条件式の語彙 (等価判定、順序比較、論理結合、真偽値明示比較)
  - 条件式の優先順位 (左結合、grouping 不採用)
  - import (`を Y として 取り込む` alias、`全て取り込む` 撤回)
  - `の` chain (3 役割、深さ制限、判定表)
  - property access (built-in 型のみ、immutable binding 限定、初版 property リスト)
  - predicate / comparison (built-in keyword vs default function)
  - 集合 disjunction (`〜 のいずれか` / `〜 に 含まれる`、中点 `・`)
  - 異常終了 (`〜 で終える` / `〜 として終える` 両立形、終了型 marker、built-in 例外/警告/通知)
  - match 構文 (`〜 について、`、暗黙 field access、暗黙終端、default 不要)
  - indexed accessor (1-indexed、inclusive 4 形)
  - no-op (`何もしない。`)
  - 型 postfix 修飾子合成 (`？` / `配列`)
- **AC-002**: Phase A/B で notes.md に記録された全 **未決着論点** が memo §5 に転記されている。具体的には:
  - catch / recover 構文
  - checked vs unchecked exception
  - user 定義 終了型 marker 構文
  - user 定義 type の derived property
  - 個別名 alias の import (`〜 から X を Y として 取り込む。`)
  - 辞書 / 集合 / タプル literal
  - コメント構文 (`＃` 仮使用中)
  - ループ syntax 統一
  - 論理結合の口語的 form 試験運用結果
  - 真偽値中間束縛構文
  - 比較演算の `空である` 述語の正式採否
  - インスタンス property の lazy/eager 戦略
  - 部分型 / generic / pattern matching (型システム本格設計時)
  - `を取り込む` 無スペース form
  - `を返す` の空白対応 (compound keyword 化で解決済との対応関係明記)
  - インデント tab 化 (E-4 確定で解決済との対応関係明記)
  - `真` の IME 問題
- **AC-003**: notes.md (sample-1.koto / sample-2.koto / handler.koto を含むディレクトリ全体) が `_docs/archives/draft/Lang/discord-bot-handwrite/` へ `git mv` で移送されている。archive 先 notes.md 冒頭に archive マーク (status: archived、archive 日、memo 参照) が追記されている。
- **AC-004**: memo 既存セクション番号 §3-1〜§3-18 が維持され、新規追加は §3-19 以降に続いている。memo 構造の論理的連続性が保たれている。
- **AC-005**: 撤回された option (「たぶん〜」、メソッド将来追加、`ここまで。`、`もしくは`、`未満` / `超える`、`は` 形変数束縛、value-level `または` distribute、終了型の継承、`〜 として 全て取り込む`) が memo 内で **撤回マーク付きで** 記録されている (歴史を消さず、誤った参照を残さない)。
- **AC-006**: memo / 他 Intent / 他 Plan / 他文書から旧 notes.md パス (`_docs/draft/Lang/discord-bot-handwrite/notes.md`) への参照リンクが、archive 先パス or 該当 memo セクションへの参照に張り替えられている。link 切れは 0 件。
- **AC-007**: `scripts/check-docs.sh` 等のドキュメント validator が PASS する。markdown 構造 (見出し階層、リスト、コードブロック) が崩れていない。
- **AC-008**: 各 Phase (Plan §Tasks の Phase 1〜7) ごとに commit が分割されている。1 巨大 commit ではなく、各 Phase が独立した review unit として確認可能。

## Intent-derived Invariants

- INV-001: 「確定した spec 変更」(notes.md) 全件が memo §3 に反映 (改訂 or 新規セクション)
- INV-002: 「未決着論点」(notes.md) 全件が memo §5 に転記
- INV-003: 撤回された option は撤回マーク付きで記録される
- INV-004: memo セクション番号 §3-1〜§3-18 維持、新規は §3-19 以降
- INV-005: notes.md とその同梱ファイルはディレクトリごと `git mv` で archive
- INV-006: archive 先 notes.md 冒頭に archive 完了マーク追記
- INV-007: 旧 notes.md パスへの参照リンクは張り替え or 削除、link 切れ 0
- INV-008: 設計議論の再開なし (新 spec 追加 / 既存 spec 修正は本タスクで扱わない)
- INV-009: Phase 単位 commit 分割
- INV-010: vocabulary 固定原則に基づき canonical / 不採用 form の対が明示

## Risk Assessment

- **Risk level**: Medium
- **Risk rationale**: memo は project の single source of truth であり、誤りは下流の Tooling / parser に伝播する。Phase A/B 確定事項の漏れや誤転記が起きると、後続作業者が誤った仕様を実装しうる。
- **Regression risk**: memo の既存記述が誤って削除されたり、撤回マークなしに置換されると、設計史が断たれて将来の参照に支障。Phase 単位 commit + diff review で防ぐ。
- **Data safety risk**: なし (documentation のみ)。
- **Security / privacy risk**: なし。
- **UX risk**:
  - memo が 2x の規模になることで読み手の navigation が困難化する可能性 (目次追加は Follow-up)
  - archive 後に旧 notes.md パスを参照していた agent / 人が「ファイルが消えた」と誤認する可能性 (archive マークと redirection 注釈で対処)
- **Agent misbehavior risk**:
  - 後続 agent が「memo に書かれていないから未確定」と誤判断する可能性 → memo に未決着論点も明示することで防ぐ (AC-002)
  - 設計議論を勝手に再開して spec を変える可能性 → Non-Goals と INV-008 で明示し、PR review で確認
  - notes.md を archive せず draft のまま放置する可能性 → AC-003 で完了基準として強制
- **Process risk**: 改訂中に「memo と notes.md の二重 source」状態が一時的に発生。Phase 単位で短期間に完結させることで影響最小化。

## Test Strategy

- **Unit**: 該当なし (documentation 更新)
- **Integration**: 該当なし
- **Manual review (主軸)**:
  - Plan の Scope 表を **checklist 化** し、各セクションの改訂が完了しているか目視確認
  - notes.md の「確定した spec 変更」「未決着論点」「Phase B 議論項目 (resolved 状態)」を 1 項目ずつ拾い、memo の対応セクションに反映されているか cross-reference
  - 撤回マークの存在を grep で確認 + 文脈レビュー
- **Validator / static check**:
  - `scripts/check-docs.sh` 実行 (frontmatter 完全性、参照リンク健全性、markdown render 妥当性)
  - `grep -r "discord-bot-handwrite/notes.md"` で旧パス残存検出 (0 件であることを確認)
  - `git log --follow` で archive 履歴の連続性確認
- **Diff review**:
  - PR 上で Phase 単位の commit を順に review
  - 各 commit が単一の論理単位 (1 Phase) で完結しているか確認
  - 撤回・置換が明示されているか確認
  - 設計議論の再開 (新 spec 追加) が混入していないか確認

## Test Matrix

| ID | Source | Requirement / Invariant | Test Type | Command / File | Expected Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | TODO | 確定 spec 変更全件が memo に反映 | manual review checklist + cross-reference | notes.md「確定した spec 変更」セクション ↔ memo §3 | 全 20+ 項目の対応関係が成立する | planned |
| AC-002 | TODO | 未決着論点全件が memo §5 に転記 | manual review checklist + cross-reference | notes.md「未決着論点」「Phase B 議論項目」 ↔ memo §5 | 全 13+ 項目の対応関係が成立する | planned |
| AC-003 | TODO | notes.md ディレクトリ全体が archive | file existence + git log | `_docs/archives/draft/Lang/discord-bot-handwrite/` | ディレクトリ存在、notes.md 冒頭に archive マーク、`git log --follow` で履歴連続 | planned |
| AC-004 | TODO | memo セクション番号 §3-18 維持 + §3-19 以降 | diff review | memo 見出し構造 | §3-1〜§3-18 既存 + §3-19〜§3-26 新規追加で番号連続 | planned |
| AC-005 | TODO | 撤回 option の撤回マーク付き記録 | grep + diff review | memo 内 | 「たぶん〜」「メソッド将来追加」「ここまで」「もしくは」「未満」「超える」「は形」「value-level または distribute」「終了型継承」「全て取り込む」が撤回マーク付きで存在 | planned |
| AC-006 | TODO | 旧 notes.md パスへの参照 link 切れ 0 | grep + manual link check | `grep -r "_docs/draft/Lang/discord-bot-handwrite/notes.md" _docs/` | 0 件 (張り替え済 or 削除済) | planned |
| AC-007 | TODO | docs validator PASS | `scripts/check-docs.sh` | リポジトリ root で実行 | exit 0、warning なし | planned |
| AC-008 | TODO | Phase 単位 commit 分割 | `git log` | feature branch | 各 Phase が独立した commit (Phase 1〜7 で 7+ commit) | planned |
| INV-001 | intent | 確定事項全件反映 | AC-001 と同じ | (同上) | (同上) | planned |
| INV-002 | intent | 未決着論点全件転記 | AC-002 と同じ | (同上) | (同上) | planned |
| INV-003 | intent | 撤回マーク付き記録 | AC-005 と同じ | (同上) | (同上) | planned |
| INV-004 | intent | セクション番号連続性 | AC-004 と同じ | (同上) | (同上) | planned |
| INV-005 | intent | ディレクトリ単位 archive | AC-003 と同じ | (同上) | (同上) | planned |
| INV-006 | intent | archive マーク追記 | AC-003 と同じ | (同上) | (同上) | planned |
| INV-007 | intent | link 切れ 0 | AC-006 と同じ | (同上) | (同上) | planned |
| INV-008 | intent | 設計議論再開なし | diff review | feature branch の diff 全体 | Phase A/B で確定していない新 spec の追加が 0 件 | planned |
| INV-009 | intent | Phase 単位 commit | AC-008 と同じ | (同上) | (同上) | planned |
| INV-010 | intent | canonical / 不採用 form 対の明示 | diff review | memo 内 | 主要 vocabulary で canonical / 不採用 form 対の記述が存在 | planned |

## Manual QA Checklist

### Phase A/B 確定 spec 変更の反映確認 (AC-001)

notes.md「確定した spec 変更」セクションを開きながら、各項目について memo への反映を確認:

- [ ] 構造的ルール 6 項目 (句読点、動詞活用、`である`、全角 space separator、tab indent、compound keyword 無 space、変数束縛 canonical) → memo §3-1
- [ ] 関数シグネチャ 4 項目 → memo §3-2
- [ ] 関数本体終端 / 早期終了 4 項目 → memo §3-9 (or 新規セクション)
- [ ] メソッド・OOP 2 項目 → memo §3-11 (撤回マーク付き)
- [ ] 引数 1 項目 → memo §3-8
- [ ] 型・リテラル 7 項目 → memo §3-3
- [ ] 条件式の語彙 4 項目 → memo §3-7
- [ ] 条件式の優先順位 + grouping 不採用 → memo 新規 (条件式 セクション)
- [ ] import 4 項目 → memo §3-13
- [ ] `の` chain → memo §3-25 (新規) + §3-16 改訂
- [ ] property access → memo §3-16 改訂 + §3-25 (新規)
- [ ] predicate / comparison → memo §3-20 (新規)
- [ ] 集合 disjunction → memo §3-21 (新規)
- [ ] 異常終了 → memo §3-19 (新規)
- [ ] match 構文 → memo §3-22 (新規)
- [ ] indexed accessor → memo §3-5 拡張
- [ ] no-op → memo §3-24 (新規)
- [ ] 型 postfix 修飾子合成 → memo §3-23 (新規)
- [ ] 変数束縛 canonical 形 → memo §3-26 (新規) or §3-1 統合

### Phase A/B 未決着論点の転記確認 (AC-002)

notes.md「未決着論点」+ Phase B 議論項目 (resolved 後の残り) を 1 項目ずつ確認:

- [ ] catch / recover 構文 → memo §5
- [ ] checked vs unchecked exception → memo §5
- [ ] user 定義 終了型 marker → memo §5
- [ ] user 定義 type の derived property → memo §5
- [ ] 個別名 alias import → memo §5
- [ ] 辞書 / 集合 / タプル literal → memo §5
- [ ] コメント構文 → memo §5
- [ ] ループ syntax 統一 → memo §5
- [ ] 論理結合 口語的 form 試験 → memo §5
- [ ] 真偽値中間束縛構文 → memo §5
- [ ] 比較演算 `空である` 述語 → memo §5
- [ ] property lazy/eager 戦略 → memo §5
- [ ] 部分型 / generic / pattern matching → memo §5
- [ ] sugar 形 `として終える` 成立条件正式化 → memo §5
- [ ] `真` IME 問題 → memo §5

### 撤回 option のマーク確認 (AC-005)

memo 内で以下が撤回マーク付きで記録されているか:

- [ ] 「たぶん〜」(Optional の暫定案)
- [ ] メソッド将来追加 (§3-11 既存)
- [ ] `ここまで。` (Phase B で不採用確定)
- [ ] `もしくは` (B-3 で不採用)
- [ ] `未満` / `超える` (条件式語彙、不採用)
- [ ] 変数束縛 `は` 形 (A-8 で不採用)
- [ ] value-level `または` distribute (B-2 で不採用)
- [ ] 終了型の継承 (C-1 で不採用)
- [ ] `〜 として 全て取り込む` (import で撤回済)

### archive 処理確認 (AC-003 / AC-006)

- [ ] `_docs/draft/Lang/discord-bot-handwrite/` が存在しない (`git mv` 済)
- [ ] `_docs/archives/draft/Lang/discord-bot-handwrite/` が存在し、4 ファイル (notes.md + sample-1.koto + sample-2.koto + handler.koto) が含まれる
- [ ] archive 先 notes.md 冒頭に archive マーク (status: archived、日付、memo 参照) が記載されている
- [ ] `grep -r "_docs/draft/Lang/discord-bot-handwrite/notes.md" _docs/` で残存参照が 0 件 (link 切れ 0)
- [ ] `grep -r "draft/Lang/discord-bot-handwrite" _docs/` で archive 先以外の参照が張り替え or 削除されている

### memo 構造確認 (AC-004 / AC-007 / AC-008)

- [ ] memo の見出し階層が崩れていない (h2 / h3 / 表 等の render 確認)
- [ ] §3-1〜§3-18 が既存通り存在
- [ ] §3-19〜§3-26 (新規) が連続番号で追加
- [ ] frontmatter の `updated_at` が更新されている
- [ ] `scripts/check-docs.sh` が PASS
- [ ] git log で Phase 単位の commit 分割が確認できる (7+ commits)

## Regression Checklist

- [ ] memo §1 / §2 / §6 (動機・評価基準・原則) は本タスクで変更されていない (Non-Goal)
- [ ] memo §4 例文集の既存例 (4-1〜4-6) は新仕様での書き直しのみで、新規例追加は 4 例以内
- [ ] notes.md archive 後、git history 上で `_docs/draft/Lang/discord-bot-handwrite/notes.md` の編集履歴が連続して辿れる (`git log --follow`)
- [ ] Tooling-Feat-9 / Tooling-Feat-10 の関連 doc (`_docs/intent/Tooling/vscode-koto-grammar*/`) が本タスクで変更されていない

## High-risk Checklist

- [ ] Phase 単位の commit 分割が守られている (1 巨大 commit が混入していない)
- [ ] memo 既存記述の削除箇所が、撤回マーク付き記録 or 該当 spec 変更の cross-reference で説明されている (silent deletion なし)
- [ ] 新規 spec (Phase A/B で確定していないもの) が混入していない (INV-008)
- [ ] archive 後の notes.md は read-only / immutable と看做せる状態 (誤編集を招く文言なし)

## Out of Scope

- memo に目次 (TOC) を追加する作業 (Follow-up)
- 未決着論点ごとの個別タスク起票 (Follow-up)
- parser 実装着手タスクの起票 (Follow-up、Phase C 相当)
- 標準ライブラリ設計タスクの起票 (Follow-up)
- Tooling-Feat-14 (grammar v3) の plan / intent / qa 作成 (本 memo 更新完了後の別タスク)
- memo の構造再設計 (セクション番号付け方式の変更等)
- notes.md 同梱の sample-*.koto / handler.koto の内容更新 (archive のみ、書き換えなし)
- 設計議論の再開 (Phase A/B で確定したものをそのまま反映、改善案は別 issue)

## Open Questions

- archive 先 notes.md の冒頭 archive マークは specific な format が決まっていない (status: archived の frontmatter 値 + 本文冒頭の説明文? どの程度詳細に書くか) — 実装時に judgment
- memo §4 例文集の新規例 (match / 異常終了 / 集合 disjunction / property access) について、各例の題材を Discord bot 関連で揃えるか、別文脈にするか — 実装時に judgment
- `scripts/check-docs.sh` の存在と動作内容を未確認 — 実装時に確認、なければ別 follow-up 検討
- memo 改訂中に新たに気づく不整合 (Phase A/B 確定事項間の矛盾、用語の揺れ等) を、本タスクで修正するか別 issue にするか — case-by-case、影響大なら別 issue
