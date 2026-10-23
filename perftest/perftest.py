import time
import numpy as np
import pandas as pd
import finufft
import math
import argparse
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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


def make_plot(df, plot_path):

    df["run"] = np.arange(1, len(df) + 1)
    df["commit_label"] = df["commit"].astype(str).str.slice(0, 8)
    xlabels = df["commit_label"] + " (#" + df["run"].astype(str) + ")"

    plt.figure(figsize=(10, 6))
    for mean_col, std_col, label in [
        ("execute_mean_ms", "execute_std_ms", "execute"),
        ("makeplan_mean_ms", "makeplan_std_ms", "makeplan"),
        ("set_pts_mean_ms", "set_pts_std_ms", "setpts"),
    ]:
        x = df["run"]
        y = df[mean_col]
        yerr = df[std_col]
        (line,) = plt.plot(x, y, marker="o", label=label)
        mask = y.notna() & yerr.notna()
        if mask.any():
            plt.fill_between(
                x[mask],
                (y - yerr)[mask],
                (y + yerr)[mask],
                color=line.get_color(),
                alpha=0.2,
            )

    plt.xticks(df["run"], xlabels, rotation=45, ha="right")
    plt.xlabel("Commit / run")
    plt.ylabel("Mean time (ms) ± std")
    plt.title("FINUFFT perftest.py timings")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)


def main():
    parser = argparse.ArgumentParser(description="Run Type-1 FINUFFT performance test.")
    parser.add_argument("commit_hash", help="Git commit hash for tracking")
    parser.add_argument("csv_path", help="Path to CSV file to append results")
    parser.add_argument(
        "--plot_path",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "pics", "perftest_timings.png")),
        help="Path to output graph image (PNG)",
    )
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

    for i in range(n_runs):
        amortized_timer.start()

        makeplan_timer.start()
        plan = finufft.Plan(1, tuple([N1]), n_trans=ntransf, eps=tol, dtype=cdtype, **opts)
        makeplan_timer.stop()
        setpts_timer.start()
        plan.setpts(x)
        setpts_timer.stop()

        execute_timer.start()
        plan.execute(c)
        execute_timer.stop()

        amortized_timer.stop()

    # Collect results into a single row
    result_row = pd.DataFrame([{
        'commit': args.commit_hash,
        'makeplan_mean_ms': makeplan_timer.mean(),
        'set_pts_mean_ms':  setpts_timer.mean(),
        'execute_mean_ms':  execute_timer.mean(),
        'total_mean_ms':    amortized_timer.mean(),
        'makeplan_std_ms':  makeplan_timer.std(),
        'set_pts_std_ms':   setpts_timer.std(),
        'execute_std_ms':   execute_timer.std(),
        'total_std_ms':     amortized_timer.std()
    }])
    if os.path.exists(args.csv_path):
        df = pd.read_csv(args.csv_path)
        df = pd.concat([df, result_row])
    else:
        df = result_row
    df.to_csv(args.csv_path, index=False)
    make_plot(df, args.plot_path)

    print(f"Results appended to {args.csv_path}")
    print(f"Graph saved to {args.plot_path}")

if __name__ == "__main__":
    main()
