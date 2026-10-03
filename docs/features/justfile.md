---
icon: material/console
---

# Task Automation

Similar to `Make`, [Just](https://just.systems/) simplifies the execution of common and repetitive tasks.
This means you can specify targets in your justfile to reduce regularly executed tasks with complex commands (such as building your documentation) from, for example,
```bash
uv run --group docs sphinx-build -b html docs/ docs/_build/html
``` 
to `just docs` :rocket: 

## Installing just

`just` is a single binary. The quickest route, since the generated project already requires `uv`:

```bash
uv tool install rust-just
```

Other options (Homebrew, Scoop, winget, Cargo, distro packages) are listed in the
[official documentation](https://just.systems/man/en/packages.html).

!!! tip "Not installed? You are not blocked"
    Every recipe is a thin wrapper around a `uv` command, so you can always read the `justfile` and
    run the command directly. The generated project's README lists the equivalents for the common
    tasks.

## Task overview
Run `just` in your terminal, and it will list all the recipies available for execution:

```yaml
Available recipes:
  build            # Build the project, useful for checking that packaging is correct
  clean            # Remove all build, test, coverage and Python artifacts
  clean-build      # Remove build artifacts
  clean-docs       # Remove documentation build artifacts
  clean-pyc        # Remove Python file artifacts
  clean-test       # Remove test and coverage artifacts
  clear-images     # Remove PNG files that were derived from a PDF or JPG of the same name
  convert-images   # Convert JPG and PDF figures to PNG, discarding conversions that compress badly
  coverage         # Run coverage, and build to HTML
  crop-pdf         # Crop whitespace from all PDF figures in place
  crop-png         # Crop PNG figures in place, leaving a white border
  docs             # Compile the documentation
  docs-serve       # Serve the documentation with live reload
  figures          # Regenerate all figures: clear stale PNGs, crop sources, convert, crop results
  format           # Run ruff formatter, modifying files and fixing lint errors
  lint             # Run ruff linter without modifying files
  pdb *ARGS        # Run all the tests, but on failure, drop into the debugger
  publish          # Publish to PyPI (manual alternative to GitHub Actions)
  qa               # Run all the formatting, linting, and testing commands
  release          # Create a GitHub release for the current version, triggering the PyPI upload
  set-pypi-review  # Set the user as required reviewer for the PyPI environment
  tag              # Tag the current version in git and put to github
  test *ARGS       # Run all the tests, but allow for arguments to be passed
  test-gh-actions  # Test github actions locally
  version          # Print the current version of the project
```

Some commands allow for arguments to be passed.
For the exact commands, have a look at the justfile in the project directory.

!!! note "Figure recipes"
    `clear-images`, `convert-images`, `crop-pdf`, `crop-png` and `figures` operate on
    `reports/figures/` and are therefore only generated for research projects. They shell out to
    ImageMagick, and `crop-pdf` additionally needs `pdfcrop` from TeX Live.

!!! note "`release` and `set-pypi-review`"
    `release` creates a GitHub release named after the version in `pyproject.toml`, which starts the
    [release workflow](./publish-package.md#automated-publishing). `set-pypi-review` adds you as a
    required reviewer on the repository's `pypi` environment, so the release workflow waits for your
    approval before uploading to PyPI; it only needs to be run once. Both need the
    [GitHub CLI](https://cli.github.com/); `set-pypi-review` additionally needs admin rights on the
    repository.


## Add your own tasks

You can add custom tasks to your `justfile`, simply by defining a target and the actions to execute:

```make
# Short description of my new task
my-new-task:
    echo "My new task..."
    # Add your commands
```

For more details on Just, read the [official documentation](https://just.systems/man/en/).



## Create shortcuts for complex commands

I usually structure my data-processing workflow such that I can run a single process via the command line[^CLI], for example 
```bash
python scripts/process-raw-data.py -i data/raw/input_data.csv  -o ./data/interim/ --clean-data --fill_nan
```
[^CLI]: The Python packages [Typer](https://typer.tiangolo.com/), [Click](https://click.palletsprojects.com/) and [docopt](http://docopt.org/) provide neat functionalities to convert your scripts into interactive command-line interfaces. The template can scaffold any of the three for your package — see the `command_line_interface` [prompt](../prompts.md#tool-choices).

These commands I set as targets in the justfile, for example:

```make
# Process raw data and write the newly generated data into ./data/interim/
process-raw-data:
    python scripts/process-raw-data.py -i data/raw/input_data.csv  -o ./data/interim/ --clean-data --fill_nan
```

I can now simply run `just process-raw-data` in the project's root directory.


<!-- ### Handling dependencies

Let's assume that the previous step (processing the raw data) generates new data inside `./data/interim/`. 
If now I have a second processing step that depends on the data generated by the previous step, I can set these data as dependencies for the new rule:

```make
# Process interim data
process_interim_data: $(wildcard data/interim/**/*)
    python scripts/process-interim-data.py
```

This way, the last step is only executed if the data it depends on has changed since the last time of execution.

→ This seems to be available only for Makefiles -->
