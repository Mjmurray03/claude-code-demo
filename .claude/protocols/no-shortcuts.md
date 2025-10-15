# No Shortcuts Protocol

## Problem Statement

AI-assisted code generation consistently produces technical debt through seemingly minor shortcuts that accumulate into major maintenance burdens:

**Common shortcuts that undermine code quality:**
- Placeholder implementations that appear functional but produce incorrect results
- Hardcoded values masquerading as dynamic calculations
- Commented-out code left behind "temporarily"
- TODO comments signaling incomplete implementations
- Simplified workarounds replacing complex-but-correct solutions
- Missing error handling that works "most of the time"
- Skipped validation because "users won't do that"
- Fake test data instead of realistic scenarios

**Why shortcuts are tempting:**
- Faster initial delivery (short-term productivity gain)
- Appearance of progress (looks complete superficially)
- Avoidance of complex problem-solving
- Uncertainty about correct implementation

**True cost of shortcuts:**
- Bugs discovered in production (expensive, damages reputation)
- Misleading test results (false confidence in system reliability)
- Difficult debugging (misleading code obscures real issues)
- Compounding technical debt (shortcuts breed more shortcuts)
- Refactoring overhead (fixing shortcuts takes longer than doing it right initially)

## Protocol Objective

Enforce rigorous implementation standards that prevent technical debt accumulation. Every implementation must be production-ready, fully functional, and maintainable. No exceptions.

## Core Enforcement Rules

### Rule 1: Implementation Integrity

```
IF implementing a feature or function
THEN all functionality must be complete and correct
  AND all edge cases must be handled
  AND all error conditions must be addressed
  AND all calculations must use real formulas
  AND all data must be dynamically generated or fetched

NEVER create implementations that:
  - Appear functional but produce incorrect results
  - Use hardcoded values where dynamic data is required
  - Skip error handling for "unlikely" scenarios
  - Rely on assumptions about input data
  - Work only for happy path cases
```

**Verification questions:**
- Does this code produce correct results for all valid inputs?
- Have I tested edge cases (empty data, null values, boundary conditions)?
- What happens if external services are unavailable?
- What happens if input data is malformed or malicious?

### Rule 2: Error Handling Discipline

```
IF writing code that performs I/O operations (file, network, database)
THEN all operations must be wrapped in appropriate error handling
  AND errors must be logged with actionable context
  AND errors must propagate or be handled explicitly
  AND resources must be cleaned up properly (use context managers)

NEVER:
  - Use bare except: clauses (catches system exits and interrupts)
  - Silently swallow exceptions (except Exception: pass)
  - Return None to indicate errors (raises ambiguity)
  - Let exceptions propagate without context (raise bare exceptions)
```

**Example - Incorrect:**
```python
def fetch_data(url: str):
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None  # Which error occurred? How should caller handle?
```

**Example - Correct:**
```python
def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch JSON data from URL with proper error handling.

    Args:
        url: HTTP URL to fetch data from

    Returns:
        Parsed JSON data

    Raises:
        ValueError: If URL is invalid or empty
        ConnectionError: If network request fails
        TimeoutError: If request exceeds timeout
        ValueError: If response is not valid JSON
    """
    if not url:
        raise ValueError("URL cannot be empty")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout fetching data from {url}", exc_info=e)
        raise TimeoutError(f"Request to {url} timed out after 10 seconds") from e
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error fetching {url}", exc_info=e)
        raise ConnectionError(f"Failed to connect to {url}") from e
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error {e.response.status_code} from {url}", exc_info=e)
        raise ConnectionError(f"HTTP {e.response.status_code} from {url}") from e
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON from {url}", exc_info=e)
        raise ValueError(f"Response from {url} is not valid JSON") from e
```

### Rule 3: No TODO Comments or Placeholders

```
IF you cannot implement something correctly
THEN explicitly state what information or resources are needed
  AND do NOT create placeholder code that looks complete

NEVER write code containing:
  - TODO comments
  - FIXME comments
  - Placeholder return values (return None, return 0, return [])
  - Commented-out code (fix it or delete it)
  - Pass statements in function bodies (except for abstract base classes)
```

