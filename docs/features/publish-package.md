---
icon: simple/pypi
---

# Publishing

Once your package is ready, you can publish it to [PyPI](https://pypi.org/) (Python Package Index) so others can install it with `pip`.

There are two routes: [manually](#manual-publishing) from your machine with `just publish`, or
[automatically](#automated-publishing) via the generated `release.yml` workflow whenever you publish
a GitHub release.

## Prerequisites

1. Create a free account at [pypi.org](https://pypi.org/) — and, for the automated route, a separate
   one at [test.pypi.org](https://test.pypi.org/)
2. For manual publishing: generate an API token in your PyPI account settings. The automated route
   needs no token (see [Trusted publishing](#1-register-the-workflow-as-a-trusted-publisher))

## Manual Publishing

### 1. Update Version

Edit `pyproject.toml`:

```toml
[project]
name = "your-package"
version = "1.0.0"
description = "Your package description"
```

Follow [Semantic Versioning](https://semver.org/): MAJOR.MINOR.PATCH
- **Major** (1.0.0) - Breaking changes
- **Minor** (0.1.0) - New features
- **Patch** (0.0.1) - Bug fixes

### 2. Update Changelog

Document changes in `CHANGELOG.md`:

```markdown
## Version 1.0.0 (2024-02-25)

### Added
- New feature X

### Fixed
- Bug in module Y
```

### 3. Build Package

```bash
just build
# Creates dist/your-package-*.whl and dist/your-package-*.tar.gz
```

### 4. Upload to PyPI

```bash
just publish
# Equivalent to: uv build && uv publish
```

When prompted for credentials, use:
- Username: `__token__`
- Password: Your PyPI API token

**View on PyPI:**
```
https://pypi.org/project/your-package-name/
```

Users can then install your package:
```bash
pip install your-package-name
```

## Automated Publishing

The generated project ships `.github/workflows/release.yml`. It runs whenever you **publish a
GitHub release** and passes the package through three jobs:

1. **`build`** — runs `uv build` once and uploads `dist/` as a workflow artifact
2. **`test-pypi`** — uploads that artifact to [TestPyPI](https://test.pypi.org/) (GitHub environment `testpypi`)
3. **`pypi`** — runs only if the TestPyPI upload succeeded, and uploads the very same files to
   PyPI (GitHub environment `pypi`)

Both upload jobs authenticate via [trusted publishing](https://docs.pypi.org/trusted-publishers/)
(OpenID Connect, hence `permissions: id-token: write`): PyPI trusts this particular workflow in
this particular repository, so there is no API token to create, store as a secret, or leak.

### 1. Register the workflow as a trusted publisher

Do this once on **both** [PyPI](https://pypi.org/manage/account/publishing/) and
[TestPyPI](https://test.pypi.org/manage/account/publishing/). For a project that does not exist on
the index yet, add a *pending publisher* with:

| Field             | Value                                               |
| ----------------- | --------------------------------------------------- |
| PyPI Project Name | the `name` in your `pyproject.toml` (your project slug) |
| Owner             | your GitHub user or organization                    |
| Repository name   | your repository                                     |
| Workflow name     | `release.yml`                                       |
| Environment name  | `pypi` on PyPI, `testpypi` on TestPyPI              |

The environment name must match exactly — it is part of what PyPI verifies.

### 2. Optional: approve each PyPI upload by hand

Uploads to PyPI are permanent: a version number can never be reused, even after deleting the
release on PyPI. To get a final confirmation step between TestPyPI and PyPI, make yourself a *required
reviewer* on the `pypi` environment:

```bash
just set-pypi-review
```

The recipe uses the [GitHub CLI](https://cli.github.com/) (`gh`, logged in with admin rights on the
repository) to create the `pypi` environment if needed and add you as its reviewer. Self-review is
explicitly allowed, so you can approve releases you started yourself. From then on, each release
run pauses before the `pypi` job until you click **Review deployments** in the run's page on the
**Actions** tab. Alternatively, configure the same under **Settings → Environments → pypi →
Required reviewers**.

!!! warning "Private repositories need GitHub Enterprise"
    On GitHub Free, Pro and Team plans, required reviewers are only available for
    [public repositories](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

### 3. Publish a release

Bump the version in `pyproject.toml` and update the changelog (steps 1 and 2 of
[Manual Publishing](#manual-publishing)), commit and push, then release:

```bash
just release    # gh release create v1.0.0 --generate-notes, version taken from pyproject.toml
```

If the tag `v1.0.0` does not exist yet, `gh` creates it on the tip of the default branch on GitHub —
so push first. To release from an annotated tag instead, run `just tag` beforehand; `just release`
then uses the existing tag. You can also create the release in the GitHub UI (**Releases → Draft a
new release**). Pushing a tag alone does **not** trigger the workflow — only publishing a release
does.

The workflow first checks that the release tag equals `v` + the `version` in `pyproject.toml` and
stops before uploading anything if they differ — for example when the version bump was not pushed.
It then uploads to TestPyPI, waits for your approval if you set up a reviewer, and uploads to PyPI.
Follow its progress on the **Actions** tab.

!!! tip "A failed release needs a new version number"
    If the PyPI job fails after the TestPyPI upload succeeded, re-running the whole workflow fails
    at TestPyPI, because that version already exists there. Re-run only the failed job, or bump the
    version and release again.


!!! note
    Always test your package locally before publishing!
## Configuration Reference

Key `pyproject.toml` fields:

```toml
[project]
name = "package-name"              # Unique on PyPI
version = "1.0.0"
description = "Brief description"
readme = "README.md"
requires-python = ">= 3.10"
license = {file = "LICENSE"}
authors = [{name = "Your Name", email = "you@example.com"}]

[project.urls]
Homepage = "https://github.com/user/package"
Documentation = "https://user.github.io/package"
Repository = "https://github.com/user/package.git"
Issues = "https://github.com/user/package/issues"

[project.scripts]
my-cli = "my_package.cli:main"     # CLI entry point
```

## See Also

- [GitHub Actions](./github-actions.md) - CI/CD workflows
- [Task Automation](./justfile.md) - `just release`, `just tag`, `just build` and `just set-pypi-review`

## Further Reading

- [PyPI.org](https://pypi.org/)
- [Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [uv publish](https://docs.astral.sh/uv/guides/package/#publishing-your-package)
- [GitHub deployment environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Semantic Versioning](https://semver.org/)
- [Python Packaging Guide](https://packaging.python.org/)
