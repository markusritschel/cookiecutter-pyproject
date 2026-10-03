# Change Log

## Unreleased

### Template

- **Fixed:** `docs/_static/` (a Sphinx `html_static_path` holding `custom.css` and the logo) was
  generated for all three documentation engines, leaving two orphan files in every Zensical and MyST
  project. Its path is now gated on `docs_engine == 'sphinx'`
- **Fixed:** `docs/readme.md`, `docs/license.md` and `docs/bibliography.md` are built from MyST
  directives (`{include}`, `{bibliography}`) that Python-Markdown does not implement, so a Zensical
  project got three pages rendering as literal code blocks or bare headings. They are no longer
  generated for Zensical, along with the then-unused `references.bib`. Providing Zensical variants
  was rejected: `{include}` has no equivalent without configuring `pymdownx.snippets`, and a page
  that only links to `README.md` earns less than the file it costs
- **Fixed:** `docs/example.md` demonstrated `{cite}`, `{math}` and `{py:obj}` regardless of engine,
  so under Zensical the starter page taught syntax that does not work. It now has an engine-specific
  body — admonitions, content tabs and code annotations for Zensical, and the API cross-reference
  section only for Sphinx, which is the only engine with an inventory to resolve it against
- **Fixed:** `just clean-docs` removed `docs/_build/` and `docs/api/` for every engine, so under
  Zensical it cleaned nothing and left the actual output in `site/`. The recipe is now generated per
  engine
- **Fixed:** `notebooks/jupyter_startup.ipy` ran `%load_ext jupyternotify`, but `jupyternotify` is
  not a dependency and that line — unlike the imports below it — had no `try`/`except`, so the
  startup script every notebook is told to `%run` failed on its second line. The extension and its
  commented `%autonotify` companion were removed rather than adding the dependency, since nothing
  else used them
- **Fixed:** `pyproject.toml` hardcoded `version = "0.1.0"` and ignored the `project_version`
  answer, while `CHANGELOG.md`, `CITATION.cff` and `__version__` used it. Answering anything but
  the default generated a project that disagreed with itself about its own version
- **Fixed:** `__version__` was a literal written once at generation time, so it went stale on the
  first `uv version --bump` — and nothing caught it, since `just tag`, `just release` and
  `release.yml` read only `pyproject.toml`. It is now read from the installed package metadata via
  `importlib.metadata`, leaving `pyproject.toml` the single source of the version
- Removed `mkdocstrings-python` from the Zensical `docs` group. It was installed but never
  configured, so it produced no API documentation while implying that it did
- **Added:** `.github/workflows/release.yml`, which publishes to TestPyPI and then PyPI whenever a
  GitHub release is published. It builds once and uploads the same files to both indexes, so what
  reaches PyPI is exactly what passed TestPyPI, and authenticates via trusted publishing, so no
  long-lived API token has to be stored as a repository secret
- **Added:** `just set-pypi-review`, which uses `gh` to make the current user a required reviewer on
  the `pypi` environment, turning the PyPI upload into a manual approval step. Self-review stays
  allowed, since in a single-maintainer project the person who publishes the release is the only
  possible reviewer

### Documentation

- Replaced the "Automated Publishing" section of `docs/features/publish-package.md`, which told users
  to write their own tag-triggered `publish.yml` around twine and a `PYPI_API_TOKEN` secret, with the
  setup for the generated `release.yml`: registering trusted publishers on PyPI and TestPyPI,
  `just set-pypi-review`, and releasing via `just tag` + `gh release create`. `release.yml` is also
  covered in `docs/features/github-actions.md`, `set-pypi-review` in `docs/features/justfile.md`,
  and the release flow in the generated `.claude/CLAUDE.md`
- Rewrote `docs/features/documentation.md`, which described Sphinx as if it were the only option
  although `docs_engine` has offered three since 1.0.0. It now leads with a comparison table and a
  recommendation (Sphinx, as the only engine generating API docs from docstrings), followed by
  per-engine content tabs covering configuration, navigation, citations and what each engine cannot
  do. Three separate pages were rejected — the shared 80% would have had to be maintained in
  triplicate
- Added `docs/features/package-conventions.md`. The path variables, `setup_logger()`, the
  `singledispatch` `save()` and its git-hash provenance decorator, `.env` loading and the matplotlib
  style sheets were documented only in the generated `.claude/CLAUDE.md` — that is, visible to
  coding agents but not to the humans the template is for
- Added `docs/features/cli.md` covering the `command_line_interface` prompt, the generated entry
  point, and how to replace the placeholder in each of the three flavours
- Added a "Doctests" section to `docs/features/code-quality.md`. `testpaths` includes `src` and
  `--doctest-modules` is enabled, so docstring examples are collected as tests — the most likely way
  for a newly generated project to go red unexpectedly. Documents the `pytest.skip()` convention the
  root `conftest.py` exists to support
