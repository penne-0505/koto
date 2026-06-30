---
title: 設計メモ Phase A/B 統合更新 設計判断
status: proposed
draft_status: n/a
created_at: 2026-07-01
updated_at: 2026-07-01
references:
  - "_docs/plan/Lang/design-memo-update/plan.md"
  - "_docs/qa/Lang/design-memo-update/test-plan.md"
  - "_docs/standards/japanese-lang-design-memo.md"
  - "_docs/archives/draft/Lang/discord-bot-handwrite/notes.md"
related_issues: []
related_prs: []
---

# 設計メモ Phase A/B 統合更新 設計判断

## Context

Phase A (Lang-Chore-11) / Phase B (Lang-Chore-12) の Discord bot 手書き演習で、memo に書かれていない・あるいは memo の暫定案を上書きする形で、多数の spec が確定した。これらは現状 `_docs/draft/Lang/discord-bot-handwrite/notes.md` に蓄積されているが:

- notes.md は **draft 文書** であり、design memo に対する一次的な議論ログという位置づけ
- 確定した spec が draft に閉じ込められたままでは、parser 実装や標準ライブラリ設計が「どの spec を正本とすべきか」迷う
- 並行作業 (Tooling-Feat-14 = VSCode grammar v3) が memo を読みに来ても、Phase A/B の確定事項を見つけられない
- 時間が経つと「notes.md と memo のどちらが正しいか」が author 自身ですら不明になる risk

memo を single source of truth に戻す必要がある。Phase A/B で確定した 20+ 件の spec 変更と 13+ 件の新規未決着論点を memo に統合し、notes.md は archive する。

## Decision

memo (`_docs/standards/japanese-lang-design-memo.md`) を以下の方針で更新する:

1. **既存 §3 セクションの改訂** (§3-1 / 3-2 / 3-3 / 3-5 / 3-7 / 3-9 / 3-10 / 3-11 / 3-13 / 3-16 / 3-18 の 11 個)
2. **§3 新規セクションの追加** (§3-19〜3-26 の 8 個 — 異常終了 / predicate と comparison / 集合 disjunction / match / 型 postfix / no-op / `の` chain / 変数束縛 canonical)
3. **§4 例文集の更新** (既存 6 例を新仕様に書き直し + 新規 4 例を追加)
4. **§5 未決定事項の更新** (解決済 3 件にマーク + Phase A/B 由来の新規未決着論点 ~13 件を転記)
5. **§7 次のステップの更新** (完了済を ✅ マーク + 次ステップ追記)
6. **notes.md の archive** (`_docs/draft/Lang/discord-bot-handwrite/` を `_docs/archives/draft/Lang/discord-bot-handwrite/` へ `git mv`)

改訂は **section ごとに分割した phased approach** で進める (Plan 参照)。各 phase の終了時に diff review を行い、撤回・置換が明示されているか確認する。

### 撤回・置換の扱い

memo 既存記述を撤回 / 置換する場合は以下のルールを守る:

- **撤回した case**: 撤回された option / proposed name を「撤回」 marker 付きで簡潔に記録 (歴史を消さない、誤った参照を残さない)。例: `~~たぶん〜~~ → 撤回。`T？` postfix Optional を採用 (§3-3 参照)`
- **置換**: 旧記述を削除して新記述で置き換え。撤回経緯が重要な場合のみ「撤回」記録を残す
- **拡張**: 旧記述を維持しつつ新規箇条書き / サブセクションを追加

「歴史を完全に消す」「歴史だけ残して新仕様を散逸させる」のどちらも避ける。**正本としての可読性を最優先**しつつ、撤回した option を辿れる程度に記録を残す。

### vocabulary 固定原則の徹底

memo §3-1 の語彙固定原則 (memo §3-1) を、改訂で再確認する。Phase A/B で確定した **canonical form (採用) / 不採用 form (撤回)** をそれぞれ明示することで、書き手の判断を支援する。例:

- canonical: `または`、`もしくは` は不採用
- canonical: `以上` / `以下`、`未満` / `超える` は不採用
- canonical: `を` 形変数束縛、`は` 形は不採用

### notes.md archive のタイミング

