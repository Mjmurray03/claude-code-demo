# Stock Analysis Pipeline - Claude Code Configuration

## Project Overview

### System Architecture
This project implements a production-grade real-time stock market analysis pipeline designed for algorithmic trading systems. The architecture leverages event-driven patterns to process market data streams, execute technical analysis calculations, and expose analytical results through RESTful APIs.

### Technology Stack Specifications

**Runtime Environment:**
- Python 3.11.x (CPython implementation)
- Minimum Python version: 3.11.0
- Recommended: 3.11.7 or latest patch release

**Core Framework:**
- FastAPI 0.104.x or higher
- Pydantic 2.x for runtime type validation
- Uvicorn ASGI server with multiprocessing support
- Starlette for async request handling

**Data Infrastructure:**
- PostgreSQL 15.x (primary relational datastore)
- Redis 7.x (pub/sub message broker and caching layer)
- TimescaleDB extension for time-series optimization
- Connection pooling via asyncpg (PostgreSQL) and aioredis (Redis)

**Development Dependencies:**
- pytest 7.x with pytest-asyncio for async test execution
- pytest-cov for coverage analysis
- black 23.x for code formatting
- mypy 1.7.x for static type checking
- ruff for fast linting

## Architectural Principles

### Event-Driven Design
All system components communicate via asynchronous message passing. State changes propagate through Redis pub/sub channels to ensure loose coupling and horizontal scalability.

**Event Flow:**
1. Market data ingestion layer publishes raw tick data
2. Analysis workers subscribe to relevant instrument channels
3. Technical indicators compute on streaming windows
4. Results publish to aggregation channels
5. API layer exposes computed metrics via WebSocket and REST

### Fail-Fast Error Handling
The system adheres to the "let it crash" philosophy borrowed from Erlang/OTP. Service boundaries enforce strict contracts:

- Invalid input data raises ValueError with descriptive context
- Resource exhaustion (DB connections, memory) raises ResourceError
- External service failures raise ServiceUnavailableError
- All exceptions propagate with full stack traces in development
- Production mode logs errors with correlation IDs and sanitized messages

### Structured Logging Strategy
All logging output follows the JSON Lines format for automated ingestion:

```python
{
  "timestamp": "2025-10-15T14:32:01.123Z",
  "level": "INFO",
  "service": "analysis-worker",
  "correlation_id": "req-abc123",
  "message": "RSI calculation completed",
  "context": {
    "symbol": "AAPL",
    "period": 14,
    "value": 67.42,
    "execution_time_ms": 12
  }
}
```

**Log Levels:**
- DEBUG: Detailed diagnostic information (disabled in production)
- INFO: Normal operational events (service start, job completion)
- WARNING: Degraded performance or approaching limits
- ERROR: Operation failed but service continues
- CRITICAL: Service-level failure requiring immediate attention

## Coding Standards

### Type Annotation Requirements

All function signatures must include complete type annotations for parameters and return values. Use `typing` module generics for collections.

**Required:**
```python
from typing import List, Dict, Optional, Union
from decimal import Decimal

def calculate_vwap(
    prices: List[Decimal],
    volumes: List[int],
    window_size: int = 20
) -> Optional[Decimal]:
    pass
```

**Prohibited:**
```python
def calculate_vwap(prices, volumes, window_size=20):  # Missing types
    pass
```

### Docstring Convention

Use Google-style docstrings for all public APIs (modules, classes, functions). Private functions (prefix `_`) may omit docstrings if purpose is obvious from context.

**Template:**
```python
def moving_average_convergence_divergence(
    prices: List[Decimal],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9
) -> Dict[str, List[Optional[Decimal]]]:
    """
    Calculate MACD indicator with signal line and histogram.

    Implements the standard MACD formula using exponential moving averages.
    Returns three series: MACD line, signal line, and histogram (MACD - Signal).

    Args:
        prices: Time series of closing prices in chronological order
        fast_period: Period for fast EMA calculation (default: 12)
        slow_period: Period for slow EMA calculation (default: 26)
        signal_period: Period for signal line EMA (default: 9)

    Returns:
        Dictionary with keys 'macd', 'signal', 'histogram', each containing
        a list of Decimal values. Early values are None until sufficient
        data points are available.

    Raises:
        ValueError: If fast_period >= slow_period or any period < 1
        ValueError: If prices list has fewer than slow_period elements

    Example:
        >>> prices = [Decimal(str(p)) for p in [100, 102, 101, 103, 105]]
        >>> result = moving_average_convergence_divergence(prices)
        >>> result['macd'][-1]
        Decimal('0.42')
    """
```

