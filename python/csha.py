#!/usr/bin/env python3

import hashlib as h
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(prog="Compare Hash", 
                                usage="cmp_sha hello.txt -c 'HASH'",
                                description="Compare a files SHA256 hash with the" \
                                "given hash from the supplier")

parser.add_argument("file", type=Path, help="File you wish to grab hash value")
parser.add_argument("-w", "--with", dest="compare_file", type=Path,
                    help="File you wish to compare hash value against")
parser.add_argument("-c", "--compare", dest="compare_hash", type=str,
                    help="Hash string you wish to compare against")

class Hash:
    def __init__(self, path: Path, other_path: Path | None, hash_string: str | None) -> None:
        self.path = path
        self.other = other_path
        self.hstr = hash_string

    def hash_file(self) -> str:
        if self.path.exists():
            if self.path.stat().st_size == 0:
                print(f"Error: {self.path} is empty")
                return ""

            hash = h.sha256()
            buffer = self.path.read_bytes()

            if buffer:
                hash.update(buffer)
            else:
                print("Couldn't hash file :(")
                return ""

            return hash.hexdigest()
        else:
            print(f"Path: {self.path} does not exist")
            return ""
        
    def compare(self, hashed_file: str):
        other_hash = self.hstr

        if self.other is not None:
            other_hash = Hash.hash_file(Hash(self.other, None, None))

        if not other_hash:
            print(hashed_file)
            return

        if hashed_file == other_hash:
            print("Hash is correct\n")
            print(f"{hashed_file}\n{other_hash}")
        else:
            print("--- NO MATCH ---")
            print(f"{hashed_file}\n{other_hash}")

if __name__ == "__main__":
    args = parser.parse_args()

    hash_obj = Hash(
        args.file,
        args.compare_file,
        args.compare_hash
    )

    hashed = Hash.hash_file(hash_obj)

    hash_obj.compare(hashed_file=hashed)
