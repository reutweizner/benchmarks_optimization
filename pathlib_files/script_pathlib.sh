#!/bin/bash

# ============================================
# Run Script: Benchmarks + Profiling + FlameGraphs
# Full setup 
# ============================================

set -e

# ------------------------------

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y git python3 python3-pip linux-tools-common linux-tools-$(uname -r) build-essential

# ------------------------------

echo "Installing Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install pyperf 

# ------------------------------

FLAMEGRAPH_DIR=$HOME/FlameGraph
if [ ! -d "$FLAMEGRAPH_DIR" ]; then
    echo "Cloning FlameGraph into $FLAMEGRAPH_DIR..."
    git clone https://github.com/brendangregg/FlameGraph.git "$FLAMEGRAPH_DIR"
fi

# ------------------------------

profile_benchmark() {
    local script=$1
    local base_name=$(basename "$script" .py)

    echo "Profiling $script ..."

    # Remove old files if they exist
    [ -f "${base_name}.perf" ] && rm "${base_name}.perf"
    [ -f "${base_name}.folded" ] && rm "${base_name}.folded"
    [ -f "${base_name}.svg" ] && rm "${base_name}.svg"

    # Record perf
    perf record -F 999 -g -- python3 "$script"
    perf script > "${base_name}.perf"

    # Generate flamegraph
    $FLAMEGRAPH_DIR/stackcollapse-perf.pl "${base_name}.perf" > "${base_name}.folded"
    $FLAMEGRAPH_DIR/flamegraph.pl "${base_name}.folded" > "${base_name}.svg"

    echo "Flamegraph generated: ${base_name}.svg"
}

# ------------------------------

echo "Running pathlib benchmarks..."
profile_benchmark original_pathlib_benchmark.py
profile_benchmark optimized_pathlib_benchmark.py

echo "All benchmarks and flamegraphs completed successfully."
