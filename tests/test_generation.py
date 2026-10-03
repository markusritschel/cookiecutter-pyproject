"""Generation tests for the template itself.

These render the template from the *working tree* and assert on the resulting
file tree. They exist because the CI pipeline cannot catch a dropped file: it
runs `pytest` in the generated project, which exits 0 on the doctests in
`core/utils.py` even when `tests/` is empty and the example modules are missing.

Rendering goes through a plain (non-git) copy of the repository so that copier
takes its filesystem path rather than its VCS path. That renders exactly what is
on disk — uncommitted changes included — and avoids `--vcs-ref` resolving to the
latest git tag.
"""

import re
import shutil
from pathlib import Path

import pytest
from copier import run_copy

REPO_ROOT = Path(__file__).resolve().parents[1]

# Directories that must not be handed to copier as part of the template source.
IGNORED = shutil.ignore_patterns(
    ".git",
    ".venv",
    ".remember",
    "site",
    ".cache",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
)

# Real dotfiles, as opposed to a filename whose Jinja-conditional stem rendered
# to the empty string (e.g. `.ipynb`, `.md`) — see test_no_filename_lost_its_stem.
KNOWN_DOTFILES = {
    ".env",
    ".gitignore",
    ".gitkeep",
    ".gitattributes",
    ".copier-answers.yml",
}

BARE_EXTENSION = re.compile(r"^\.[a-z]+$")


@pytest.fixture(scope="session")
def template_src(tmp_path_factory):
    """A plain-directory copy of the template repository."""
    src = tmp_path_factory.mktemp("template_src") / "template-repo"
    shutil.copytree(REPO_ROOT, src, ignore=IGNORED)
    return src


def _generate(template_src, dst, **answers):
    run_copy(
        str(template_src),
        str(dst),
        data={"project_name": "Python Boilerplate", **answers},
        defaults=True,
        unsafe=True,  # the template declares _tasks and a jinja extension
        skip_tasks=True,  # git init / uv sync are not under test here
        quiet=True,
    )
    return dst


@pytest.fixture(scope="session")
def research_project(template_src, tmp_path_factory):
    dst = tmp_path_factory.mktemp("research") / "proj"
    return _generate(template_src, dst, is_research_project=True)


@pytest.fixture(scope="session")
def library_project(template_src, tmp_path_factory):
    dst = tmp_path_factory.mktemp("library") / "proj"
    return _generate(template_src, dst, is_research_project=False)


# Example/boilerplate files a freshly generated project must contain. Keep in
# sync with `example_files` in tasks/post_gen.py, which un-stages them.
# Note: cli.py is deliberately absent — `command_line_interface` defaults to
# "No command-line interface". The CLI flavours are covered separately below.
COMMON_EXAMPLE_FILES = [
    "docs/example.md",
    "src/python_boilerplate/submodule.py",
    "tests/conftest.py",
    "tests/test_submodule.py",
]

# (answer, module the generated cli.py must import)
CLI_CHOICES = [("Typer", "typer"), ("Click", "click"), ("Docopt", "docopt")]
RESEARCH_EXAMPLE_FILES = [
    "notebooks/01-minimal-example.ipynb",
    "scripts/01-test.py",
]


@pytest.mark.parametrize("relpath", COMMON_EXAMPLE_FILES + RESEARCH_EXAMPLE_FILES)
def test_research_project_has_example_file(research_project, relpath):
    assert (research_project / relpath).is_file()


@pytest.mark.parametrize("relpath", COMMON_EXAMPLE_FILES)
def test_library_project_has_example_file(library_project, relpath):
    assert (library_project / relpath).is_file()


def test_default_answers_omit_the_cli(research_project):
    """`command_line_interface` defaults to "No command-line interface"."""
    assert not (research_project / "src/python_boilerplate/cli.py").exists()
    assert "[project.scripts]" not in (research_project / "pyproject.toml").read_text()


def test_typer_app_defines_a_command(template_src, tmp_path):
    """A Typer app with no command raises when the entry point is invoked."""
    proj = _generate(template_src, tmp_path / "proj", command_line_interface="Typer")
    cli = (proj / "src/python_boilerplate/cli.py").read_text()
    assert "@app.command()" in cli


@pytest.mark.parametrize(("choice", "module"), CLI_CHOICES)
def test_cli_choice_selects_the_library(template_src, tmp_path, choice, module):
    """Every `command_line_interface` answer must change what is generated."""
    proj = _generate(
        template_src, tmp_path / "proj", command_line_interface=choice, is_research_project=False
    )
    cli = (proj / "src/python_boilerplate/cli.py").read_text()
    pyproject = (proj / "pyproject.toml").read_text()

    assert f"import {module}" in cli or f"from {module} import" in cli
    # the other CLI libraries must not be pulled in as dependencies
    for other in {m for _, m in CLI_CHOICES} - {module}:
        assert f'"{other}"' not in pyproject
    assert "[project.scripts]" in pyproject


def test_no_cli_choice_omits_the_entry_point(template_src, tmp_path):
    """A registered entry point pointing at a missing module fails at runtime."""
    proj = _generate(
        template_src,
        tmp_path / "proj",
        command_line_interface="No command-line interface",
        is_research_project=False,
    )
    assert not (proj / "src/python_boilerplate/cli.py").exists()
    assert "[project.scripts]" not in (proj / "pyproject.toml").read_text()


def test_docopt_usage_is_the_module_docstring(template_src, tmp_path):
    """docopt parses __doc__, so the usage text must be the first statement."""
    proj = _generate(
        template_src,
        tmp_path / "proj",
        command_line_interface="Docopt",
        is_research_project=False,
    )
    cli = (proj / "src/python_boilerplate/cli.py").read_text()
    assert cli.lstrip().startswith('"""')
    assert "Usage:" in cli.split('"""')[1]


def test_example_script_imports_a_module_that_exists(research_project):
    """`scripts/01-test.py` imports submodule.py; both must ship together."""
    assert (research_project / "src/python_boilerplate/submodule.py").is_file()
    script = (research_project / "scripts/01-test.py").read_text()
    assert "from python_boilerplate.submodule import" in script


def test_no_filename_lost_its_stem(research_project):
    """Catch a Jinja-conditional filename whose condition rendered falsy.

    An undefined variable in a path condition yields an empty stem, leaving a
    bare extension like `.ipynb` instead of dropping the file loudly.
    """
    lost = [
        p.relative_to(research_project)
        for p in research_project.rglob("*")
        if p.is_file() and p.name not in KNOWN_DOTFILES and BARE_EXTENSION.match(p.name)
    ]
    assert not lost, f"filenames rendered to a bare extension: {lost}"


def test_no_unrendered_jinja_in_filenames(research_project):
    leftover = [
        p.relative_to(research_project)
        for p in research_project.rglob("*")
        if "{%" in p.name or "{{" in p.name
    ]
    assert not leftover, f"unrendered Jinja in filenames: {leftover}"


def test_tests_directory_is_not_empty(research_project):
    assert list((research_project / "tests").glob("test_*.py"))


def test_research_directories_are_conditional(research_project, library_project):
    for relpath in ("data", "notebooks", "references", "reports", "scripts"):
        assert (research_project / relpath).is_dir()
        assert not (library_project / relpath).exists()


def test_project_version_answer_sets_the_package_version(template_src, tmp_path):
    """The release tooling reads the version from pyproject.toml only."""
    proj = _generate(template_src, tmp_path / "proj", project_version="1.2.3")
    assert 'version = "1.2.3"' in (proj / "pyproject.toml").read_text()
