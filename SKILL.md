---
name: simplify
description: >
  Critical code refactoring engine that surgically improves code clarity, consistency, and
  maintainability while preserving exact functionality. Use when: (1) code was just written or
  modified and needs refinement, (2) user asks to simplify, refactor, clean up, or improve code
  quality, (3) user wants to audit or find problems in code without necessarily fixing them,
  (4) user wants to review a specific module, directory, file, or the entire repository,
  (5) code smells like deep nesting, long functions, DRY violations, or naming issues are noticed.
  Triggers on: "simplify", "refactor", "clean up", "improve readability", "code quality",
  "find problems", "audit code", "review module", "scan repo".
  Do NOT use for: adding features, writing tests, formatting (use a formatter), or architecture changes.
---

# Code Simplifier

Senior refactoring engineer. Not a formatter, not a linter — an architect who sees structural
flaws invisible to the original author and surgically corrects them without breaking anything.

Goal: make code **obvious** — where the next developer reads it and thinks "of course."

---

## Iron Laws (inviolable)

1. **FUNCTIONALITY IS SACRED** — Zero behavior changes. Tests that passed before must pass after.
2. **CLARITY OVER BREVITY** — Explicit code beats clever one-liners. A 5-line `if/else` beats a nested ternary.
3. **CONSISTENCY OVER PERFECTION** — Follow the project's established patterns. Migrate ALL or NONE.
4. **ATOMIC CHANGES** — One refactoring concern per edit. Each change independently reviewable.
5. **EVIDENCE OVER OPINION** — "It's cleaner" is NOT valid. "Reduces nesting from 5→2 via guard clauses" IS.

Before ANY change, check `references/rationalization-defense.md`.

---

## Execution Strategy: Parallelism & Agents

**Always maximize parallelism.** Use `multi_tool_use.parallel` for every batch operation.

**When multi-agent is available** (check: feature `multi_agent` enabled):

- **Small scope** (1-5 files): Single-agent mode. Do all analysis sequentially.
- **Medium scope** (6-20 files): Spawn **3 explorer agents in parallel** for Phase 3 analysis (one per pass). Collect results, then apply changes as single agent.
- **Large scope** (20+ files): Spawn **explorer agents per module/directory** for Phase 3, then spawn **worker agents per independent module** for Phase 5 refactoring. Collect and consolidate.

**Agent roles to use:**
- `explorer` (read-only) — for analysis passes (Phase 2 and 3). Safe, cannot modify files.
- `worker` — for refactoring (Phase 5) on independent modules that don't share mutable state.
- Main agent — for orchestration, decision gates, verification, and reporting.

**When multi-agent is NOT available:** Fall back to sequential execution with parallel tool calls. Batch all file reads together, batch all searches together.

---

## Process

### Phase 1: Scope & Mode Detection

Determine **what** to analyze and **how**:

**Mode detection** (from user intent):
- **Refactor mode** (default) — find problems AND fix them
- **Audit mode** — find and report problems WITHOUT editing. Activate when user says "find problems", "audit", "scan", "review without fixing", or "what's wrong with"

**Scope detection:**
1. If user specified files → use that exact scope
2. If user specified a directory or module → recursively include all source files in it
3. If user said "entire repo", "whole project", or "everything" → run `scripts/detect_scope.py --repo` to list all tracked source files, warn about context cost, process in batches
4. If no arguments → run `scripts/detect_scope.py` to detect recent git changes
5. If no git changes found → ask user what to review

For large scopes (> 20 files), sort by size descending, process in batches, report incrementally.

**STOP** if no files found.

### Phase 2: Context Loading

**Batch all reads in parallel using `multi_tool_use.parallel`.**

1. Read project standards — AGENTS.md, CLAUDE.md, .editorconfig, linter configs, tsconfig (all in one parallel batch)
2. Read ALL target files completely — batch together, not one-by-one
3. Read adjacent files — imports, importers, shared types (second parallel batch if needed)
4. Identify project conventions from the code read above

**For large scopes:** Spawn an `explorer` agent to map project conventions while main agent reads target files. The explorer should return: naming patterns, import style, error handling pattern, function declaration style, and 3-5 representative code examples.

### Phase 3: Multi-Dimensional Analysis

Three analysis passes. See `references/analysis-dimensions.md` for detailed criteria.

**For medium/large scopes — spawn 3 parallel explorer agents:**

- **Explorer 1 — Structural Complexity:** Functions > 30 lines, nesting > 3 levels, cyclomatic complexity > 10, parameter lists > 4, mixed concerns. Return findings as `[file:line] — issue — severity (0-100)`.

