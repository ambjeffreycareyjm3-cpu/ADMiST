#!/usr/bin/env python3
"""
Run MCMC for ADMST with Planck likelihoods (wrapper around Cobaya)

This script is a thin helper that calls Cobaya with the example YAML.
It expects `cobaya` to be installed in the environment where it's run and
Planck likelihood files to be available if you enable them.
"""
import sys
import os

def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else "examples/cobaya_admst_planck.yaml"
    print(f"Running ADMST MCMC with config: {config_file}")
    try:
        from cobaya.run import run
    except Exception as e:
        print("Cobaya not available in this environment. Install via `pip install cobaya`.")
        raise

    updated_info, sampler = run(config_file, output=True)
    print("Cobaya run finished.")
    if sampler is None:
        print("No sampler object returned. Check Cobaya output and config.")
        return 1
    print("Sampler completed; output at:", updated_info.get('output', 'unknown'))
    return 0

if __name__ == '__main__':
    sys.exit(main())
