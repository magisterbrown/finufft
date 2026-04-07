import time
import numpy as np
import pandas as pd
import finufft
import math
import argparse
import os

class Timer:
    def __init__(self):
        self.starts = []
        self.stops = []

    def start(self):
        self.starts.append(time.perf_counter())

    def stop(self):
        self.stops.append(time.perf_counter())

    def mean(self):
        return self.tot() / len(self.starts) if self.starts else 0.0

    def min(self):
        return min((stop - start) * 1000 for start, stop in zip(self.starts, self.stops)) if self.starts else 0.0

    def std(self):
        if not self.starts:
            return 0.0
        avg = self.mean()
        var = sum(((stop - start) * 1000 - avg) ** 2 for start, stop in zip(self.starts, self.stops)) / len(self.starts)
        return math.sqrt(var)

    def tot(self):
        return sum((stop - start) * 1000 for start, stop in zip(self.starts, self.stops)) if self.starts else 0.0

    def count(self):
        return len(self.starts)


def main():
    parser = argparse.ArgumentParser(description="Run Type-1 FINUFFT performance test.")
    parser.add_argument("commit_hash", help="Git commit hash for tracking")
    parser.add_argument("csv_path", help="Path to CSV file to append results")
    args = parser.parse_args()

    prec = 'f'             # 'f' for single precision, 'd' for double
    n_runs = 10            # Number of iterations
    N1 = 1e6               # Output modes (dim 1)
    N2 = 1                 # Output modes (dim 2)
    N3 = 1                 # Output modes (dim 3)
    M_points = 2e6         # Number of nonuniform points
    ntransf = 1            # Number of simultaneous transforms
    tol = 1e-5             # Tolerance
    threads = 0            # Number of threads (0 means automatic)
    sort = 1               # Sort points strategy
    upsampfact = 0         # Upsampling factor (0 defaults to optimal)
    debug = 0              # Debug output level

    M = int(M_points)
    ntransf = int(ntransf)
    
    dtype = 'float32' if prec == 'f' else 'float64'
    cdtype = 'complex64' if prec == 'f' else 'complex128'

    x = (np.random.uniform(-np.pi, np.pi, size=M)).astype(dtype)

    c = np.random.normal(size=(ntransf, M)) + 1j * np.random.normal(size=(ntransf, M))
    c = c.astype(cdtype)
    if ntransf == 1:
        c = c.reshape(-1)

    opts = {}
    if debug > 0:
        opts['debug'] = debug
    if upsampfact > 0:
        opts['upsampfac'] = upsampfact
    if sort >= 0:
        opts['spread_sort'] = sort
    if threads > 0:
        opts['nthreads'] = threads

    makeplan_timer = Timer()
    setpts_timer = Timer()
    execute_timer = Timer()
    amortized_timer = Timer()

    amortized_timer.start()

    makeplan_timer.start()
    plan = finufft.Plan(1, tuple([N1]), n_trans=ntransf, eps=tol, dtype=cdtype, **opts)
    makeplan_timer.stop()

    pts_args = [x]

    for i in range(n_runs):
        setpts_timer.start()
        plan.setpts(*pts_args)
        setpts_timer.stop()

        execute_timer.start()
        plan.execute(c)
        execute_timer.stop()

    amortized_timer.stop()

    nupts_tot = M * n_runs * ntransf

    # Collect results into a single row
    result_row = {
        'commit': args.commit_hash,
        'makeplan_mean_ms': f"{makeplan_timer.mean():.6f}",
        'set_pts_mean_ms': f"{setpts_timer.mean():.6f}",
        'execute_mean_ms': f"{execute_timer.mean():.6f}",
        'total_mean_ms': f"{amortized_timer.mean():.6f}"
    }

    df = pd.DataFrame([result_row])
    df.to_csv(args.csv_path, mode="a", header=not os.path.exists(args.csv_path), index=False)

    print(f"Results appended to {args.csv_path}")

if __name__ == "__main__":
    main()
