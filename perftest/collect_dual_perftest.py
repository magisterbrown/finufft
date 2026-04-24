#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, fields
from numbers import Number
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

    def args(self) -> list[str]:
        return [f"{f.name}={getattr(self, f.name)}" for f in fields(self)]

    def pretty_string(self) -> str:
        return ", ".join(f"{f.name}={getattr(self, f.name)}" for f in fields(self))

    def get_hash(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True)
        return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


NRUNS = 10

PARAM_LIST = [
    Params("f", 1e4, 1, 1, 1, 1, 1e7, 1e-4),
    Params("d", 1e4, 1, 1, 1, 1, 1e7, 1e-9),
    Params("f", 320, 320, 1, 1, 1, 1e7, 1e-5),
    Params("d", 320, 320, 1, 1, 1, 1e7, 1e-9),
    Params("f", 320, 320, 1, 1, 0, 1e7, 1e-5),
    Params("d", 192, 192, 128, 1, 0, 1e7, 1e-7),
]

TRANSFORMS = [3, 2, 1]
DEFAULT_EXTRA_ARGS = [
    f"n_runs={NRUNS}",
    "sort=1",
    "upsampfact=0",
    "kerevalmethod=1",
    "debug=0",
    "bandwidth=1.0",
]


def build_comment_body(
    all_rows: list[dict[str, str | Number]], failures: list[str]
) -> str:
    rows_by_tag: dict[str, int] = {}
    for row in all_rows:
        tag = str(row["tag"])
        rows_by_tag[tag] = rows_by_tag.get(tag, 0) + 1

    lines = ["<!-- pr-managed-comment -->", "### Dual perftest summary", ""]
    lines.append(f"Total benchmark rows: {len(all_rows)}")
    lines.append("")
    lines.append("| tag | rows | status |")
    lines.append("| --- | ---: | --- |")
    for tag in ["master", "pr-head"]:
        ok = rows_by_tag.get(tag, 0) > 0
        lines.append(
            f"| {tag} | {rows_by_tag.get(tag, 0)} | {'ok' if ok else 'failed'} |"
        )

    if failures:
        lines.append("")
        lines.append("#### Failures")
        for failure in failures:
            lines.append(f"- {failure}")

    return "\n".join(lines) + "\n"


def run_command(command: str, args: list[str], cwd: Path | None = None) -> str:
    cmd = [command] + args
    print("Running command:", " ".join(cmd), file=sys.stderr)
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.stderr.strip():
        print(result.stderr, file=sys.stderr)
    return result.stdout


def configure_and_build(source_dir: Path, build_dir: Path, jobs: int) -> None:
    build_dir.mkdir(parents=True, exist_ok=True)
    run_command(
        "cmake",
        ["-S", str(source_dir), "-B", str(build_dir), "-DFINUFFT_BUILD_TESTS=ON"],
    )
    run_command(
        "cmake",
        ["--build", str(build_dir), "--target", "perftest", "-j", str(jobs)],
    )


def resolve_perftest_bin(build_dir: Path) -> Path | None:
    candidates = [
        build_dir / "perftest" / "perftest",
        build_dir / "perftest",
    ]
    for candidate in candidates:
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate
    return None


def parse_perftest_output(output: str) -> dict[str, dict[str, str]]:
    filtered_lines = [line for line in output.splitlines() if not line.startswith("#")]
    reader = csv.DictReader(io.StringIO("\n".join(filtered_lines)))
    rows: dict[str, dict[str, str]] = {}
    for row in reader:
        event = row.get("event")
        if event:
            rows[event] = row
    return rows


def run_benchmarks_for_bin(
    perftest_bin: Path, tag: str
) -> list[dict[str, str | Number]]:
    collected_rows: list[dict[str, str | Number]] = []
    run_count = 0

    for param in PARAM_LIST:
        param_id = param.get_hash()
        param_label = param.pretty_string()
        for transform in TRANSFORMS:
            perftest_args = param.args() + DEFAULT_EXTRA_ARGS + [f"type={transform}"]
            output = run_command(str(perftest_bin), perftest_args)
            test_res = parse_perftest_output(output)
            required_events = ["makeplan", "setpts", "execute"]
            missing_events = [
                event for event in required_events if event not in test_res
            ]
            if missing_events:
                raise RuntimeError(
                    f"{perftest_bin} did not report {', '.join(missing_events)}"
                )

            collected_rows.append(
                {
                    "tag": tag,
                    "params_hash": param_id,
                    "params": param_label,
                    "transform": transform,
                    "makeplan_mean(ms)": float(test_res["makeplan"]["mean(ms)"]),
                    "makeplan_std(ms)": float(test_res["makeplan"]["std(ms)"]),
                    "setpts_mean(ms)": float(test_res["setpts"]["mean(ms)"]),
                    "setpts_std(ms)": float(test_res["setpts"]["std(ms)"]),
                    "execute_mean(ms)": float(test_res["execute"]["mean(ms)"]),
                    "execute_std(ms)": float(test_res["execute"]["std(ms)"]),
                }
            )
            run_count += 1

    print(f"Ran {run_count} perftest invocations successfully for {tag}.")
    return collected_rows


def collect_two_perftests(
    master_source: Path,
    pr_source: Path,
    builds_root: Path,
    jobs: int,
) -> str:
    specs = [("master", master_source), ("pr-head", pr_source)]
    all_rows: list[dict[str, str | Number]] = []
    failures: list[str] = []

    for tag, source_dir in specs:
        build_dir = builds_root / tag
        try:
            configure_and_build(source_dir, build_dir, jobs)
            perftest_bin = resolve_perftest_bin(build_dir)
            if perftest_bin is None:
                raise RuntimeError(f"could not find executable perftest in {build_dir}")
            tag_rows = run_benchmarks_for_bin(perftest_bin, tag)
            all_rows.extend(tag_rows)
        except Exception as exc:
            failures.append(f"{tag}: {exc}")
            print(f"Failed to collect {tag}: {exc}", file=sys.stderr)

    comment_body = build_comment_body(all_rows, failures)

    if failures:
        print(comment_body)
        raise RuntimeError("; ".join(failures))

    if not all_rows:
        print(comment_body)
        raise RuntimeError("No benchmark data collected from either perftest")

    return comment_body


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build, run, and collect benchmark results from master and PR head."
    )
    parser.add_argument(
        "--master-source", required=True, help="Path to the master worktree."
    )
    parser.add_argument(
        "--pr-source", required=True, help="Path to the PR head worktree."
    )
    parser.add_argument(
        "--builds-root",
        default="../builds",
        help="Directory where the two build trees will be created.",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=max(1, os.cpu_count() or 1),
        help="Parallel build jobs to pass to cmake --build.",
    )
    args = parser.parse_args()

    comment_body = collect_two_perftests(
        master_source=Path(args.master_source),
        pr_source=Path(args.pr_source),
        builds_root=Path(args.builds_root),
        jobs=args.jobs,
    )
    print(comment_body)


if __name__ == "__main__":
    main()