### Error Handling Policy

**Validation Errors:**
- Validate all input parameters at function entry
- Raise `ValueError` with specific error message describing constraint violation
- Never use bare `except:` clauses

**Resource Errors:**
- Wrap all I/O operations (file, network, database) in try/except blocks
- Use context managers (`with` statement) for resource cleanup
- Implement retry logic with exponential backoff for transient failures

**Example:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def fetch_market_data(symbol: str) -> MarketSnapshot:
    """Fetch current market data with automatic retry on transient failures."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.MARKET_DATA_API}/quote/{symbol}",
                timeout=5.0
            )
            response.raise_for_status()
            return MarketSnapshot.model_validate(response.json())
    except httpx.TimeoutException as e:
        logger.warning(f"Timeout fetching data for {symbol}", exc_info=e)
        raise ServiceUnavailableError(f"Market data service timeout: {symbol}") from e
    except httpx.HTTPStatusError as e:
        if e.response.status_code >= 500:
            raise ServiceUnavailableError(f"Market data service error: {e}") from e
        raise ValueError(f"Invalid symbol or request: {symbol}") from e
```

### Configuration Management

All runtime configuration must externalize to environment variables or configuration files. Never hardcode:

- API endpoints or service URLs
- Database connection strings
- Authentication credentials
- Feature flags or operational parameters
- Threshold values or business logic constants

**Configuration Loading:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration loaded from environment."""

    # Database
    postgres_dsn: str
    postgres_pool_min_size: int = 10
    postgres_pool_max_size: int = 50

    # Redis
    redis_url: str
    redis_max_connections: int = 100

    # API Keys (loaded from secrets management)
    market_data_api_key: str

    # Business Logic
    default_analysis_window_days: int = 90
    max_concurrent_analysis_jobs: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

## Testing Requirements

### Test Coverage Targets

- Minimum overall coverage: 80%
- Critical path functions (trading logic, risk calculations): 100%
- Configuration and startup code: 60% minimum
- UI/presentation layer: 70% minimum

### Test Organization

**Structure:**
```
tests/
  unit/
    analysis/
      test_technical_indicators.py
      test_statistical_functions.py
    models/
      test_market_data.py
  integration/
    test_api_endpoints.py
    test_database_operations.py
    test_redis_pubsub.py
  performance/
    test_indicator_benchmarks.py
```

### Unit Test Standards

Each test function must:
- Test exactly one behavior or edge case
- Use descriptive test names following pattern: `test_<function>_<scenario>_<expected_result>`
- Use AAA pattern: Arrange, Act, Assert
- Mock all external dependencies (databases, APIs, file I/O)

**Example:**
```python
import pytest
from decimal import Decimal
from analysis.indicators import relative_strength_index

def test_rsi_with_all_gains_returns_hundred():
    """RSI should return 100 when all price changes are positive."""
    # Arrange
    prices = [Decimal(str(p)) for p in [100, 101, 102, 103, 104, 105]]

    # Act
    result = relative_strength_index(prices, period=5)

    # Assert
    assert result == Decimal("100.00")

def test_rsi_with_insufficient_data_raises_value_error():
    """RSI should raise ValueError when fewer than period+1 prices provided."""
    # Arrange
    prices = [Decimal("100"), Decimal("101")]

    # Act & Assert
    with pytest.raises(ValueError, match="Need at least 15 prices"):
        relative_strength_index(prices, period=14)
```

### Integration Test Standards

Integration tests verify component interactions:
- Database query correctness and transaction handling
- API request/response contract compliance
- Message queue pub/sub delivery guarantees
- Caching layer invalidation logic

Use test fixtures for:
- Database schema setup/teardown
- Redis instance lifecycle
- Test data seeding

**Example:**
```python
import pytest
import asyncpg
from httpx import AsyncClient

@pytest.fixture
async def db_pool():
    """Create isolated test database pool."""
    pool = await asyncpg.create_pool(
        "postgresql://test:test@localhost/test_db",
        min_size=1,
        max_size=5
    )

    # Setup schema
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS market_snapshots (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(10) NOT NULL,
                price DECIMAL(12,2) NOT NULL,
                timestamp TIMESTAMPTZ NOT NULL
            )
        """)

    yield pool

    # Teardown
    async with pool.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS market_snapshots")
    await pool.close()

@pytest.mark.asyncio
async def test_api_stores_market_snapshot_in_database(db_pool):
    """POST /snapshots should persist data to PostgreSQL."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/snapshots", json={
            "symbol": "AAPL",
            "price": "150.25",
            "timestamp": "2025-10-15T14:30:00Z"
        })

    assert response.status_code == 201

    # Verify database persistence
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM market_snapshots WHERE symbol = $1",
            "AAPL"
        )
        assert row is not None
        assert row['price'] == Decimal("150.25")
```

