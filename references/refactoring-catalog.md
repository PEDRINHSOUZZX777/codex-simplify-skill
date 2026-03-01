# Refactoring Catalog — Techniques by Risk Level

Reference for Phase 5. Each technique includes risk level, when to apply, and a concrete example.

## Table of Contents

1. [Very Low Risk](#very-low-risk)
2. [Low Risk](#low-risk)
3. [Medium Risk](#medium-risk)
4. [High Risk](#high-risk)

---

## Very Low Risk

Safe to apply autonomously without user confirmation.

### Remove Dead Imports

```diff
- import { useState, useEffect, useCallback } from "react";
+ import { useState, useEffect } from "react";
```

**Verify:** `useCallback` has no reference in the file. Search for dynamic usage patterns.

### Remove Dead Variables

```diff
  function process(data) {
-   const temp = data.map(transform);
    const result = data.filter(isValid).map(transform);
    return result;
  }
```

**Verify:** `temp` is never read after assignment.

### Remove Commented-Out Code

```diff
  function calculate(x) {
-   // const oldWay = x * 2 + 1;
-   // return oldWay;
    return x * MULTIPLIER + OFFSET;
  }
```

**Rationale:** Git preserves history. Comments are not version control.

### Rename Local Variable (contained scope)

```diff
  function fetchUsers(query) {
-   const d = await api.get("/users", { params: query });
-   return d.data;
+   const response = await api.get("/users", { params: query });
+   return response.data;
  }
```

---

## Low Risk

Safe when the logic equivalence is verifiable by inspection.

### Extract Named Constant

```diff
+ const SESSION_TIMEOUT_MS = 30 * 60 * 1000;
+
  function checkSession(session) {
-   if (Date.now() - session.startedAt > 1800000) {
+   if (Date.now() - session.startedAt > SESSION_TIMEOUT_MS) {
      return expired();
    }
  }
```

### Add Guard Clause / Early Return

```diff
  function processOrder(order) {
-   if (order) {
-     if (order.items.length > 0) {
-       if (order.status === "pending") {
-         // actual logic here
-         return execute(order);
-       }
-     }
-   }
-   return null;
+   if (!order) return null;
+   if (order.items.length === 0) return null;
+   if (order.status !== "pending") return null;
+
+   return execute(order);
  }
```

### Simplify Boolean Logic

```diff
- if (isActive === true && isDeleted === false) {
+ if (isActive && !isDeleted) {
```

```diff
- return condition ? true : false;
+ return condition;
```

```diff
- if (x) {
-   return true;
- } else {
-   return false;
- }
+ return Boolean(x);
```

### Replace Nested Ternary with if/else or switch

```diff
- const label = status === "active" ? "Active" : status === "pending" ? "Pending" : status === "expired" ? "Expired" : "Unknown";
+ let label;
+ switch (status) {
+   case "active":  label = "Active";  break;
+   case "pending": label = "Pending"; break;
+   case "expired": label = "Expired"; break;
+   default:        label = "Unknown";
+ }
```

### Replace Conditional Chain with Lookup

```diff
- function getStatusColor(status) {
-   if (status === "success") return "green";
-   if (status === "warning") return "yellow";
-   if (status === "error") return "red";
-   if (status === "info") return "blue";
-   return "gray";
- }

+ const STATUS_COLORS = {
+   success: "green",
+   warning: "yellow",
+   error: "red",
+   info: "blue",
+ };
+
+ function getStatusColor(status) {
+   return STATUS_COLORS[status] ?? "gray";
+ }
```

---

## Medium Risk

Requires verifying all call sites. Double-check references before AND after.

### Extract Helper Function (3+ duplicates)

```diff
+ function formatUserName(user) {
+   return `${user.firstName} ${user.lastName}`.trim();
+ }
+
  function renderProfile(user) {
-   const name = `${user.firstName} ${user.lastName}`.trim();
+   const name = formatUserName(user);
    // ...
  }

  function renderComment(comment) {
-   const authorName = `${comment.author.firstName} ${comment.author.lastName}`.trim();
+   const authorName = formatUserName(comment.author);
    // ...
  }
```

**Rule of three:** Extract only when 3+ identical blocks exist. Two similar blocks → tolerate.

### Inline Unnecessary Abstraction (used once)

```diff
- function getActiveUserCount(users) {
-   return filterActiveUsers(users).length;
- }
-
- function filterActiveUsers(users) {
-   return users.filter(u => u.active);
- }

+ function getActiveUserCount(users) {
+   return users.filter(u => u.active).length;
+ }
```

**When:** The abstraction has exactly ONE caller and adds indirection without reuse value.
**Not when:** The function name adds significant clarity over the inline version.

### Replace Boolean Parameters with Options Object

```diff
- function createUser(name, email, isAdmin, sendWelcome, skipValidation) {
+ function createUser(name, email, options = {}) {
+   const { isAdmin = false, sendWelcome = true, skipValidation = false } = options;
```

**Verify:** Update ALL call sites.

### Restructure Control Flow

Convert `if/else if` chains to `switch`, strategy pattern, or polymorphism when:
- 5+ branches on the same discriminant
- Each branch is self-contained
- The pattern appears in multiple places

---

## High Risk

ALWAYS verify with user before applying. Requires updating all references.

### Change Function Signature

Renaming, reordering, or adding/removing parameters of exported functions.

**Protocol:**
1. Search ALL references project-wide (grep for function name)
2. Present change + all affected call sites to user
3. Apply atomically: signature + ALL call sites in one logical change
4. Run tests

### Move Code Between Files

Relocating functions, classes, or constants to a different module.

**Protocol:**
1. Identify all importers (grep for the import path)
2. Present the move + all import updates to user
3. Apply: create new location → update all imports → remove from old location
4. Run tests

### Rename Exported Symbol

Changing the name of a function, class, type, or constant that other files import.

**Protocol:**
1. Search ALL references project-wide
2. Include type references, string references, and test references
3. Present scope of change to user
4. Apply atomically across all files
5. Run tests
