[![Run Organizer Test](https://github.com/<your-username>/auto-file-organizer/actions/workflows/test-run.yml/badge.svg)](https://github.com/<your-username>/auto-file-organizer/actions/workflows/test-run.yml)

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)

![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-blue?logo=githubactions)

![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen)

# Auto File Organizer

Simple Python script to sort files in a folder into subfolders based on extension.

## Usage
- Dry run (safe):  
  ```
  python organizer.py --path "test_files" --dry"
  ```
- Apply (actually move files):  
  ```
  python organizer.py --path "test_files" --apply"
  ```

## Configuration (NEW 🔧)
You can edit which extensions go into which folders using `config.py`.

### Example:
Inside `config.py`, there’s a dictionary called `EXT_MAP`:

```python
EXT_MAP = {
    ".pdf": "Documents",
    ".py": "Code",
    ".md": "Docs",  # markdown files go into 'Docs/'
}
```

To test your changes:
1. Add a sample file — e.g. `test_files/readme.md`
2. Go to **Actions → Run Organizer Test → Run workflow**
3. Check the logs — it should move `readme.md` into `test_files/Docs`

## GitHub Actions (cloud testing)
This repo includes a workflow at `.github/workflows/test-run.yml` that:
- Runs the script in dry mode  
- Runs the script in apply mode  
- Prints folder structure before/after

You can trigger it manually from the **Actions** tab.

## Tech
- Python 3.8+
- Standard library only
- Works locally or directly on GitHub via Actions

## Future ideas
- Recursive mode to handle nested folders
- Simple GUI with Streamlit
- Watchdog mode to auto-sort as files appear
