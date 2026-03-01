# Analysis Dimensions — Detailed Criteria

Reference material for Phase 3 of the simplify skill. Load only the relevant section based on the current analysis pass.

## Table of Contents

1. [Pass 1: Structural Complexity](#pass-1-structural-complexity)
2. [Pass 2: Code Smells & Anti-Patterns](#pass-2-code-smells--anti-patterns)
3. [Pass 3: Convention & Consistency](#pass-3-convention--consistency)

---

## Pass 1: Structural Complexity

### Function Length (threshold: 30 lines)

Functions exceeding 30 lines are candidates for extraction. Look for:
- Logical sections separated by blank lines or comments (natural extraction boundaries)
- Setup/teardown blocks that can become separate functions
- Nested conditionals that handle distinct concerns

**Not a violation when:** The function is a straightforward sequence with no branching (e.g., a build/config function), or extraction would create artificial abstractions with no reuse.

### Nesting Depth (threshold: 3 levels)

Nesting beyond 3 levels signals control flow that's hard to follow. Remedies:
- **Guard clauses / early returns** — Invert condition, return early, flatten the happy path
- **Extract inner block** — If the nested block is self-contained, extract to a named function
- **Replace nested conditionals with lookup** — `if/else if/else if` → `Map` or `switch`

```
// BAD: 4 levels deep
function process(items) {
  if (items) {
    for (const item of items) {
      if (item.active) {
        if (item.valid) {
          // actual logic buried here
        }
      }
    }
  }
}

// GOOD: 1 level deep
function process(items) {
  if (!items) return;
  for (const item of items) {
    if (!item.active || !item.valid) continue;
    // actual logic at top level
  }
}
```

### Cyclomatic Complexity (threshold: 10)

Count decision points (if, else if, &&, ||, ?, case, catch). Above 10 → decompose:
- Extract each branch into a named function
- Use strategy pattern for polymorphic behavior
- Replace conditional chains with data-driven dispatch

### Parameter Count (threshold: 4)

Functions with > 4 parameters are hard to call correctly. Remedies:
- **Options object** — Group related params into a single typed object
- **Builder pattern** — For complex construction sequences
- **Partial application** — When some params are always the same

### Mixed Concerns

Single file or function handling multiple unrelated responsibilities:
- Data fetching + rendering + validation in one component
- Business logic + I/O + formatting in one function
- Types/interfaces + implementation + utilities in one file

Remedy: Extract each concern into its own unit. Name clearly.

---

## Pass 2: Code Smells & Anti-Patterns

### DRY Violations (threshold: 3 identical blocks)

Three or more identical (or near-identical, >80% similar) code blocks warrant extraction.

**Two similar blocks:** Tolerate. The cost of premature abstraction outweighs duplication.
**Three+:** Extract. The pattern is proven. Create a shared function/component.

When extracting:
- Name the abstraction after WHAT it does, not WHERE it came from
- Parameterize the differences, don't over-generalize
- Place the abstraction near its most frequent usage

### Dead Code

- **Unreachable branches** — `if (false)`, conditions that can never be true given types
- **Unused variables** — Declared but never read (not just assigned)
- **Unused imports** — Import statements with no reference in the file
- **Unused exports** — Exported symbols with no external consumers (verify with project-wide search!)
- **Commented-out code** — If it's in git history, delete it. Comments are not version control.

**Verification:** ALWAYS search the entire project for references before removing exports or "dead" functions. Dynamic imports, string-based lookups, and test files may reference them.

### Magic Values

Literal strings/numbers used in logic without named constants:
- `if (status === 3)` → `if (status === STATUS_APPROVED)`
- `setTimeout(fn, 86400000)` → `setTimeout(fn, ONE_DAY_MS)`
- `role === "admin"` → `role === ROLES.ADMIN` (if used in 2+ places)

**Exception:** Single-use literals with obvious meaning from context (e.g., `padding: 0`, `index === 0`).

### Feature Envy

A function that accesses more data from another module/class than its own:
- Reads 3+ properties from an external object
- Calls 2+ methods on an external object
- Contains logic that "belongs" to the other module

Remedy: Move the function to where the data lives, or extract the relevant data via a method on the owning module.

### Boolean Parameter Smell

`doThing(true, false, true)` — caller has no idea what the booleans mean.

Remedies:
- **Options object:** `doThing({ retry: true, silent: false, force: true })`
- **Separate functions:** `doThingWithRetry()`, `doThingSilently()`
- **Enum/union:** Replace boolean with descriptive union type

### Temporal Coupling

Operations that must happen in a specific order but nothing enforces it:
- `init()` must be called before `start()`
- `setConfig()` must precede `connect()`

Remedy: Builder pattern, state machine, or combine into a single function that enforces order.

---

## Pass 3: Convention & Consistency

### Project Standard Deviations

Compare against project docs (CLAUDE.md, AGENTS.md, linter config):
- Import style (relative vs absolute, extensions, aliases)
- Function declaration style (`function` keyword vs arrow, methods)
- Error handling pattern (try/catch, Result type, error codes)
- Naming convention (camelCase, snake_case, PascalCase for types)
- File organization (exports at top/bottom, type declarations location)

**Rule:** If the project doc says X, follow X even if the codebase has some Y. The doc is the intended standard.

### Naming Quality

Good names reveal intent without requiring a comment:
- `getUserById` > `getUser` > `get` > `g`
- `isAuthenticated` > `auth` > `a`
- `formatCurrency` > `format` > `fmt`
- `MAX_RETRY_COUNT` > `MAX` > `N`

**Red flags:** `data`, `result`, `temp`, `info`, `item`, `value`, `thing`, single letters (outside tiny scopes like `i` in a loop).

**Exception:** Well-established short names in domain context (e.g., `tx` for transaction in a DB module, `req`/`res` in HTTP handlers).

### Comment Quality

**Remove:** Comments that describe WHAT the code does (the code already says that)
```
// BAD: Increment counter by one
counter += 1;
```

**Keep/Add:** Comments that explain WHY a non-obvious decision was made
```
// GOOD: Use floor instead of round to match the billing system's truncation behavior
const amount = Math.floor(rawAmount * 100) / 100;
```

**Fix or Remove:** Comments that are outdated, wrong, or misleading (worse than no comment).

### Import Ordering

Follow the project's established pattern. Common conventions:
1. External packages (node_modules)
2. Internal aliases (@/...)
3. Relative imports (../../)
4. Type-only imports
5. Side-effect imports

Each group separated by a blank line, alphabetized within groups.
