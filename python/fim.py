#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
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

#TODO - add regex
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

class Hash:
    def __init__(self, paths: list[Path]) -> None:
        self.paths = paths
    
    def hash_file(self) -> list[str]:
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
            
            h_list.append(f"{i.name}: {h.hexdigest()}")

        return h_list

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
    d_list = Recurse(args.directory).get_all()

    hash_obj = Hash(d_list)
    hash_str = hash_obj.hash_file()
    if hash_str:
        sha_list.extend(f"{line}\n" for line in hash_str)

    if getattr(args, "location", None) is not None:
        log_obj = Log(args.all, args.location, sha_list)
        log_obj.log()
