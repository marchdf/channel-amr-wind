# coding: utf-8
import argparse
import glob
import re

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp
import yt
from matplotlib.backends.backend_pdf import PdfPages

plt.style.use("../project.mplstyle")
## Define constants for Re_tau ~ 5200
kappa = 0.384
B = 4.27
nu = 8e-6
ut = 0.0415


def natsort(s):
    """Sorts files in a natural order, f1 < f2 < f3 ... < f22 < ... < f100"""
    return [(int(t) if t.isdigit() else t.lower()) for t in re.split(r"(\d+)", s)]


def log_law(u_tau, zf):
    return u_tau * (np.log(zf * u_tau / nu) / kappa + B)


def log_law_deriv(u_tau, zf):
    return (1 + np.log(zf * u_tau / nu)) / kappa + B


def get_utau(U, zf):
    prev, curr = 0, ut
    iters = 0
    while np.abs(curr - prev) > 1e-5 and iters < 25:
        prev = curr
        curr = curr - (log_law(prev, zf) - U) / log_law_deriv(prev, zf)
        iters += 1
    if iters == 25:
        print("ERROR in utau computation")
    return curr


def main():
    """Plot data."""
    parser = argparse.ArgumentParser(description="A simple plot tool")
    parser.add_argument(
        "-f", "--fdirs", help="Folders to plot", required=True, type=str, nargs="+"
    )
    parser.add_argument(
        "-l",
        "--labels",
        help="Labels for each case",
        type=str,
        required=False,
        nargs="+",
    )
    parser.add_argument(
        "-n",
        "--navg",
        help="Numer of plot files to average",
        default=1,
        type=int,
        required=False,
    )

    args = parser.parse_args()
    if args.labels is None:
        labels = args.fdirs
    else:
        labels = args.labels

    fname = "channel_mean.pdf"
    for i, fdir in enumerate(args.fdirs):
        plt_files = sorted(glob.glob(f"{fdir}/plt*"), key=natsort)[-args.navg :]
        n_avg = len(plt_files)
        U = 0
        for plt_file in plt_files:
            print(plt_file)
            d = yt.load(plt_file)
            data = d.all_data()
            u = data["velocityx"].reshape(d.domain_dimensions)
            U = u.mean(axis=(0, 1)) + U
        U = U / n_avg
        nz = len(U)
        z = np.linspace(0, 1, nz) + 0.5 / nz
        zplus = z * ut / nu
        tck = interp.splrep(z, U)
        dUdz = interp.splev(z, tck, 1)
        u_ll = log_law(ut, z)
        with PdfPages(fname) as pdf:
            zplus = z * ut / nu
            plt.figure("dUdy")
            plt.plot(dUdz / ut * z * kappa, zplus, label=labels[i], ls="solid")

            plt.figure("U")
            plt.semilogx(zplus, U / ut, label=labels[i], ls="solid")

            plt.figure("U_linear")
            plt.plot(U, z, label=labels[i], ls="solid")

    with PdfPages(fname) as pdf:
        zplus = z * ut / nu
        plt.figure("dUdy")
        plt.plot(np.ones_like(z), zplus, "--", label="Log law")
        plt.legend()
        plt.xlabel(r"$\frac{\mathrm{d}U^+}{\mathrm{d}z} \kappa z$")
        plt.ylabel(r"$z^+$")
        pdf.savefig()

        plt.figure("U")
        plt.semilogx(zplus, u_ll / ut, "--", label="Log law")
        plt.xlabel(r"$z^+$")
        plt.ylabel(r"$U^+$")
        plt.legend()
        pdf.savefig()

        plt.figure("U_linear")
        plt.plot(u_ll, z, "--", label="Log law")
        plt.xlabel(r"$U$")
        plt.ylabel(r"$z$")
        plt.legend()
        pdf.savefig()
    plt.close("all")


if __name__ == "__main__":
    main()
