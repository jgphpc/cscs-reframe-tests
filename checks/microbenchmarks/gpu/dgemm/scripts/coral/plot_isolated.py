#!/usr/bin/env python3
"""Display CoralGemm per-GPU isolation results (ROCR_VISIBLE_DEVICES=N).

Usage:
    source 20261120_01/myvenv/bin/activate
    python3 plot_isolated.py [datadir] [pngfile]

Inputs:
    <datadir>/<node>/latest.json   ReFrame report; the test returns -1 GFLOPS
                                   for non-visible GPUs, so exactly one
                                   _gpuN_avg per testcase carries a real value.
    _gflops.csv next to <datadir>  optional fleet reference (maintenance day);
                                   per-device medians drawn as dashed lines.

Output:
    <pngfile> (default: <datadir>/isolated_packages.png) with two panels:
      left : mean isolated GFLOP/s per package for both nodes, min-max
             whiskers, deficit annotations, fleet reference lines
      right: every individual run as a jittered point (run-to-run spread)
plus a summary table on stdout.
"""

import csv
import glob
import json
import math
import os
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = {"nid002520": "tab:red", "nid002518": "tab:green"}
FALLBACK_COLORS = ["tab:red", "tab:green", "tab:blue", "tab:orange"]


def load_isolated(datadir):
    """node -> {device: [gflops per run]} from the ReFrame reports."""
    data = {}
    for path in sorted(glob.glob(os.path.join(datadir, "*", "latest.json"))):
        node = os.path.basename(os.path.dirname(path))
        with open(path) as f:
            report = json.load(f)
        for tc in report["runs"][0]["testcases"]:
            rocr = int(tc["name"].split("%rocr_visible_devices=")[1].split()[0])
            for i in range(4):
                v = tc["perfvalues"].get(f"_gpu{i}_avg")
                if v and v[0] > 0:                      # -1 = not visible
                    data.setdefault(node, {}).setdefault(rocr, []).append(v[0])
                    break
    return data


