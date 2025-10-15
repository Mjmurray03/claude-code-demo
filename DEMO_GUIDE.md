# Claude Code Demo Guide

## Overview

This demo showcases advanced Claude Code features including custom agents, slash commands, and protocols that enforce production-quality code standards.

## Demo Flow (15-20 minutes)

### Part 1: Introduction (2 minutes)

**What to say:**
"I'm going to demonstrate how Claude Code can be configured with custom agents and protocols to enforce enterprise-grade engineering standards. This project simulates a stock analysis pipeline where we need production-ready code with no shortcuts."

**Show:** Open `.claude/CLAUDE.md` briefly to highlight:
- Technology stack specifications
- Architectural principles
- Security requirements

---

### Part 2: The Architect Agent (5 minutes)

**Scenario:** Design a real-time notification system for stock price alerts

**Command to run:**
```
/architect
```

**What to say to Claude:**
"Design a system to send real-time notifications when stock prices hit user-defined thresholds. We need to support 1000 concurrent users with sub-second notification latency."

**What to highlight:**
- Claude asks clarifying questions about scale, latency targets, notification channels
- Provides detailed architecture with component diagrams
- Includes trade-off analysis for every decision
- Lists alternatives considered and why they were rejected
- Identifies risks with mitigation strategies
- Does NOT write implementation code (stays at architecture level)

**Key point to emphasize:**
"Notice the architect agent doesn't write any code - it focuses purely on design decisions with explicit justifications. This is enforced by the agent configuration."

---

### Part 3: The Implementer Agent (5 minutes)

**Scenario:** Implement a technical indicator calculation

**Command to run:**
```
/implementer
```

**What to say to Claude:**
"Implement a function to calculate the Bollinger Bands indicator. It needs the 20-period simple moving average and standard deviation bands at +2 and -2 sigma."

**What to highlight:**
- Complete type hints on all functions
- Comprehensive error handling with specific exceptions
- Full docstrings with examples
- No TODO comments or placeholders
- Actual mathematical formulas fully implemented
- Complete test suite with edge cases

**Key point to emphasize:**
"The implementer agent produces production-ready code on the first pass - no placeholders, no TODOs, no shortcuts. Every formula is fully implemented and tested."

**Demo the enforcement:** Ask Claude to "just use a placeholder for now" and watch it refuse, citing the No Shortcuts Protocol.

---

### Part 4: Security Audit Command (4 minutes)

**Scenario:** Audit a vulnerable code sample

**Create a vulnerable file first:**

Create `examples/vulnerable_api.py`:
```python
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Hardcoded database password
DB_PASSWORD = "admin123"

@app.route('/user/<user_id>')
def get_user(user_id):
    # SQL injection vulnerability
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    return {"user": user, "password": user[2]}  # Exposing password in response
```

**Command to run:**
```
/security-audit examples/vulnerable_api.py
```

**What to highlight:**
- Detects hardcoded credentials
- Identifies SQL injection vulnerability
- Flags sensitive data exposure (password in response)
- Provides risk level (CRITICAL)
- Gives specific remediation with corrected code examples
- Blocks production deployment

**Key point to emphasize:**
"The security audit automatically catches common vulnerabilities and provides actionable fixes with corrected code examples."

---

### Part 5: No Shortcuts Protocol (3 minutes)

**Scenario:** Demonstrate protocol enforcement

**What to say to Claude:**
"Implement a function to calculate portfolio volatility. Just return 0.15 as a placeholder for now and we'll implement it later."

**What to highlight:**
- Claude refuses to create placeholder
- Explains why shortcuts create technical debt
- Requests complete specifications needed
- Will NOT proceed with incomplete implementation

**Alternative demo:**
Ask for implementation with "TODO: optimize this later" comment - watch Claude remove the TODO and either implement properly or request information.

**Key point to emphasize:**
"The No Shortcuts Protocol prevents technical debt at the source. No TODOs, no placeholders, no fake implementations."

---

### Part 6: Integration Demo (3 minutes)

**Scenario:** Complete feature development workflow

**Show the full cycle:**

1. **Architecture:**
   ```
   /architect
   Design a cache invalidation strategy for our technical indicators when new market data arrives.
   ```

2. **Implementation:**
   ```
   /implementer
   [Copy the architecture design from step 1]
   Implement the cache invalidation system according to this design.
   ```

3. **Security check:**
   ```
   /security-audit
   [Review the implemented code]
   ```

**Key point to emphasize:**
"This workflow ensures architectural planning, quality implementation, and security validation before any code reaches production."

---

## Quick Demo Script (5 minutes)

If you have limited time, focus on:

1. **Show the problem** (30 seconds)
   - "AI code often has placeholders, TODOs, and shortcuts"
   - "This creates technical debt and production bugs"

2. **Demo No Shortcuts Protocol** (2 minutes)
   - Ask for function with placeholder
   - Watch refusal and explanation
   - Show complete implementation instead

3. **Demo Security Audit** (2 minutes)
   - Run audit on vulnerable code
   - Show detailed findings with fixes

4. **Show the configuration** (30 seconds)
   - Briefly open `.claude/CLAUDE.md`
   - Highlight that all these behaviors are configured, not hardcoded

---

## Example Prompts Library

### For Architect Agent

**Good prompts:**
- "Design a rate limiting system that prevents API abuse while allowing burst traffic"
- "Design a data pipeline to ingest 10,000 stock quotes per second with fault tolerance"
- "Architect a microservices system for real-time portfolio calculation"