**When blocked, respond with:**
```
I need the following information to implement this correctly:

1. [Specific requirement or specification]
   Why needed: [How this affects correctness]
   Example: "What should the function return if database connection fails?"

2. [Technical detail or formula]
   Why needed: [How this affects implementation]
   Example: "Which RSI formula variant should be used (Wilder's or Cutler's)?"

3. [Configuration parameter or external dependency]
   Why needed: [How this affects integration]
   Example: "What is the API endpoint URL for production market data service?"

I will NOT create placeholder code that appears functional but produces incorrect
results. Providing these details will allow me to implement a complete, correct,
production-ready solution.
```

### Rule 4: Calculation Accuracy

```
IF implementing a formula or algorithm
THEN use the correct, industry-standard formula
  AND implement all steps of the algorithm
  AND validate outputs against known test cases
  AND document the formula source

NEVER:
  - Create "simplified" versions that produce different results
  - Use approximations without explicit documentation and justification
  - Return fake calculated values
  - Skip algorithm steps because they are complex
```

**Example - Incorrect:**
```python
def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculate RSI (Relative Strength Index)."""
    # Simplified approximation
    return 50.0 + random.uniform(-20, 20)  # Fake calculation
```

**Example - Correct:**
```python
def calculate_rsi(prices: List[Decimal], period: int = 14) -> Decimal:
    """
    Calculate Relative Strength Index using Wilder's smoothing method.

    Formula: RSI = 100 - (100 / (1 + RS))
    where RS = Average Gain / Average Loss

    Reference: J. Welles Wilder Jr., "New Concepts in Technical Trading Systems"

    Args:
        prices: Time series of closing prices (chronological order)
        period: Number of periods for calculation (default: 14)

    Returns:
        RSI value between 0 and 100

    Raises:
        ValueError: If period < 1 or prices insufficient for calculation
    """
    if period < 1:
        raise ValueError(f"Period must be at least 1, got {period}")
    if len(prices) < period + 1:
        raise ValueError(
            f"Need at least {period + 1} prices, got {len(prices)}"
        )

    # Calculate price deltas
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]

    # Separate gains and losses
    gains = [max(d, Decimal(0)) for d in deltas]
    losses = [max(-d, Decimal(0)) for d in deltas]

    # Initial average (simple moving average)
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # Apply Wilder's smoothing
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    # Calculate RSI
    if avg_loss == 0:
        return Decimal("100.00")

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.quantize(Decimal("0.01"))
```

### Rule 5: Data Authenticity

```
IF data should be dynamic (calculated, fetched from API, queried from database)
THEN implement the mechanism to retrieve or compute it
  AND handle failure cases explicitly
  AND validate data format and content

NEVER:
  - Use hardcoded values where real data should be used
  - Return static responses from functions that should be dynamic
  - Use placeholder data without clear documentation it is temporary
```

**Example - Incorrect:**
```python
async def get_stock_price(symbol: str) -> Decimal:
    """Get current stock price."""
    # TODO: Connect to real API
    return Decimal("150.00")  # Hardcoded placeholder
```

**Example - Correct:**
```python
async def get_stock_price(symbol: str) -> Decimal:
    """
    Get current stock price from market data API.

    Args:
        symbol: Stock ticker symbol (uppercase alphanumeric)

    Returns:
        Current price in USD

    Raises:
        ValueError: If symbol format invalid
        ServiceUnavailableError: If market data API unavailable
        SymbolNotFoundError: If symbol not recognized
    """
    # Validate input
    if not re.match(r'^[A-Z0-9]{1,10}$', symbol):
        raise ValueError(f"Invalid symbol format: {symbol}")

    # Fetch from API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.MARKET_DATA_API_URL}/quote",
                params={"symbol": symbol},
                headers={"Authorization": f"Bearer {settings.MARKET_DATA_API_KEY}"},
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()

            if "price" not in data:
                raise ValueError(f"No price data in API response for {symbol}")

            return Decimal(str(data["price"]))

    except httpx.TimeoutException as e:
        logger.error(f"Timeout fetching price for {symbol}", exc_info=e)
        raise ServiceUnavailableError(
            f"Market data API timeout for {symbol}"
        ) from e
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise SymbolNotFoundError(f"Unknown symbol: {symbol}") from e
        elif e.response.status_code >= 500:
            raise ServiceUnavailableError(
                f"Market data API error: {e.response.status_code}"
            ) from e
        raise
```

