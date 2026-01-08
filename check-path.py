import os

def print_environment_paths():
    # 1. Extract the 'PATH' string from environment variables
    # We use .get() to avoid an error if PATH is somehow missing
    path_string = os.environ.get('PATH', '')

    if not path_string:
        print("No PATH variable found.")
        return

    # 2. Determine the separator based on the Operating System
    # Windows uses ';' while Linux/macOS uses ':'
    separator = os.pathsep

    # 3. Split the string into a list
    path_list = path_string.split(separator)

    # 4. Print the formatted list
    print(f"{'#' * 20}")
    print(f"System PATH Entries ({len(path_list)} total)")
    print(f"{'#' * 20}\n")

    for i, path in enumerate(path_list, 1):
        # We use an f-string to pad the numbers for better alignment
        print(f"{i:02d} | {path}")

if __name__ == "__main__":
    print_environment_paths()