- Added sections on the DevContainer, the generated scaffolding files (`CITATION.cff` and its ORCID
  placeholder, issue/PR templates, `labeler.yml`) and the shipped `.claude/CLAUDE.md` to
  `docs/features/development.md`, all of which were previously undocumented — the first two were
  even advertised on the index page with nowhere to click through to
- Added jupytext and startup-script documentation to `docs/features/research-projects.md`. The
  triple-format pairing is configured in `pyproject.toml`, but `docs/tips.md` recommended jupytext
  generically without mentioning that the template already sets it up. Also added the missing
  `LOG_DIR` to the path-variable table
- Removed `docs/features/snakemake.md`. It was absent from the `nav` (so unreachable through the
  site), positioned Snakemake relative to a `Makefile` that 2.0.0 deleted, and documented a tool the
  template does not ship
- **Fixed:** every documented generation command was missing `--trust`, so following the README, the
  docs site or the tutorial aborted with `Template uses potentially unsafe features:
  jinja_extensions, tasks` and created nothing. Both features are load-bearing — `jinja2-time`
  stamps the year into `LICENSE`/`CITATION.cff`, and `_tasks` runs `git init`, the first commit,
  `uv sync --dev` and pre-commit installation — so dropping them to make the flag unnecessary was
  rejected. The flag is now in `README.md`, `docs/index.md`, `docs/tutorial.md` (including the
  commented alternative URIs) and the `copier.yml` header, each with an explanation of *why* copier
  demands it, since an unexplained mandatory flag invites users to drop it again
- **Fixed:** the "strict type checking" snippet in `docs/features/code-quality.md` documented
  `[tool.ty] python_version` and `strict = true`, neither of which exists — `ty` accepts only the
  `environment`/`src`/`rules`/`terminal`/`analysis`/`overrides` subtables and rejects the entire
  `pyproject.toml` as invalid on a stray top-level key, so anyone copying it broke `just qa`. It now
  shows `[tool.ty.environment]` and per-rule severities, and notes that `ty` has no single strict
  switch
- **Fixed:** the `pyproject.toml` dependency snippet in `docs/features/uv.md` listed four packages
  that mostly are not in the template (`click`, `pandas`, `numpy`, `colorama`) instead of the actual
  17-package scientific baseline, and omitted `pre-commit` from the `dev` group and `safety` from the
  `test` group. The `docs` group is now marked as depending on the chosen `docs_engine` rather than
  hardcoding the Sphinx set
- **Fixed:** `docs/features/code-quality.md` documented the pre-commit config as lockfile
  maintenance only, omitting the `ruff` and `ruff-format` hooks — that is, the two hooks that
  actually rewrite the user's code on every commit. It also presented `pre-commit install` as a
  required one-time step, although `tasks/post_gen.py` already runs it during generation
- **Fixed:** the `ruff.toml` snippet in `docs/features/code-quality.md` showed 8 of the 16 enabled
  rule families and none of `target-version`, `include`/`exclude`, `per-file-ignores`, `mccabe` or
  `isort`. Reproducing all ~23 annotated `ignore` entries was rejected as unmaintainable
  duplication — the snippet now elides that one list explicitly and points at the generated file,
  while the rationale for `target-version` (it must not exceed `requires-python`) is stated inline,
  since getting it wrong breaks the CI matrix
- **Fixed:** `docs/features/github-actions.md` described the CI steps in the wrong order (lint runs
  before the format check, not after), omitted `--output-format=github`, the `actions/labeler` step
  and `workflow_dispatch`, and described the docs job as unconditionally installing Pandoc and
  building Sphinx — it is generated per `docs_engine`, and Zensical needs no Pandoc and publishes
  from `site/` rather than `docs/_build/html/`
- **Fixed:** `docs/features/development.md` described `cli.py` as an always-present Typer entry
  point, though the CLI is opt-in and defaults to none, and listed the uncommitted demo files as
  `tests/test_*.py` where `tasks/post_gen.py` actually excludes all of `tests/*.py` including
  `conftest.py`. The pre-commit step in the workflow section now mentions the ruff hooks
- **Fixed:** the CLI footnote in `docs/features/justfile.md` recommended `fire`, which the template
  does not offer, and omitted Typer, which it does; `docs/tutorial.md` showed a sample run selecting
  Typer although the default has been "No command-line interface" since 2.0.0
- **Fixed:** extensionless internal links (`](prompts)`, `](./uv)`, `](./tutorial)`) were emitted
  verbatim into the HTML instead of being resolved, and `](./features)` pointed at a directory with
  no page behind it

## 2.0.0

Finalized the migration from cookiecutter (+ cruft) to copier, and made the template more robust and user-friendly. The following changes were made:

- **Fixed:** the example/boilerplate files (`submodule.py`, `docs/example.md`, the demo notebook, everything in `tests/`) were missing from *every* generated project, and `cli.py` was emitted as a CLI app with no commands behind a registered entry point. They had been guarded with `{% if _copier_operation == 'copy' %}` — in the filename for the former, around the body for the latter — but copier only defines `_copier_operation` when evaluating `_tasks`/`_migrations` conditions; during path and content rendering it is undefined, so the condition was always false, filenames rendered to an empty stem and the guarded body rendered empty. Intent is now expressed via `_skip_if_exists`, which does not resurrect files the user deleted because `copier update` applies a template-side diff. Added `tests/` at the repo root, which renders the template and asserts on the generated tree, and wired the template's own tests into CI — the existing pipeline could not catch this, since `pytest` in a generated project exits 0 on the `src/` doctests even with an empty `tests/`
- The `command_line_interface` question now has an effect. Previously all four answers produced the same Typer `cli.py`, entry point and dependency set; now each generates the matching CLI and only the selected library, and "No command-line interface" omits `cli.py` and `[project.scripts]` altogether
- The `command_line_interface` question now defaults to "No command-line interface" (previously Typer) — choose Typer, Click or Docopt to opt in
- Removed the `Makefile` and consolidated on `just`. It predated the uv migration and contradicted the justfile beside it (conda environments, an editable install via pip, a hardcoded `sphinx-build` regardless of the chosen docs engine, and the invalid flag `uv sync --groups docs`). Its figure-processing targets — the only content `just` did not already cover — were ported to the justfile for research projects; keeping a second task runner just for those was rejected. Since this makes `just` a de-facto requirement, the generated `README.md` gained a "Don't have `just`?" section giving the plain `uv` command behind each common recipe (every recipe is a thin wrapper around one), the docs now cover installing it via `uv tool install rust-just`, and the repository README no longer calls `just` "optional but recommended"
- Rewrote the generated `README.md` around uv and just. It still instructed users to run `make conda-env`, `make src-available` and `make documentation` and recommended Conda/Mamba, contradicting the generated docs, which already documented `uv sync`. Its structure listing advertised `setup.py`, `requirements.txt`, `environment.yml`, `src/tests` and `reports/book`, none of which the template produces
- Fixed `pytest` `addopts` passing `"-ra -v"` as one entry, which argparse read as `-r` with the value `"a -v"`, silently dropping `-v`
- Fixed ruff `target-version = "py311"` against `requires-python = ">=3.10"`, which let the `UP` rules rewrite to syntax the lowest supported (and CI-tested) interpreter cannot parse
- Fixed the generated docs workflow referencing `steps.deployment.outputs.page_url` with no step carrying `id: deployment`, which left the GitHub Pages environment URL empty
- Fixed the package `__init__.py` appending a `scripts/` path that only exists for research projects, and importing `sys` solely for it, which tripped ruff F401 on library projects
- Replaced the example notebook's kernelspec, which was pinned to a personal conda environment
- Removed duplicate and unusable runtime dependencies (`jupytext` listed twice; `jupyterbook-latex` and `mystmd` in both the main dependencies and the docs group; `nodejs` and `pandoc`, which are not usable as PyPI packages)
- Renamed copier questions to copier's well-known variable names: `project_author` → `user_name`, `email` → `user_email`, `github_username` → `github_user`. Projects generated under the old names are remapped automatically on `copier update` via a `_migrations` entry in `copier.yml`.
- Added `scripts/migrate_cookiecutter_to_copier.py` to bootstrap a `.copier-answers.yml` for projects still generated with the old cookiecutter/cruft template, so they can adopt `copier update` — see [docs/tips.md](docs/tips.md#migrating-an-existing-cookiecuttercruft-project-to-copier)
- Project generation now uses `uvx --with jinja2-time copier copy gh:markusritschel/cookiecutter-pyproject my-project`
- Template updates now use `copier update` (replacing `cruft update`), tracked via the generated `.copier-answers.yml`
- Removed `cookiecutter.json` and the `hooks/` directory; prompts, conditional generation, and post-generation setup are now defined in `copier.yml`
- Replaced the inline POSIX-shell post-generation `_tasks` (git init/commit, `uv sync --dev`, pre-commit install) with a standalone `tasks/post_gen.py`, so project generation also works on native Windows without WSL/git-bash; the simpler inline-shell approach was considered but rejected for not being cross-platform
- Updated all user-facing documentation (README, docs site) to the copier workflow
- Migrated the template engine from cookiecutter (+ cruft for updates) to [copier](https://copier.readthedocs.io) — rationale in [docs/tips.md](docs/tips.md#why-copier-instead-of-cookiecutter-and-cruft)

## 1.0.0

- Merged two repositories ([cookiecutter-pypackage](https://github.com/markusritschel/cookiecutter-pypackage) & [cookiecutter-pysci-project](https://github.com/markusritschel/cookiecutter-pysci-project))
- Renamed the repository to `cookiecutter-pyproject`
- The new project now has its own documentation hosted on GitHub pages
- The documentation now includes more detailed information in favour of a shortened README.md
- Now uses `uv` as dependency manager
- Now uses justfile as taskrunner
- Now has extensive documentation on https://markusritschel.github.io/cookiecutter-pyproject/
- Uses Zensical for main documentation