### Rule 6: Quality Gates

```
BEFORE marking any implementation complete:
  1. All calculations use real formulas (not approximations or fake math)
  2. All dynamic data has proper fetch/compute mechanisms (not static values)
  3. All errors are handled explicitly (not swallowed or ignored)
  4. All code executes correctly (not just "looks good")
  5. All features work end-to-end (not just partially)
  6. All edge cases are tested (not just happy path)
  7. All functions have type hints and docstrings (not undocumented)
  8. All tests pass (not skipped or commented out)
```

## Detection and Prevention

### Phase 1: Self-Monitoring

Watch for these internal warning signals (RED FLAGS):

**Linguistic red flags in your own thinking:**
- "for now"
- "temporary solution"
- "can be made dynamic later"
- "good enough"
- "we can improve this"
- "placeholder"
- "I'll come back to this"
- "quick workaround"

**When you detect these thoughts, STOP:**

1. Identify the specific gap:
   - What information is missing?
   - What complexity am I avoiding?
   - What error case am I not handling?

2. Choose appropriate response:
   - **Option A:** Implement properly (if you have all information needed)
   - **Option B:** Request clarification (if requirements unclear)
   - **NEVER Option C:** Create placeholder and move on

### Phase 2: Code Review Self-Check

Before submitting any implementation, perform this verification:

**Verification Checklist:**

```
[ ] I have NOT written any TODO or FIXME comments
[ ] I have NOT used placeholder return values
[ ] I have NOT hardcoded data that should be dynamic
[ ] I have NOT skipped error handling for any I/O operation
[ ] I have NOT simplified algorithms to avoid complexity
[ ] I have NOT left commented-out code
[ ] I have tested edge cases, not just happy path
[ ] I have written complete docstrings for all public functions
[ ] I have added type hints to all function signatures
[ ] All tests pass without skipping or mocking critical logic
```

**If ANY box is unchecked, implementation is INCOMPLETE.**

### Phase 3: Automated Checks

Enforce quality through linting and static analysis:

**Python Checks:**
```bash
# Type checking
mypy --strict src/

# Security and quality
bandit -r src/
ruff check src/

# Complexity
radon cc src/ -a -nb

# Test coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

**Fail CI/CD if:**
- Type errors detected
- Security issues found (hardcoded secrets, SQL injection patterns)
- Cyclomatic complexity > 10 for any function
- Test coverage < 80%
- Any test failures

## Enforcement Strategy

### Enforcement Level 1: Gentle Reminder

First violation:
```
PROTOCOL REMINDER: No Shortcuts Protocol

I detected a potential shortcut in my implementation. Specifically:
[Description of shortcut: placeholder value, missing error handling, etc.]

This violates the No Shortcuts Protocol which requires production-ready code
with no placeholders or incomplete implementations.

I will now correct this by:
[Specific corrective action]

Revised implementation:
[Complete, correct code]
```

### Enforcement Level 2: Mandatory Correction

Repeated violations:
```
PROTOCOL VIOLATION: No Shortcuts Protocol

Multiple shortcuts detected:
1. [Shortcut description and location]
2. [Shortcut description and location]
3. [Shortcut description and location]

This code is NOT production-ready and contains technical debt that will lead
to bugs, maintenance burden, and system unreliability.

I am REQUIRED to implement correctly or explicitly request missing information.

Corrective action required:
[List of specific fixes needed]

I will NOT proceed until these issues are resolved properly.
```

### Enforcement Level 3: Implementation Block

Systematic violation pattern:
```
IMPLEMENTATION BLOCKED: No Shortcuts Protocol Violation

I have consistently attempted to take shortcuts rather than implementing
correctly. This indicates either:
1. Requirements are unclear or incomplete
2. Technical complexity exceeds current capability
3. Missing information prevents correct implementation

Rather than continuing to produce flawed code, I am requesting:

Clarification needed:
1. [Specific requirement or specification]
2. [Technical detail or formula]
3. [Configuration or dependency information]

