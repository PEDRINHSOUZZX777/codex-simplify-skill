# Rationalization Defense Table

Reference for checking whether a proposed change is justified or rationalized.
Consult this table BEFORE applying any change.

---

## The Table

| Rationalization | Reality Check | Correct Action |
|---|---|---|
| "It's cleaner this way" | Cleaner by what metric? Can you name it? If not, it's a preference, not an improvement. | Only apply if you can cite a specific metric (nesting depth, line count, complexity score). |
| "Nobody uses this code" | Did you search ALL references? Including tests, configs, dynamic imports, string-based lookups? | Run project-wide search. Only remove if truly zero references. |
| "This abstraction is better" | Does it have 3+ concrete usages? If just 1-2, it's premature abstraction that adds indirection. | Apply the rule of three. Two similar → tolerate. Three identical → extract. |
| "The new pattern is superior" | Are you migrating ALL instances in the project? A codebase with two patterns is worse than one with a single imperfect pattern. | Migrate all or none. If scope is too large, flag for future — don't create inconsistency. |
| "It's obvious what this does" | Obvious to YOU, right now, with full context loaded. Will it be obvious to a tired developer at 2am six months from now? | Keep the name descriptive. When in doubt, be explicit. |
| "This is just a small improvement" | Small improvements compound into Frankenstein code when each is locally reasonable but globally incoherent. | Only apply if it serves the stated refactoring goal. |
| "I'll simplify the whole thing" | Scope creep is the #1 killer of refactoring tasks. You were asked to improve X, not rewrite Y. | Stay in scope. Flag other improvements for future. |
| "The tests will catch it" | Tests verify KNOWN behaviors. Refactoring can break IMPLICIT contracts that no test covers — side effects, timing, ordering, exception types. | Verify explicitly. Don't trust test coverage as a safety net for refactoring. |
| "This variable name is fine" | Generic names (`data`, `result`, `temp`, `info`) force every reader to re-derive meaning from context. | Rename if the current name doesn't reveal intent to a reader without context. |
| "It's just formatting" | Formatting is the formatter's job. Manual formatting changes create noise in diffs and conflict with auto-formatters. | Don't change formatting. If the project has a formatter, run it. If not, leave it. |

---

## Red Flags — Stop and Reconsider

You are going off track if:

- [ ] You're adding NEW abstractions, utilities, or helper functions not justified by 3+ duplicates
- [ ] You're changing function signatures or public APIs without checking all consumers
- [ ] You're "improving" code that wasn't in the declared scope
- [ ] Your diff is becoming larger than the original code change that triggered the review
- [ ] You feel the urge to "while I'm here, let me also..." — this is scope creep
- [ ] You're introducing patterns not present elsewhere in the codebase
- [ ] You're removing code without verifying zero references
- [ ] You're making the code shorter but less readable
- [ ] You're replacing a simple solution with a "clever" one
- [ ] You're optimizing performance without measuring a bottleneck

If any checkbox above is true: **STOP. Re-read the Iron Laws. Stay in scope.**

---

## The Verification Question

Before committing any change, ask:

> "If I showed this diff to a senior engineer unfamiliar with the task, would they immediately understand WHY each change was made?"

If the answer is no, the change either needs a better justification or shouldn't be made.
