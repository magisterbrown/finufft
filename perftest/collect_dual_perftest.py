import argparse
import subprocess
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Params:
    prec: str = "f"
    N1: Number = 320
    N2: Number = 320
    N3: Number = 1
    ntransf: int = 1
    threads: int = 1
    M: Number = 1e6
    tol: float = 1e-5

    def ndim(self) -> int:
        if self.N3 > 1:
            return 3
        if self.N2 > 1:
            return 2
        return 1

    def args(self) -> list[str]:
        return [f"{f.name}={getattr(self, f.name)}" for f in fields(self)]

    def pretty_string(self) -> str:
        return ", ".join(f"{f.name}={getattr(self, f.name)}" for f in fields(self))


NRUNS = 10

PARAM_LIST = [
    Params("f", 1e4, 1, 1, 1, 1, 1e7, 1e-4),
    # Params("d", 1e4, 1, 1, 1, 1, 1e7, 1e-9),
    # Params("f", 320, 320, 1, 1, 1, 1e7, 1e-5),
    # Params("d", 320, 320, 1, 1, 1, 1e7, 1e-9),
    # Params("f", 320, 320, 1, 1, 0, 1e7, 1e-5),
    # Params("d", 192, 192, 128, 1, 0, 1e7, 1e-7),
]

# TRANSFORMS = [3, 2, 1]
TRANSFORMS = [1]


DEFAULT_EXTRA_ARGS = [
    f"n_runs={NRUNS}",
    "sort=1",
    "upsampfact=0",
    "kerevalmethod=1",
    "debug=0",
    "bandwidth=1.0",
]


def run_one_perftest(binary_path: str) -> str:
    res = ""
    for param in PARAM_LIST:
        for transform in TRANSFORMS:
            result = subprocess.run(
                [binary_path]
                + param.args()
                + DEFAULT_EXTRA_ARGS
                + [f"type={transform}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            test_res = pd.read_csv(
                io.StringIO(
                    "\n".join(
                        [
                            line
                            for line in result.stdout.splitlines()
                            if not line.startswith("#")
                        ]
                    )
                ),
                sep=",",
            )
            res = f"{res}\n{test_res.to_string(index=False)}"
    return res


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--master-perftest", default="../builds/master/perftest/perftest"
    )
    parser.add_argument("--pr-perftest", default="../builds/pr-head/perftest/perftest")
    args = parser.parse_args()

    perftest_summary = (
        run_one_perftest(args.master_perftest)
        + "\n"
        + run_one_perftest(args.pr_perftest)
    )

    timestamp = datetime.now().strftime("%a %d %b %Y %H:%M:%S %Z")
    body = "<!-- pr-managed-comment -->\\n"
    body += f"Time now: {timestamp}\\n"
    body += "Perftest runs:\\n"
    for line in perftest_summary:
        body += f"- {line}\\n"
    print(f"body={body}")


if __name__ == "__main__":
    main()
