#!/bin/bash

# FlameGraph directory
FLAMEGRAPH_DIR=~/FlameGraph

# Clone FlameGraph if missing
if [ ! -d "$FLAMEGRAPH_DIR" ]; then
  echo "Cloning FlameGraph into $FLAMEGRAPH_DIR..."
  git clone https://github.com/brendangregg/FlameGraph.git "$FLAMEGRAPH_DIR"
fi

# Function to profile a Python benchmark
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

# Profile both benchmarks
profile_benchmark original_pathlib_benchmark.py
profile_benchmark optimized_pathlib_benchmark.py