Once these are provided, I will implement a complete, production-ready solution
that meets all quality standards.
```

## Examples of Protocol Application

### Example 1: Formula Implementation

**Scenario:** Implement moving average convergence divergence (MACD) indicator

**Shortcut approach (PROHIBITED):**
```python
def calculate_macd(prices: List[float]) -> float:
    # TODO: Implement actual MACD formula
    # Using simplified approximation for now
    return sum(prices[-12:]) / 12 - sum(prices[-26:]) / 26
```

**Problems:**
- Incorrect formula (MACD uses EMA, not SMA)
- Missing signal line calculation
- Missing histogram calculation
- Incomplete return type (should return multiple values)
- No error handling

**No Shortcuts approach (REQUIRED):**
```python
from typing import Dict, List, Optional
from decimal import Decimal

def calculate_ema(
    prices: List[Decimal],
    period: int,
    smoothing: Decimal = Decimal("2")
) -> List[Optional[Decimal]]:
    """
    Calculate Exponential Moving Average.

    EMA = (Price - Previous EMA) * Multiplier + Previous EMA
    where Multiplier = smoothing / (period + 1)

    Args:
        prices: Time series of prices
        period: Number of periods for EMA
        smoothing: Smoothing factor (default: 2)

    Returns:
        List of EMA values (None for initial periods without enough data)
    """
    if period < 1:
        raise ValueError(f"Period must be at least 1, got {period}")
    if len(prices) < period:
        raise ValueError(
            f"Need at least {period} prices for EMA, got {len(prices)}"
        )

    multiplier = smoothing / (period + 1)
    ema_values: List[Optional[Decimal]] = [None] * (period - 1)

    # Initial EMA is SMA of first period
    sma = sum(prices[:period]) / period
    ema_values.append(sma)

    # Calculate remaining EMAs
    for i in range(period, len(prices)):
        ema = (prices[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)

    return ema_values

def calculate_macd(
    prices: List[Decimal],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9
) -> Dict[str, List[Optional[Decimal]]]:
    """
    Calculate MACD (Moving Average Convergence Divergence) indicator.

    MACD Line = EMA(fast) - EMA(slow)
    Signal Line = EMA(MACD Line, signal_period)
    Histogram = MACD Line - Signal Line

    Args:
        prices: Time series of closing prices
        fast_period: Fast EMA period (default: 12)
        slow_period: Slow EMA period (default: 26)
        signal_period: Signal line EMA period (default: 9)

    Returns:
        Dictionary with 'macd', 'signal', 'histogram' lists

    Raises:
        ValueError: If fast_period >= slow_period
        ValueError: If insufficient price data
    """
    if fast_period >= slow_period:
        raise ValueError(
            f"Fast period ({fast_period}) must be less than slow period ({slow_period})"
        )

    required_length = slow_period + signal_period
    if len(prices) < required_length:
        raise ValueError(
            f"Need at least {required_length} prices for MACD, got {len(prices)}"
        )

    # Calculate EMAs
    fast_ema = calculate_ema(prices, fast_period)
    slow_ema = calculate_ema(prices, slow_period)

    # Calculate MACD line
    macd_line: List[Optional[Decimal]] = []
    for i in range(len(prices)):
        if fast_ema[i] is None or slow_ema[i] is None:
            macd_line.append(None)
        else:
            macd_line.append(fast_ema[i] - slow_ema[i])

    # Calculate signal line (EMA of MACD line)
    # Filter out None values for signal calculation
    macd_values_only = [v for v in macd_line if v is not None]
    signal_ema = calculate_ema(macd_values_only, signal_period)

    # Align signal line with original data (prepend Nones)
    none_count = len([v for v in macd_line if v is None])
    signal_line = [None] * none_count + signal_ema

    # Calculate histogram
    histogram: List[Optional[Decimal]] = []
    for i in range(len(prices)):
        if macd_line[i] is None or signal_line[i] is None:
            histogram.append(None)
        else:
            histogram.append(macd_line[i] - signal_line[i])

    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }
```

### Example 2: API Integration

**Scenario:** Fetch user profile data from external API

**Shortcut approach (PROHIBITED):**
```python
def get_user_profile(user_id: int):
    # TODO: Connect to real API
    return {"id": user_id, "name": "Test User", "email": "test@example.com"}
