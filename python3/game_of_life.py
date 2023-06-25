"""Simple Conway's Game of Life implementation."""

from argparse import ArgumentParser, Namespace
from gameoflife import MainGame


def main() -> None:
    """Run the game."""
    parser: ArgumentParser = ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "-f",
        "--file",
        # don't use FileType here - we want a str to use a context manager with later
        nargs=1,
        help="specify a file to read initial cells from",
    )
    parser.add_argument(
        "-w",
        "--wrap",
        default=False,
        action="store_true",
        help="change the default from using an infinite universe to instead use a universe of a "
        + "fixed size which wraps around the edges, the fixed size universe will default to the "
        + "size of the terminal on start and cannot be changed later",
    )
    parser.add_argument(
        "-r",
        "--rows",
        default=[0],
        type=int,
        nargs=1,
        help="specify the number of rows to use when using --wrap - default is terminal height",
    )
    parser.add_argument(
        "-c",
        "--cols",
        default=[0],
        type=int,
        nargs=1,
        help="specify the number of columns to use when using --wrap - default is terminal width",
    )
    args: Namespace = parser.parse_args()
    if not args.wrap and (args.rows or args.cols):
        raise ValueError("Do not specify --rows or --cols without --wrap")
    file: str = args.file[0] if args.file else ""
    print(f"{args.rows} {args.cols}")
    MainGame(args.wrap, file, args.rows[0], args.cols[0]).main()


if __name__ == "__main__":
    main()
