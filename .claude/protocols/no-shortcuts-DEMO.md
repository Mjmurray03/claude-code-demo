# No Shortcuts Protocol

## The Problem
AI agents take shortcuts that create technical debt:
- Fake implementations that "look right" but don't work
- Placeholder values instead of real calculations
- Commented-out broken code
- "Good enough for now" solutions

## Core Rules

### 1. Implementation Integrity
```
IF you don't have complete requirements
THEN state what's missing
DO NOT create placeholder code
```

### 2. No Fake Formulas
```
IF you reference a formula
THEN implement the actual, correct formula
DO NOT create fake math that looks plausible
```

### 3. Fix, Don't Hide
```
IF code causes an error
THEN fix the root cause or remove it
DO NOT comment out broken code
```

## Detection (RED FLAGS)
Watch for these phrases:
- "for now"
- "temporary solution"
- "can be made dynamic later"
- "good enough"
- "TODO" / "FIXME"

## Response Protocol

When detecting a shortcut:

**Option A: Implement Properly**
"I'll implement complete solution with [details]"

**Option B: Request Information**
"I need [X] to implement properly. I will NOT create placeholder."

**NEVER Option C: Assume**
❌ "I'll use a default value for now..."

## Examples

### ❌ BAD
```python
def calculate_moving_average(prices):
    # TODO: Implement later
    return [0.0] * len(prices)
```

### ✅ GOOD
```python
def calculate_moving_average(
    prices: List[float], 
    window: int
) -> List[float]:
    """Calculate SMA with actual rolling window logic."""
    result = []
    for i in range(len(prices)):
        start = max(0, i - window + 1)
        window_data = prices[start:i + 1]
        result.append(sum(window_data) / len(window_data))
    return result
```

### ✅ GOOD (Requesting Info)
"I need clarification to implement correctly:
- Which MA variant? (Simple, Exponential, Weighted)
- Handle insufficient data how? (None, partial, exception)

I will NOT implement 'close enough' version."

---
📄 See `no-shortcuts.md` for complete 784-line specification