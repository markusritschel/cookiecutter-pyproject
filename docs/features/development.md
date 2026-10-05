---
icon: material/code-braces
---

# Development Flow

This template provides a full, modern development environment with integrated tools for testing, code quality, and documentation.


## Core Tools

| Tool           | Purpose                                             |
| -------------- | --------------------------------------------------- |
| **uv**         | [Dependency & environment manager](./uv.md)         |
| **Ruff**       | [Linting & formatting](./code-quality.md)           |
| **ty**         | [Type checking](./code-quality.md)                  |
| **pytest**     | [Testing & coverage](./code-quality.md)             |
| **pre-commit** | [Git hooks for automated checks](./code-quality.md) |
| **Just**       | [Task automation](./justfile.md)                    |
| **Sphinx**, **Zensical** or **MyST** | [Documentation](./documentation.md) — whichever you chose at generation |


## Getting Started

I recommend you to use `uv` as a dependency and environment manager.
Read the [corresponding section of the documentation](./uv.md).
In your project's directory, run the following commands 

=== ":fontawesome-brands-apple: macOS / :fontawesome-brands-linux: Linux"
    ```bash
    uv venv

    source .venv/bin/activate

    uv sync --dev
    just qa                    # Verify setup
    ```

=== ":fontawesome-brands-windows: Windows"
    ```powershell
    uv venv

    .\.venv\Scripts\activate

    uv sync --dev
    just qa                    # Verify setup
    ```

