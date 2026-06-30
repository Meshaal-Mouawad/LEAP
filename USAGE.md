# Step-by-step CLI Usage (macOS + Windows)

This guide shows exactly how to install and run the `bluebook` command-line tool on macOS and Windows. The CLI wires
directly to your pipeline and generates the HTML Bluebook.

## Prerequisites

- Python 3.10 or newer
- An OpenAI API key set as `OPENAI_API_KEY`
- This repository cloned locally

Optional but recommended:

- Sphinx for HTML docs; it’s already declared in pyproject and will install with `pip install -e .`. If `sphinx-build`
  is missing, the pipeline completes but HTML build will be skipped.

---

## macOS (Terminal)

1) Open Terminal and go to your repo folder

- `cd /Users/meshaalmouawad/AI-Powered_KPI_Extractor_Interactive_Bluebook_Generator`

2) Create and activate a virtual environment

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- Optional: `python -m pip install --upgrade pip`

3) Install the package in editable mode (exposes the `bluebook` command)

- `pip install -e .`

4) Set your OpenAI API key in your shell session

- `export OPENAI_API_KEY=sk-...`  (use your real key)

5) Verify the CLI is available

- `bluebook --help`

6) Run the generator against your source code

- For your sample: `bluebook generate ./sample_project_50`
- For a real project: `bluebook generate /path/to/your/source`
- Useful options:
    - `--clean-build` delete `docs/_build` before building
    - `--workers 8` set parallel AI workers

7) Open the generated HTML Bluebook

- `open docs/_build/index.html`

Note: If you prefer not to install the console script, you can run:

- `python -m bluebook_generator.cli generate ./sample_project_50`

---

## Windows (PowerShell)

1) Open PowerShell and go to your repo folder

- `cd C:\path\to\AI-Powered_KPI_Extractor_Interactive_Bluebook_Generator`

2) Create and activate a virtual environment

- `py -3.10 -m venv .venv`
- `.\.venv\Scripts\Activate.ps1`
- Optional: `python -m pip install --upgrade pip`

3) Install the package (exposes the `bluebook` command)

- `pip install -e .`

4) Set your OpenAI API key

- Permanent for future shells: `setx OPENAI_API_KEY "sk-..."` (then open a new PowerShell)
- Or just for this session: `$env:OPENAI_API_KEY = "sk-..."`

5) Verify the CLI is available

- `bluebook --help`

6) Run the generator against your source code

- `bluebook generate .\sample_project_50`
- Or any project folder: `bluebook generate C:\path\to\your\source`
- Options:
    - `--clean-build`
    - `--workers 8`

7) Open the generated HTML Bluebook

- `start .\docs\_build\index.html`

Alternative (without installing the console script):

- `python -m bluebook_generator.cli generate .\sample_project_50`

---

## Environment options

- Set workers via environment variable instead of the flag:
    - macOS/Linux: `export KPI_AI_WORKERS=8`
    - Windows (PowerShell): `$env:KPI_AI_WORKERS = 8`

## Common troubleshooting

- "bluebook: command not found" or "'bluebook' is not recognized":
    - Ensure your virtual environment is activated and `pip install -e .` succeeded.
    - On Windows, confirm the venv `Scripts` directory is on PATH (it is when activated).
- Missing API key or 401 errors:
    - Set `OPENAI_API_KEY` correctly in the same shell session you run the command.
- "No KPIs found" message:
    - Make sure your code has lines like `# KPI: Your KPI Name` inside a function.
- Sphinx HTML not generated:
    - If `sphinx-build` isn’t found, the CLI will say HTML was skipped. Install with `pip install sphinx` (already in
      dependencies) and re-run with `--clean-build`.
- PowerShell activation policy errors:
    - Temporarily allow scripts: `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`

## Push your changes to GitHub and create a Pull Request

If you fixed formulas locally but do not see any Pull Request in GitHub, it usually means your commit is still only on your machine (not pushed yet), or it was pushed directly to a branch without opening a PR.

### 1) Check your current branch and latest commits

- `git branch --show-current`
- `git log --oneline -n 5`

### 2) Push your branch to GitHub

- First time pushing this branch:
  - `git push -u origin <your-branch-name>`
- Next pushes on same branch:
  - `git push`

### 3) Open PR in GitHub UI

1. Go to your repository on GitHub.
2. GitHub usually shows a **Compare & pull request** banner after push — click it.
3. Set:
   - **base** = your target branch (often `main`)
   - **compare** = your feature branch (the one you pushed)
4. Click **Create pull request**.

### 4) Optional: create PR from CLI

If you use GitHub CLI:

- `gh pr create --base main --head <your-branch-name> --title "Fix KPI formula rendering" --body "Describe changes"`

### Why you may not see a PR

- You committed locally but did not run `git push`.
- You pushed to `main` directly (no PR is created automatically).
- You are viewing a different fork/org/repository than the one you pushed to.
- Your branch has no differences versus the base branch.

## Quick end-to-end test (macOS example)

- `cd /Users/meshaalmouawad/AI-Powered_KPI_Extractor_Interactive_Bluebook_Generator`
- `python3 -m venv .venv && source .venv/bin/activate`
- `pip install -e .`
- `export OPENAI_API_KEY=sk-...`
- `bluebook generate ./sample_project_50 --clean-build --workers 4`
- `open docs/_build/index.html`
