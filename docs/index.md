---
icon: material/rocket-launch
---

<!-- https://fpgmaas.github.io/cookiecutter-uv/ -->
# PyProject Template 


This is a [copier](https://copier.readthedocs.io) template for Python projects.
It uses modern tools for development, testing, and packaging.
Depending on the responses to the [initial prompts](prompts.md), it can create a boilerplate for data science projects or for a general Python package.

??? note "Requirements"
    To use this template, you need to have [copier](https://copier.readthedocs.io) available on your machine.
    Either install it globally via pip or conda, or use `uv` to run it without the need of installing it.
    The latter is recommended.

## Quickstart
To get started, simply run
```bash
uvx --with jinja2-time copier copy --trust gh:markusritschel/cookiecutter-pyproject my-project
```
and follow the [prompts](prompts.md) to customize your project.
Once finished, navigate into the created `my-project/` directory to start working on your new Python project!

!!! warning "`--trust` is required"
    copier classifies two of the features this template relies on as unsafe and refuses to run
    without `--trust`:

    - the **`jinja2-time` extension**, which stamps the current year into `LICENSE` and `CITATION.cff`, and
    - a **post-generation task**, which initializes the git repository, makes the first commit,
      runs `uv sync --dev` and installs the pre-commit hooks.

    Omitting the flag aborts generation with
    `Template uses potentially unsafe features: jinja_extensions, tasks` — no project directory
    is created. The same applies to [`copier update`](tips.md#keep-your-project-up-to-date-with-copier).

??? note "Without uv"
    If you don't want to use uv, you can also install copier globally and run it with the following commands:
    ```bash
    pip install copier jinja2-time
    copier copy --trust gh:markusritschel/cookiecutter-pyproject my-project
    ```


## Features

This template comes ready with a collection of modern and useful tools for an efficient [development flow](features/development.md):

- **[Package Management](features/uv.md)**: [uv](https://docs.astral.sh/uv/) for blazingly fast dependency management and virtual environments (it's _a lot_ faster than conda 🚀)
- **[Code Quality](features/code-quality.md)**: Ruff for linting & formatting, ty for type checking, pytest for testing
- **[Task Automation](features/justfile.md)**: Just as a modern Make alternative (`just qa`, `just docs`, …)
- **[GitHub Actions CI/CD](features/github-actions.md)**: Automated testing, linting, and documentation deployment; Dependabot for dependency updates
- **[Documentation](features/documentation.md)**: Your pick of Sphinx, Zensical or MyST, with GitHub Pages deployment wired up for each
- **[Package Conventions](features/package-conventions.md)**: Project-root path variables, a logging setup, and a `save()` helper that stamps the git commit into every output file
- **[Command-Line Interface](features/cli.md)**: Optional CLI scaffolding with Typer, Click or docopt
- **[Publishing](features/publish-package.md)**: PyPI publishing via `just publish`, or automatically on each GitHub release (TestPyPI first, trusted publishing, optional manual approval)
- **[Research Projects](features/research-projects.md)**: Optional data science structure: `data/`, `notebooks/`, `reports/`
- **src layout**: Ensures tests always run against the installed package, not loose source files
- **[DevContainer](features/development.md#devcontainer)**: VSCode dev container for a reproducible development environment
- **[AI-agent ready](features/development.md#ai-coding-agents)**: Ships a `.claude/CLAUDE.md` describing the project's structure and conventions


## Next Steps

Read the [Tutorial](tutorial.md) for a step-by-step guide to create a new project.
In the **Features** section of the menu — starting with the [development flow](features/development.md) — you can find detailed documentation for each tool and feature.
