# Py(thon)-Project Template <!-- omit in toc -->

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
![build](https://github.com/markusritschel/cookiecutter-pyproject/actions/workflows/main.yml/badge.svg)
[![License MIT](https://img.shields.io/github/license/markusritschel/cookiecutter-pyproject)](./LICENSE)

> [!IMPORTANT]
> **This template has moved from Cookiecutter to [Copier](https://copier.readthedocs.io).**
> The repository keeps its name, but projects are now generated with `copier copy` (see [🚀 Get started](#-get-started)) and updated with `copier update` instead of `cruft update` ([why?](docs/tips.md#why-copier-instead-of-cookiecutter-and-cruft)).
>
> Already have a project generated with the old cookiecutter/cruft version? [`scripts/migrate_cookiecutter_to_copier.py`](scripts/migrate_cookiecutter_to_copier.py) bootstraps the `.copier-answers.yml` for you — see [Migrating an existing cookiecutter/cruft project](docs/tips.md#migrating-an-existing-cookiecuttercruft-project-to-copier) (or the [rendered version of the docs](https://markusritschel.github.io/cookiecutter-pyproject/tips/#migrating-an-existing-cookiecuttercruft-project-to-copier)).

> 👉 If you're tired of setting up the same directory and file structure for your new Python projects again and again, then this might be for you ;-)

This repository provides a "template" of a directory structure for small to medium-sized (scientific) projects, making use of [copier](https://copier.readthedocs.io), a templating engine for project structures.
Check out the links at the [bottom of the page](#sources-of-inspiration) to create your own template or use this one to start your project.
Also, feel free to fork the repository and adjust it to your own needs.

***

## <u>Table of contents</u> <!-- omit in toc -->

- [Copier as your productivity booster](#copier-as-your-productivity-booster)
- [Usage](#usage)
  - [✅ Requirements](#-requirements)
  - [🚀 Get started](#-get-started)
- [Features](#features)
  - [🔧 Tools](#-tools)
  - [🚀 Just run(s) your tasks](#-just-runs-your-tasks)
  - [📓 Documentation](#-documentation)
  - [📂 Directory structure](#-directory-structure)
- [Sources of inspiration](#sources-of-inspiration)
- [Maintainer \& Contribution](#maintainer--contribution)

***

## Copier as your productivity booster

By running *copier* with this repository, a new directory will be created with a pre-defined structure and some default files, making you all set to start a new Python project. 
No need to manually create the same files and directory structure over and over again.
This includes

- code that is importable from every place in your environment
- automatically resolved paths to the project's root and the directories for data, plots, logs, etc.
- commands to run automated unit tests, create documentation of your code, etc.
- creating a nice HTML representation of your project's documentation, including Jupyter notebooks, docstrings, etc.
- and so on... 🚀

<!-- It is indeed so easy:<br />
![copier](assets/copier.gif) -->


## Usage
### ✅ Requirements

- [uv](https://docs.astral.sh/uv/)
- [git](https://git-scm.com/)
  <details><summary>For first time use</summary>
  If you use git it for the first time on your machine, make sure to set your global configuration:

  ```text
  $ git config --global user.name "John Doe"
  $ git config --global user.email johndoe@example.com
  ```
  
  </details>
- [just](https://just.systems/) — the task runner the generated project uses.
  Install it with the toolchain you already have: `uv tool install rust-just`.
  <details><summary>Strictly optional</summary>

  Every recipe in the generated `justfile` is a thin wrapper around a `uv` command, so you can run
  those directly instead. The generated project's README lists the equivalents for the common tasks.

  </details>
- [GitHub](https://github.com/) account (optional)


### 🚀 Get started
The easiest way to get started is using [uv](https://docs.astral.sh/uv/).
Make sure you have `uv` installed, and then run the following command to create a new project from this template:
```bash
$ uvx --with jinja2-time copier copy --trust gh:markusritschel/cookiecutter-pyproject my-project
```
This creates the project in a new `my-project/` directory (replace `my-project` with the path you want).

> [!IMPORTANT]
> `--trust` is not optional. The template uses the `jinja2-time` Jinja extension (for the copyright
> year in `LICENSE` and `CITATION.cff`) and a post-generation task (`git init` + first commit,
> `uv sync --dev`, pre-commit installation). copier considers both unsafe and aborts with
> `Template uses potentially unsafe features: jinja_extensions, tasks` if the flag is missing —
> without creating anything. `copier update` needs it for the same reason.

<details>
<summary>Alternatively, without uv</summary>

install [copier](https://copier.readthedocs.io) and the `jinja2-time` extension via pip or conda, and then run the following command to create a new project from this template:
```bash
$ pip install copier jinja2-time
$ copier copy --trust gh:markusritschel/cookiecutter-pyproject my-project
```

</details><br />

<!-- Alternative URIs:
$ copier copy --trust https://github.com/markusritschel/cookiecutter-pyproject.git my-project
$ copier copy --trust git+ssh://git@github.com/markusritschel/cookiecutter-pyproject.git my-project
-->

Once you have answered the questions, your directory structure will be created and you're set, ready to start working on your new project 🚀.

> [!TIP]
> For further information, see also the README of your new project.
> You may also want to check out the justfile targets (simply type `just` in your terminal to get a command overview).
> Also see the next section


## Features

This is a boilerplate for Python projects – both for package development and (scientific) data projects.
It comes with a set of tools supportingyou r development workflow.
It also provides an optional structure for research projects (see corresponding section below and the documentation for details).


### 🔧 Tools

| Purpose               | Tool           | Comment                                                           |
| --------------------- | -------------- | ----------------------------------------------------------------- |
| Dependency management | *uv*           | A modern and blazingly fast dependency manager for Python         |
| Version control       | *Git*          | A popular version control system (VCS), automatically initialized |
| Documentation         | *Sphinx*       | A popular and versatile docs generator for Python                 |
| Code quality          | *Ruff*         | A fast linter and code formatter for Python                       |
| Testing               | *Pytest*       | A powerful testing framework for Python                           |
| Git hooks             | *pre-commit*   | Automatically enforces checks (e.g. lockfile sync) before commits |
| Task automation       | *Just*         | A modern taskrunner, simplifying your workflow                    |
| Test Github Actions   | *Act*          | A tool to run GitHub Actions locally                              |




### 🚀 Just run(s) your tasks
[just](https://just.systems/) is a modern taskrunner alternative to Make.
It can help you keep your workflow clean, simple, memorable, and reproducable.
You can add complex commands such as
```bash
python scripts/raw_data_processing.py -i data/input_data.csv --clean-data --pre-process-data -o data/output.csv
```
to your justfile
```yaml
# Process raw data
process-raw-data:
  python scripts/raw_data_processing.py -i data/input_data.csv --clean-data --pre-process-data -o data/output.csv
```
and then simply run `just process-raw-data` to execute the command.

For more available commands, simply execute `just` in your terminal in your newly created project.

👉 Check out the corresponding page in the documentation.


### 📓 Documentation
The template ships with a Sphinx-powered documentation setup.
Write your documentation in [Markdown](https://www.markdownguide.org/), paired with the flexibility and customizability of Sphinx.
For example, use reference to literature, parse your docstrings, cross-link your own and third-party API, even from within your docstrings.

👉 Check out the corresponding page in the documentation.

### 📂 Directory structure
<!-- Some tips and thoughts regarding the code layout -->
The project follows a *src* layout, which means that the package's source code resides in a subdirectory of *src*.
This follows the [Good Integration Practices from pytest.org](https://docs.pytest.org/en/6.2.x/goodpractices.html#choosing-a-test-layout-import-rules) and is a common and recommended layout for Python project;
it helps avoid issues with imports and ensures that the installed version of the package is always used during development and testing.
<!-- If the package's source code would exist in a direct subdirectory of the root directory, import statements like 
```python
import mypackage
```
would refer to the subdirectory instead of the installed version. -->

👉 Check out the corresponding page in the documentation.

<details>
  <summary>directory structure</summary>

  ```
    ├── assets             <- A place for assets like shapefiles or config files
    │
    ├── data               <- Contains all data used for the analyses in this project.
    │   │                     The sub-directories can be links to the actual location of your data.
    │   │                     However, they should never be under version control! (-> .gitignore)
    │   ├── interim        <- Intermediate data that have been transformed from the raw data
    │   ├── processed      <- The final, processed data used for the actual analyses
    │   └── raw            <- The original, immutable(!) data
    │
    ├── docs               <- The technical documentation (default engine: Sphinx; but feel free to 
    │                         use MkDocs, Jupyter-Book or anything similar).
    │                         This should contain only documentation of the code and the assets.
    │                         A report of the actual project should be placed in `reports/book`.
    │
    ├── logs               <- Storage location for the log files being generated by scripts
    │
    ├── notebooks          <- Jupyter Notebooks. Follow a naming convention, such as a number (for ordering),
    │   │                     and a short `-` or `_` delimited description, e.g. `01-initial-analyses`
    │   ├── _paired        <- Optional location for your paired Jupyter Notebook files
    │   ├── exploratory    <- Notebooks for exploratory tasks
    │   └── reports        <- Notebooks generating reports and figures
    │
    ├── references         <- Data descriptions, manuals, and all other explanatory materials
    │
    ├── reports            <- Generated reports (e.g. HTML, PDF, LaTeX, etc.)
    │   ├── figures        <- Generated graphics and figures to be used in reporting
    │   └── README.md      <- More information about Jupyter-Book and MyST-MD
    │
    ├── scripts            <- High-level scripts that use (low-level) source code from `src/`
    ├── src                <- Source code (and only source code!) for use in this project
    │   └── <package_name>
    │       ├── core       <- Provides some core functionalities
    │       ├── cli.py     <- Command-line entry point
    │       └── __init__.py  <- Provides the global path variables and utility functions
    │
    ├── tests              <- Contains the tests for the code in `src/`
    │
    ├── .env               <- In this file, specify all your custom environment variables
    │                         Keep this out of version control! (i.e. have it in your .gitignore)
    ├── .gitignore         <- Here, list all the files and folders (patterns allowed) that you want to
    │                         keep out of git version control.    
    ├── CHANGELOG.md       <- All major changes should go in there
    ├── CITATION.cff       <- The citation information for this project (update your ORCID ID!)
    ├── justfile           <- Task runner recipes; run `just` to list them
    ├── LICENSE            <- The license used for this project
    ├── pyproject.toml     <- Configuration file for the project (manages all dependencies)
    ├── README.md          <- The top-level README of this project
    ├── ruff.toml          <- Linter and formatter configuration
    └── uv.lock            <- Lock file for reproducible dependency resolution (managed by uv)
  ```

</details><br />

<u>**Further reading:**</u>
- https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure


## Sources of inspiration

Some great sources of inspiration and orientation when I created this template:

- A great article on how to structure your scientific data projects: https://drivendata.github.io/cookiecutter-data-science
- https://coderefinery.github.io/reproducible-research/
- https://github.com/drivendata/cookiecutter-data-science
- https://github.com/audreyfeldroy/cookiecutter-pypackage
- https://github.com/hackalog/easydata
- https://github.com/aubricus/cookiecutter-python-package
- Martin, R. C. (Ed.). (2009). Clean code: A handbook of agile software craftsmanship. Prentice Hall.
- Croucher, M., Graham, L., James, T., Krystalli, A., & Michonneau, F. (2019). Reproducible Code (Guides to Better Science). British Ecological Society. https://www.britishecologicalsociety.org/publications/guides-to/


## Maintainer & Contribution
[markusritschel](https://github.com/markusritschel) maintains this project. \
Issues & pull-requests accepted.


***

&copy; [Markus Ritschel](https://github.com/markusritschel) 2021–2026
