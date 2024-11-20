# File Organizer 📁
This is a Python script to help you organize your files into a cleaner structure with folder based on type and date (will increase the variety in the future)

## What it does

- **Organize by Type**: Sorts files into folders like Images, Documents, Videos etc.
- **Organize by Date**: Groups files by their creation date
- **Undo Feature**: Allow you to undo the last organization
- **History Tracking**: Keeps track of what files were moved where (for fun)


## Supported File Types

- Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .heic, .raw
- Documents: .pdf, .doc, .docx, .txt, .rtf, .odt, .pages
- Spreadsheets: .xls, .xlsx, .numbers, .csv
- Presentations: .ppt, .pptx, .key
- Videos: .mp4, .mov, .avi, .wmv, .flv, .mkv
- Audio: .mp3, .wav, .aac, .m4a, .flac
- Archives: .zip, .rar, .7z, .tar, .gz
- Code: .py, .java, .cpp, .js, .html, .css, .php

## Requirements

- Python 3.6+
- tqdm

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/file-organizer.git
```

2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages
```pip3 install tqdm```

4. Run the script
```python3 organizor.py```

## Usage
Choose organization method:

Option 1: Organize by file type
Option 2: Organize by date
Option 3: Undo last operation
Option 4: Show organization history
Enter source directory path

Enter destination directory path (or press Enter to organize in-place)

