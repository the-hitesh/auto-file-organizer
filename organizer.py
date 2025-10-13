"""
Auto File Organizer — now with recursive support.

Behavior:
- If a `config.py` file exists in the repo, use EXT_MAP and OTHER_FOLDER from it.
- Otherwise, fall back to the built-in default mapping.
- Use --recursive (or -r) to scan subfolders too. When recursive, files keep their
  relative folder structure under the destination category (so nested/a.txt ->
  target/Docs/nested/a.txt for example).
- Files already inside any destination-category folder (Images, Docs, Others, etc.)
  are skipped to avoid re-processing organizer outputs.

Usage examples:
    python organizer.py --path "test_files" --dry
    python organizer.py --path "test_files" --apply
    python organizer.py --path "test_files" --apply --recursive
"""

import argparse
import logging
from pathlib import Path
import shutil
from typing import Dict, List

# Try to import user-provided mapping from config.py
try:
    from config import EXT_MAP, OTHER_FOLDER  # type: ignore
except Exception:
    EXT_MAP: Dict[str, str] = {
        ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images", ".bmp": "Images",
        ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents", ".txt": "Documents",
        ".pptx": "Documents", ".ppt": "Documents", ".xlsx": "Documents", ".xls": "Documents",
        ".zip": "Archives", ".rar": "Archives", ".tar": "Archives", ".gz": "Archives",
        ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos", ".mp3": "Audio", ".wav": "Audio",
        ".py": "Code", ".cpp": "Code", ".c": "Code", ".h": "Code", ".java": "Code", ".js": "Code",
        ".exe": "Installers", ".msi": "Installers",
    }
    OTHER_FOLDER = "Others"

logging.basicConfig(level=logging.INFO, format="%(message)s")


def find_files(target: Path, recursive: bool = False) -> List[Path]:
    """Return all files in target. Non-recursive by default; recursive if asked."""
    if recursive:
        return [p for p in target.rglob("*") if p.is_file()]
    return [p for p in target.iterdir() if p.is_file()]


def classify(file: Path, mapping: Dict[str, str]) -> str:
    return mapping.get(file.suffix.lower(), OTHER_FOLDER)


def safe_move(src: Path, dst: Path, dry_run: bool = True) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        logging.info(f"[DRY] Would move: {src} -> {dst}")
    else:
        final_dst = dst
        i = 1
        while final_dst.exists():
            final_dst = dst.with_name(f"{dst.stem}({i}){dst.suffix}")
            i += 1
        shutil.move(str(src), str(final_dst))
        logging.info(f"Moved: {src} -> {final_dst}")


def organize(target_dir: str, mapping: Dict[str, str], dry_run: bool = True, recursive: bool = False) -> None:
    target = Path(target_dir).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        logging.error(f"Target not a directory: {target}")
        return

    # Precompute set of destination-folder names to avoid reprocessing files already inside them
    dest_folder_names = set(mapping.values()) | {OTHER_FOLDER}

    files = find_files(target, recursive=recursive)
    if not files:
        logging.info("No files found. Nothing to do.")
        return

    for f in files:
        # skip files that are inside any of the destination folders directly under target
        try:
            rel = f.relative_to(target)
        except Exception:
            # unexpected: if relative path can't be computed, skip
            logging.debug(f"Skipping (not under target): {f}")
            continue

        # If first path part is a destination folder name, skip (already organized)
        if rel.parts and rel.parts[0] in dest_folder_names:
            logging.debug(f"Skipping already-organized file: {f}")
            continue

        folder = classify(f, mapping)

        if recursive and rel.parent != Path("."):
            # preserve relative path under the destination folder
            destination = target / folder / rel.parent / f.name
        else:
            destination = target / folder / f.name

        safe_move(f, destination, dry_run=dry_run)


def parse_args():
    parser = argparse.ArgumentParser(description="Auto File Organizer")
    parser.add_argument("--path", "-p", required=True, help="Target directory to organize.")
    parser.add_argument("--recursive", "-r", action="store_true", help="Scan subfolders recursively.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry", action="store_true", help="Dry run. Show moves but don't execute.")
    group.add_argument("--apply", action="store_true", help="Actually move files.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    dry = not args.apply
    logging.info(f"{'DRY-RUN' if dry else 'APPLY'} on: {args.path} (recursive={args.recursive})")
    organize(args.path, EXT_MAP, dry_run=dry, recursive=args.recursive)
    logging.info("Done.")
