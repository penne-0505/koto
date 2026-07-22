---
title: Docs-driven template v1.0.0 migration inventory
status: active
draft_status: n/a
created_at: 2026-07-22
updated_at: 2026-07-22
references:
  - "_docs/plan/Workflow/docs-template-v1-migration/plan.md"
  - "_docs/intent/Workflow/docs-template-v1-migration/decision.md"
  - "_docs/qa/Workflow/docs-template-v1-migration/test-plan.md"
related_issues: []
related_prs: []
---

# Docs-driven template v1.0.0 migration inventory

## Provenance and cutoff

- Source: `https://github.com/penne-0505/docs_driven_dev_template.git`
- B: `e6dc4331a81af21494208610b22ef2d9ecdce885` (legacy, untagged).
- U: tag `v1.0.0`, commit `f71e9ab20466ea2972158334261f5ae2b2265754`.
- P: `6ad65726c93d729a5a84d29da6e67064c1594214`.
- Cutoff: `2026-07-22T12:29:14+09:00`; staged, unstaged, and untracked manifests were empty.
- Destination: branch `codex/docs-template-v1.0.0-koto` in `/tmp/docs-template-v1-rollout/koto`.
- Ownership: this worktree/repository only; active Koto checkout, main, other repositories, and remote refs are out of scope.
- Included upstream lane: exact `B..U` only.
- Excluded upstream heads: `agent/why-first-intent-scope@511f44e178fc923423d303efb6186091083a2b78` and `codex/metacognitive-audit-hooks@34ac6a40f86a8900c9c3bccca7411d56d56b39af`; `main` and `origin/main` resolve to U but are not provenance inputs.

## Classification rules

- Upstream delta: unchanged, added, modified, or removed from B to U.
- Project relation: `upstream-owned-unmodified`, `customized-shared`, or `project-only`, comparing B with P.
- Resolution: exactly one of apply, merge, keep, remove, or defer.
- `defer` below means deliberately excluded template-self history, not unresolved migration work.
- Schema/workflow flags identify paths whose contract or validation surface is affected; project-only legacy docs remain compatible until a semantic edit warrants schema v2.

## B/U/P union inventory

