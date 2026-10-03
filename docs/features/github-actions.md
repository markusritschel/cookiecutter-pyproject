---
icon: fontawesome/brands/github
---

# GitHub Actions CI/CD

The template includes automated Continuous Integration (CI) and Continuous Deployment (CD) via [GitHub Actions](https://github.com/features/actions).

!!! NOTE
    Keep in mind that the deployment may take a while. You can check the status of the workflow by clicking on "Action" in the menu bar of your repository.

## Workflow Files

The template ships the following workflow files:

### `main.yml` — CI

Runs on every push to `main` or `develop`, on pull requests targeting `main`, and on demand via the GitHub Actions UI (`workflow_dispatch`).

**`build` job** (matrix: Python 3.10, 3.12):

1. **Setup**: Installs uv and syncs all dev dependencies (`uv sync --locked --dev`)
2. **Lint**: Runs `ruff check . --output-format=github`, so violations appear as inline annotations on the diff
3. **Format check**: Runs `ruff format --check .` — no auto-fixing[^ci-format]
4. **Testing**: Runs `pytest -v`
5. **Coverage**: Uploads coverage data to [Codecov](https://codecov.io/) (requires `CODECOV_TOKEN` secret)
6. **Labeling**: Applies labels via [`actions/labeler`](https://github.com/actions/labeler) according to the rules in `.github/labeler.yml`

[^ci-format]: Formatting is deliberately kept out of CI's control: it should be applied locally
    (`just format`, or the pre-commit hook) rather than committed back by a workflow.

### `docs.yml` — Documentation

Runs only on pushes to `main` when documentation-related files change (`docs/**`, `src/**`, `*.md`). Can also be triggered manually via the GitHub Actions UI (`workflow_dispatch`).

**`build-documentation` job**: Installs uv, syncs the `docs` dependency group, and builds the documentation with the engine you chose during generation. The workflow is generated to match that choice — Sphinx and MyST additionally get Pandoc installed, and the artifact is uploaded from `docs/_build/html/` for Sphinx and MyST, or from `site/` for Zensical.

**`deploy-documentation` job** (runs after `build-documentation`): Deploys the uploaded artifact to GitHub Pages

### `release.yml` — Publishing

Runs when you publish a GitHub release (`just release`). It checks that the release tag matches the
version in `pyproject.toml`, builds the package once, uploads it to TestPyPI, and —
only if that succeeded — uploads the same files to PyPI. Both uploads use trusted publishing, so no
API token secret is needed, but each index must be told to trust the workflow first. The `pypi`
job runs in the `pypi` environment, which `just set-pypi-review` turns into a manual approval gate.
See [Publishing](./publish-package.md#automated-publishing) for the one-time setup and the release
steps.

### `dependabot-reviewer.yml` — Dependency updates

Approves and auto-merges Dependabot pull requests; see [Tips](../tips.md#keep-your-dependencies-up-to-date-with-dependabot).


## Workflow Status

Pull requests show status checks:

- ✅ **Passed** - All checks successful; safe to merge
- ❌ **Failed** - Fix issues before merging
- ⏳ **Running** - Workflow in progress


## Enable GitHub Pages Deployment

1. Go to **Settings → Pages**
2. Set source to **GitHub Actions**
3. Docs deploy automatically on main branch commits (URL: `https://<username>.github.io/<repo>`)


## Troubleshooting

**Workflow failed** – Click the run to view logs and find the failing step.

**Docs didn't deploy** – Verify GitHub Pages is set to use GitHub Actions as the source.

**Release stuck on "Waiting"** – The `pypi` job has a required reviewer. Open the run and click **Review deployments**.

**Trusted publishing failed (`invalid-publisher`)** – The publisher registered on PyPI/TestPyPI does not match the run; check owner, repository, workflow name (`release.yml`) and environment name (`pypi` / `testpypi`).

**Release tag does not match version** – The tag (e.g. `v1.2.0`) must equal `v` + the `version` in `pyproject.toml` of the released commit. Delete the release and its tag, push the version bump, and release again.

**Codecov upload skipped** – Add `CODECOV_TOKEN` to your repository secrets (**Settings → Secrets and variables → Actions**).


## See Also

- [Publishing](./publish-package.md) - PyPI deployment
- [Documentation](./documentation.md) - What gets built


## Further Reading

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [uv GitHub Actions Setup](https://github.com/astral-sh/setup-uv)
