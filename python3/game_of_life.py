"""Simple Conway's Game of Life implementation."""

from argparse import ArgumentParser, Namespace

# from sys import exit as sysexit
from gameoflife import MainGame


def main() -> None:
    """Run the game."""
    parser: ArgumentParser = ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "-f",
        "--file",
        # don't use FileType here - we want a str to use a context manager with later
        nargs="?",
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
    # mypy ignore below should work in next mypy version
    # REMEMBER to remove --no-warn-unused-ignores from workspace config when fixed
    # TODO: we don't need to add ability to load anything but RLE at this point
    # group = parser.add_mutually_exclusive_group()  # type: ignore[unused-ignore]
    # group.add_argument(
    #     "-r",
    #     "--rle",
    #     action="store_true",
    #     help="the specified file is of type Run Length Encoded (RLE)",
    # )
    args: Namespace = parser.parse_args()

    # is there a way to make argparse ensure we have exactly one type if we have a file arg?
    # if args.file and not args.rle:
    #     print("\nFilename specified but no file type argument given.\n")
    #     parser.print_help()
    #     sysexit(1)

    MainGame(args.wrap, args.file).main()


if __name__ == "__main__":
    main()