**What makes them good:**
- Focuses on system design
- Has scale/performance requirements
- Involves multiple components

### For Implementer Agent

**Good prompts:**
- "Implement the Exponential Moving Average indicator with Wilder's smoothing"
- "Create an API endpoint to fetch historical stock prices with pagination"
- "Implement a connection pool manager for PostgreSQL with health checks"

**What makes them good:**
- Specific implementation task
- Clear requirements
- Testable outcomes

### For Security Audit

**Good prompts:**
- "Run security audit on src/api/users.py"
- "Check the authentication module for vulnerabilities"
- "Audit all database query functions for SQL injection"

**What makes them good:**
- Specific files or modules
- Clear security focus

---

## Live Coding Demo

If you want to show real development:

**Scenario:** Build a simple stock price alert system

1. **Architecture phase** (use /architect):
   - "Design a system where users can set price alerts for stocks"
   - Show: component diagram, data flow, technology choices

2. **Create data model** (use /implementer):
   - "Create Pydantic models for PriceAlert with validation"
   - Show: type safety, validation rules, docstrings

3. **Implement alert checking** (use /implementer):
   - "Implement function to check if current price triggers any alerts"
   - Show: complete logic, error handling, tests

4. **Add API endpoint** (use /implementer):
   - "Create FastAPI endpoint POST /alerts to create price alerts"
   - Show: input validation, error responses, OpenAPI docs

5. **Security review** (use /security-audit):
   - Audit all the code created
   - Show: vulnerability detection (if any) or approval

**Time estimate:** 10-15 minutes for full cycle

---

## Troubleshooting

**If Claude doesn't use the agents:**
- Make sure you're invoking with `/architect` or `/implementer`
- Check that `.claude/` directory exists in working directory

**If protocols aren't enforced:**
- Verify `.claude/protocols/no-shortcuts.md` exists
- Check `.claude/CLAUDE.md` references the protocol

**If commands don't work:**
- Ensure `.claude/commands/security-audit.md` exists
- Verify the YAML frontmatter includes `description` field

---

## Key Talking Points

**Why this matters:**
- Reduces technical debt
- Enforces security best practices
- Ensures code quality consistency
- Accelerates code review process
- Prevents "works on my machine" issues

**Business value:**
- Faster time to production
- Lower maintenance costs
- Fewer production incidents
- Better security posture
- Easier onboarding for new developers

**Technical advantages:**
- Type safety catches errors at development time
- Comprehensive error handling prevents runtime failures
- Security audits prevent vulnerabilities before deployment
- Architecture-first approach reduces refactoring needs

---

## Q&A Preparation

**Q: Can I customize the agents for my specific needs?**
A: Absolutely. All agent behaviors are defined in markdown files. You can modify them or create new agents for your specific domain.

**Q: Does this slow down development?**
A: Initially, it may feel slower, but it eliminates debugging time, reduces bugs, and prevents technical debt. Net result is faster delivery of production-ready code.

**Q: What about existing codebases?**
A: You can gradually introduce these standards. Start with security audits on critical paths, then expand to new features.

**Q: Can I integrate this with CI/CD?**
A: The audit commands can be run as pre-commit hooks or CI pipeline steps to enforce standards before code review.

**Q: What if I need to prototype quickly?**
A: You can create a "prototyping" agent with relaxed standards, but clearly separate it from production code paths.

---

## After the Demo

**Follow-up resources:**
1. GitHub repository: https://github.com/Mjmurray03/claude-code-demo
2. Documentation files in `.claude/` directory
3. Example implementations created during demo

**Next steps for attendees:**
1. Clone the repository
2. Explore the `.claude/` configuration files
3. Try the demo scenarios themselves
4. Customize for their own projects

---

## Advanced Demo: Protocol Enforcement

**Show how protocols catch common mistakes:**

**Mistake 1: Placeholder returns**
```
Prompt: "Create a function to calculate RSI, just return 50.0 for now"
Result: Claude refuses, explains why, requests full specification
```

**Mistake 2: TODO comments**
```
Prompt: "Add a TODO comment to optimize this later"
Result: Claude removes TODO, either implements properly or states what's needed
```

**Mistake 3: Hardcoded credentials**
```
Prompt: "Connect to database with password 'admin123'"
Result: Security audit flags it immediately as CRITICAL issue
```

**Mistake 4: Missing error handling**
```
Prompt: "Just let the exception bubble up for now"
Result: Implementation protocol requires explicit error handling with context
```

---

## Demo Environment Setup

**Before the demo:**

1. Open terminal in the project directory
2. Have `.claude/` files visible in file explorer
3. Prepare the vulnerable code example file
4. Have GitHub repository URL ready to share
5. Open a text editor with example prompts ready to paste

**Screen layout:**
- Left side: Claude Code terminal
- Right side: Code editor showing configuration files

**Backup plan:**
- Have screenshots of successful runs
- Keep example outputs saved as reference
- Have the GitHub repo open in browser

---

## Closing Statement

"What you've seen is Claude Code configured to enforce production-grade engineering standards automatically. Every architectural decision is justified, every implementation is complete, and every security vulnerability is caught before deployment.

This isn't about making AI stricter - it's about making AI a reliable engineering partner that upholds the same standards we expect from senior engineers.

All of this configuration is open source and available in the GitHub repository. Feel free to clone it, customize it, and adapt it for your own projects."
