# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x | ✅ |

## Responsible Disclosure

If you discover a security vulnerability, please do NOT open a public GitHub issue. Instead:

1. Email the maintainer directly with details
2. Include a description of the vulnerability
3. Include steps to reproduce
4. Allow reasonable time for a fix before public disclosure

## Security Design

### Network Isolation

- The Tor client (`tor_net`) runs in an isolated Docker network with `internal: true` — it cannot communicate with any other Docker services and has no general internet access except through the Tor daemon
- `solace_net` is the main application network — Tor has zero connectivity here

### Secret Management

- All API keys and passwords are environment variables — never hardcoded
- `SECRET_KEY` is required to be at minimum 32 characters
- Database passwords are enforced at container startup
- Credentials directory (`credentials/`) is mounted read-only inside containers

### TLP Classification Enforcement

Report routing enforces TLP:
- TLP:RED → Signal (encrypted) + Telegram priority + Discord
- Nothing marked TLP:RED is sent to public-facing channels

### Data Retention

SOLACE does not automatically delete data. Operators should implement their own retention policies:
```sql
-- Example: delete raw items older than 90 days
DELETE FROM raw_intel_items WHERE collected_at < NOW() - INTERVAL '90 days';
```

## Legal Notice

SOLACE is designed for passive, open-source intelligence collection of publicly available information. It is the responsibility of the operator to:

- Comply with all applicable laws in their jurisdiction
- Respect the Terms of Service of all data sources
- Handle any collected personal data in accordance with GDPR, CCPA, and applicable privacy law
- Not use SOLACE to collect intelligence on individuals without appropriate legal authority
