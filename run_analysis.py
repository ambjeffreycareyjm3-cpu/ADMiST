"""Quick runner for ADMST minimal scaffold

Usage:
    python3 run_analysis.py

This script runs the compact ADMST calculations and saves a PNG with
predictions into the repository root.
"""
import sys

from admst import SCBCCosmology


def main():
    cosmo = SCBCCosmology()
    out = cosmo.plot_predictions(out_png="ADMST_predictions_min.png")
    print(f"Saved minimal ADMST predictions to: {out}")


if __name__ == "__main__":
    main()
