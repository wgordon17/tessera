# Testing

**Status**: ✅ 93 tests, 90% coverage

## Run Tests

```bash
pytest                    # Run all tests
pytest -m unit            # Unit tests only
pytest -m integration     # Integration tests only
pytest -n auto            # Parallel execution
```

Coverage reports in `.cache/coverage/index.html`

## Test Structure

```
tests/
├── conftest.py              # Auto-mocking fixtures
├── test_models.py           # 18 tests, 100% coverage
├── test_config.py           # 20 tests, 96% coverage
├── test_supervisor.py       # 18 tests, 93% coverage
├── test_interviewer.py      # 15 tests, 91% coverage
├── test_panel.py            # 14 tests, 81% coverage
├── test_integration.py      # 8 tests
├── examples/                # Usage examples
└── README.md                # This file
```

## Key Features

**Auto-mocking**: All LLM calls mocked automatically (no API keys needed)
**Pytest 9.0**: Native `pyproject.toml` configuration
**Fast**: Full suite runs in <1 second
**Deterministic**: No flaky tests

## CI/CD

```yaml
- run: uv sync --extra dev
- run: pytest
```

All test data and caches in `.cache/` directory.