def load_fleet(path):
    """Per-device medians (GFLOP/s) of the maintenance-day mi300 fleet."""
    if not os.path.exists(path):
        return None
    devs = {d: [] for d in range(4)}
    with open(path, newline="") as f:
        for rec in csv.reader(f):
            if not rec or rec[0].lstrip().startswith("#"):
                continue
            rec = [c.strip().strip('"') for c in rec]
            if rec[0] != "gfx942" or len(rec) < 10:
                continue
            nums = []
            for c in rec[4:]:
                try:
                    nums.append(float(c))
                except ValueError:
                    pass
            if len(nums) >= 5:
                g0, g1, g2, g3 = nums[-5:-1]
                for d, v in enumerate((g0, g1, g2, g3)):
                    if v > 0:
                        devs[d].append(v)
    return [sorted(v)[len(v) // 2] for v in devs.values()]


def overall_mean(data, node):
    vals = [v for d in range(4) for v in data[node][d]]
    return sum(vals) / len(vals)


def node_label(data, node, nodes):
    """Legend label: tag the slowest and fastest node by overall mean."""
    if len(nodes) > 1 and node == nodes[0]:
        return f"{node} (slowest)"
    if len(nodes) > 1 and node == nodes[-1]:
        return f"{node} (fastest)"
    return node


def table(data):
    nodes = sorted(data, key=lambda n: overall_mean(data, n))  # slow node first
    print(f"\n{'device':>7}", end="")
    for node in nodes:
        print(f"{node + ' GF/s':>22}", end="")
    print(f"{'deficit':>9}")
    for d in range(4):
        print(f"{d:>7}", end="")
        means = []
        for node in nodes:
            xs = data[node][d]
            mean = sum(xs) / len(xs)
            means.append(mean)
            print(f"{f'{mean:8.0f} (n={len(xs)}, {min(xs):.0f}-{max(xs):.0f})':>22}",
                  end="")
        print(f"{100 * (means[0] - means[1]) / means[1]:>+8.1f}%")


def plot(data, fleet, pngfile):
    nodes = sorted(data, key=lambda n: overall_mean(data, n))  # slow node first
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6))

    # left: means with min-max whiskers + deficit labels + fleet reference
    for i, node in enumerate(nodes):
        off = (i - 0.5) * 0.36
        xs, ys, yerr = [], [], []
        for d in range(4):
            v = data[node][d]
            mean = sum(v) / len(v)
            xs.append(d + off)
            ys.append(mean)
            yerr.append([mean - min(v), max(v) - mean])
        ax1.bar(xs, ys, width=0.34, color=COLORS.get(node, FALLBACK_COLORS[i]),
                yerr=[[e[0] for e in yerr], [e[1] for e in yerr]],
                capsize=4, label=node_label(data, node, nodes))
        for x, y in zip(xs, ys):
            ax1.text(x, y + 260, f"{y:.0f}", ha="center", fontsize=8)
    if fleet:
        for d, ref in enumerate(fleet):
            ax1.plot([d - 0.42, d + 0.42], [ref, ref], "k--", lw=1,
                     label="128 nodes median (maintenance day)" if d == 0 else None)
    lo = min(min(v) for node in nodes for d in range(4) for v in [data[node][d]])
    hi = max(max(v) for node in nodes for d in range(4) for v in [data[node][d]])
    for d in range(4):
        a = sum(data[nodes[0]][d]) / len(data[nodes[0]][d])
        b = sum(data[nodes[1]][d]) / len(data[nodes[1]][d])
        top = max(a, b)
        ax1.text(d, top + (hi - lo) * 0.16, f"{100 * (a - b) / b:+.1f}%",
                 ha="center", fontsize=9, fontweight="bold")
    ax1.set_xticks(range(4))
    ax1.set_xticklabels([f"GPU {d}" for d in range(4)])
    ax1.set_ylabel("isolated GFLOP/s")
    pad = (hi - lo) * 0.25
    ax1.set_ylim(lo - pad, hi + pad * 2.2)
    ax1.legend(loc="upper left", fontsize=8)
    ax1.set_title("Mean per-device performance (min-max whiskers)")
    ax1.grid(axis="y", alpha=0.3)
    ax1.grid(axis="x", alpha=0.3)

    # right: all individual runs, jittered
    rng = random.Random(7)
    for i, node in enumerate(nodes):
        off = (i - 0.5) * 0.36
        for d in range(4):
            for v in data[node][d]:
                ax2.plot(d + off + rng.uniform(-0.07, 0.07), v, "o",
                         color=COLORS.get(node, FALLBACK_COLORS[i]),
                         markersize=5, alpha=0.75)
    ax2.set_xticks(range(4))
    ax2.set_xticklabels([f"GPU {d}" for d in range(4)])
    ax2.set_ylim(*ax1.get_ylim())
    ax2.set_title("Individual runs (repeated 6 times on each GPU)")
    handles, labels = ax1.get_legend_handles_labels()
    pairs = [(h, l) for h, l in zip(handles, labels) if "median" not in l]
    ax2.legend([h for h, _ in pairs], [l for _, l in pairs],
               loc="upper left", fontsize=8)
    ax2.grid(axis="y", alpha=0.3)
    ax2.grid(axis="x", alpha=0.3)

    fig.suptitle("MI300 CoralGemm performance (R_64F m=n=k=16000, ROCR_VISIBLE_DEVICES)", y=1.00)
    fig.tight_layout()
    fig.savefig(pngfile, dpi=150, bbox_inches="tight")
    print(f"\nwrote {pngfile}")


def main():
    datadir = sys.argv[1] if len(sys.argv) > 1 else "20261120_01"
    pngfile = (sys.argv[2] if len(sys.argv) > 2
               else os.path.join(datadir, "isolated_packages.png"))
    data = load_isolated(datadir)
    if not data:
        sys.exit(f"no latest.json reports found under {datadir}")
    fleet = load_fleet(os.path.join(os.path.dirname(datadir.rstrip("/")),
                                    "_gflops.csv"))
    table(data)
    plot(data, fleet, pngfile)


if __name__ == "__main__":
    main()
