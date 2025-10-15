# Claude Code Demo - Quick Reference

## Available Commands

### Slash Commands
```bash
/architect        # Design system architecture
/implementer      # Write production code
/security-audit   # Run security analysis
```

## Demo Scenarios (Copy & Paste)

### 1. Architecture Design (2 minutes)

**Invoke architect:**
```
/architect
```

**Prompt:**
```
Design a real-time notification system for stock price alerts. Requirements:
- Support 1000 concurrent users
- Sub-second notification latency
- Multiple notification channels (email, SMS, push)
- Handle 10,000 price updates per second
```

**Expected behavior:**
- Asks clarifying questions about scale
- Provides component diagram
- Justifies every design decision with trade-offs
- Lists alternatives considered
- Identifies risks with mitigations
- Does NOT write implementation code

---

### 2. Implementation (2 minutes)

**Invoke implementer:**
```
/implementer
```

**Prompt:**
```
Implement a function to calculate Bollinger Bands indicator:
- 20-period simple moving average
- Upper band: SMA + (2 * standard deviation)
- Lower band: SMA - (2 * standard deviation)
- Input: list of prices
- Return: dict with 'sma', 'upper_band', 'lower_band' lists
```

**Expected behavior:**
- Complete type hints
- Full error handling
- Comprehensive docstrings
- Actual formula implementation (no placeholders)
- Complete test suite
- No TODO comments

---

### 3. Security Audit (2 minutes)

**Run audit:**
```
/security-audit examples/vulnerable_api.py
```

**Expected findings:**
- Hardcoded credentials (CRITICAL)
- SQL injection vulnerabilities (CRITICAL)
- Command injection (CRITICAL)
- PII exposure in responses (HIGH)
- Missing authentication (HIGH)
- Missing authorization (HIGH)
- Sensitive data in logs (MEDIUM)

---

### 4. Protocol Enforcement (2 minutes)

**Test placeholder rejection:**

Prompt:
```
Create a function to calculate portfolio volatility. Just return 0.15 as a placeholder for now.
```

**Expected behavior:**
- Refuses to create placeholder
- Cites No Shortcuts Protocol
- Requests complete specifications
- Will NOT proceed with incomplete implementation

**Test TODO rejection:**

Prompt:
```
Add a comment "TODO: optimize this later" to the function.
```

**Expected behavior:**
- Removes TODO comment
- Either implements properly or requests information
- Explains why TODOs create technical debt

---

## Demo Flow Checklist

- [ ] Part 1: Show vulnerable code file
- [ ] Part 2: Run security audit
- [ ] Part 3: Show security findings
- [ ] Part 4: Invoke architect for design
- [ ] Part 5: Invoke implementer for code
- [ ] Part 6: Test protocol enforcement (placeholder rejection)
- [ ] Part 7: Show configuration files in `.claude/`
- [ ] Part 8: Share GitHub repository link

---

## Key Talking Points

**Opening:**
"AI-generated code often has shortcuts: placeholders, TODOs, missing error handling. This demo shows how to configure Claude Code to enforce production-grade standards."

**During architect demo:**
"Notice it asks clarifying questions and justifies every decision. It will NOT write implementation code - that's enforced by configuration."

**During implementer demo:**
"This is production-ready on the first pass. No placeholders, no TODOs. Every formula is fully implemented and tested."

**During security audit:**
"The audit catches vulnerabilities automatically and provides specific fixes with corrected code examples."

**During protocol enforcement:**
"The No Shortcuts Protocol prevents technical debt at the source. Claude refuses to create placeholders or incomplete implementations."

**Closing:**
"All of this is configured, not hardcoded. Every behavior you saw is defined in markdown files you can customize for your needs."

---

## Backup Prompts

### If architect needs more guidance:
```
Design a caching strategy for technical indicators. Consider:
- Cache invalidation when new market data arrives
- Handle 1000 different stock symbols
- Each indicator cached for 60 seconds
- Redis vs in-memory vs database caching trade-offs
```

### If implementer needs different example:
```
Implement an API endpoint using FastAPI:
- POST /indicators
- Request body: {"symbol": str, "indicator": str, "period": int}
- Validate: symbol is uppercase alphanumeric, period is 1-365
- Return 202 Accepted with job_id
- Include comprehensive error handling
```

### If security audit doesn't find issues:
Use the `examples/vulnerable_api.py` file which has multiple critical vulnerabilities.

---

## Troubleshooting

**Commands not working:**
- Check you're in the project directory
- Verify `.claude/` folder exists
- Try restart Claude Code

**Agents not behaving as expected:**
- Ensure agent markdown files exist in `.claude/agents/`
- Check file encoding is ASCII/UTF-8
- Verify agent frontmatter has `description` field

**Protocols not enforcing:**
- Verify `.claude/protocols/no-shortcuts.md` exists
- Check `.claude/CLAUDE.md` references the protocol
- Restart Claude Code session

---

## Repository Link

Share with audience:
```
https://github.com/Mjmurray03/claude-code-demo
```

All configuration files, examples, and documentation available for cloning and customization.

---

## Time Estimates

- **5-minute demo:** Security audit + protocol enforcement
- **10-minute demo:** Add architect design flow
- **15-minute demo:** Full cycle with implementation
- **20-minute demo:** Live coding scenario

---

## Success Metrics

After the demo, audience should understand:
1. How to configure custom agents
2. How to enforce coding standards
3. How to prevent technical debt
4. How to automate security audits
5. How to customize for their needs

---

## Follow-Up Resources

**Documentation:**
- `.claude/CLAUDE.md` - Project configuration
- `.claude/agents/architect.md` - Architecture agent spec
- `.claude/agents/implementer.md` - Implementation standards
- `.claude/commands/security-audit.md` - Security audit protocol
- `.claude/protocols/no-shortcuts.md` - Quality enforcement

**Examples:**
- `examples/vulnerable_api.py` - Vulnerable code for auditing
- `DEMO_GUIDE.md` - Comprehensive demo instructions
- `QUICK_REFERENCE.md` - This file

**Repository:**
- GitHub: https://github.com/Mjmurray03/claude-code-demo
- Clone and customize for your own projects