| Path | Upstream delta | Project relation | Flag | Resolution | Rationale |
| --- | --- | --- | --- | --- | --- |
| .agents/skills/docs-cleanup/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/docs-inventory/SKILL.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/docs-prep/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/docs-template-migration/SKILL.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/frontend-design/SKILL.md | removed | customized-shared | schema/workflow | remove | already absent at P and U |
| .agents/skills/implementation-prep/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/post-implementation/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/qa-prep/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/qa-review/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .agents/skills/test-maintenance/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/settings.json | added | upstream-owned-unmodified | - | apply | apply reusable U path |
| .claude/skills/docs-cleanup/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/docs-inventory/SKILL.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/docs-prep/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/docs-template-migration/SKILL.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/frontend-design/SKILL.md | removed | customized-shared | schema/workflow | remove | already absent at P and U |
| .claude/skills/implementation-prep/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/post-implementation/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/qa-prep/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/qa-review/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .claude/skills/test-maintenance/SKILL.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| .codex/hooks.json | added | upstream-owned-unmodified | - | apply | apply reusable U path |
| .github/workflows/docs-ci.yml | modified | upstream-owned-unmodified | schema/workflow | merge | apply U workflow and set downstream P plus ACMR scope |
| AGENTS.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| QUICKSTART.md | modified | upstream-owned-unmodified | - | apply | apply reusable U path |
| README.md | modified | upstream-owned-unmodified | - | apply | apply reusable U path |
| TODO.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _docs/archives/draft/Lang/discord-bot-handwrite/handler.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/archives/draft/Lang/discord-bot-handwrite/notes.md | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/archives/draft/Lang/discord-bot-handwrite/sample-1.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/archives/draft/Lang/discord-bot-handwrite/sample-2.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/documentation_guide.md | modified | upstream-owned-unmodified | - | apply | apply reusable U path |
| _docs/draft/Lang/discord-bot-reminder/example.py | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/draft/Lang/discord-bot-reminder/notes.md | unchanged | project-only | lint compatibility | keep | preserve canonical tab sample with exact-file MD010 directive |
| _docs/draft/Lang/discord-bot-reminder/reminder.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/draft/Lang/parser/parser.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/intent/Lang/design-memo-update/decision.md | unchanged | project-only | lint compatibility | keep | code-span whitespace only; semantic text preserved |
| _docs/intent/Template/intent-qa-finalization/decision.md | removed | customized-shared | template-self | remove | template-only history; U removed or replaced it |
| _docs/intent/Tooling/vscode-koto-grammar-v2/decision.md | unchanged | project-only | lint compatibility | keep | code-span whitespace only; semantic text preserved |
| _docs/intent/Tooling/vscode-koto-grammar-v3/decision.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/intent/Tooling/vscode-koto-grammar/decision.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/intent/Workflow/code-intent-traceability/decision.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/intent/Workflow/incremental-adoption-scope/decision.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/intent/Workflow/intentional-omission-risk/decision.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/intent/Workflow/lifecycle-self-audit/decision.md | added | upstream-owned-unmodified | template-self | defer | upstream self-audit history excluded from downstream guidance |
| _docs/plan/Lang/design-memo-update/plan.md | unchanged | project-only | lint compatibility | keep | preserve global task IDs with exact-file MD029 directive |
| _docs/plan/Template/intent-qa-finalization/plan.md | removed | customized-shared | template-self | remove | template-only history; U removed or replaced it |
| _docs/plan/Tooling/vscode-koto-grammar-v2/plan.md | unchanged | project-only | lint compatibility | keep | code-span whitespace only; semantic text preserved |
| _docs/plan/Tooling/vscode-koto-grammar-v3/plan.md | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/plan/Tooling/vscode-koto-grammar/plan.md | unchanged | project-only | - | keep | project-only content preserved from P |
| _docs/plan/Workflow/code-intent-traceability/plan.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/plan/Workflow/incremental-adoption-scope/plan.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/plan/Workflow/lifecycle-self-audit/plan.md | added | upstream-owned-unmodified | template-self | defer | upstream self-audit history excluded from downstream guidance |
| _docs/qa/Lang/design-memo-update/test-plan.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/qa/Lang/design-memo-update/verification.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/qa/Template/intent-qa-finalization/test-plan.md | removed | customized-shared | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Template/intent-qa-finalization/verification.md | removed | customized-shared | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Tooling/vscode-koto-grammar-v2/test-plan.md | unchanged | project-only | lint compatibility | keep | code-span whitespace only; semantic text preserved |
| _docs/qa/Tooling/vscode-koto-grammar-v2/verification.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/qa/Tooling/vscode-koto-grammar-v3/test-plan.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/qa/Tooling/vscode-koto-grammar-v3/verification.md | unchanged | project-only | lint compatibility | keep | escape regex table pipes; semantic text preserved |
| _docs/qa/Tooling/vscode-koto-grammar/test-plan.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/qa/Tooling/vscode-koto-grammar/verification.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/qa/Workflow/code-intent-traceability/test-plan.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Workflow/code-intent-traceability/verification.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Workflow/incremental-adoption-scope/test-plan.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Workflow/incremental-adoption-scope/verification.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Workflow/intentional-omission-risk/test-plan.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Workflow/intentional-omission-risk/verification.md | removed | upstream-owned-unmodified | template-self | remove | template-only history; U removed or replaced it |
| _docs/qa/Workflow/lifecycle-self-audit/test-plan.md | added | upstream-owned-unmodified | template-self | defer | upstream self-audit history excluded from downstream guidance |
| _docs/qa/Workflow/lifecycle-self-audit/verification.md | added | upstream-owned-unmodified | template-self | defer | upstream self-audit history excluded from downstream guidance |
| _docs/standards/documentation_guidelines.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _docs/standards/documentation_operations.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _docs/standards/japanese-lang-design-memo.md | unchanged | project-only | lint compatibility | keep | fence/type/table Markdown syntax only; language-design semantics preserved |
| _docs/standards/japanese-lang-why-not.md | unchanged | project-only | schema/workflow | keep | project-only content preserved from P |
| _docs/standards/jj_workflow.md | removed | customized-shared | schema/workflow | remove | already absent at P and U |
| _docs/standards/quality_assurance.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _docs/standards/templates/intent.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _docs/standards/templates/plan.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _docs/standards/templates/qa-test-plan.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _docs/standards/templates/qa-verification.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/README.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/archive-flow.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/breaking-change.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/experimental-baseline.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/historical-prompt-not-operational.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/intentional-omission-risk.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/medium-feature.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/misleading-optimization.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/qa-prep-from-intent.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/rationale-preserving-change.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/refactor-behavior-preservation.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/small-bug.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/stale-draft-cleanup.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/cases/template-version-migration.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/agent-workflows/expected-invariants.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/validator-fixtures/README.md | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/validator-fixtures/intent/invalid/missing-why.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/validator-fixtures/intent/invalid/orphan-invariant.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/validator-fixtures/intent/valid/decision.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/validator-fixtures/links/valid-reference-anchor.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/validator-fixtures/qa/invalid/missing-invariant.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _evals/validator-fixtures/qa/invalid/qa-archive-path.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _evals/validator-fixtures/qa/invalid/status-verdict-mismatch.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _evals/validator-fixtures/qa/invalid/v2-missing-decision-scope.md | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| _evals/validator-fixtures/qa/invalid/verification-in-progress-status.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _evals/validator-fixtures/qa/invalid/verification-missing-test-plan-reference.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _evals/validator-fixtures/qa/valid/test-plan.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| _evals/validator-fixtures/qa/valid/verification-pass.md | modified | customized-shared | schema/workflow | merge | preserve P customization and apply U contract |
| docs-template.lock.example.json | added | upstream-owned-unmodified | - | apply | apply reusable U path |
| scripts/agent-workflow-hook.mjs | added | upstream-owned-unmodified | schema/workflow | merge | apply U hook and retarget intent anchors to retained downstream decision |
| scripts/check-docs.sh | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| scripts/scope.mjs | modified | upstream-owned-unmodified | - | apply | apply reusable U path |
| scripts/test-agent-workflow-hook.mjs | added | upstream-owned-unmodified | schema/workflow | merge | apply U tests with equivalent hook-safe source spelling |
| scripts/test-agent-workflow-smoke.mjs | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| scripts/test-validators.mjs | modified | upstream-owned-unmodified | schema/workflow | merge | apply U fixtures and add schema-marker versus unknown-warning pilot coverage |
| scripts/validate-doc-links.mjs | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| scripts/validate-frontmatter.mjs | modified | upstream-owned-unmodified | schema/workflow | merge | apply U validator and recognize correct intent_schema and qa_schema markers |
| scripts/validate-intent.mjs | added | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| scripts/validate-qa.mjs | modified | upstream-owned-unmodified | schema/workflow | apply | apply reusable U path |
| tools/vscode-koto/README.md | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/language-configuration.json | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/package.json | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/syntaxes/koto.tmLanguage.json | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/tests/fixtures/entity-names.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/tests/fixtures/half-width-boundary.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/tests/fixtures/incomplete-pickup.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/tests/fixtures/max-value.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/tests/fixtures/phase-b.koto | unchanged | project-only | - | keep | project-only content preserved from P |
| tools/vscode-koto/tests/fixtures/task-table.koto | unchanged | project-only | - | keep | project-only content preserved from P |

