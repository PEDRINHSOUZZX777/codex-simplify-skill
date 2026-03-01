# $simplify — Code Simplifier Skill for OpenAI Codex

A production-grade skill that transforms Codex into a **senior refactoring engineer** — not a formatter, not a linter, but an architect who sees structural flaws invisible to the original author and surgically corrects them without breaking anything.

## What makes this different

| Feature            | Typical "refactor" skills | This skill                                                          |
| ------------------ | ------------------------- | ------------------------------------------------------------------- |
| **Process**        | "Simplify this code"      | 7-phase structured workflow with mandatory gates                    |
| **Analysis**       | Single vague pass         | 3 parallel analysis dimensions with measurable thresholds           |
| **Safety**         | Hope for the best         | 5 Iron Laws + 10-item rationalization defense table                 |
| **Prioritization** | Apply everything blindly  | Confidence scoring (0-100) with decision gates                      |
| **Verification**   | None                      | Mandatory lint + typecheck + test gate before completion            |
| **Parallelism**    | Sequential only           | Adaptive scaling with multi-agent support (explorer + worker roles) |
| **Scope**          | Recent changes only       | Files, directories, modules, or entire repo — with audit-only mode  |
| **Reporting**      | None                      | Structured impact report with metrics and flagged future items      |

## Quick start

### Install

```bash
# Clone directly into your Codex skills directory
git clone https://github.com/tavaresgmg/codex-simplify-skill.git ~/.codex/skills/simplify
```

Or with the built-in installer inside Codex:

```
$skill-installer install simplify from github.com/tavaresgmg/codex-simplify-skill
```

### Enable skills (if not already)

Add to `~/.codex/config.toml`:

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
Review and simplify src/modules/, use parallel agents
```

## Modes

| Mode                   | Trigger                                               | Behavior                   |
| ---------------------- | ----------------------------------------------------- | -------------------------- |
| **Refactor** (default) | `$simplify`, "simplify", "refactor", "clean up"       | Find problems AND fix them |
| **Audit**              | "find problems", "audit", "scan", "what's wrong with" | Report only — zero edits   |

## How it works

### 7-Phase Process

```
Phase 1: Scope & Mode Detection
    ↓ What files? What mode?
Phase 2: Context Loading
    ↓ Read project standards + target code + dependencies (parallel batch)
Phase 3: Multi-Dimensional Analysis
    ↓ 3 parallel passes: structural complexity, code smells, conventions
Phase 4: Prioritized Plan
    ↓ Confidence scoring, decision gate (auto for small, ask for large)
Phase 5: Surgical Refactoring
    ↓ Atomic edits, priority order, stop-loss on failures
Phase 6: Verification Gate
    ↓ lint + typecheck + tests in parallel — MANDATORY
Phase 7: Impact Report
    → Structured summary with metrics
```

### Adaptive Parallelism

The skill scales execution strategy based on scope:

| Scope          | Strategy                                                                       |
| -------------- | ------------------------------------------------------------------------------ |
| **1-5 files**  | Single agent, sequential                                                       |
| **6-20 files** | 3 `explorer` agents in parallel for analysis → single agent refactors          |
| **20+ files**  | Explorers per module for analysis → `worker` agents per module for refactoring |

Requires `multi_agent = true` in config. Falls back to sequential with parallel tool calls when unavailable.

### The 5 Iron Laws

1. **FUNCTIONALITY IS SACRED** — Zero behavior changes
2. **CLARITY OVER BREVITY** — Explicit code beats clever one-liners
3. **CONSISTENCY OVER PERFECTION** — Follow project patterns, migrate all or none
4. **ATOMIC CHANGES** — One concern per edit
5. **EVIDENCE OVER OPINION** — Every change needs concrete justification

### Rationalization Defense

Built-in protection against 10 common rationalizations that lead to bad refactoring decisions. The skill checks each proposed change against a defense table before applying it.

## Skill structure

```
simplify/
├── SKILL.md                              # Core workflow (216 lines)
├── agents/
│   └── openai.yaml                       # UI metadata for Codex app
├── references/
│   ├── analysis-dimensions.md            # Detailed criteria for each analysis pass
│   ├── refactoring-catalog.md            # 15+ techniques with diff examples by risk level
│   └── rationalization-defense.md        # Anti-rationalization table + red flags checklist
└── scripts/
    └── detect_scope.py                   # Git-based scope detection with filtering
```

Following Codex's **progressive disclosure** pattern: SKILL.md stays lean (216 lines, well under the 500-line limit), while detailed reference material loads only when needed.

## Analysis dimensions

### Pass 1 — Structural Complexity

Functions > 30 lines, nesting > 3 levels, cyclomatic complexity > 10, parameter lists > 4, mixed concerns

### Pass 2 — Code Smells & Anti-Patterns

DRY violations (3+ identical blocks), dead code, magic values, feature envy, boolean params, temporal coupling

### Pass 3 — Convention & Consistency

Project standard deviations, naming inconsistencies, import ordering, type annotation gaps, stale comments

## Refactoring catalog

15+ techniques organized by risk level, each with concrete `diff` examples:

| Risk         | Examples                                                                              |
| ------------ | ------------------------------------------------------------------------------------- |
| **Very Low** | Remove dead imports, remove dead variables, remove commented-out code                 |
| **Low**      | Extract constants, guard clauses, simplify booleans, replace nested ternaries         |
| **Medium**   | Extract helper functions (rule of 3), inline single-use abstractions, options objects |
| **High**     | Change function signatures, move code between files, rename exports                   |

## Confidence scoring

Every finding gets a score (0-100):

| Score  | Action                                             |
| ------ | -------------------------------------------------- |
| 0-25   | Skip — subjective preference                       |
| 26-50  | Apply only if zero-risk                            |
| 51-75  | Apply — clear improvement                          |
| 76-100 | Must fix — complexity bomb or convention violation |

## Requirements

- [OpenAI Codex CLI](https://github.com/openai/codex) with `skills = true`
- Git (for scope detection)
- Python 3.10+ (for `detect_scope.py`)
- Optional: `multi_agent = true` for parallel analysis

## Language support

The skill is **language-agnostic** — it adapts to the project's language, framework, and conventions. Examples in references use JavaScript/TypeScript, but the analysis criteria and refactoring techniques apply to any language.

## Contributing

1. Use the skill on a real project
2. Notice where it struggles or makes bad decisions
3. Open an issue describing the scenario
4. PRs welcome — especially for new refactoring techniques in the catalog

## License

MIT
