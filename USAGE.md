# Usage

## Auth flow
1. `POST /api/auth/register`
2. `POST /api/auth/login`
3. Use `Authorization: Bearer <access_token>` for protected endpoints.
4. Refresh token: `POST /api/auth/refresh`
5. Revoke refresh token: `POST /api/auth/logout`

## Run a pipeline
```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{"target":"Acme Corp","target_type":"organization"}'
```

Expected response includes:
- `report_id`
- `session_id`
- `entities_saved`

## Key read endpoints
- `GET /api/reports`
- `GET /api/reports/{report_id}`
- `GET /api/panel`
- `GET /api/entities`
- `GET /api/search?q=<query>`
- `GET /api/metrics`
- `GET /api/health`
