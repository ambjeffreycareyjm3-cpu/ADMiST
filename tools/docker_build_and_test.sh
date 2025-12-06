#!/bin/bash
# tools/docker_build_and_test.sh
# Comprehensive Docker build, setup, and verification script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}ℹ $1${NC}"; }
log_success() { echo -e "${GREEN}✓ $1${NC}"; }
log_error() { echo -e "${RED}✗ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

# Configuration
DOCKER_IMAGE="admst-class"
DOCKER_TAG="latest"
CONTAINER_NAME="admst-class-build-test"
BUILD_LOG="docker_build.log"
TEST_LOG="docker_test.log"

echo
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  ADMST-CLASS Docker Build & Test Automation              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo

# ==================== Step 1: Check Docker ====================
echo "Step 1: Checking Docker installation..."

if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Install from https://docs.docker.com/get-docker/"
    exit 1
fi

log_success "Docker $(docker --version | cut -d' ' -f3)"

if ! command -v docker-compose &> /dev/null; then
    log_warn "docker-compose not found, using docker compose plugin"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

log_success "Using: $DOCKER_COMPOSE"

# ==================== Step 2: Build Image ====================
echo
echo "Step 2: Building Docker image (this may take 5-10 minutes)..."

if docker build -t "$DOCKER_IMAGE:$DOCKER_TAG" -f Dockerfile . 2>&1 | tee "$BUILD_LOG"; then
    log_success "Docker image built: $DOCKER_IMAGE:$DOCKER_TAG"
    BUILD_SIZE=$(docker images "$DOCKER_IMAGE:$DOCKER_TAG" --format "{{.Size}}")
    log_info "Image size: $BUILD_SIZE"
else
    log_error "Docker build failed. See $BUILD_LOG for details."
    exit 1
fi

# ==================== Step 3: Verify Build ====================
echo
echo "Step 3: Verifying Docker image environment..."

docker run --rm "$DOCKER_IMAGE:$DOCKER_TAG" bash -c "
echo 'Checking Python environment...'
python3 --version
echo ''
echo 'Checking installed packages:'
python3 -c 'import cobaya; print(f\"  Cobaya: {cobaya.__version__}\")'
python3 -c 'from classy import Class; print(\"  CLASS: OK\")'
python3 -c 'import numpy; print(f\"  NumPy: {numpy.__version__}\")'
python3 -c 'import matplotlib; print(f\"  Matplotlib: {matplotlib.__version__}\")'
echo ''
echo 'Checking CLASS binary:'
which ./external/class/class 2>/dev/null && echo '  CLASS binary: Found' || echo '  CLASS binary: (In /workspace/external/class/)'
" 2>&1 | tee "$TEST_LOG"

log_success "Environment verification complete"

# ==================== Step 4: Test CLASS Vanilla ====================
echo
echo "Step 4: Testing vanilla CLASS (LCDM baseline)..."

docker run --rm \
    -v "$(pwd)/output:/workspace/output" \
    "$DOCKER_IMAGE:$DOCKER_TAG" \
    bash -c "
    cd /workspace
    echo 'Running LCDM baseline test...'
    ./external/class/class examples/test_lcdm.ini 2>&1 | tail -15
    if [ -f output/test_lcdm_scalCls.dat ]; then
        echo ''
        echo '✓ CLASS output generated successfully'
        ls -lh output/test_lcdm*
    else
        echo '✗ CLASS did not produce output'
        exit 1
    fi
    " 2>&1 | tee -a "$TEST_LOG"

log_success "CLASS vanilla test complete"

# ==================== Step 5: Interactive Setup ====================
echo
echo "Step 5: Setup complete!"
echo

cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║              Quick Start Commands                        ║
╚═══════════════════════════════════════════════════════════╝

1. START INTERACTIVE CONTAINER:
   docker-compose run --rm admst-class

   Or:
   docker run -it --rm -v $(pwd):/workspace admst-class bash

2. INSIDE CONTAINER, test ADMST patches:
   ./tools/build_test_admst.sh

3. RUN MCMC (requires Planck data):
   python tools/run_mcmc.py examples/cobaya_admst_planck.yaml

4. START JUPYTER NOTEBOOK:
   docker-compose up -d admst-class
   docker exec admst-class jupyter notebook --ip=0.0.0.0 --port=8888
   # Then open: http://localhost:8888

5. VIEW CONTAINER LOGS:
   docker logs admst-class-dev

6. STOP RUNNING CONTAINERS:
   docker-compose down

╔═══════════════════════════════════════════════════════════╗
║              Useful Docker Commands                      ║
╚═══════════════════════════════════════════════════════════╝

# Build and start in background
docker-compose up -d admst-class

# Open interactive shell
docker-compose exec admst-class bash

# Run a specific command
docker-compose exec admst-class ./tools/build_test_admst.sh

# View logs
docker-compose logs -f admst-class

# Clean up
docker-compose down
docker system prune -a

╔═══════════════════════════════════════════════════════════╗
║            Image Information                             ║
╚═══════════════════════════════════════════════════════════╝
EOF

docker images "$DOCKER_IMAGE:$DOCKER_TAG" --format "Image: {{.Repository}}:{{.Tag}} | Size: {{.Size}} | Created: {{.CreatedAt}}"

echo
log_success "Docker setup complete! See commands above to get started."
echo
echo "Build log: $BUILD_LOG"
echo "Test log: $TEST_LOG"
echo
