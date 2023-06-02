"""Simple Conway's Game of Life implementation."""

import argparse
from gameoflife import MainGame


def main() -> None:
    """Run the game."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Conway's Game of Life"
    )
    parser.add_argument(
        "-r",
        "--rle",
        nargs="?",
        type=argparse.FileType("r"),
        help="specify a Run Length Encoded file to read initial cells from",
    )
    args: argparse.Namespace = parser.parse_args()

    MainGame(rle_file=args.rle).main()


if __name__ == "__main__":
    main()