- **Explorer 2 — Code Smells & Anti-Patterns:** DRY violations (3+ identical blocks), dead code, magic values, feature envy, boolean params, temporal coupling. Return findings same format.

- **Explorer 3 — Convention & Consistency:** Project standard deviations, naming inconsistencies, import ordering, type annotation gaps, stale/obvious comments. Return findings same format.

Each explorer must read `references/analysis-dimensions.md` (its relevant section) and return a structured list of findings with confidence scores.

**For small scopes:** Run all three passes sequentially as single agent.

Wait for all agents to complete. Collect and deduplicate findings.

### Phase 4: Prioritized Plan

Consolidate all findings. Score each (0-100 confidence):

| Score | Action |
|---|---|
| 0-25 | Skip. Subjective preference. |
| 26-50 | Apply only if zero-risk and obvious. |
| 51-75 | Apply. Clear improvement with concrete benefit. |
| 76-100 | Must fix. Complexity bomb, bug risk, or convention violation. |

Present grouped by priority: Critical (76-100) → Improvement (51-75) → Minor (26-50).
Each item: `[file:line] — description — justification — confidence: N`

**If AUDIT MODE:** Present the full report and STOP. The report IS the deliverable.

**If REFACTOR MODE — Decision gate:**
- **Small** (< 10 edits, all low-risk) → proceed autonomously
- **Significant** (> 10 edits OR structural changes) → present summary, ask user
- **Public API changes** → ALWAYS ask user first

### Phase 5: Surgical Refactoring

**For large scopes with independent modules:** Spawn `worker` agents in parallel, one per module. Each worker gets its module's findings and applies changes atomically. Workers must not cross module boundaries — flag cross-module changes for main agent.

**Module independence criteria** — two modules are safe to refactor in parallel when:
- They don't import from each other (no circular dependency)
- No finding requires changes in BOTH modules simultaneously
- They don't share mutable state (global variables, singletons)

If unsure, refactor sequentially. Safety > speed.

**For small/medium scopes or cross-cutting changes:** Apply as single agent.

Rules for ALL refactoring (worker or main):
1. Work in priority order (Critical → Improvement → Minor)
2. Re-read current file state before each edit
3. Group related changes in same file
4. Never edit a file not read in this session
5. Read `references/refactoring-catalog.md` for techniques and safety levels

**Stop-Loss:** If the same edit fails verification **twice**, STOP trying that change. Log it in the report as "attempted, reverted — reason: [error]" and move to the next finding. Do not brute-force.

### Phase 6: Verification Gate

**MANDATORY. No exceptions. No "it's obviously fine."**

> No completion claim without fresh verification evidence.

**First, discover available commands** by checking: `package.json` scripts, `Makefile`, `pyproject.toml`, `Cargo.toml`, `composer.json`, or project docs (AGENTS.md often lists them). Use the first match found.

**Then run in parallel using `multi_tool_use.parallel`:**
1. Lint command (e.g., `npm run lint`, `ruff check .`, `cargo clippy`)
2. Typecheck command (e.g., `tsc --noEmit`, `mypy .`, `cargo check`)
3. Test suite covering modified code (e.g., `npm test`, `pytest`, `cargo test`)

Read FULL output of all three. Zero new errors.

If verification fails: **REVERT** the failing change (don't fix tests), report what happened, move on.

If no automated checks available: re-read every modified file, manually verify no behavior change, state risk level explicitly.

### Phase 7: Impact Report

```
## Simplification Report

### Execution
- Mode: refactor | audit
- Scope: N files (recent changes | directory: X | entire repo)
- Agents used: N explorers + N workers (or single-agent)

### Changes Applied (N total)
- [file:line] — What changed — Why (confidence: N)

### Verification
- Lint: PASS/FAIL
- TypeCheck: PASS/FAIL
- Tests: PASS/FAIL (N passed, M total)

### Metrics
- Lines: +N / -M (net: ±K)
- Files touched: N

### Flagged for Future (out of scope)
- [file:line] — What could improve — Why not now
```

---

## Boundaries

**This skill does NOT:**
- Add features or new functionality
- Write or modify tests (separate concern)
- Change architecture (flag it, don't fix it)
- Format code (use the project's formatter)
- Upgrade dependencies (flag outdated ones)
- Touch code outside scope (unless updating a broken reference from a rename)

---

## Adaptation

Before applying any pattern:
1. Check project docs (AGENTS.md, CLAUDE.md, etc.) — they define the law
2. Check surrounding code — follow what the team does, not textbook rules
3. Check language idioms — Rust ≠ TypeScript ≠ Python
4. Check framework conventions — React, Next.js, Django have their own patterns

Project docs contradict codebase → follow project docs (intended standard).
No project docs → follow dominant pattern in existing code.
