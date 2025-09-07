# Benchmarks Optimization

This repository documents the process of optimizing two distinct Python benchmarks: 
one for file system operations (`pathlib`) and another for cryptography (`crypto_pyaes`). 
The project demonstrates how to identify performance bottlenecks using profiling tools, implement targeted software optimizations, and analyze the impact of hardware on performance.

## Benchmarks

### 1. File System Operations (`pathlib`)
This benchmark evaluates the performance of file system operations using Python's `pathlib` module. It includes tasks such as file creation, iteration, and globbing, which are common in many applications.

### 2. Cryptography (`crypto_pyaes`)
This benchmark assesses the performance of cryptographic operations using the `pycryptodome` library's AES implementation. It involves encryption and decryption of data, which are critical operations in secure applications.

## Optimization Process

The optimization process for each benchmark involves the following steps:

1. **Profiling**: Use tools like `perf` and `pyperf` to gather performance data and identify bottlenecks.
2. **Analysis**: Examine the profiling data to understand where improvements can be made.
3. **Optimization**: Implement changes to the code to enhance performance.
4. **Validation**: Re-run the benchmarks to ensure that optimizations have the desired effect.

## Tools Used

- `pyperf`: A Python module for benchmarking.
- `perf`: A performance analysis tool for Linux.
- `FlameGraph`: A tool for visualizing profiling data.
- `pycryptodome`: A Python library for cryptographic operations.

## Results
### Pathlib Benchmark:

**Speedup** : ~7.8x

**Key improvements**:

Reduced Python object creation overhead
 
Fewer redundant system calls

### Crypto Benchmark:

**Speedup**: ~5.7x

**Key improvements**:

Parallelized AES encryption using multiple cores

C-based pycryptodome library instead of pure-python

Flame graphs and profiling results are included in the repository for detailed analysis.
## Usage

To run the benchmarks and generate flame graphs: 
  # Clone the repository
  git clone https://github.com/reutweizner/benchmarks_optimization.git
  cd benchmarks_optimization
  
  # Run the benchmark scripts
  python pathlib_benchmark.py
  python crypto_benchmark.py

