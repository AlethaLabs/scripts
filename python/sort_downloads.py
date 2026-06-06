#!/usr/bin/env python3

from pathlib import Path
import shutil

DOWNLOADS_PATH = Path.home() / "Downloads"
TARGET = {
    "pdf": Path.home() / "Documents" / "PDFs",
    "iso": Path.home() / "VM" / "iso",
    "jpg": Path.home() / "Pictures" / "Images",
    "jpeg": Path.home() / "Pictures" / "Images",
    "png": Path.home() / "Pictures" / "Images",
}

def dest_path(dest_dir: Path, filename: str) -> Path:
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        print(f"Made directory: {dest_dir}")

    path = dest_dir / filename
    if not path.exists():
        return path

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    n = 1
    while True:
        path = dest_dir / f"{stem} ({n}){suffix}"
        if not path.exists():
            return path
        n += 1

if __name__ == "__main__":
    if not DOWNLOADS_PATH.exists():
        print(f"Downloads path does not exist at: {DOWNLOADS_PATH}")
        raise SystemExit(1)
    
    count = 0

    for fp in DOWNLOADS_PATH.iterdir():
        if not fp.is_file():
            continue

        dest_dir = TARGET.get(fp.suffix.lower().lstrip("."))
        if dest_dir is None:
            continue # skip files not in TARGET

        path = dest_path(dest_dir, fp.name)

        shutil.move(str(fp), str(path))
        count += 1
        print(f"Moved {fp.name} -> {path}")
        
    print(f"Moved {count} file(s)")