# Auto File Organizer

Simple Python script to sort files in a folder into subfolders based on extension.

## Usage
- Dry run: `python organizer.py --path "test_files" --dry`
- Apply: `python organizer.py --path "test_files" --apply`

## How to test on GitHub
1. Go to the **Actions** tab.
2. Open **Run Organizer Test** and click **Run workflow**.
3. Check the logs for the dry-run output and the apply output.

## Tech
- Python 3.8+
- Standard library only

## Next steps (optional)
- Make `EXT_MAP` editable via `config.py` (I can paste that file if you want)
- Add `--recursive` flag
- Add a simple web UI with Streamlit
