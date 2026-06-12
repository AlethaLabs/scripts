#!/usr/bin/env python3

import argparse
import os
import json
from pathlib import Path
import hashlib as hash
from datetime import datetime
from typing import Optional

parser = argparse.ArgumentParser(prog="FIM", 
                                 description="File Integrity Monitor - Monitor directories for changing hashes")

parser.add_argument("directory", type=Path, help="Directory you wish to monitor")

sub = parser.add_subparsers()

"""
Log sub command:
    - logs as json or txt files
    - can be configured to log a base case
    - can log warnings of recent hash changes compared to base
"""
log = sub.add_parser("log")
log.add_argument("-a", "--all", dest="all", 
                action="store_true", default=True, 
                help="log all output to text / json file"
                )
log.add_argument("-b", "--base", dest="base", 
                action="store_true", default=False, 
                help="log all output for base comparison"
                )
log.add_argument("-w", "--warnings", dest="warnings", 
                action="store_true", default=False, 
                help="only log warnings of mismatch comparisons from base"
                )
log.add_argument("-j", "--json", dest="json", 
                action="store_true", default=False, 
                help="log output as json"
                )
log.add_argument("location", type=Path, help="location of output text file")

"""
Recurse class:
    - walks directories
    - follows symlinks to find all nested directories/files
"""
#TODO - add depth configuration
class Recurse:
    def __init__(self, path: Path) -> None:
        self.path = path 

    def get_all(self) -> list[Path]:
        file_list = []
        for root, _, files in os.walk(self.path, followlinks=True):
            root_path = Path(root)
            for file_name in files:
                file_list.append(root_path / file_name)
        return file_list

#TODO - Add compare class / functionality  

"""
Hash class:
    - hashes a given file
    - uses sha256 
"""
class Hash:
    def __init__(self, paths: list[Path]) -> None:
        self.paths = paths
    
    def hash_file(self) -> list[tuple[Path, str]]:
        h_list = []
        for i in self.paths:
            if not i.exists():
                print(f"Path: {i} does not exist :(")
                continue
            else:
                if i.stat().st_size == 0:
                    print(f"File: {i} is empty")
                    continue

            h = hash.sha256()
            bytes = i.read_bytes()

            if bytes:
                h.update(bytes)
            else:
                print("Couldn't hash file")
                continue
            
            h_list.append((i, h.hexdigest()))

        return h_list

class Log:
    def __init__(
                self, 
                output_all: bool, 
                location: Path, 
                sha_list: Optional[list[str]],
                json_data: Optional[dict[str, str]],
            ) -> None:
        self.all = output_all 
        self.location = location
        self.sha_list = sha_list
        self.json_data = json_data

    def log(self):
        time = datetime.now().isoformat("_")
        if self.all:
            if self.json_data:
                json_log = self.location.joinpath(f"log_{time}_.json")
                with open(json_log, 'w', encoding='utf-8') as f:
                    json.dump(self.json_data, f, indent=2)
                    print(f"Made log - {json_log}")
            else:
                txt_log = self.location.joinpath(f"log_{time}_.txt")
                if self.sha_list:
                    txt_log.write_text("".join(self.sha_list)) 
                    print(f"Made log - {txt_log}")

"""
Constructs data for json output
"""
def construct_data(hash_entries: list[tuple[Path, str]]) -> dict[str, str]:
    data = {}
    for p, s in hash_entries:
        data[str(p)] = {"Hash": s}
    return data

if __name__ == "__main__":
    args = parser.parse_args()

    print("Welcome to Aletha Labs - FIM\n")

    sha_list = []
    data = None
    d_list = Recurse(args.directory).get_all()
    hash_obj = Hash(d_list)
    hash_entries = hash_obj.hash_file()

    if hash_entries:
        sha_list.extend(f"{path.name}: {digest}\n" for path, digest in hash_entries)
        if args.json:
            data = construct_data(hash_entries)

    if getattr(args, "location", None) is not None:
        log_obj = Log(args.all, args.location, sha_list, data)
        log_obj.log()
