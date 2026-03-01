import os
import shutil
import logging
import json
from colorama import Fore, init

init(autoreset=True)

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ---------------- FILE TYPES ----------------
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".tar", ".gz"]
}


def get_folder(file):
    _, ext = os.path.splitext(file.lower())

    for folder, extensions in FILE_TYPES.items():
        if ext in extensions:
            return folder

    return "Others"


# ---------------- ORGANIZER ----------------
def organize_files(path, preview=False):

    if not os.path.exists(path):
        print(Fore.RED + "❌ Path does not exist!")
        return

    moves = []

    for file in os.listdir(path):

        source_path = os.path.join(path, file)

        # Skip folders
        if os.path.isdir(source_path):
            print(Fore.BLUE + f"📁 Skipping folder: {file}")
            continue

        folder_name = get_folder(file)
        destination_folder = os.path.join(path, folder_name)
        destination_path = os.path.join(destination_folder, file)

        os.makedirs(destination_folder, exist_ok=True)

        if preview:
            print(
                Fore.YELLOW +
                f"👀 Would move: {file} → {folder_name}/"
            )
        else:
            try:
                shutil.move(source_path, destination_path)

                print(
                    Fore.GREEN +
                    f"✅ Moved: {file} → {folder_name}/"
                )

                logging.info(f"Moved {file} to {folder_name}")

                moves.append({
                    "src": source_path,
                    "dst": destination_path
                })

            except Exception as e:
                print(Fore.RED + f"❌ Error moving {file}: {e}")

    # Save history for undo
    if not preview and moves:
        with open("history.json", "w") as f:
            json.dump(moves, f, indent=4)


# ---------------- UNDO FEATURE ----------------
def undo():

    if not os.path.exists("history.json"):
        print(Fore.RED + "❌ No history found to undo.")
        return

    with open("history.json", "r") as f:
        moves = json.load(f)

    for move in reversed(moves):
        try:
            shutil.move(move["dst"], move["src"])
            print(
                Fore.GREEN +
                f"↩ Restored: {os.path.basename(move['src'])}"
            )
            logging.info(f"Restored {move['src']}")
        except Exception as e:
            print(Fore.RED + f"❌ Undo failed: {e}")

    print(Fore.CYAN + "✅ Undo completed")