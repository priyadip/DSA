# 0/1 Knapsack Problem

## Problem Definition

You have a knapsack that can hold a maximum weight **W**. You are given **n** items, each with a weight `wt[i]` and a profit `pr[i]`. You must choose a subset of items such that:

- The total weight does not exceed **W**
- The total profit is maximized
- Each item is either taken or not taken - **no partial selection** (this is the "0/1" constraint)

**Formally:**

> Maximize: Σ pr[i] · xᵢ  
> Subject to: Σ wt[i] · xᵢ ≤ W, where xᵢ ∈ {0, 1}

---

## Theoretical Solution Approach

The brute-force approach checks every subset - 2ⁿ possibilities - which is exponential and impractical for large n.

The key insight for dynamic programming is **optimal substructure**: the optimal solution for `(n items, capacity W)` depends only on optimal solutions to smaller sub-problems. Specifically, for each item `i` at remaining capacity `w`, you face exactly two choices:

- **Skip** item `i` → problem reduces to `(i-1 items, w)`
- **Take** item `i` (only if `wt[i] ≤ w`) → gain `pr[i]`, problem reduces to `(i-1 items, w - wt[i])`

The recurrence is:

```
dp(i, w) = 0                                         if i < 0 or w ≤ 0
dp(i, w) = dp(i-1, w)                                if wt[i] > w
dp(i, w) = max( dp(i-1, w),  pr[i] + dp(i-1, w-wt[i]) )   otherwise
```

This gives **O(n × W)** time and space - pseudo-polynomial complexity.

---

## How to Choose Loop Bounds and Iteration Order

This is the most conceptually important part to get right. Getting the bounds or order wrong leads to subtle bugs that are hard to catch.

### The Two-State Sub-problem: `(i, w)`

Every DP formulation of 0/1 knapsack has two axes:

| Axis | Meaning | Range |
|------|---------|-------|
| `i` | which items are available (item index) | `0` to `n-1` (or `1` to `n` with 1-indexed DP table) |
| `w` | remaining weight capacity | `0` to `W` |

### Which Loop Goes Outer, Which Goes Inner?

**In the 2-D table (bottom-up):** both loops are independent of each other - the order doesn't matter **functionally**, but the convention is:

```
outer loop → i (items), from 1 to n
inner loop → w (capacity), from 1 to W
```

Why? Because for a fixed item `i`, you want to fill in all capacities before moving to item `i+1`. Each row `i` depends only on row `i-1` (the previous item), so you fill row by row.

```
for i in range(1, n+1):         ← outer: iterate over items
    for w in range(1, W+1):     ← inner: iterate over all capacities
        dp[i][w] = max(skip, take)
```

**In the 1-D rolling array (bottom-up):** the inner loop direction is **critical**:

```
for i in range(n):              ← outer: iterate over items
    for j in range(W, wt[i]-1, -1):   ← inner: go RIGHT TO LEFT (decreasing)
```

Why right to left? Because `dp[j - wt[i]]` must refer to the **previous item's value**, not the current item's already-updated value. If you went left to right, you'd overwrite `dp[j - wt[i]]` before reading it, which would allow taking the same item more than once (that's the unbounded knapsack problem, not 0/1).

The lower bound of the inner loop is `wt[i]` (not 0), because for `j < wt[i]`, item `i` can never be taken - those cells stay unchanged.

**In recursion (top-down):** there is no explicit loop. The recursion naturally explores `(i-1, w)` and `(i-1, w - wt[i])`, which mirrors the exact same structure - just driven by the call stack instead of loops.

### Summary Table

| Approach | Outer | Inner | Direction | Why |
|----------|-------|-------|-----------|-----|
| 2-D bottom-up | items `i`: `1→n` | capacity `w`: `1→W` | both forward | rows independent, fill row by row |
| 1-D rolling | items `i`: `0→n-1` | capacity `j`: `W→wt[i]` | **backward** | prevents reusing the same item |
| Top-down recursion | no explicit loops | driven by call stack | - | same logic, lazy evaluation |

---

## Top-Down vs Bottom-Up: Pros, Cons, and When to Use

### Top-Down (Memoization)

Recursion + a cache. You only compute sub-problems that are actually needed.

**Pros:**
- Natural to write - directly mirrors the recurrence relation
- Only computes states that are actually reachable (sparse problems benefit significantly)
- Easier to reason about correctness from the mathematical definition
- Works well when W is very large but the solution only touches a small region of the state space

**Cons:**
- Recursive call stack overhead - Python's default recursion limit (`sys.setrecursionlimit`) can be a problem for large `n`
- Cache lookup (dict or 2-D array) has slightly more overhead than direct array access
- Harder to optimize memory usage without restructuring the code

**Use top-down when:** the state space is sparse, W is enormous (making a full table wasteful), or you want fast, readable code for competitive programming with small n.

### Bottom-Up (Tabulation)

Iterative loops filling a table from base cases upward.

**Pros:**
- No recursion overhead - tight loops are faster in Python and most languages
- No recursion depth limit issues
- Easier to apply the rolling array optimization (reduce O(nW) space to O(W))
- Cache access is sequential - better CPU cache locality with the 2-D array

**Cons:**
- Computes **all** sub-problems even if many aren't needed for the final answer
- Slightly less intuitive to derive directly from the recurrence
- Rolling array version loses the ability to reconstruct which items were chosen (unless you add a separate structure)

