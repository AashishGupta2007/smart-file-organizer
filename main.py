import argparse
from organizer.core import organize_files, undo

parser = argparse.ArgumentParser(
    description="Smart File Organizer"
)

parser.add_argument(
    "--path",
    help="Folder path to organize"
)

parser.add_argument(
    "--preview",
    action="store_true",
    help="Preview changes without moving files"
)

parser.add_argument(
    "--undo",
    action="store_true",
    help="Undo last organization"
)

args = parser.parse_args()

if args.undo:
    undo()
else:
    if not args.path:
        print("❌ Please provide --path")
    else:
        organize_files(args.path, args.preview)