```

**Problems:**
- Returns fake data instead of calling real API
- No error handling
- Missing type hints
- No input validation

**No Shortcuts approach (REQUIRED):**
```python
from typing import Dict, Any
from dataclasses import dataclass
import httpx
import logging

logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """User profile data from external API."""
    id: int
    name: str
    email: str
    created_at: str

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "UserProfile":
        """Create UserProfile from API response data."""
        required_fields = ["id", "name", "email", "created_at"]
        missing = [f for f in required_fields if f not in data]

        if missing:
            raise ValueError(f"Missing required fields in API response: {missing}")

        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            created_at=str(data["created_at"])
        )

async def get_user_profile(user_id: int) -> UserProfile:
    """
    Fetch user profile from external API.

    Args:
        user_id: Numeric user identifier

    Returns:
        UserProfile object with user data

    Raises:
        ValueError: If user_id is invalid (< 1)
        UserNotFoundError: If user_id does not exist
        ServiceUnavailableError: If API is unavailable or times out
        ValueError: If API response is malformed
    """
    if user_id < 1:
        raise ValueError(f"Invalid user_id: {user_id} (must be >= 1)")

    api_url = f"{settings.USER_API_BASE_URL}/users/{user_id}"

    logger.info(f"Fetching user profile", extra={"user_id": user_id})

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                api_url,
                headers={"Authorization": f"Bearer {settings.USER_API_TOKEN}"},
                timeout=5.0
            )
            response.raise_for_status()

            data = response.json()
            profile = UserProfile.from_api_response(data)

            logger.info(
                f"Successfully fetched user profile",
                extra={"user_id": user_id, "email": profile.email}
            )

            return profile

    except httpx.TimeoutException as e:
        logger.error(f"Timeout fetching user {user_id}", exc_info=e)
        raise ServiceUnavailableError(
            f"User API timeout after 5 seconds"
        ) from e

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.warning(f"User not found", extra={"user_id": user_id})
            raise UserNotFoundError(f"No user exists with id: {user_id}") from e
        elif e.response.status_code >= 500:
            logger.error(
                f"User API server error: {e.response.status_code}",
                extra={"user_id": user_id}
            )
            raise ServiceUnavailableError(
                f"User API server error: {e.response.status_code}"
            ) from e
        else:
            logger.error(
                f"User API client error: {e.response.status_code}",
                extra={"user_id": user_id}
            )
            raise

    except (ValueError, KeyError) as e:
        logger.error(
            f"Invalid response format from User API",
            extra={"user_id": user_id},
            exc_info=e
        )
        raise ValueError(f"Malformed API response for user {user_id}") from e
```

## Success Metrics

Track protocol compliance over time:

**Quality Metrics:**
```
Implementation Success Rate = (Implementations passing first review) / (Total implementations) * 100
Target: > 90%

Refactoring Rate = (Lines refactored due to shortcuts) / (Total lines written) * 100
Target: < 5%

Bug Escape Rate = (Bugs found in production) / (Total features deployed) * 100
Target: < 2%

Test Coverage = (Lines covered by tests) / (Total lines) * 100
Target: > 80%
```

**You are following this protocol correctly when:**
- Implementations work correctly on first or second attempt
- No TODO or FIXME comments in production code
- Error messages are clear and actionable
- Code passes review without major refactoring required
- Features work end-to-end without post-deployment patches
- Test coverage meets minimum thresholds
- No shortcuts detected in code reviews

**You are violating this protocol when:**
- You say "this is temporary" or "good enough for now"
- Code breaks in ways you "didn't expect"
- You fix the same issue multiple times
- Reviewers find missing error handling
- Tests reveal incorrect calculations
- Production bugs trace back to shortcuts taken during implementation

## Summary

The No Shortcuts Protocol enforces professional software engineering standards. Shortcuts create technical debt that compounds over time, leading to unreliable systems, expensive maintenance, and diminished trust.

Production-ready code requires:
- Complete implementations using correct formulas and algorithms
- Comprehensive error handling for all failure modes
- Dynamic data fetching/calculation (no placeholders)
- Full test coverage including edge cases
- Clear documentation explaining purpose and usage

When uncertain, request clarification. When blocked, state requirements explicitly. Never create the illusion of completeness through shortcuts.

Implement completely. Test thoroughly. Deliver reliably.
