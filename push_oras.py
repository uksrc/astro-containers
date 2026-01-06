import argparse
import oras.client


def parse_args():
    parser = argparse.ArgumentParser(description="Push artifacts to an ORAS registry.")
    parser.add_argument(
        "--hostname",
        default="harbor.ral.uksrc.org",
        help="ORAS registry hostname",
    )
    parser.add_argument("--username", default="Jack_Radcliffe", help="Registry username")
    parser.add_argument(
        "--password",
        help="Registry password",
    )
    parser.add_argument(
        "--target",
        help="Push target, e.g. <registry>/<repo>:<tag>",
    )
    parser.add_argument(
        "--no-chunking",
        dest="chunked",
        action="store_false",
        default=True,
        help="Disable chunked upload (default is chunked)",
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Files to push",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    client = oras.client.OrasClient(hostname=args.hostname)
    client.login(username=args.username, password=args.password)
    client.push(files=args.files, target=args.target, do_chunked=args.chunked)


if __name__ == "__main__":
    main()
