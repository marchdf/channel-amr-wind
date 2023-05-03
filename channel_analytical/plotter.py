"""Plotting script."""

import argparse
import pathlib

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

plt.style.use("../project.mplstyle")
plt.rcParams.update({"figure.max_open_warning": 0})


def main():
    """Plot data."""
    parser = argparse.ArgumentParser(description="A simple plot tool")
    parser.add_argument(
        "-f", "--fdirs", help="Folders to plot", required=True, type=str, nargs="+"
    )
    args = parser.parse_args()

    lst = []
    for fdir in args.fdirs:
        fname = pathlib.Path(fdir) / "channel_flow.log"
        df = pd.read_csv(fname, delim_whitespace=True)
        lst.append({"n": int(fdir), "ue": df.L2_u.iloc[-1]})

        plt.figure("u")
        plt.plot(df.time, df.L2_u, label=f"$n={fdir}$")

    df = pd.DataFrame(lst)
    theory_order = 2
    idx = 1
    df["theory"] = df["ue"].iloc[idx] * (df["n"].iloc[idx] / df["n"]) ** theory_order
    plt.figure("ue")
    plt.loglog(df.n, df.ue, marker="s", ms=10, label="AMR-Wind")
    plt.loglog(df.n, df.theory, color="black", label="2nd order")

    fname = "plots.pdf"
    with PdfPages(fname) as pdf:
        plt.figure("u")
        plt.xlabel(r"$t$")
        plt.ylabel(r"$L_2(u)$")
        plt.gca().legend()
        pdf.savefig()

        plt.figure("ue")
        plt.xlabel(r"$n$")
        plt.ylabel(r"$L_2(u)$")
        plt.gca().legend()
        pdf.savefig()


if __name__ == "__main__":
    main()
