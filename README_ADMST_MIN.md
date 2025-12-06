# ADMST Minimal Scaffold

This scaffold provides a compact, runnable subset of the ADMST-SCBC cosmology
code so you can verify basic calculations quickly in the dev container.

Files added:
- `admst/cosmo_min.py` : minimal cosmology implementation
- `admst/__init__.py` : package init
- `run_analysis.py` : runner script that saves plots
- `requirements.txt` : minimal Python dependencies

Quick start (in workspace root):
```bash
python3 -m pip install --user -r requirements.txt
python3 run_analysis.py
```
The script saves `ADMST_predictions_min.png` in the workspace root.

This scaffold is intentionally small; if you want I can:
- add a fuller `cosmo.py` that mirrors your full module
- scaffold a GitHub repository layout with CI and tests
- integrate a modified CLASS backend (more involved)
