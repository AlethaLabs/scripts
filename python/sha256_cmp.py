import hashlib as h
from pathlib import Path
import os
import argparse

parser = argparse.ArgumentParser(prog="Compare Hash", usage="Compare two hashes")

parser.add_argument("file", type=Path, help="File you wish to parse")
parser.add_argument("-c", type=str, help="Hash you wish to compare")

def hash_file(path: Path):
    # Check if file is empty
    if path.stat().st_size == 0:
        print("Error: {} is empty", path)

    m = h.sha256()
    buffer = path.read_bytes()
    if buffer:
        m.update(buffer)
    else:
        print("Couldn't hash file :(")

    return m.hexdigest()

if __name__ == "__main__":
    args = parser.parse_args()
    path = args.file
    given = args.c
    if path.exists():
        hashed = hash_file(path)
        if str(hashed) == given:
            print("Hash is correct\n")
            print(f"{hashed}\n{given}")
        else:
            print("HASH IS NOT THE SAME")
            print(f"{hashed}\n{given}")
    else:
        print("Sorry, path does not exist :(")