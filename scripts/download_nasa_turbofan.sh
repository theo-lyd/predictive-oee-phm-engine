#!/bin/bash
# Download NASA Turbofan Failure Data from Kaggle and unzip to data/raw/sensors/

set -e

DATASET="bishals098/nasa-turbofan-engine-degradation-simulation"
TARGET_DIR="data/raw/sensors"

mkdir -p "$TARGET_DIR"

# Download all files from the dataset
kaggle datasets download -d "$DATASET" -p "$TARGET_DIR" --unzip

echo "NASA Turbofan Failure Data downloaded and extracted to $TARGET_DIR"
