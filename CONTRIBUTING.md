# Contributing

## Development workflow
```bash
cp .env.example .env
pip install -r requirements.txt
python -m compileall .
pytest -q
```

## Code standards
- Python 3.11+
- FastAPI + Pydantic v2 patterns
- SQLAlchemy 2.0 typed ORM style (`Mapped`, `mapped_column`)
- Keep route names and schemas stable
- Prefer additive changes over destructive rewrites

## Pull request checklist
- [ ] Tests added/updated
- [ ] `python -m compileall .` passes
- [ ] `pytest` passes
- [ ] Docs updated for behavior changes
- [ ] No secrets committed

## Suggested PR structure
1. Problem statement
2. Design summary
3. Implementation notes
4. Testing evidence
5. Rollout/ops notes
