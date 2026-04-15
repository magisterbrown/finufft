#!/usr/bin/env python3
import argparse
import csv
import subprocess
from dataclasses import dataclass
from numbers import Number


@dataclass
class Params:
    prec: str
    N1: Number
    N2: Number
    N3: Number
    ntransf: int
    thread: int
    M: Number
    tol: float


PARAM_LIST = [
    Params("f", 1e4, 1, 1, 1, 1, 1e7, 1e-4),
    Params("d", 1e4, 1, 1, 1, 1, 1e7, 1e-9),
    Params("f", 320, 320, 1, 1, 1, 1e7, 1e-5),
    Params("d", 320, 320, 1, 1, 1, 1e7, 1e-9),
    Params("f", 320, 320, 1, 1, 0, 1e7, 1e-5),
    Params("d", 192, 192, 128, 1, 0, 1e7, 1e-7),
]

TRANSFORMS = ["3", "2", "1"]
UPSAMP = ["1.25", "2.00"]


def build_args(args: dict[str, str]) -> list[str]:
    return [f"{key}={value}" for key, value in args.items()]


def run_command(command: str, args: list[str]) -> str:
    cmd = [command] + args
    print("Running command:", " ".join(cmd))
    result = subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.stderr.strip():
        print(result.stderr)
    return result.stdout


def validate_perftest_output(output: str) -> None:
    data_lines = [line for line in output.splitlines() if line and not line.startswith("#")]
    rows = list(csv.DictReader(data_lines))
    events = {row["event"] for row in rows}
    expected = {"makeplan", "setpts", "execute", "amortized"}
    if events != expected:
        raise RuntimeError(f"unexpected events: got={sorted(events)} expected={sorted(expected)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run bench.py-style perftest parameter matrix against a perftest binary."
    )
    parser.add_argument(
        "--perftest-bin",
        default="./build/perftest/perftest",
        help="Path to perftest executable.",
    )
    parser.add_argument(
        "--n-runs",
        default="1",
        help="Value for --n_runs passed to perftest.",
    )
    args = parser.parse_args()

    perftest_args = {
        "--type": "1",
        "--prec": "f",
        "--n_runs": args.n_runs,
        "--sort": "1",
        "--N1": "320",
        "--N2": "320",
        "--N3": "1",
        "--ntransf": "1",
        "--threads": "1",
        "--M": "1E6",
        "--tol": "1E-5",
        "--upsampfact": "1.25",
        "--kerevalmethod": "1",
        "--debug": "0",
        "--bandwidth": "1.0",
    }

    run_count = 0

    for param in PARAM_LIST:
        for key, value in param.__dict__.items():
            option_key = "--threads" if key == "thread" else f"--{key}"
            perftest_args[option_key] = str(value)
        for transform in TRANSFORMS:
            perftest_args["--type"] = transform
            for upsampfac in UPSAMP:
                perftest_args["--upsampfact"] = upsampfac
                output = run_command(args.perftest_bin, build_args(perftest_args))
                validate_perftest_output(output)
                run_count += 1

    print(f"Ran {run_count} perftest invocations successfully.")


if __name__ == "__main__":
    main()
