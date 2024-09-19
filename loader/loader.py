from argparse import ArgumentParser

from .vectorstore import VectorStore


def main(args=None):
    parser = ArgumentParser(prog="loader", allow_abbrev=False)
    excl_group = parser.add_mutually_exclusive_group(required=True)
    excl_group.add_argument(
        "--seed",
        action="store",
        nargs="?",
        const="",
        help="Path to folder with data to seed the vector store",
    )
    excl_group.add_argument("--drop", action="store_true")
    args = parser.parse_args(args)

    store = VectorStore(seed_on_init=False)

    if args.drop:
        store.drop()

    if (seed := args.seed) or seed == "":
        store.seed(seed)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
