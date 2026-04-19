# SOLACE — Contributing Guide

---

## Development Setup

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/solace.git
cd solace
```

### 2. Create `.env` for testing

```bash
cp .env.example .env
# Edit .env with test credentials
# At minimum:
# SECRET_KEY=test_secret_key_minimum_32_characters_long
# POSTGRES_URL=postgresql+asyncpg://solace:test@localhost/solace
# MONGODB_URL=mongodb://localhost/solace
# NEO4J_PASSWORD=test
# REDIS_URL=redis://localhost:6379/0
# CLICKHOUSE_PASSWORD=test
# MINIO_ACCESS_KEY=testkey
# MINIO_SECRET_KEY=testsecret
# ANTHROPIC_API_KEY=sk-ant-test
# OPENAI_API_KEY=sk-test
# GOOGLE_AI_API_KEY=test
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start dev databases

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d \
  postgres redis mongodb neo4j minio clickhouse
```

### 5. Run tests

```bash
PYTHONPATH=. python3 -m pytest tests/test_solace.py -v
# Expected: 129 passed
```

### 6. Start dev server

```bash
PYTHONPATH=. uvicorn api.main:app --reload --port 8000
```

### 7. Start dashboard dev server

```bash
cd dashboard
npm install
npm run dev
# Opens at http://localhost:3000
```

---

## Test Suite

Tests are in `tests/test_solace.py`. They run without live databases or API calls — all external dependencies are implicit (env vars set to dummies, DB connections never actually made in unit tests).

### Test structure (11 classes, 129 tests)

| Class | Tests | What it covers |
|-------|-------|----------------|
| `TestSettings` | 5 | Config loading, defaults, celery broker |
| `TestSchemas` | 11 | All Pydantic schemas, enums, validation |
| `TestReportSchema` | 14 | ID format, uniqueness, markdown sections |
| `TestBaseCollector` | 4 | SHA-256 hashing, determinism |
| `TestAggregator` | 10 | Dedup, filtering, reliability normalization |
| `TestNLPPipeline` | 8 | Keyword fallback, language detection |
| `TestPanelSessionState` | 18 | Full session lifecycle, serialization |
| `TestLoopDetector` | 10 | Empty prior, identical content, threshold variants |
| `TestPanelPrompts` | 12 | Prompt content, format, template vars |
| `TestDirectorParsing` | 13 | Question/status/topics extraction |
| `TestReportGeneratorLogic` | 15 | Confidence scoring, threat assessment, gaps |
| `TestIntegrationFlow` | 3 | End-to-end data flow |

### Running specific tests

```bash
# Single class
PYTHONPATH=. pytest tests/test_solace.py::TestPanelSessionState -v

# Single test
PYTHONPATH=. pytest tests/test_solace.py::TestLoopDetector::test_identical_keyword_loop -v

# With coverage
PYTHONPATH=. pytest tests/test_solace.py --cov=. --cov-report=term-missing
```

### Test helpers

```python
def make_raw_item(**overrides) -> RawIntelItemSchema
def make_enriched_item(**overrides) -> EnrichedIntelItem
def make_collection_result(...) -> CollectionResult
```

Use these in new tests to avoid repetitive boilerplate.

---

## Code Standards

### Python

- **Type hints** on every function signature
- **Google-style docstrings** on every class and public function
- **structlog** for all logging — always include `component` field
- **No bare `except:`** — catch specific exceptions
- **No stubs** — every function fully implemented
- **Lazy imports** in `__init__.py` files for optional dependencies

Example:
```python
async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
    """Collect intelligence for the target.

    Args:
        target: Subject to collect on.
        target_type: Classification of the target.

    Returns:
        CollectionResult with all collected items.

    Raises:
        ValueError: If target is empty.
    """
    if not target:
        raise ValueError("target cannot be empty")
    
    start = time.monotonic()
    items: list[RawIntelItemSchema] = []
    errors: list[str] = []
    
    try:
        data = await self._fetch(url)
        # ... process data
    except aiohttp.ClientError as exc:
        self.logger.error("fetch_failed", error=str(exc), url=url)
        errors.append(f"Fetch error: {exc}")
    
    return self._build_result(target, target_type.value, items,
                              time.monotonic() - start, errors)
```

### TypeScript/React

- Functional components with hooks only
- TypeScript types on all props and state
- Inline styles using CSS variables from `globals.css`
- No external UI libraries (Tailwind utilities only)

### Git

- Commit messages follow conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- One commit per logical change
- Tests must pass before PR

---

## Pull Request Process

1. Fork the repo and create a feature branch: `git checkout -b feat/my-feature`
2. Make your changes
3. Add or update tests to cover your changes
4. Ensure `129 passed` (or more) with no failures
5. Run the linter: `ruff check . && mypy .` (if configured)
6. Open a PR with:
   - Clear description of what changed and why
   - Test coverage summary
   - Any new dependencies added to `requirements.txt`

---

## Adding Features

### New Spider Bot

1. Create `collectors/spider_mybot.py` extending `BaseCollector`
2. Add `source_type` to `SOURCE_RELIABILITY` in `aggregator.py`
3. Register in `collectors/__init__.py` `get_spider()` factory
4. Add to `get_all_spiders()`
5. Update `COLLECTORS.md`
6. Add tests in `TestAggregator`

### New Storage Backend

1. Create `storage/mystore_client.py` with async methods
2. Add singleton `mystore_client = MyStoreClient()` at module level
3. Export from `storage/__init__.py`
4. Integrate into `tasks/collection_tasks.py` pipeline
5. Add Docker service to `docker-compose.yml`

### New API Endpoint

1. Add route to `api/main.py`
2. Use `Depends(get_db)` for database session
3. Return consistent JSON structure
4. Add to API documentation in `ARCHITECTURE.md`
5. Test with `curl` examples

### Modifying Panel Behavior

Panel prompts are in `panel/prompts.py`. Changes to the system prompts affect analytical behavior significantly — test carefully.

After changes, run:
```bash
PYTHONPATH=. pytest tests/test_solace.py::TestPanelPrompts tests/test_solace.py::TestDirectorParsing -v
```

---

## Reporting Issues

Please include:
1. Your OS and Docker version
2. The error message and full stack trace
3. Steps to reproduce
4. Contents of `docker compose ps` and relevant `docker compose logs`
5. Your `.env` (redact all API keys and passwords)

---

## License

By contributing, you agree your contributions will be licensed under the MIT License.
