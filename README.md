# poly-pyhelpers
[![Tests](https://github.com/polyhydra-games/poly-pyhelpers/actions/workflows/test.yml/badge.svg)](https://github.com/polyhydra-games/poly-pyhelpers/actions/workflows/test.yml)

## Tags

- poly-pyhelpers
- docs
- poly
- pyhelpers
- game
- testing

# Purpose
Code for various helper methods will be added here.

Will expand and organize as need presents itself.

# Development

## Running Tests

Hermes Kanban test-foundation slice: `t_75b002e2`.

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html
```

The pytest harness is configured in `pyproject.toml` with shared fixtures in `test/conftest.py`. See [poly-pyhelpers Core Functions](./docs/features/poly-pyhelpers.md#test-foundation) for the test foundation notes.

## 📖 Documentation
Detailed documentation can be found in the following sections:
- [Docs Index](./docs/README.md)
- [Feature Index](./docs/features/README.md)
- [Core Capabilities](./docs/features/core-capabilities.md)
- [Roadmap Index](./docs/roadmaps/README.md)
