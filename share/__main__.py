from argparse import ArgumentParser

from .upload_single import upload_single
from .upload_multiple import upload_multiple


parser = ArgumentParser(
    description="Upload a file to a sharing service and print a URL to it",
    usage="share FILE [-h] [--host HOST]"
)

parser.add_argument("file", nargs="*", help="path to the file to upload")
parser.add_argument(
    "--host", 
    choices=("imgur", "gist", "anonfile"),
    help="explicitly specify the host to use")

args = parser.parse_args()


if len(args.file) == 0:
    print("No file(s) specified.")
    exit(1)
elif len(args.file) == 1:
    upload_single(args.file[0], args.host)
else:
    upload_multiple(args.file, args.host)
