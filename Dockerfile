FROM ubuntu:22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    gfortran \
    git \
    wget \
    curl \
    python3 \
    python3-pip \
    python3-dev \
    libopenmpi-dev \
    libfftw3-dev \
    libgsl-dev \
    libhdf5-dev \
    libblas-dev \
    liblapack-dev \
    pkg-config \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install Python packages
RUN pip3 install \
    numpy \
    scipy \
    matplotlib \
    jupyter \
    ipython \
    getdist \
    cython \
    mpi4py \
    pyyaml

# Install specific Cobaya version
RUN pip3 install cobaya==3.3.1

# Create workspace directory structure
WORKDIR /workspace
RUN mkdir -p /workspace/{tools,patches,examples,output,chains,data,external}

# Clone and build CLASS v3.2.1 (vanilla baseline)
RUN git clone https://github.com/lesgourg/class_public.git /workspace/external/class && \
    cd /workspace/external/class && \
    git checkout v3.2.1 && \
    echo "Building vanilla CLASS..." && \
    make -j4 2>&1 | tail -10

# Install classy Python interface
RUN cd /workspace/external/class && \
    pip3 install . --upgrade 2>&1 | grep -E "Successfully|Requirement"

# Verify installations
RUN python3 -c "import cobaya; print('✓ Cobaya', cobaya.__version__)" && \
    python3 -c "from classy import Class; print('✓ CLASS/classy ready')" && \
    python3 -c "import numpy; import scipy; print('✓ NumPy/SciPy ready')"

# Copy ADMST code and tools from host
COPY admst /workspace/admst
COPY tools /workspace/tools
COPY patches /workspace/patches
COPY examples /workspace/examples
COPY requirements.txt /workspace/requirements.txt 2>/dev/null || echo "No requirements.txt"
COPY requirements-dev.txt /workspace/requirements-dev.txt 2>/dev/null || echo "No requirements-dev.txt"

# Install ADMST package in editable mode
RUN cd /workspace && pip3 install -e . 2>/dev/null || echo "setup.py not found, skipping"

# Make scripts executable
RUN chmod +x /workspace/tools/*.sh 2>/dev/null || true && \
    chmod +x /workspace/tools/*.py 2>/dev/null || true

# Create startup/info script
RUN cat > /workspace/docker_info.sh << 'EOF'
#!/bin/bash
cat << 'BANNER'
╔═══════════════════════════════════════════════════════════╗
║     ADMST-CLASS Docker Environment (v3.2.1)              ║
║     Reproducible Cosmological Simulations                ║
╚═══════════════════════════════════════════════════════════╝

ENVIRONMENT:
  • Ubuntu 22.04 base
  • CLASS v3.2.1 (built and ready)
  • Cobaya 3.3.1 (MCMC framework)
  • Python 3.10 + NumPy/SciPy/Matplotlib

QUICK START:
  1. Test ΛCDM baseline:
     ./external/class/class examples/test_lcdm.ini

  2. Build and test ADMST patches:
     ./tools/build_test_admst.sh

  3. Run MCMC with minimal parameters:
     python tools/run_mcmc.py examples/cobaya_admst_planck.yaml

  4. Start Jupyter notebook:
     jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

DIRECTORY STRUCTURE:
  /workspace/
  ├── admst/                 # ADMST Python package
  ├── external/class         # CLASS source + build
  ├── tools/                 # Build/test/MCMC scripts
  ├── patches/               # Physics modification patches
  ├── examples/              # Configuration files
  ├── output/                # CLASS calculation outputs
  ├── chains/                # MCMC chain results
  └── data/                  # Likelihood data (Planck, etc.)

USEFUL COMMANDS:
  bash /workspace/docker_info.sh          # Show this message
  cd /workspace && ./tools/build_test_admst.sh  # Full workflow
  python3 -c "from classy import Class; print('OK')"

JUPYTER ACCESS:
  http://localhost:8888 (token-based, see container logs)

For detailed info:
  • CLASS: http://class-code.net
  • Cobaya: https://cobaya.readthedocs.io
  • ADMST patches: see CLASS_INTEGRATION_README.md

BANNER
EOF
chmod +x /workspace/docker_info.sh

# Set container entrypoint
ENTRYPOINT ["/workspace/docker_info.sh"]
CMD ["/bin/bash"]
