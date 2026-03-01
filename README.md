# $simplify — Code Simplifier Skill for OpenAI Codex

A lean skill that gives Codex a **structured refactoring process** — not a knowledge dump, but guardrails that keep a smart model honest.

## Philosophy

Modern LLMs already know what cyclomatic complexity is, how to extract guard clauses, and what constitutes a code smell. Teaching them refactoring theory is like teaching a fish to swim. What they *don't* have is:

- A **structured process** (7 phases from scope detection to impact report)
- **Guardrails** that prevent rationalized bad changes (anti-rationalization checklist)
- **Decision gates** that know when to auto-apply vs. ask the user
- **Parallelism awareness** (when to spawn agents vs. go sequential)

This skill provides process, not knowledge. **145 lines, 2 files.**

## Quick start

```bash
# Clone into your Codex skills directory
git clone https://github.com/tavaresgmg/codex-simplify-skill.git ~/.codex/skills/simplify
```

Enable skills in `~/.codex/config.toml`:

```toml
[features]
skills = true
multi_agent = true  # optional, enables parallel analysis
```

### Use

```
$simplify                          # Recent changes (git diff)
$simplify src/auth/                # Specific directory
$simplify src/utils/format.ts      # Specific file
```

Natural language also works:

```
Simplify the entire repository
Audit src/api/ — find problems but don't fix anything
```

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Refactor** (default) | `$simplify`, "simplify", "refactor", "clean up" | Find problems AND fix them |
| **Audit** | "find problems", "audit", "scan", "what's wrong with" | Report only — zero edits |

## 7-Phase Process

1. **Scope** — detect target files (user-specified, directory, repo, or git diff)
2. **Context** — batch-read project standards, target files, and dependencies
3. **Analysis** — structural complexity, code smells, convention consistency
4. **Plan** — confidence scoring (0-100) with decision gates
5. **Refactoring** — atomic edits in priority order with stop-loss on failures
6. **Verification** — mandatory lint + typecheck + tests gate
7. **Report** — structured summary with metrics and flagged future items

## The 5 Iron Laws

1. **FUNCTIONALITY IS SACRED** — Zero behavior changes
2. **CLARITY OVER BREVITY** — Explicit beats clever
3. **CONSISTENCY OVER PERFECTION** — Follow project patterns, migrate all or none
4. **ATOMIC CHANGES** — One concern per edit
5. **EVIDENCE OVER OPINION** — Every change needs concrete justification

## Skill structure

```
simplify/
├── SKILL.md              # Process + guardrails (145 lines)
└── agents/
    └── openai.yaml       # UI metadata for Codex app (7 lines)
```

## Requirements

- [OpenAI Codex CLI](https://github.com/openai/codex) with `skills = true`
- Git (for scope detection)
- Optional: `multi_agent = true` for parallel analysis

## License

MIT
