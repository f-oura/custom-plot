"""Compare two semantic color sets on identical synthetic repository data.

Run from any directory with the repository's Python environment:
  python python/color_compare.py
Outputs paper/slides PDF and PNG comparisons under output/.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.colors import ListedColormap, LogNorm, TwoSlopeNorm

ROOT = Path(__file__).resolve().parents[1]
OPTIONS = json.loads((ROOT / "config/color_options.json").read_text())


def read_csv(name: str) -> np.ndarray:
    return np.loadtxt(ROOT / "data" / name, delimiter=",")


def axes_style(ax, *, title=None):
    if title:
        ax.set_title(title, pad=4)
    ax.tick_params(direction="in", top=True, right=True)


def draw_counts(fig, spec, candidate, counts, preset):
    x, observed, reference, _background, model = counts.T
    pair = GridSpecFromSubplotSpec(2, 1, subplot_spec=spec,
                                   height_ratios=(3.0, 1.0), hspace=0.17)
    top = fig.add_subplot(pair[0])
    ratio = fig.add_subplot(pair[1], sharex=top)
    colors = OPTIONS["candidates"][candidate]["conditions"]
    top.errorbar(x, observed, yerr=np.sqrt(observed), color=colors["observed"],
                 marker="o", ms=3 if preset == "paper" else 4.2, lw=1.3,
                 capsize=1.4, label="Observed (stat. $\\sqrt{N}$)", zorder=3)
    top.errorbar(x, reference, yerr=np.sqrt(reference), color=colors["reference"],
                 marker="s", ms=2.8 if preset == "paper" else 4.0, lw=1.15,
                 ls="--", capsize=1.3, label="Reference (stat. $\\sqrt{N}$)", zorder=2)
    top.plot(x, model, color=colors["model"], lw=1.8, ls=":",
             label="Fixed-shape fit", zorder=1)
    top.set(xlim=(0, 8), ylim=(0, 210), ylabel="Counts / 0.2 GeV")
    top.legend(loc="upper right", frameon=False, borderaxespad=.25,
               handlelength=1.65, labelspacing=.25)
    axes_style(top, title=f"Candidate {candidate}: {OPTIONS['candidates'][candidate]['short_name']}")
    top.tick_params(labelbottom=False)
    valid = reference > 0
    q = observed[valid] / reference[valid]
    qerr = q * np.sqrt(1 / np.maximum(observed[valid], 1) + 1 / reference[valid])
    ratio.errorbar(x[valid], q, yerr=qerr, color=colors["observed"], marker="o",
                   ms=2.6 if preset == "paper" else 3.8, lw=1.05, capsize=1.2)
    ratio.axhline(1, color="#666666", lw=.85, ls="--")
    ratio.set(xlim=(0, 8), ylim=(0, 5), xlabel="Mass [GeV]", ylabel="O / R")
    axes_style(ratio)
    ratio.yaxis.set_label_coords(-.105, .5)
    return top, ratio


def density_panel(fig, ax, X, Y, Z, cmap, norm, title, *, log=False):
    if log:
        masked = np.ma.masked_where(Z <= 0, Z)
        ax.set_facecolor("#eeeeee")
    else:
        masked = Z
    lut = OPTIONS["palettes"]["samples"][cmap]
    cmap_obj = ListedColormap(lut, name=f"{cmap}-shared-128")
    im = ax.pcolormesh(X, Y, masked, cmap=cmap_obj, norm=norm, shading="auto",
                       rasterized=False)
    cb = fig.colorbar(im, ax=ax, fraction=.047, pad=.035)
    cb.solids.set_rasterized(False)
    cb.ax.tick_params(labelsize=plt.rcParams["xtick.labelsize"])
    cb.set_label("Difference" if "difference" in title.lower() else "Counts", labelpad=2)
    ax.set(xlim=(-3.130434783, 3.130434783), ylim=(-3.130434783, 3.130434783),
           xlabel="$x$ [a.u.]", ylabel="$y$ [a.u.]")
    axes_style(ax, title=title)


def make_figure(preset: str):
    counts = read_csv("counts.csv")
    density = read_csv("density.csv")
    Xv, Yv, Z, difference = density.T
    # The checked-in grid is regular and common to every panel/backend.
    xs = np.unique(Xv)
    ys = np.unique(Yv)
    X, Y = np.meshgrid(xs, ys)
    Z = Z.reshape(len(ys), len(xs))
    difference = difference.reshape(len(ys), len(xs))
    font = 10 if preset == "paper" else 15
    plt.style.use(str(ROOT / "styles" / f"classic-{preset}.mplstyle"))
    plt.rcParams.update({"font.size": font, "axes.labelsize": font,
                         "axes.titlesize": font, "xtick.labelsize": font * .85,
                         "ytick.labelsize": font * .85,
                         "legend.fontsize": font * .79,
                         "pdf.fonttype": 42, "ps.fonttype": 42,
                         "font.family": "DejaVu Serif"})
    figsize = (12, 10) if preset == "paper" else (16, 13)
    fig = plt.figure(figsize=figsize)
    outer = GridSpec(4, 4, figure=fig, height_ratios=(1.48, 1.0, 1.0, .24),
                     hspace=.42, wspace=.42)
    fig.subplots_adjust(left=.075, right=.94, bottom=.075, top=.93)
    fig.suptitle(f"Classic layout | color comparison 1 vs 4 | {preset} | SYNTHETIC",
                 fontsize=font * 1.2, fontweight="bold")
    left = GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[0, :2])
    right = GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[0, 2:])
    draw_counts(fig, left[0], "1", counts, preset)
    draw_counts(fig, right[0], "4", counts, preset)

    density_maps = ["viridis", "Blues", "YlGnBu"]
    for row, is_log in ((1, False), (2, True)):
        for col, cmap in enumerate(density_maps):
            ax = fig.add_subplot(outer[row, col])
            norm = LogNorm(vmin=1, vmax=60) if is_log else mcolors.Normalize(vmin=0, vmax=60)
            title = f"{cmap} | {'log 1–60' if is_log else 'linear 0–60'}"
            density_panel(fig, ax, X, Y, Z, cmap, norm, title, log=is_log)
            if col>0: ax.set_ylabel("")
        if not is_log:
            ax = fig.add_subplot(outer[row, 3])
            norm = TwoSlopeNorm(vmin=-30, vcenter=0, vmax=30)
            density_panel(fig, ax, X, Y, difference,
                          OPTIONS["palettes"]["signed_difference"], norm,
                          "Shared difference | 0 centered")
            ax.set_ylabel("")
        else:
            ax = fig.add_subplot(outer[row, 3])
            ax.axis("off")
            ax.text(.02, .96, "READING GUIDE", transform=ax.transAxes,
                    va="top", fontweight="bold", fontsize=font * .78)
            guide = ("1 · blue / orange / teal\n"
                     "    magenta is reserved auxiliary\n\n"
                     "4 · black / blue / vermilion\n"
                     "    three semantic colors only\n\n"
                     "Log maps mask 261 zero bins (gray).\n"
                     "Zero and negative values are not clipped.")
            ax.text(.02, .83, guide, transform=ax.transAxes, va="top",
                    fontsize=font * .68, linespacing=1.35)

    foot = fig.add_subplot(outer[3, :])
    foot.axis("off")
    foot.text(.5, .5,
              "SYNTHETIC repository demonstration · same CSV, axes, units, bins and normalization · "
              "statistical errors only · fixed-shape example fit · 261 zeros masked in log views\n"
              "Linear density: 0–60 · log density: 1–60 · signed difference: −30 to +30, centered at 0",
              transform=foot.transAxes, ha="center", va="center", fontsize=font * .77)
    fig.savefig(ROOT / "output" / f"color-mpl-{preset}.png", dpi=180)
    fig.savefig(ROOT / "output" / f"color-mpl-{preset}.pdf")
    plt.close(fig)


def export_color_header():
    """Regenerate the ROOT interface from the same JSON used by ListedColormap."""
    rows = []
    for key in ("1", "4"):
        colors = OPTIONS["candidates"][key]["conditions"]
        rows.append([mcolors.to_rgb(colors[name]) for name in ("observed", "reference", "model")])
    fmt = lambda row: "{" + ", ".join(format(float(x), ".17g") for x in row) + "}"
    lines = ["// Generated from config/color_options.json; run python/color_compare.py.",
             "#pragma once", "struct ColorRGB { double r, g, b; };",
             "static const ColorRGB optColors[2][3] = {"]
    lines += ["  {" + ", ".join(fmt(row) for row in group) + "}," for group in rows]
    lines += ["};", "static const ColorRGB reservedAuxiliary1 = " +
              fmt(mcolors.to_rgb(OPTIONS["candidates"]["1"]["reserved_auxiliary"])) + ";"]
    for name, lut in OPTIONS["palettes"]["samples"].items():
        assert np.asarray(lut).shape == (128, 3)
        lines += [f"static const double cmap_{name}[128][3] = {{"]
        lines += ["  " + fmt(row) + "," for row in lut]
        lines += ["};"]
    (ROOT / "root/color_options.h").write_text("\n".join(lines) + "\n")


def main():
    export_color_header()
    for preset in ("paper", "slides"):
        make_figure(preset)
        print(f"wrote output/color-mpl-{preset}.pdf and .png")
    zero_count = int(np.count_nonzero(read_csv("density.csv")[:, 2] == 0))
    print(f"density zero cells explicitly masked in log panels: {zero_count}")


if __name__ == "__main__":
    main()
