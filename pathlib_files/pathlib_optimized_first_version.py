"""
Test the performance of pathlib operations.

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
        for ext in [".py", ".txt", ".tar.gz", ""]:
            i += 1
            yield os.path.join(tmp_path, str(i) + ext)
            num_files -= 1


def setup(num_files):
    tmp_path = tempfile.mkdtemp()
    for fn in generate_filenames(tmp_path, num_files):
        with open(fn, "wb") as f:
            f.write(b'benchmark')
    return tmp_path


def bench_pathlib(loops, tmp_path):
    base_path = pathlib.Path(tmp_path)
    # Warm up the filesystem cache and keep some objects in memory.
    all_entries = list(base_path.iterdir())
    py_entries = [p for p in all_entries if p.suffix == ".py"]
    # FIXME: does this code really cache anything?
    for p in all_entries:
        p.stat()
    assert len(all_entries) == NUM_FILES, len(all_entries)

    range_it = range(loops)
    t0 = pyperf.perf_counter()


    for _ in range_it:
        # Precompute all stats once per loop
        all_stats = [p.stat() for p in all_entries]
        py_stats  = [p.stat() for p in py_entries]

        # Repeat access to simulate original 4× pattern
        for stats in [all_stats, py_stats, all_stats, py_stats]:
            for s in stats:
                _ = s.st_size  # trivial access to prevent optimization away

    return pyperf.perf_counter() - t0


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = ("Test the performance of "
                                      "pathlib operations.")

    modname = pathlib.__name__
    runner.metadata['pathlib_module'] = modname

    tmp_path = setup(NUM_FILES)
    try:
        runner.bench_time_func('pathlib', bench_pathlib, tmp_path)
    finally:
        shutil.rmtree(tmp_path)