**Use bottom-up when:** you need maximum performance, n and W are both large, memory is a concern (rolling array), or you need to avoid recursion limits.

### Quick Decision Guide

```
Large W, sparse access         →  Top-Down (dict memo)
Large n, full table needed     →  Bottom-Up 2-D or Rolling
Memory critical                →  Rolling Array (1-D bottom-up)
Need to reconstruct solution   →  Top-Down or Bottom-Up 2-D (not rolling)
Competition / quick code       →  Top-Down (dict is fastest to write)
```

---

## Code Walkthroughs


### [ Top-Down with 2-D Array Memoization ](Memoization.py)




**Key design choices:**

- Uses a **pre-allocated 2-D array** (`DT`) with sentinel value `-1` to mark unvisited states. This is faster than dict lookup for dense state spaces because array indexing (`DT[i][M]`) avoids hashing.
- The table has `n+1` rows even though the recursion is 0-indexed - this avoids an `IndexError` when `i = n-1` and a state is stored at row `n-1`.
- **Subtle difference from Code 1:** when `wt[i] > M`, the result is returned directly as `val(i-1, M)` without writing to `DT[i][M]`. This is correct but means the same "can't take" state might be recomputed if visited again. A minor optimization would be to cache it.
- The [walrus operator](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions) on the return line stores into `DT` and returns the value in one expression - concise but functionally identical to a two-line `DT[i][M] = val; return val`.
- Items are 0-indexedused the same way as [Top-Down with Dictionary Memoization](Memoization_Dict.py).

**Difference from [Top-Down with Dictionary Memoization](Memoization_Dict.py):** dict  allocates lazily and is better for sparse access; array  allocates upfront and is better for dense access with faster constant-time indexing.

---

### [Top-Down with Dictionary Memoization](Memoization_Dict.py)

**Key design choices:**

- Uses a **dictionary** as the memo table instead of a 2-D array. This is ideal when the recursion only visits a fraction of the `n × W` states - no memory wasted on unreachable states.
- The [**walrus operator** (`:=`)](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions) on the return line stores into `dp` and returns the value in one expression - concise but functionally identical to a two-line `dp[(i,w)] = val; return val`.
- Items are 0-indexed. The recursion goes from `i = n-1` down to `i = -1` (base case), which is the natural "process last item first" order.
- `take` is initialized to 0 and only computed when `wt[i] <= w` - avoids a branch with an otherwise meaningless `take` path.

---

### [Bottom-Up with 2-D DP Table](Tabulation.py)


**Key design choices:**

- The DP table is **1-indexed** for items (`i` goes from 1 to n), so inside the loop, `wt[i-1]` and `pr[i-1]` are used to access the 0-indexed input arrays. This is the classic textbook layout.
- Row 0 and column 0 are naturally 0 (no items / zero capacity → zero profit), serving as the base case without explicit initialization.
- `dp[i][w]` depends only on `dp[i-1][...]` - the **previous row**. This is why row-by-row filling works: by the time you compute row `i`, row `i-1` is completely filled.
- This version preserves the **full table**, which makes it possible to trace back which items were selected (by walking back from `dp[n][M]`).
- Space complexity: **O(n × W)** - the trade-off for being able to reconstruct the solution.

---

### [Bottom-Up with 1-D Rolling Array](RoolingArrays.py)

**Key design choices:**

- **Single 1-D array** replaces the full 2-D table - space drops from O(n × W) to **O(W)**. Instead of "rows", the array is updated in-place for each item.
- **The inner loop must go right to left** (`range(W, wt[i]-1, -1)`). Here's exactly why:
  - When computing `dp[j]`, you need `dp[j - wt[i]]` to represent the state **before** item `i` was considered.
  - If you went left to right, `dp[j - wt[i]]` would already be overwritten for the current item `i`, effectively allowing item `i` to be taken multiple times (unbounded knapsack behavior).
  - Going right to left ensures `dp[j - wt[i]]` is still the "old" value from the previous iteration.
- The lower bound `wt[i]` (exclusive stop in Python's `range`) means the loop only runs for capacities where item `i` could possibly fit. Indices below `wt[i]` are untouched.
- The **walrus operator** checks and assigns in one line: if the new value (take item `i`) beats the old (skip), update in place.
- **Trade-off:** you cannot reconstruct which items were selected from the 1-D array alone (the history is overwritten). Use [Bottom-Up with 2-D DP Table](Tabulation.py)
 if you need the item list, Code 4 if you only need the maximum value.

[LeetCode Problem →](https://leetcode.com/problem-list/50vif4uc/)  
[GeeksForGeeks →](https://www.geeksforgeeks.org/problems/0-1-knapsack-problem0945/1)

##  Connect with me
[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=googlechrome&logoColor=white)](https://priyadipsau.in)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/PriyadipSau)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/priyadip)
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@priyadipsau)
[![Substack](https://img.shields.io/badge/Substack-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://mechinterp.substack.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/priyadip-cs)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/priyadipsau)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/pritayenedip.sau)
[![Bluesky](https://img.shields.io/badge/Bluesky-0285FF?style=for-the-badge&logo=bluesky&logoColor=white)](https://bsky.app/profile/priyadipsau.bsky.social)