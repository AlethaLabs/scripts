#!/usr/bin/env python3

import argparse
from pathlib import Path

parser = argparse.ArgumentParser("mkproj", description="Create new project repo skeleton")

parser.add_argument("name", help="Name of project directory")

parser.add_argument("--dest", 
                    type=Path, 
                    default=Path.cwd(), 
                    help="Destination path")

parser.add_argument("-r", action="store_true", help="Add README.md")

parser.add_argument("-g", action="store_true", help="Add .gitignore")

parser.add_argument("--src", 
                    type=str, 
                    default="src", 
                    help="Child source directory")

parser.add_argument("--include",
                    type=str,
                    default="include",
                    help="Create an include directory")

#TODO - Add template enum / argument
#TODO - Add license enum / argument

class Proj:
    def __init__(self,
                name, 
                dest: Path,
                src: str,
                include: str,
                readme: bool,
                gitignore: bool
    ) -> None:
        self.name = name
        self.dest = dest
        self.src = src
        self.inc = include
        self.r = readme
        self.g = gitignore

    def proj_base(self) -> Path:
        proj_path = self.dest.joinpath(self.name)

        if proj_path.exists():
            print(f"Project path: {proj_path} - exists")
            exit(0)
        else:
            proj_path.mkdir(parents=True, exist_ok=True)

        return proj_path
    
    def extras(self, proj_path: Path):
        proj_path.joinpath(self.src).mkdir(exist_ok=True)
        proj_path.joinpath(self.inc).mkdir(exist_ok=True)

        if self.r:
            proj_path.joinpath("README.md").touch(exist_ok=True)

        if self.g:
            proj_path.joinpath(".gitignore").touch(exist_ok=True)

        return

if __name__ == "__main__":
    args = parser.parse_args()
    p = Proj(
        name=args.name,
        dest=args.dest,
        src=args.src,
        include=args.include,
        readme=args.r,
        gitignore=args.g
        )
    
    base = p.proj_base()
    p.extras(base)

    exit(0)