## Security Requirements

### Input Validation Standards

All data entering the system from external sources must undergo validation:

1. **Type validation:** Pydantic models enforce runtime type checking
2. **Range validation:** Numeric inputs must fall within domain-specific bounds
3. **Format validation:** String inputs must match expected patterns (regex)
4. **Sanitization:** Remove or escape special characters before storage/display

**Example:**
```python
from pydantic import BaseModel, Field, validator
import re

class StockSymbol(BaseModel):
    """Validated stock ticker symbol."""

    symbol: str = Field(..., min_length=1, max_length=10)

    @validator('symbol')
    def symbol_must_be_uppercase_alphanumeric(cls, v):
        if not re.match(r'^[A-Z0-9]+$', v):
            raise ValueError('Symbol must contain only uppercase letters and numbers')
        return v

class PriceQuote(BaseModel):
    """Market price with validation."""

    symbol: StockSymbol
    price: Decimal = Field(..., gt=0, decimal_places=2)
    volume: int = Field(..., ge=0)
```

### Secrets Management

**Prohibited:**
- Hardcoded API keys in source code
- Credentials in configuration files committed to version control
- Passwords in log files or error messages

**Required:**
- Environment variables for local development
- Secrets management service (AWS Secrets Manager, HashiCorp Vault) for production
- Credential rotation procedures documented in runbook

**Pattern:**
```python
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def get_api_key(service_name: str) -> str:
    """
    Retrieve API key from environment or secrets manager.

    In production, this would call AWS Secrets Manager or similar.
    For development, falls back to environment variables.
    """
    key = os.getenv(f"{service_name.upper()}_API_KEY")
    if key is None:
        raise EnvironmentError(
            f"Missing required API key: {service_name.upper()}_API_KEY"
        )
    return key
```

### SQL Injection Prevention

All database queries must use parameterized statements. String concatenation or f-strings to build SQL are strictly prohibited.

**Correct:**
```python
async def get_quotes_by_symbol(conn: asyncpg.Connection, symbol: str):
    return await conn.fetch(
        "SELECT * FROM quotes WHERE symbol = $1 ORDER BY timestamp DESC LIMIT 100",
        symbol
    )
```

**Prohibited:**
```python
# DANGEROUS - SQL injection vulnerability
async def get_quotes_by_symbol(conn: asyncpg.Connection, symbol: str):
    query = f"SELECT * FROM quotes WHERE symbol = '{symbol}'"
    return await conn.fetch(query)
```

### PII and Sensitive Data Handling

This system does not process Personally Identifiable Information (PII) under normal operation. However:

- User account identifiers must be anonymized in logs (use hashed values)
- Trading positions and account balances are business-sensitive and require access controls
- Audit logs for compliance must be tamper-evident and retained per regulatory requirements

**Logging PII Protection:**
```python
import hashlib

def anonymize_user_id(user_id: str) -> str:
    """Hash user ID for logging purposes."""
    return hashlib.sha256(user_id.encode()).hexdigest()[:12]

# Usage
logger.info(
    "Portfolio calculation completed",
    extra={
        "user_id_hash": anonymize_user_id(user_id),
        "portfolio_count": len(positions)
    }
)
```

## Performance and Scalability

### Latency Targets

- API endpoint p50 latency: < 50ms
- API endpoint p95 latency: < 200ms
- API endpoint p99 latency: < 500ms
- Technical indicator calculation: < 100ms for 1000 data points
- Database query execution: < 20ms for indexed lookups

### Concurrency Model

- FastAPI runs on Uvicorn ASGI server with async/await
- Database operations use asyncpg connection pooling
- Redis operations use aioredis for non-blocking I/O
- CPU-bound tasks (heavy numerical computation) offload to ProcessPoolExecutor
- I/O-bound tasks use ThreadPoolExecutor or native async

### Caching Strategy

**Cache Layers:**
1. Application-level cache (functools.lru_cache for pure functions)
2. Redis cache for computed indicators (TTL: 60 seconds)
3. Database query result cache (5 minutes for historical data)

**Cache Invalidation:**
- Time-based expiration (TTL)
- Event-driven invalidation on new data arrival
- Manual cache busting via admin API endpoint

## Operational Procedures

### Error Recovery

When encountering unrecoverable errors:
1. Log full error context with correlation ID
2. Return appropriate HTTP status code to client
3. Emit metric to monitoring system
4. Continue serving other requests (isolation)

