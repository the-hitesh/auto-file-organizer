"""
config.py

Editable mapping of file extensions -> output folder names.
Modify EXT_MAP or OTHER_FOLDER as you like.
"""

EXT_MAP = {
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

# fallback folder for unknown extensions
OTHER_FOLDER = "Others"
