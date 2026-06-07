#!/usr/bin/env python3

import argparse
from pathlib import Path
# import re
import hashlib as hash
from datetime import datetime

parser = argparse.ArgumentParser(prog="FIM", 
                                 description="File Integrity Monitor - Monitor directories for changing hashes"
                                 )

parser.add_argument("directory", type=Path, help="Directory you wish to monitor")

sub = parser.add_subparsers()

#TODO - add json logging / specified output - ex. only changed hashes
log = sub.add_parser("log")
log.add_argument("-a", "--a", dest="all", default=True, help="log all output to text file")
log.add_argument("location", type=Path, help="location of output text file")

#TODO - add regex / recursive functionality

class Hash:
    def __init__(self, path: Path) -> None:
        self.path = path
    
    def hash_file(self) -> str:
        if not self.path.exists():
            print(f"Path: {self.path} does not exist :(")
            return ""
        else:
            if self.path.stat().st_size == 0:
                print(f"File: {self.path} is empty")
                return ""

            h = hash.sha256()
            bytes = self.path.read_bytes()

            if bytes:
                h.update(bytes)
            else:
                print("Couldn't hash file")
                return ""
            
            return h.hexdigest()

class Log:
    def __init__(self, output_all: bool, location: Path, sha: list[str]) -> None:
        self.all = output_all 
        self.location = location
        self.sha = sha

    def log(self):
        time = datetime.now()
        if self.all:
            new_log = self.location.joinpath(f"log_{time}_.txt")
            new_log.write_text("".join(self.sha)) 

            

if __name__ == "__main__":
    args = parser.parse_args()
    
    sha_list = []
    for f in args.directory.iterdir():
        if not f.is_file():
            continue

        hash_obj = Hash(f)
        hash_str = hash_obj.hash_file()
        if hash_str:
            sha_list.append(f"{f.name}: {hash_str}\n")

    if getattr(args, "location", None) is not None:
        log_obj = Log(args.all, args.location, sha_list)
        log_obj.log()