## Deletion evidence

The following migration-time removals all had exact B=P blobs, no project guidance references after the U standards merge, and were absent at U:

| Path | B=P blob |
| --- | --- |
| `_docs/intent/Workflow/code-intent-traceability/decision.md` | `86489d64ee61257656004537bd096a9ce754d924` |
| `_docs/plan/Workflow/code-intent-traceability/plan.md` | `f3d814a69c816b9ee8d9ae1ab3066f4ceeaadcf2` |
| `_docs/qa/Workflow/code-intent-traceability/test-plan.md` | `0806437ed79a40dedb6e5089138d515b811f3cd5` |
| `_docs/qa/Workflow/code-intent-traceability/verification.md` | `36e26ba976da8e5be49e38a6037e9bb375e3ee37` |
| `_docs/intent/Workflow/incremental-adoption-scope/decision.md` | `0de90f547a83d810703e1bea286fd51fe08eda21` |
| `_docs/plan/Workflow/incremental-adoption-scope/plan.md` | `1c3f881c00ec43c1d24a27cb3b0b41c31b745f91` |
| `_docs/qa/Workflow/incremental-adoption-scope/test-plan.md` | `42c8c3370e3fb278aedceeefb312f79ec37d670d` |
| `_docs/qa/Workflow/incremental-adoption-scope/verification.md` | `039fae41a74840b599aa5f390f8d230fed49eba9` |
| `_docs/intent/Workflow/intentional-omission-risk/decision.md` | `cee0e73b7a3f8499e05f0ae3969213bc9330a477` |
| `_docs/qa/Workflow/intentional-omission-risk/test-plan.md` | `42c8e60ade0d6ac416d663cfd7f76203bd575776` |
| `_docs/qa/Workflow/intentional-omission-risk/verification.md` | `73456c3bbd2b84b1c1cea215a07ed99126371004` |