archive は memo 改訂が完了し、cross-reference check で「notes.md の全確定事項が memo に転記されている」ことが確認できた後に実施する。順序を逆にすると、memo 改訂中に notes.md を参照したい場面で `git log` を遡る必要が出てしまい不便。

archive 時には、archive 先 notes.md の冒頭に **archive 完了マーク** (status: archived、archive 日、memo 参照先) を追記し、将来「これは draft の歴史で、正本は memo」という認識を強制する。

## Alternatives

- **memo を更新せず notes.md を正本扱いする**: draft 文書を normative にすると、draft の status semantic (proposed / exploring) と矛盾する。また `_docs/standards/` ではなく `_docs/draft/` 配下にあることが standard 化の signal にならない。却下。
- **memo を「Phase A/B sections」として別ファイルに分離する**: `japanese-lang-design-memo.md` と `japanese-lang-design-memo-phase-b.md` のように分けると、書き手 / 読み手が「どこに何があるか」を覚えないといけない。single source of truth の意味が薄れる。却下。
- **memo を完全書き直し (re-author from scratch)**: 既存 memo の論理構造 (§3-1 から §3-18 まで番号付け、§4 例文、§5 未決定、§6 原則、§7 次のステップ) は機能している。完全書き直しは無駄な労力 + 既存参照 (Intent / Plan / 他 doc) が断たれる。却下。本タスクは **追記・置換・拡張** に留める。
- **archive を後回しにする (memo 更新だけ先に commit)**: notes.md を archive せずに残すと、「memo と notes.md のどちらが正本か」の曖昧性が残る。memo 更新の完了基準を「archive まで完了」と定義することで、曖昧性を構造的に排除する。本決定通り。
- **Phase 単位の commit 分割をしない (1 commit にまとめる)**: 1 commit が巨大化すると review 困難。Phase 単位 (Phase 1 既存改訂 / Phase 2 新規追加 / Phase 3 例文 / 等) で commit を分けることで、review しやすさ + ロールバック粒度の細分化を確保。本決定通り。

## Rationale

memo を single source of truth に戻すことは、koto project の next phase (parser 実装、標準ライブラリ設計、Tooling-Feat-14) の前提条件。これが未完だと:

- 並行作業者 (人間 / agent) が「どの仕様を正と扱うべきか」迷う
- notes.md と memo のどちらか / 両方を参照する必要があり、認知負荷が高い
- 時間経過で notes.md の draft 性が薄れ、「事実上の正本」になってしまう (status 管理の崩壊)

phased approach で進める理由:

- memo 484 行 → 700-900 行という大規模改訂を 1 セッションで通すと、review が困難 + 中断時の再開が難しい
- Phase ごとに完結した unit (例: §3 既存改訂 → §3 新規追加 → §4 例文 → 等) として進めることで、各 phase 終了時に diff review + 中断可能
- ロールバック単位も細分化される

撤回・置換のルール (「撤回 marker を残しつつ正本可読性優先」) は、設計史を辿りたい場面 (なぜこの form が canonical になったか) と、現在の正本として読みたい場面 (今 koto を書くときの参照) の両方を支える。

## Consequences / Impact

- memo が **2x 近い行数** になる (484 → 700-900 行)。読み手の navigation には目次的な仕掛けが要るかもしれない (本タスクでは目次追加までは Non-Goal だが、改訂後に検討)
- notes.md と sample-*.koto / handler.koto が archive 移動する。これらへの参照リンクは memo / 他 Intent / Plan で発生している可能性があり、張り替えが必要 (link integrity check で確認)
- Tooling-Feat-14 が memo を読みに来る前提が整う。Tooling-Feat-14 の作業が effectively unblocked になる
- Phase A/B の議論経過 (notes.md 全体) は git 履歴 + archive で保全される。設計史の参照可能性は維持される
- memo 改訂中は「memo と notes.md の二重 source」状態が一時的に発生する。改訂期間を短く保つことで影響を最小化 (1 セッション or 数セッション内で完結させる)
- 設計議論の禁欲 (Non-Goals) を守ることで、本タスクの scope creep を防ぐ。改善案を発見しても本タスクでは扱わず、別 issue / TODO 化する規律が必要

## Quality Implications

