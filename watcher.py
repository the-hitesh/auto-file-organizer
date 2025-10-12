#!/usr/bin/env python3
"""
watcher.py

Simple folder watcher that triggers the organizer when files change.
Usage:
    python watcher.py --path "test_files"            # run indefinitely
    python watcher.py --path "test_files" --duration 15  # run for 15 seconds then exit (useful for CI demo)
    python watcher.py --path "test_files" --dry     # dry-run mode: organizer invoked with dry_run=True

Behavior:
- Debounces rapid events (waits `--debounce` seconds after last event).
- Ignores files already inside organizer-created destination folders.
- Uses organizer.organize(...) to do the moving (so config.py mapping is respected).
"""
import argparse
import logging
import threading
import time
from pathlib import Path
from typing import Optional

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
except Exception as e:
    raise RuntimeError("watchdog is required. Install via `pip install watchdog`") from e

# Import organizer.organize to reuse logic
try:
    from organizer import organize, EXT_MAP  # type: ignore
except Exception:
    # If import fails, the script will still run but will raise when an event triggers.
    organize = None
    EXT_MAP = {}

logging.basicConfig(level=logging.INFO, format="%(message)s")


class DebouncedHandler(FileSystemEventHandler):
    def __init__(self, target: Path, dry_run: bool = True, debounce: float = 1.0):
        super().__init__()
        self.target = target
        self.dry_run = dry_run
        self.debounce = debounce
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()

        # Destination folder names to ignore events inside them
        self.dest_folders = set(EXT_MAP.values()) | {"Others"}

    def _schedule_run(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce, self._run_organizer)
            self._timer.daemon = True
            self._timer.start()

    def _run_organizer(self):
        logging.info("Debounce timer fired — running organizer...")
        try:
            if organize is None:
                logging.error("organize() not available (failed to import organizer).")
                return
            organize(str(self.target), EXT_MAP, dry_run=self.dry_run, recursive=True)
        except Exception as e:
            logging.exception(f"Organizer run failed: {e}")

    def _should_ignore(self, event: FileSystemEvent) -> bool:
        """
        Ignore events where the file is inside one of the destination folders
        directly under the target directory (to avoid loops).
        """
        try:
            p = Path(event.src_path).resolve()
            rel = p.relative_to(self.target)
            if rel.parts and rel.parts[0] in self.dest_folders:
                return True
        except Exception:
            # If we can't compute relative path, don't ignore by default
            return False
        return False

    def on_any_event(self, event):
        # Only react to file events (not directories)
        if event.is_directory:
            return
        if self._should_ignore(event):
            logging.debug(f"Ignored event inside destination folder: {event.src_path}")
            return
        logging.info(f"Detected filesystem event: {event.event_type} -> {event.src_path}")
        self._schedule_run()


def parse_args():
    parser = argparse.ArgumentParser(description="Watcher for Auto File Organizer")
    parser.add_argument("--path", "-p", required=True, help="Target directory to watch.")
    parser.add_argument("--dry", action="store_true", help="Run organizer in dry-run mode when triggered.")
    parser.add_argument("--debounce", type=float, default=1.0, help="Seconds to debounce events.")
    parser.add_argument("--duration", type=int, default=0, help="Number of seconds to run the watcher (0 = forever).")
    return parser.parse_args()


def main():
    args = parse_args()
    target = Path(args.path).expanduser().resolve()
    if not target.exists():
        logging.error(f"Target does not exist: {target}")
        return

    event_handler = DebouncedHandler(target=target, dry_run=args.dry, debounce=args.debounce)
    observer = Observer()
    observer.schedule(event_handler, str(target), recursive=True)
    observer.start()
    logging.info(f"Started watcher on: {target} (dry_run={args.dry}, debounce={args.debounce})")

    try:
        if args.duration and args.duration > 0:
            # Run for a fixed duration (useful in CI)
            end = time.time() + args.duration
            while time.time() < end:
                time.sleep(0.5)
        else:
            # Run forever until Ctrl-C
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Watcher interrupted by user.")
    finally:
        observer.stop()
        observer.join()
        logging.info("Watcher stopped.")


if __name__ == "__main__":
    main()