Template finalization records, frontend-design skill, and jj workflow were already absent at P and remain absent. U's four lifecycle-self-audit records are excluded by resolution `defer`.

## Migration-created artifact ledger

The B/U/P union above covers 130 paths. The following six migration-created artifacts and the eight project-local compatibility records below complete final-diff coverage; a read-only closure check compares their union with the final P diff and requires zero unclassified paths.

| Path | Purpose | Final state |
| --- | --- | --- |
| `_docs/plan/Workflow/docs-template-v1-migration/plan.md` | migration contract | tracked |
| `_docs/intent/Workflow/docs-template-v1-migration/decision.md` | durable rationale | tracked |
| `_docs/qa/Workflow/docs-template-v1-migration/test-plan.md` | QA contract | tracked |
| `_docs/reference/Workflow/docs-template-v1-migration/reference.md` | union inventory and ledger | tracked |
| `_docs/qa/Workflow/docs-template-v1-migration/verification.md` | closure evidence | tracked |
| `docs-template.lock.json` | U provenance | final migration write after compatibility PASS |

## Project-local Markdownlint compatibility ledger

These eight paths were unchanged in the B/U/P tree but must be presentation-adjusted because the v1 CI lints the full non-archive Markdown scope. The support horizon is the lifetime of the named Koto tab/global-ID representations or the relevant Markdown rule; the directives are exact-file and no directory/config exclusion was added.

| Path | Findings before | Remedy | Semantic preservation |
| --- | --- | --- | --- |
| `_docs/draft/Lang/discord-bot-reminder/notes.md` | MD010 ×3 | local MD010 directive around the canonical tab sample | Koto tabs unchanged |
| `_docs/plan/Lang/design-memo-update/plan.md` | MD029 ×33 | exact-file MD029 directive | global task order and IDs unchanged |
| `_docs/standards/japanese-lang-design-memo.md` | MD040 ×43, MD033 ×5, MD056 ×2 | fence languages, code-wrapped placeholders, complete table cells | language-design semantics unchanged |
| `_docs/intent/Lang/design-memo-update/decision.md` | MD038 ×1 | code-span boundary correction | decision text unchanged |
| `_docs/intent/Tooling/vscode-koto-grammar-v2/decision.md` | MD038 ×1 | code-span boundary correction | regex anchor text unchanged |
| `_docs/plan/Tooling/vscode-koto-grammar-v2/plan.md` | MD038 ×1 | code-span boundary correction | Koto spacing representation unchanged |
| `_docs/qa/Tooling/vscode-koto-grammar-v2/test-plan.md` | MD038 ×1 | code-span boundary correction | QA expectation unchanged |
| `_docs/qa/Tooling/vscode-koto-grammar-v3/verification.md` | MD056 ×2 | escaped regex table pipes | verification evidence unchanged |

`TODO.md` held a temporary migration task during execution. After PASS it is removed and `Next ID No` returns to the checkpoint value; only the three pathwise schema-v2 workflow rule merges remain in its final diff.
