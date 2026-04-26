# Security Policy and Model

## Implemented controls
- bcrypt password hashing (`security/passwords.py`)
- JWT access + refresh tokens (`security/auth.py`)
- claims: `tenant_id`, `role`, `jti`, `type`, `exp`
- bearer-auth dependency enforcement (`security/deps.py`)
- token revocation checks (`RevokedToken` + `TokenStore`)
- IP-based rate limiting middleware
- security headers (`X-Content-Type-Options`, `X-Frame-Options`)

## Operational guidance
- Set a strong `SECRET_KEY` in production.
- Use TLS termination at the reverse proxy/load balancer.
- Restrict CORS to approved origins.
- Back `DATABASE_URL` with Postgres in production.
- Use short access token lifetimes and rotate refresh tokens.

## Reporting vulnerabilities
Please disclose privately to maintainers; do not open public exploit details before mitigation.
