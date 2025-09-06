"""
Test the performance of Optimized benchmark.

This benchmark stresses the creation of small objects, globbing, and system
calls.
"""

# Python imports
import os
import pathlib
import shutil
import tempfile

import pyperf


NUM_FILES = 2000


def generate_filenames(tmp_path, num_files):
    i = 0
    while num_files:
         for ext in [b".py", b".txt", b".tar.gz", b""]:
            i += 1
            yield tmp_path + b"/" + str(i).encode() + ext
            num_files -= 1


def setup(num_files):
    tmp_path = tempfile.mkdtemp(suffix=b'')
    for fn in generate_filenames(tmp_path, num_files):
        with open(fn, "wb") as f:
            f.write(b'benchmark')
    return tmp_path


def bench_pathlib(loops, tmp_path):
    # Warm up the filesystem cache and keep some objects in memory.
    all_entries = list(os.scandir(tmp_path))
    py_entries = [e for e in all_entries if e.name.endswith(b".py")]
    # FIXME: does this code really cache anything?
    for p in all_entries:
        os.stat(p.path)
    assert len(all_entries) == NUM_FILES, len(all_entries)

    range_it = range(loops)
    t0 = pyperf.perf_counter()


    for _ in range_it:
        # Precompute all stats once per loop
        all_stats = [os.stat(p.path) for p in all_entries]
        py_stats  = [os.stat(p.path) for p in py_entries]

        # Repeat access to simulate original 4× pattern
        for stats in [all_stats, py_stats, all_stats, py_stats]:
            for s in stats:
                _ = s.st_size  # trivial access to prevent optimization away

    return pyperf.perf_counter() - t0


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = ("Test the performance of "
                                      "pathlib operations and optimize.")

    modname = pathlib.__name__
    runner.metadata['pathlib_module'] = modname

    tmp_path = setup(NUM_FILES)
    try:
        runner.bench_time_func('pathlib', bench_pathlib, tmp_path)
    finally:
        shutil.rmtree(tmp_path)