### Monitoring and Observability

**Key Metrics:**
- Request rate (requests per second)
- Error rate (percentage of failed requests)
- Latency distribution (p50, p95, p99)
- Database connection pool utilization
- Redis memory usage
- Active WebSocket connections

**Health Check Endpoint:**
```python
@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancer.

    Returns 200 if service is healthy, 503 if dependencies unavailable.
    """
    checks = {
        "database": await check_database_connectivity(),
        "redis": await check_redis_connectivity(),
        "api_ready": True
    }

    if all(checks.values()):
        return {"status": "healthy", "checks": checks}
    else:
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "checks": checks}
        )
```

## Development Workflow

### Feature Development Process

1. Create feature branch from `main`
2. Invoke `/architect` agent to design solution
3. Invoke `/implementer` agent to write code
4. Write tests achieving minimum coverage threshold
5. Run `/security-audit` to verify security compliance
6. Create pull request with design documentation
7. Address code review feedback
8. Merge to `main` after CI/CD pipeline passes

### Code Review Checklist

- [ ] All functions have type hints and docstrings
- [ ] Test coverage meets minimum threshold (80%)
- [ ] No hardcoded secrets or configuration
- [ ] Error handling covers expected failure modes
- [ ] Logging statements provide debugging context
- [ ] Database queries use parameterized statements
- [ ] API endpoints validate input data
- [ ] Performance meets latency targets

### Deployment Pipeline

**CI/CD Stages:**
1. Lint (ruff, black --check)
2. Type check (mypy --strict)
3. Unit tests (pytest tests/unit)
4. Integration tests (pytest tests/integration)
5. Coverage report (pytest-cov, fail if < 80%)
6. Security scan (bandit, safety)
7. Build container image
8. Deploy to staging environment
9. Run smoke tests
10. Deploy to production (blue-green deployment)

## Communication Protocols

### When Blocked or Uncertain

If requirements are ambiguous or information is missing:

1. **State explicitly what is unclear:** "I need clarification on the expected behavior when market data feed is unavailable."
2. **List assumptions you could make:** "I could assume we return cached data, return an error, or block until feed recovers."
3. **Request decision:** "Which approach aligns with system requirements?"
4. **Do not proceed with placeholder implementations**

### Reporting Progress

For multi-step tasks:
- Use TodoWrite to track implementation progress
- Mark tasks complete only when tests pass
- Report blockers immediately rather than working around them

### Asking for Help

Preferred question format:
- **Context:** What you're trying to accomplish
- **Attempted solution:** What you've tried
- **Specific question:** Exact information needed to proceed
- **Impact:** What is blocked by this question

## File Organization

```
claude-code-demo/
  .claude/
    CLAUDE.md                    # This file
    agents/
      architect.md               # Architecture design agent
      implementer.md             # Implementation agent
      qa.md                      # Quality assurance agent
    commands/
      security-audit.md          # Security audit workflow
      commit.md                  # Intelligent commit helper
      tdd-implement.md           # TDD workflow
    protocols/
      no-shortcuts.md            # Quality enforcement protocol
  src/
    analysis/
      indicators.py              # Technical indicator calculations
      statistical.py             # Statistical functions
    api/
      main.py                    # FastAPI application
      routers/
        quotes.py                # Market data endpoints
        analysis.py              # Analysis endpoints
      dependencies.py            # Dependency injection
    models/
      market_data.py             # Pydantic models
      analysis_results.py        # Analysis result schemas
    services/
      database.py                # Database connection pool
      cache.py                   # Redis cache client
      market_data.py             # External API client
    config/
      settings.py                # Configuration management
      logging.py                 # Logging configuration
  tests/
    unit/
      analysis/
      api/
      models/
    integration/
    performance/
    conftest.py                  # Pytest fixtures
  docs/
    architecture.md              # System architecture
    api_spec.yaml                # OpenAPI specification
    runbook.md                   # Operational procedures
  scripts/
    setup_db.py                  # Database initialization
    seed_test_data.py            # Test data generation
  requirements/
    base.txt                     # Production dependencies
    dev.txt                      # Development dependencies
  .env.example                   # Environment variable template
  pyproject.toml                 # Build configuration
  README.md                      # Project overview
```

## Additional Resources

**Internal Documentation:**
- Architecture Decision Records (ADRs): `docs/adr/`
- API Documentation: Auto-generated from OpenAPI spec
- Database Schema: `docs/schema.sql`

**External References:**
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- PostgreSQL: https://www.postgresql.org/docs/15/
- Redis: https://redis.io/docs/