To get more familiar with `uv`, I recommend you to have a look at the [official documentation](https://docs.astral.sh/uv/).

***

## A typical Development Workflow

### 1. Write Code

Edit source code in `src/mypackage/`:

```python
def user_data(name: str, age: int) -> dict: # (1)!
    """Process user data.
    
    Parameters
    ----------
    name : str
        User's full name
    age : int
        User's age in years
    """ # (2)!
    return {name: age}
```

1. Always make use of type hints
2. Give your functions meaningful docstrings, including parameter information and (if it helps the understanding) examples.

### 2. Write Tests

Add tests in `tests/`:

```python
def test_user_data():
    assert user_data("Albert", 30) == {"Albert": 30}
```

### 3. Run Quality Checks

```bash
just qa            # Autofix → Format → Lint → Type check → Test
```

### 4. Commit

```bash
git add .
git commit -m "Add user_data function"
```

Pre-commit hooks run automatically at this point — they autofix lint violations with `ruff check --fix`, reformat with `ruff format`, and update `uv.lock` and `requirements.txt` if needed. If a hook modifies a file, the commit is aborted; re-stage the changes and commit again.

!!! tip "Best practice"
    Make atomic commits. That is, commit every logical "bite" that does something meaningful in your code.
    Use "active" language, i.e. describe what the commit does when applied.


### 5. Update Documentation

Keep your project's [documentation](./documentation.md) up-to-date. Edit the markdown files in `docs/` and preview the rendered version, running
```bash
just docs-serve    # View at http://localhost:8000
```


### 6. Push to Github
```bash
git push
```

GitHub Actions automatically runs CI/CD. See [GitHub Actions](./github-actions.md). <br />
If GitHub pages is configured, your documentation will be served online on `https://<your-username>.github.io/<package-slug>`.


*** 

## Common Tasks

| Task               | Command                       |
| ------------------ | ----------------------------- |
| Add dependency     | `uv add package-name`         |
| Add dev dependency | `uv add --group dev package`  |
| Run specific test  | `just test tests/test_foo.py` |
| Format code        | `uv run ruff format .`        |
| Type check         | `uv run ty check .`           |
| Build package      | `just build`                  |
| Clean artifacts    | `just clean`                  |


## Demo Files and Git History

The template ships with a set of demo files to help you get started:

| File                         | Purpose                                                     |
| ---------------------------- | ----------------------------------------------------------- |
| `src/mypackage/cli.py`       | Example CLI entry point — only if you chose a CLI library[^cli] |
| `src/mypackage/submodule.py` | Example module with a documented function                   |
| `tests/*.py`                 | Minimal test stubs, including `conftest.py`                 |
| `scripts/*.py`               | Example helper scripts (research projects only)             |
| `notebooks/*.ipynb`          | Example notebooks (research projects only)                  |

[^cli]: The `command_line_interface` prompt defaults to **No command-line interface**, in which case
    neither `cli.py` nor the `[project.scripts]` entry point is generated. Choosing Typer, Click or
    Docopt generates the matching flavour — all three expose the entry point as `app`.

These files are deliberately **excluded from the initial git commit** by the post-generation hook. They exist in your working tree so you have something to reference, but they won't appear in your project's history. Replace or delete them as you build out your own code.


## Project Structure

The `src/` layout ensures tests run against installed package.

```yaml
├── src/mypackage/
├── tests/
├── docs/
├── notebooks/      # Jupyter notebooks for data exploration (1)
├── reports/        # Data reports, figures, etc. (2)
├── pyproject.toml  # (3)!
├── ruff.toml
└── justfile  # (4)!
```

1. Only present if `is_research_project` is answered with `yes`
2. Only present if `is_research_project` is answered with `yes`
3. Most of the project's configuration is in here
4. The justfile holds default tasks that can run simply like `just docs`.


## Project Scaffolding

Besides the code, the template generates the supporting files a maintained project is expected to
have. Most need one edit from you at some point:

| File | Purpose | Needs your attention |
| --- | --- | --- |
| `CITATION.cff` | Machine-readable citation metadata; GitHub renders a "Cite this repository" button | **Yes** — add your ORCID iD |
| `CHANGELOG.md` | Record of user-visible changes | With each release |
| `AUTHORS.md` | Contributors | When someone joins |
| `LICENSE` | The license you chose at generation | No |
| `.github/ISSUE_TEMPLATE.md` | Prompts for reporters to include the useful details | Optional |
| `.github/PULL_REQUEST_TEMPLATE.md` | Checklist shown when opening a PR | Optional |
| `.github/labeler.yml` | Path-based rules for automatic PR labels | When your layout changes |
| `.github/dependabot.yml` | Weekly dependency update PRs | No — see [Tips](../tips.md) |

!!! note "`LICENSE` and `CITATION.cff` are frozen after generation"
    Both embed the current year, so they are listed in the template's `_skip_if_exists` to stop
    `copier update` from silently rewriting the date. The consequence is that later structural
    improvements to these two files do not reach existing projects either.


## DevContainer

`.devcontainer/` defines a reproducible container environment for
[VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) and GitHub
Codespaces. Opening the project in a supported editor offers to reopen it in the container.

It is based on the official Microsoft Python image and, on creation, installs `uv`, runs `uv sync`,
and installs the pre-commit hooks. The VS Code settings point the Python interpreter and pytest at
the in-container `.venv`, so test discovery works without further configuration.

Use it when you want the toolchain isolated from your machine, or to give a collaborator a
working environment without a setup call. It is entirely optional — delete the directory if you
develop natively.


## AI Coding Agents

The generated project includes a `.claude/CLAUDE.md` describing its own structure: the package
layout, the path variables and `save()` helper, the testing and doctest conventions, the linting
rules, and how template updates work. Agents that read repository instructions pick this up
automatically, which saves re-explaining the project's shape in every session.

It ships with a **TBD** placeholder at the top, along with an instruction telling the agent to
interview you about the project's purpose and conventions and rewrite that section before doing
anything else. Fill it in early — the rest of the file describes the template, but only you know
what the project is for.

!!! tip
    Keep it current when the structure changes. A stale description is worse than none, since it is
    followed confidently.


## See Also

- [Package Conventions](./package-conventions.md) - Path variables, logging, `save()`
- [Code Quality](./code-quality.md) - Linting, type checking, testing
- [Task Automation](./justfile.md) - Available tasks
- [Documentation](./documentation.md) - Building docs
- [GitHub Actions](./github-actions.md) - CI/CD pipeline

## Further Reading

- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Docs](https://pytest.org/)
- [Sphinx Docs](https://www.sphinx-doc.org/)



