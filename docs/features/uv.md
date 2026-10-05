---
icon: material/package-variant-closed
---

# Package Management

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and virtual environment manager that replaces traditional tools like `pip`, `pip-tools`, and `venv`. The template uses uv as the primary tool for dependency management.

## Virtual Environment

uv automatically creates and manages virtual environments. 

To initialize and activate a virtual environment:

=== ":fontawesome-brands-apple: MacOS/:fontawesome-brands-linux: Linux"
    ```bash
    uv venv
    # If a venv already exists, say "no" and just activate it:
    source .venv/bin/activate
    ```

=== ":fontawesome-brands-windows: Windows"
    ```powershell
    uv venv
    # If a venv already exists, say "no" and just activate it:
    .\.venv\Scripts\activate
    ```

## Managing Dependencies

The template defines dependencies in `pyproject.toml` with organized dependency groups:

```toml title="pyproject.toml"
[project]
dependencies = [  # (1)!
  "colorama",
  "dask",
  "Deprecated",
  "ipykernel",
  "ipython",
  "ipywidgets",
  "jupyterlab",
  "jupytext",
  "marimo",
  "markdown",
  "matplotlib",
  "numpy",
  "pandas",
  "python-dotenv",
  "rich",
  "tqdm",
  "xarray",
]

[dependency-groups]
dev = [
  {include-group = "lint"},
  {include-group = "test"},
  "pre-commit"
]
lint = [
  "ruff",
  "ty",
]
test = [
  "pytest",
  "pytest-cov",
  "safety"
]
docs = [  # (2)!
  # ...
]
```

1. A scientific baseline, installed in every generated project. Prune what you don't need —
   `uv remove <package>` keeps `uv.lock` in sync. If you chose a CLI library during generation
   (Typer, Click or Docopt), it is added here as well.
2. The contents depend on the `docs_engine` you chose: the full Sphinx toolchain, `zensical` +
   `mkdocstrings-python`, or `mystmd`. See [Documentation](./documentation.md).

## Common uv Commands

**Sync dependencies** - Install all project dependencies:
```bash
uv sync
uv sync --group dev  # Include development dependencies
```

**Add a package** - Add a new dependency to the project:
```bash
uv add requests
uv add --group dev pytest-xdist
```

**Run commands** - Execute Python or installed tools within the virtual environment:
```bash
uv run python script.py
uv run --group dev pytest
uv run --group docs sphinx-build -b html docs/ docs/_build/html
```

**Build the project** - Create distributable packages:
```bash
uv build
```

## Dependency Resolution

uv automatically resolves dependency conflicts and creates a `uv.lock` file that pins exact versions for reproducible builds. This lock file should be committed to version control to ensure all collaborators use identical dependency versions.

## Integration with Tasks

The template's `justfile` tasks use `uv run` with specific dependency groups:

- `just format` / `just lint` – Run `ruff` via the `dev` group
- `just qa` – Runs lint autofixes, format, lint, type check and tests via the `dev` group
- `just test` / `just pdb` / `just coverage` – Run `pytest` via the `test` group
- `just docs` / `just docs-serve` – Build the documentation via the `docs` group

The split matters when you install selectively: `dev` includes both `lint` and `test`, so
`uv sync --dev` covers everything you need for `just qa`.

See [Task Automation with Just](./justfile.md) for complete task documentation.

## Further Reading

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 508 - Dependency Specification](https://www.python.org/dev/peps/pep-0508/)
