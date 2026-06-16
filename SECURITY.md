# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x.x   | ✅ Active |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

### How to Report

Email: **security@[your-domain].com** (or open a private security advisory)

GitHub: [Security Advisories](https://github.com/codebytaki/ai-automation-toolkit/security/advisories/new)

### What to Include

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (optional)

### Response Timeline

- **Acknowledgement:** Within 48 hours
- **Initial assessment:** Within 7 days
- **Patch release:** Within 30 days for critical issues

## Security Best Practices for Users

- Never commit `.env` files or API keys to version control
- Rotate API keys regularly
- Use environment variables for all secrets
- Enable GitHub secret scanning on your fork
- Keep dependencies updated (Dependabot is enabled)
- Run `bandit` security scanner before deploying: `bandit -r backend/app`

## Scope

**In scope:**
- Authentication bypass
- SQL injection / command injection
- Remote code execution
- API key exposure
- SSRF vulnerabilities

**Out of scope:**
- Issues requiring physical access
- Social engineering attacks
- DoS from legitimate usage