- **正本の正確性** が project 全体の品質を決める。Phase A/B 確定事項のチェックリスト照合で抜け漏れを構造的に防ぐ (QA test-plan の test matrix に直接マッピング)
- **vocabulary 固定原則の徹底** が memo の signal-to-noise ratio を維持する。撤回した form を残し続けると「どれが canonical か」が曖昧になる
- **section 番号付け一貫性** が navigation と長期保守性を支える。§3-19 から §3-26 へ続ける既存番号系統を維持する (memo 構造再設計は Non-Goal)
- **archive 後の link integrity** が「memo を正本として参照する」運用を支える。link 切れがあると、参照先を探すために notes.md の歴史を遡る羽目になる

## Intent-derived Invariants

- INV-001: 「確定した spec 変更」(notes.md) に列挙された 20+ 件すべてが memo §3 に反映される (改訂 or 新規セクション)。漏れがあった場合は QA で検出される
- INV-002: 「未決着論点」(notes.md) に列挙された全件が memo §5 に転記される
- INV-003: 撤回された option (「たぶん〜」、メソッド将来追加、`ここまで。`、`もしくは`、`未満` / `超える`、`は` 形変数束縛、value-level `または` distribute、終了型の継承、etc.) は memo に **撤回 marker 付きで** 記録される (歴史を消さない、誤参照を残さない)
- INV-004: memo 既存セクション番号 (§3-1〜§3-18) は維持され、新規セクションは §3-19 以降に続けて番号付けされる (memo 構造の論理的連続性)
- INV-005: notes.md とその同梱ファイル (sample-1.koto / sample-2.koto / handler.koto) はディレクトリごと `_docs/archives/draft/Lang/discord-bot-handwrite/` に `git mv` される (個別ファイルの分散 archive は不可)
- INV-006: archive 後の notes.md の冒頭には **archive 完了マーク** (status / archive 日 / memo 参照) が追記される
- INV-007: memo / Intent / Plan / 他文書から notes.md (旧パス) への参照リンクは、archive 先のパスに張り替えられる or 該当 memo セクションへの参照に置換される。link 切れは 0
- INV-008: 設計議論の再開 (新 spec の追加、既存 spec の修正) は本タスク内では行わない。発見した改善点は別 issue / TODO として記録するに留める
- INV-009: Phase 単位での commit 分割が行われる (1 巨大 commit を避ける)。各 Phase は完結した review unit として扱う
- INV-010: vocabulary 固定原則 (memo §3-1) に基づき、canonical form と不採用 form の対が明示される

## Enforced in (optional)

- INV-001 / INV-002: QA test-plan の test matrix に Phase A/B 確定事項のチェックリスト化、cross-reference check で照合
- INV-003: diff review で撤回 marker の存在を確認、対応する notes.md セクションとの照合
- INV-004: memo の見出し階層を diff で確認、§3-19 以降の番号付け一貫性を目視
- INV-005 / INV-006: `git log --follow` で archive 履歴確認、archive 先 notes.md 冒頭の archive マーク存在確認
- INV-007: `grep -r "discord-bot-handwrite/notes.md"` で残存参照を検出、link integrity check で 0 件確認
- INV-008: PR review で「Phase A/B で確定していない新 spec が混入していないか」を確認
- INV-009: git log で commit 粒度を確認 (Phase ごとに分割されているか)
- INV-010: diff review で canonical / 不採用 form の対の明示を確認

## Rollback / Follow-ups

- **Rollback**:
  - memo 改訂のロールバック: `git revert` で改訂前 memo に復帰
  - notes.md archive のロールバック: `git mv` の逆方向 (`_docs/archives/draft/...` → `_docs/draft/...`) で復元、または `git revert`
  - 部分ロールバック: Phase 単位で commit を分割しているので、特定 Phase のみ revert 可能
- **Follow-ups**:
  - memo に目次 (TOC) を追加する別タスクの検討 (改訂後の memo 規模を見て判断)
  - 未決着論点ごとの個別タスク起票 (catch / recover 構文、checked vs unchecked、辞書 literal、コメント構文、etc.)
  - parser 実装着手タスクの起票 (Phase C 相当)
  - 標準ライブラリ設計タスクの起票 (built-in 型の property、終了型、predicate function 等)
  - Tooling-Feat-14 (grammar v3) の plan / intent / qa を本 memo 更新を入力に着手
