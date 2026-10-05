---
icon: material/shield-check
---

# Code Quality


This template includes modern tools to ensure consistent, high-quality code through automated linting, formatting, type checking, and testing.

## Linting & Formatting with Ruff

[Ruff](https://docs.astral.sh/ruff/) is an extremely fast Python linter and code formatter written in Rust. It replaces multiple tools (flake8, isort, black) with a single, unified tool.

**Configuration** in `ruff.toml`:

```toml title="ruff.toml"
line-length = 100
indent-width = 4
target-version = "py310"  # (1)!

include = ["src/**/*.py", "tests/**/*.py", "scripts/**/*.py"]  # (2)!
exclude = ["docs/", "notebooks/", "build/", ".venv/", "venv/", "htmlcov/"]

[format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true  # (3)!

[lint]
select = [
    "D",    # pydocstyle              — docstring presence and formatting
    "E",    # pycodestyle errors      — PEP 8 style errors
    "W",    # pycodestyle warnings    — PEP 8 style warnings
    "F",    # Pyflakes                — undefined names, unused imports
    "I",    # isort                   — import ordering and grouping
    "B",    # flake8-bugbear          — likely bugs and design issues
    "C4",   # flake8-comprehensions   — prefer comprehensions over map/filter
    "C901", # McCabe complexity       — flag overly complex functions
    "N",    # pep8-naming             — PEP 8 naming conventions
    "UP",   # pyupgrade               — modernize to newer Python syntax
    "PIE",  # flake8-pie              — miscellaneous lint rules
    "DTZ",  # flake8-datetimez        — timezone-aware datetimes
    "NPY",  # NumPy                   — NumPy-specific anti-patterns
    "PERF", # Perflint                — performance anti-patterns
    "PT",   # flake8-pytest-style     — consistent pytest patterns
    "RUF",  # Ruff-specific           — best practices unique to Ruff
]

ignore = [  ]  # (4)!

[lint.per-file-ignores]  # (5)!
"tests/**/*.py"   = ["D", "E741", "S101", "PLR2004"]
"**/__main__.py"  = ["D"]
"**/cli.py"       = ["D101", "D102", "D103"]
"scripts/**"      = ["D", "T201"]
"**/*.ipynb"      = ["B018", "F401"]
"notebooks/**"    = ["D", "E402", "T201", "B018", "F401"]

[lint.mccabe]
max-complexity = 10

[lint.isort]
known-first-party = ["mypackage"]  # (6)!
force-sort-within-sections = true

[lint.pydocstyle]
convention = "numpy"  # (7)!
```

1. Deliberately pinned to the lowest interpreter in `requires-python`. The `UP` rules rewrite code
   to the syntax of this version, so setting it higher produces code that CI's Python 3.10 job
   cannot parse.
2. Ruff only looks at `src/`, `tests/` and `scripts/`. Notebooks and docs are excluded — which is
   why the `notebooks/**` and `*.ipynb` entries under `per-file-ignores` are inert unless you widen
   `include`.
3. Formats code inside docstrings too — worth knowing, since `--doctest-modules` makes those
   examples part of your test suite.
4. Around two dozen rules are switched off individually, each with a comment explaining the rationale
   (formatting deferred to `ruff format`, patterns common in data-science code, and known Ruff
   issues). Read `ruff.toml` in your generated project for the annotated list.
5. Docstrings are not enforced in tests, scripts or notebooks, where the file name and surrounding
   context already carry the meaning.
6. Set to your `package_name`, so your own imports are grouped separately from third-party ones.
7. Choose one out of `{numpy, google, pep257}`. See also [Docstring Conventions](#docstring-conventions).

The file also documents the rule families it deliberately *omits* — `ANN` (type-annotation
enforcement), `ERA` (commented-out code), `T20` (print statements), `PL`, `S`, `SIM` and `PD` — each
with the reason it is inappropriate as a default for exploratory research code. Enable them
per-project as your code matures.

**Commands:**

| Task                     | Command                                |
| ------------------------ | -------------------------------------- |
| Check code w/o modifying | `uv run ruff check .`                  |
| Auto-fix violations      | `uv run ruff check . --fix`            |
| Format code              | `uv run ruff format .`                 |
| Sort imports             | `uv run ruff check --select I --fix .` |

Also check out the justfile shortcuts `just lint` and `just qa`.


## Type Checking with ty

[ty](https://docs.astral.sh/ty/) is a fast static type checker from the Ruff creators. It validates type annotations without running code.
Type hints help catch errors early and improve code clarity[^type-hints].

[^type-hints]: See [Python Type Hints](https://docs.python.org/3/library/typing.html) for syntax.

```python
def user_data(name: str, age: int) -> dict:
    """Process user data.
    
    Parameters
    ----------
    name : str
        User's full name
    age : int
        User's age in years
    """
    return {name: age}
```

**Commands:**

| Task                     | Command                                   |
| ------------------------ | ----------------------------------------- |
| Type check codebase      | `uv run ty check .`                       |
| Type check specific file | `uv run ty check src/mypackage/module.py` |

!!! info "Type checking in IDE"
    - `ty` provides a language server for real-time type checking
    - Most editors (VSCode, PyCharm) integrate with `ty` automatically


## Testing with pytest

[pytest](https://pytest.org/) runs unit tests and validates code behavior. Tests ensure your code works as expected and catch regressions.

**Configuration** in `pyproject.toml`:

```toml title="pyproject.toml"
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests", "src"] # (1)!
addopts = [
    "--doctest-modules",
    "--doctest-continue-on-failure",
    "-ra",
    "-v",
    "--cov=./src",
    "--cov-report=xml",
    "--cov-report=html",
    "--cov-report=term-missing"
]
```

1. Note that `src` is included alongside `tests` — see [Doctests](#doctests-your-docstrings-are-tests) below.



**Commands:**

| Task                         | Command                                                  |
| ---------------------------- | -------------------------------------------------------- |
| Run all tests                | `uv run pytest .` or `just test`                         |
| Run specific test file       | `uv run pytest tests/test_module.py`                     |
| Run specific test            | `uv run pytest tests/test_module.py::test_function_name` |
| Run tests matching pattern   | `uv run pytest -k "test_helper"`                         |
| Run with debugger on failure | `just pdb`[^pytest-debug]                                |
| Generate coverage report     | `just coverage`[^pytest-cov]                             |

[^pytest-debug]: Drops into IPython debugger when test fails, allowing inspection.

[^pytest-cov]: Generates a Terminal report showing % coverage per file as well as an HTML report in `htmlcov/index.html`.

!!! tip "Tip: Aim for >80% coverage"
    Focus on testing:

    - all public functions
    - edge cases and error conditions
    - critical code paths


### Doctests: your docstrings are tests

`testpaths` includes `src`, and `addopts` enables `--doctest-modules`. Together these mean **every
`>>>` example in your source docstrings is collected and executed as a test**. This is easy to
overlook and is a common first surprise: adding an illustrative example to a docstring can turn a
green test suite red.

```python
def add(a: int, b: int) -> int:
    """Add two numbers.

    Examples
    --------
    >>> add(2, 3)
    5
    """
    return a + b
```

`--doctest-continue-on-failure` means a failing line does not abort the remaining examples in the
same docstring, so you see every mismatch in one run rather than one per iteration.

**Skipping an illustrative example.** Not every example is meant to run — some reference files that
do not exist, or objects the reader is expected to supply. The generated project's root
`conftest.py` injects `pytest` into the doctest namespace precisely for this case, so you can bail
out of an example from inside the docstring:

```python
    Examples
    --------
    >>> pytest.skip()
    >>> save(my_object, "/tmp/out.nc")
    Save Dataset to /tmp/out.nc
```

Everything after `pytest.skip()` is reported as skipped rather than failed. Without that
`conftest.py` fixture, `pytest` would be an undefined name inside the doctest namespace and the
example would error instead.

!!! info "Consequence for empty test suites"
    Because the doctests in `src/` are collected, `pytest` exits 0 in a freshly generated project
    even before you have written a single test in `tests/`. A green run is therefore not by itself
    evidence that your own tests exist.


## Pre-commit Hooks

[pre-commit](https://pre-commit.com/) is a framework for managing and running git hooks. The template ships with a `.pre-commit-config.yaml` that formats your code and keeps your `uv` lockfile in sync automatically before each commit.

**Included hooks** (in execution order):

| Hook          | What it does                                                  |
| ------------- | ------------------------------------------------------------- |
| `ruff`        | Runs `ruff check --fix` — autofixes lint violations           |
| `ruff-format` | Runs `ruff format` — reformats the code                       |
| `uv-lock`     | Updates `uv.lock` to reflect changes to deps                  |
| `uv-export`   | Re-exports `requirements.txt` from the lockfile               |

The linter runs before the formatter on purpose: `ruff check --fix` may rewrite imports and other
constructs, and the formatter then cleans up the result.

!!! info "`uv-lock` runs on every commit"
    It is configured with `always_run: true` rather than only when `pyproject.toml` is staged, so it
    also catches a lockfile left stale by a manual edit.

**Setup:** the hooks are installed for you during project generation — `tasks/post_gen.py` runs
`uv run pre-commit install` right after `uv sync --dev`. You only need to run it yourself after
cloning the repository somewhere else, or if generation ran without `uv` available:

```bash
uv run pre-commit install
```

This registers the hooks with git. From then on they run automatically on every `git commit`.

**Run hooks manually** (without committing):

```bash
uv run pre-commit run --all-files
```

!!! tip
    If a hook modifies a file (e.g. updates `uv.lock`), the commit is aborted so you can review and re-stage the change. Just run `git add` and commit again.


## Running All Quality Checks

Execute all checks at once:

```bash
just qa
```

Runs in order: lint autofixes (incl. import sorting) → formatting → linting → type checking → tests

!!! tip
    Use this before committing code.


## Project Structure

The template uses a `src/` layout, ensuring that tests run against the installed package:

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
├── tests/
│   ├── conftest.py
│   └── test_module.py
├── pyproject.toml
└── ruff.toml
```

This way, tests validate distribution, not local files.
They also catch missing dependencies or import issues.


## Integration with CI/CD

GitHub Actions runs Ruff and pytest automatically on every push and pull request. 
All checks must pass before merging. 
See [GitHub Actions CI/CD](./github-actions.md).


## Configuration Best Practices

### Docstring Conventions

Choose one standard for your project and configure Ruff accordingly:

```toml title="ruff.toml"
[lint.pydocstyle]
convention = "numpy"
```

- **NumPy** - for comprehensive, scientific projects
- **Google** - for simple, readable format
- **PEP257** - Python fall-back convention

See also the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#google-vs-numpy) and [Ruff settings](https://docs.astral.sh/ruff/settings/#lint_pydoclint_ignore-one-line-docstrings).

### Stricter Type Checking

`ty` has no single "strict" switch. You tighten it by raising the severity of individual rules in
`pyproject.toml`, each set to `"error"`, `"warn"` or `"ignore"`:

```toml title="pyproject.toml"
[tool.ty.environment]
python-version = "3.10"  # (1)!

[tool.ty.rules]
possibly-unresolved-reference = "error"
possibly-missing-attribute = "error"
```

1. Only needed to check against a different version than the interpreter in your environment.
   `ty` otherwise infers it from `requires-python`.

Unknown rule names are reported as an `unknown-rule` warning rather than silently ignored, so a typo
is visible. See the [ty rules reference](https://docs.astral.sh/ty/rules/) for the full list.

!!! warning "`[tool.ty]` takes no top-level settings"
    Options live in the `environment`, `src`, `rules`, `terminal`, `analysis` and `overrides`
    subtables. Putting a key directly under `[tool.ty]` is a hard error — `ty` refuses to run and
    reports the whole `pyproject.toml` as invalid.

## Further Reading

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Rules Reference](https://docs.astral.sh/ruff/rules/)
- [ty Documentation](https://docs.astral.sh/ty/)
- [pytest Documentation](https://pytest.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [pre-commit Documentation](https://pre-commit.com/)
- [uv pre-commit integration](https://docs.astral.sh/uv/guides/integration/pre-commit/)
