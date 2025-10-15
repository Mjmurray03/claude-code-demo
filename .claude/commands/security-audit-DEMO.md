---
description: Security and quality audit
---

# Security & Quality Audit

## AUDIT PROCESS

### 1. Security Scan
- **PII Exposure**: SSNs, emails, credit cards
- **Hardcoded Secrets**: API keys, passwords, tokens
- **Injection Vectors**: SQL, command, XSS
- **Input Validation**: Missing sanitization

### 2. Quality Analysis
- **Error Handling**: Coverage, meaningful messages
- **Type Safety**: Missing hints, Any types
- **Code Complexity**: Functions >50 lines, cyclomatic >10
- **Testing**: Untested paths, missing edge cases

### 3. Risk Level
- **HIGH**: Security vulnerabilities, PII leaks
- **MEDIUM**: Poor error handling, validation gaps
- **LOW**: Style issues, missing docs

## OUTPUT FORMAT
```
Risk Level: [HIGH/MEDIUM/LOW]

Critical Issues:
1. [Issue with line number]

Security Concerns:
- [Description + why it matters]

Recommendations:
1. [Fix with code example]

Approve for Production: [YES/NO]
```

## EXAMPLE AUDIT
```python
# Code being audited
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
```

**RESULT:**
```
Risk Level: HIGH

Critical Issues:
1. SQL injection vulnerability - user_id concatenated

Security Concerns:
- Attacker can inject: `1 OR 1=1 --` to dump table
- No access control check

Recommendations:
1. Use parameterized queries:
   query = "SELECT id, name FROM users WHERE id = ?"
   return db.execute(query, (user_id,))

Approve: NO (SQL injection CRITICAL)
```

---
📄 See `security-audit.md` for complete 713-line specification