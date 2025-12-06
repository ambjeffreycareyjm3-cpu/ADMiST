#!/bin/bash
set -e

echo "Setting up modified CLASS for ADMST..."

CLASS_REPO="https://github.com/lesgourg/class_public.git"
CLASS_DIR="external/class"
PATCH_DIR="patches"

# Clone CLASS if not exists
if [ ! -d "$CLASS_DIR" ]; then
    echo "Cloning CLASS repository..."
    mkdir -p $(dirname "$CLASS_DIR")
    git clone $CLASS_REPO $CLASS_DIR
    cd $CLASS_DIR
    git checkout v3.2.1 || true
    cd - > /dev/null
fi

# Apply patches
echo "Applying ADMST patches..."
cd $CLASS_DIR

for patch in ../../$PATCH_DIR/*.patch; do
    if [ -f "$patch" ]; then
        echo "Applying $(basename $patch)..."
        patch -p1 < "$patch" || {
            echo "Patch failed: $patch"
            exit 1
        }
    fi
done

# Build CLASS
echo "Building modified CLASS..."
make clean
make -j$(nproc)

echo "Build complete! Modified CLASS is ready in $CLASS_DIR"
