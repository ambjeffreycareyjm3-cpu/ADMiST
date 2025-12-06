# Contributing

Thanks for contributing to the ADMiST project. This file explains the minimal
developer setup so your commits and PRs pass the project's CI checks.

Local setup (one-time per clone)
```bash
# 1) (optional) enable repository-shipped Git hooks
git config core.hooksPath .githooks

# 2) Install developer dependencies (you may prefer a venv)
python3 -m pip install --user -r requirements-dev.txt

# 3) Install pre-commit hooks (recommended)
pre-commit install

# 4) (optional) run all pre-commit hooks against the repo
pre-commit run --all-files

# 5) Run tests
pytest -q
```

Quick checks you can run manually
- Deprecated NumPy API checker:
  ```bash
  python3 tools/check_deprecated_numpy.py
  ```
- Run the minimal ADMST analysis and generate plots:
  ```bash
  python3 run_analysis.py
  ```

Pre-submit checklist
- Run `pre-commit run --all-files` and fix any failures.
- Run `pytest` and ensure tests pass.
- Keep commits small and focused; open a pull request against `main`.

CI
- GitHub Actions runs the deprecated-NumPy checker, pre-commit hooks, and the
  test suite on every push and PR.

Questions
- If you have any trouble with the developer setup, open an issue or contact
  the repository maintainers.
