# Docker Quickstart Guide for ADMST-CLASS

This guide helps you get ADMST-CLASS running in a reproducible Docker container.

## Why Docker?

- **Reproducibility:** Works identically on any machine (Linux, macOS, Windows)
- **Isolation:** No conflicts with system libraries
- **Portability:** Share environment with collaborators
- **Consistency:** Same environment for CI/CD and local development

## Prerequisites

1. **Install Docker:**
   - Linux: https://docs.docker.com/engine/install/
   - macOS: https://docs.docker.com/desktop/install/mac-install/
   - Windows: https://docs.docker.com/desktop/install/windows-install/

2. **Install docker-compose (optional, but recommended):**
   - Usually included with Docker Desktop
   - Or: `pip install docker-compose`

3. **Check installation:**
   ```bash
   docker --version
   docker-compose --version  # or: docker compose version
   ```

## Option 1: Automated Setup (Recommended)

```bash
cd /path/to/ADMST
chmod +x tools/docker_build_and_test.sh
./tools/docker_build_and_test.sh
```

This script will:
1. Build the Docker image (~2-5 GB, takes 5-10 minutes)
2. Verify all dependencies
3. Test vanilla CLASS (LCDM baseline)
4. Show you quick-start commands

## Option 2: Manual Docker Compose

```bash
# Build the image
docker-compose build

# Start the container in the background
docker-compose up -d admst-class

# Enter the container
docker-compose exec admst-class bash

# Inside the container:
cd /workspace
./tools/build_test_admst.sh  # Test ADMST patches
```

## Option 3: Direct Docker

```bash
# Build
docker build -t admst-class .

# Run interactively
docker run -it \
  -v $(pwd):/workspace \
  -p 8888:8888 \
  admst-class \
  bash
```

## Common Workflows

### Test ADMST with patches

```bash
docker-compose run --rm admst-class \
  ./tools/build_test_admst.sh
```

### Run MCMC calculation

```bash
docker-compose exec admst-class \
  python tools/run_mcmc.py examples/cobaya_admst_planck.yaml
```

### Start Jupyter notebook

```bash
# In one terminal, start container
docker-compose up -d admst-class

# In another terminal, start Jupyter
docker-compose exec -d admst-class \
  jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

# View logs to get the token
docker-compose logs admst-class | grep token

# Open http://localhost:8888 and enter the token
```

### Access files from container

```bash
# Container volumes are mounted to your local directory:
# - /workspace/output → ./output
# - /workspace/chains → ./chains
# - /workspace/data → ./data

# Example: check output files
ls -la ./output/
```

### Run a Python script

```bash
docker-compose exec admst-class \
  python3 -c "from admst import cosmo; print(cosmo.__version__)"
```

## Troubleshooting

### Docker daemon not running

**Error:** `Cannot connect to Docker daemon`

**Solution:**
- Linux: `sudo systemctl start docker`
- macOS/Windows: Open Docker Desktop application

### Permission denied

**Error:** `docker: permission denied`

**Solution (Linux):**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Not enough disk space

**Error:** `No space left on device`

**Solution:**
```bash
# Clean up unused Docker resources
docker system prune -a

# Or remove specific image
docker rmi admst-class:latest
```

### Slow build

**Tip:** Docker caches layers. Rebuild is faster if nothing changes. To force rebuild:
```bash
docker-compose build --no-cache
```

### CLASS patches don't apply

Expected behavior—patches are for v3.2.1. If they fail:
1. The script will warn you
2. Manual edits needed (see CLASS_INTEGRATION_README.md)
3. Docker has vanilla CLASS already built (ready to use)

## Image Contents

The Docker image includes:

```
Ubuntu 22.04
├── Build tools (gcc, gfortran, make)
├── Python 3.10
│   ├── NumPy, SciPy, Matplotlib
│   ├── Jupyter
│   ├── Cobaya 3.3.1
│   └── GetDist (chain analysis)
├── CLASS v3.2.1
│   ├── Compiled binary (/workspace/external/class/class)
│   └── classy Python interface
└── /workspace
    ├── admst/          (Python package)
    ├── tools/          (build/test scripts)
    ├── patches/        (physics modifications)
    ├── examples/       (configuration files)
    ├── output/         (CLASS outputs)
    ├── chains/         (MCMC results)
    └── data/           (likelihood data)
```

## Advanced: Multi-stage builds

For production, you can create separate build/test images:

```dockerfile
# Build stage
FROM ubuntu:22.04 AS builder
RUN ... # install build deps
RUN ... # compile CLASS

# Runtime stage
FROM ubuntu:22.04
COPY --from=builder /workspace /workspace
```

This reduces final image size. Contact if needed.

## Cleanup

```bash
# Stop running containers
docker-compose down

# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Full cleanup (warning: removes all unused Docker data)
docker system prune -a
```

## Next Steps

1. **Build the image:**
   ```bash
   ./tools/docker_build_and_test.sh
   ```

2. **Test ADMST patches:**
   ```bash
   docker-compose run --rm admst-class ./tools/build_test_admst.sh
   ```

3. **Prepare Planck data** (if you have it):
   ```bash
   # Download or copy Planck 2018 likelihood files to ./data/
   cp -r /path/to/planck ./data/
   ```

4. **Run MCMC:**
   ```bash
   docker-compose exec admst-class python tools/run_mcmc.py examples/cobaya_admst_planck.yaml
   ```

## Support

- Docker: https://docs.docker.com/
- CLASS: http://class-code.net/
- Cobaya: https://cobaya.readthedocs.io/
