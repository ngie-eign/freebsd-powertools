"""GNU make db to JSON converter."""

# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import pathlib
import re
import subprocess
import sys
from distutils.text_file import TextFile

_target_rx = re.compile(r"(?P<target>[^:]+)\s*:\s+(?P<dependencies>[^:]+)")


# ruff: noqa: PTH122, S603, S607


def parse_gmake_output(fn: str) -> dict[str, list[str]]:
    """Parse output from `gmake`.

    Args:
        fn: filename to parse.

    Returns:
        A dict with a target to dependencies mapping.

    """
    done = {}
    proc = subprocess.run(
        [
            "gmake",
            "--print-data-base",
            "-pqRrs",
            "-f",
            fn,
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    buffer = io.StringIO(proc.stdout)
    fp = TextFile(
        file=buffer,
        strip_comments=True,
        skip_blanks=True,
        join_lines=True,
        errors="surrogateescape",
    )
    with contextlib.closing(fp):
        for line in fp.readlines():
            res = _target_rx.match(line)
            if res is None:
                continue
            done[res[1]] = res[2].split()
    return done


def parse_depends_file(fn: str) -> dict[str, list[str]]:
    """Parse depends files output by `cpp -dM`.

    This helps build a dependency list for all build artifacts which depend on other
    files in order to function.

    Args:
        fn: filename to parse.

    Returns:
        A dict with a target to dependencies mapping.

    """
    done = {}
    fp = TextFile(
        fn,
        strip_comments=False,
        skip_blanks=True,
        join_lines=True,
        errors="surrogateescape",
    )
    with contextlib.closing(fp):
        for line in fp.readlines():
            res = _target_rx.match(line)
            if res is None:
                continue
            done[res[1]] = res[2].replace("\\", " ").split()
    return done


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-m",
        "--makefile",
        dest="makefile",
    )
    argparser.add_argument(
        "-o",
        "--output-file",
        default=sys.stdout,
        dest="output_file",
        type=argparse.FileType("w"),
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level.",
    )
    argparser.add_argument("depend_dirs", nargs="*")

    args = argparser.parse_args(args=argv)

    # ruff: noqa: E501, ERA001
    # log_level = (
    #     "debug" if args.verbose > 2 else ("info" if args.verbose > 1 else "error")
    # )
    # get_logger(__name__, level=log_level)

    depends_dict = {}

    # gmake --print-data-base | egrep '^([A-Z]+_)?LDFLAGS'

    if args.makefile:
        depends_dict.update(parse_gmake_output(args.makefile))
    else:
        for depend_dir in args.depend_dirs:
            for root, _, files in os.walk(depend_dir):
                root_p = pathlib.Path(root)
                for file in [
                    file for file in files if os.path.splitext(file)[-1] == ".d"
                ]:
                    depends_dict.update(parse_depends_file(str(root_p / file)))

    json.dump(depends_dict, args.output_file, indent=4)
