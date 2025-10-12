#!/usr/bin/env python3
"""
Auto File Organizer — simple, safe, and readable.
Usage examples:
    python organizer.py --path "test_files" --dry
    python organizer.py --path "test_files" --apply
"""

import argparse
import logging
from pathlib import Path
import shutil
from typing import Dict, List

# default mapping; edit or extend in config.py or below
EXT_MAP: Dict[str, str] = {
    # images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images", ".bmp": "Images",
    # documents
    ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents", ".txt": "Documents",
    ".pptx": "Documents", ".ppt": "Documents", ".xlsx": "Documents", ".xls": "Documents",
    # archives
    ".zip": "Archives", ".rar": "Archives", ".tar": "Archives", ".gz": "Archives",
    # video/audio
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos", ".mp3": "Audio", ".wav": "Audio",
    # code
    ".py": "Code", ".cpp": "Code", ".c": "Code", ".h": "Code", ".java": "Code", ".js": "Code",
    # installers
    ".exe": "Installers", ".msi": "Installers",
}

OTHER_FOLDER = "Others"

logging.basicConfig(level=logging.INFO, format="%(message)s")


def find_files(target: Path) -> List[Path]:
    """Return all files (not directories) in target (non-recursive)."""
    return [p for p in target.iterdir() if p.is_file()]


def classify(file: Path, mapping: Dict[str, str]) -> str:
    return mapping.get(file.suffix.lower(), OTHER_FOLDER)


def safe_move(src: Path, dst: Path, dry_run: bool = True) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        logging.info(f"[DRY] Would move: {src.name} -> {dst}")
    else:
        final_dst = dst
        i = 1
        while final_dst.exists():
            final_dst = dst.with_name(f"{dst.stem}({i}){dst.suffix}")
            i += 1
        shutil.move(str(src), str(final_dst))
        logging.info(f"Moved: {src.name} -> {final_dst.name}")


def organize(target_dir: str, mapping: Dict[str, str], dry_run: bool = True) -> None:
    target = Path(target_dir).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        logging.error(f"Target not a directory: {target}")
        return

    files = find_files(target)
    if not files:
        logging.info("No files found. Nothing to do.")
        return

    for f in files:
        folder = classify(f, mapping)
        destination = target / folder / f.name
        safe_move(f, destination, dry_run=dry_run)


def parse_args():
    parser = argparse.ArgumentParser(description="Auto File Organizer")
    parser.add_argument("--path", "-p", required=True, help="Target directory to organize.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry", action="store_true", help="Dry run. Show moves but don't execute.")
    group.add_argument("--apply", action="store_true", help="Actually move files.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    dry = not args.apply
    logging.info(f"{'DRY-RUN' if dry else 'APPLY'} on: {args.path}")
    organize(args.path, EXT_MAP, dry_run=dry)
    logging.info("Done.")
