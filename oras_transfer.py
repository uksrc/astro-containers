import argparse
import os

from oras.client


def build_parser():
    epilog = """examples:
  Push a local SIF:
    python oras_transfer.py push --target harbor.ral.uksrc.org/radio-astro-software/miriad:v2025.10.14 miriad-v2025.10.14.sif

  Pull to a directory:
    python oras_transfer.py pull --target harbor.ral.uksrc.org/radio-astro-software/miriad:v2025.10.14 --outdir ./images

  Push with explicit hostname and password (private registry):
    python oras_transfer.py --hostname harbor.ral.uksrc.org --username Jack_Radcliffe --password "$HARBOR_TOKEN" \
      push --target harbor.ral.uksrc.org/radio-astro-software/miriad:v2025.10.14 miriad-v2025.10.14.sif

  Pull from another registry hostname:
    python oras_transfer.py --hostname registry.example.org pull --target registry.example.org/myproj/image:v1 --outdir ./images
"""
    parser = argparse.ArgumentParser(
        description="Push or pull artifacts from an ORAS registry.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--hostname",
        default="harbor.ral.uksrc.org",
        help="ORAS registry hostname (no scheme, e.g. harbor.ral.uksrc.org)",
    )
    parser.add_argument("--username", default="Jack_Radcliffe", help="Registry username")
    parser.add_argument(
        "--password",
        help="Registry password or token (required for private registries)",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    try:
        subparsers.required = True
    except AttributeError:
        pass

    push_parser = subparsers.add_parser(
        "push", help="Push files to a registry", description="Push files to a registry."
    )
    push_parser.add_argument(
        "--target",
        required=True,
        metavar="TARGET",
        help="Push target, e.g. harbor.ral.uksrc.org/radio-astro-software/miriad:v2025.10.14",
    )
    push_parser.add_argument(
        "--no-chunking",
        dest="chunked",
        action="store_false",
        default=True,
        help="Disable chunked upload (default is chunked)",
    )
    push_parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="Files to push (e.g. .sif or other artifacts)",
    )

    pull_parser = subparsers.add_parser(
        "pull", help="Pull files from a registry", description="Pull files from a registry."
    )
    pull_parser.add_argument(
        "--target",
        required=True,
        metavar="TARGET",
        help="Pull target, e.g. harbor.ral.uksrc.org/radio-astro-software/miriad:v2025.10.14",
    )
    pull_parser.add_argument(
        "--outdir",
        default=".",
        metavar="DIR",
        help="Output directory for pulled files (created if missing)",
    )
    pull_parser.add_argument(
        "--no-overwrite",
        dest="overwrite",
        action="store_false",
        default=True,
        help="Do not overwrite existing files",
    )
    return parser


def get_client(args):
    client = oras.client.OrasClient(hostname=args.hostname)
    client.login(username=args.username, password=args.password)
    return client


def run_push(args):
    client = get_client(args)
    client.push(files=args.files, target=args.target, do_chunked=args.chunked)


def run_pull(args):
    client = get_client(args)
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    files = client.pull(target=args.target, outdir=outdir, overwrite=args.overwrite)
    for path in files:
        print(path)


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "push":
        run_push(args)
    elif args.command == "pull":
        run_pull(args)


if __name__ == "__main__":
    main()
