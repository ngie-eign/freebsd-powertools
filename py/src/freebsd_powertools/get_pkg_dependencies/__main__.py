"""Calculate the reverse dependencies for one or more FreeBSD packages using pkg."""

# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

import argparse
import subprocess

from freebsd_powertools.lib.logging import get_logger

# ruff: noqa: S603, S607, T201


CALCULATED_DEPENDENCIES: dict[str, set[str]] = {}
LOGGER = None


def calculate_dependencies(pkg: str) -> set[str]:
    """Calculate dependencies for a package.

    Args:
        pkg: FreeBSD package.

    Returns:
        A set of dependent packages. The set may be empty if no dependencies exist.

    """
    if pkg in CALCULATED_DEPENDENCIES:
        LOGGER.debug("Getting cached dependencies for %s", pkg)
        return CALCULATED_DEPENDENCIES[pkg]

    LOGGER.debug("Calculating dependencies for %s", pkg)
    proc = subprocess.run(
        [
            "pkg",
            "query",
            "%dn-%dv",
            pkg,
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    dependencies = proc.stdout.splitlines(keepends=False)
    LOGGER.debug("%s's dependencies according to pkg are:\n%r", pkg, dependencies)

    all_dependencies = set()
    for dependency in dependencies:
        all_dependencies.add(dependency)
        all_dependencies |= calculate_dependencies(dependency)

    CALCULATED_DEPENDENCIES[pkg] = all_dependencies
    return all_dependencies


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    global LOGGER

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-s", "--sort", action="store_true", help="Sort in alphanumeric order."
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level.",
    )
    argparser.add_argument("packages", metavar="PACKAGE", nargs="+")

    args = argparser.parse_args(args=argv)

    # ruff: noqa: PLR2004
    log_level = (
        "DEBUG" if args.verbose > 2 else ("INFO" if args.verbose > 1 else "ERROR")
    )
    LOGGER = get_logger(__name__, level=log_level)

    for pkg in args.packages:
        dependencies = calculate_dependencies(pkg)
        if args.sort:
            dependencies = sorted(dependencies)
        if args.verbose:
            order_type = (
                "alphanumerically sorted" if args.sort else "depth-first dependency"
            )
            print(f"Dependencies for {pkg} in {order_type} order: ", end="")
            if dependencies:
                print("")
                for dependency in dependencies:
                    print(f"- {dependency}")
            else:
                print("(None)")
        else:
            print(f"{pkg}: {' '.join(dependencies)}")
