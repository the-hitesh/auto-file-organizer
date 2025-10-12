# Auto File Organizer

Simple Python script to sort files in a folder into subfolders based on extension.

## Features
- Move files into typed folders (Images, Documents, Code, etc.)
- Dry-run (preview) and Apply (actually move)
- Optional JSON config (custom mapping)
- Optional recursive mode
- Safe collision handling (adds `(1)`, `(2)`, ...)

## Quick start
1. Clone/download this repo.
2. (Optional) Create a virtualenv:
   - `python3 -m venv venv && source venv/bin/activate`
3. Prepare a mapping (optional):
   - `mapping.json` example included.
4. Dry run:
   - `python organizer.py -p ./test_files --dry`
5. Apply:
   - `python organizer.py -p ./test_files --apply`

## JSON config example
See `mapping.json` for a sample. Format:
```json
{
  "EXT_MAP": { ".py": "Code", ".jpg": "Images" },
  "OTHER_FOLDER": "Misc"
}
```

## Notes
- Script uses standard library only (no pip installs).
- Default mapping used if no config provided.
- Use `--recursive` to scan subfolders (careful, start with `--dry`).

## Next ideas (bonus)
- Watch mode (auto-run when files change) using `watchdog`.
- GUI with `streamlit` or `tkinter`.
- Add tests with `pytest`.
