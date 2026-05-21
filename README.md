# Label Splitter

A tiny Python desktop app that splits an **A4 PDF label** (the kind shipping carriers like DPD, InPost, DHL, GLS, UPS or Poczta Polska generate) into separate **A6 PDFs** — one per quadrant — ready to print on a 100×150 mm thermal label printer.

No more wasting 75% of a label sheet because the carrier only gave you an A4 file with the real label hiding in the top-left corner.

![Label Splitter screenshot](docs/screenshot.png)

## Features

- Simple Tkinter GUI (no extra UI dependencies).
- Pick **any combination** of the four quadrants via checkboxes.
- Output is a real, scalable PDF — page is cropped via the PDF mediabox, **not rasterized**, so print quality stays 1:1.
- Single-file `.exe` build for Windows via PyInstaller.
- Works on Windows, macOS and Linux (Python 3.8+).

## Why?

Many return-label PDFs are A4 with the actual label occupying one quadrant. If you print that on an A6 thermal printer it either gets shrunk into a tiny corner or wastes most of the label. This app crops the PDF to the part you actually need.

## Installation

### Run from source

```bash
pip install pypdf
python label_splitter.py
```

### Build a standalone Windows .exe

```bash
pip install pypdf pyinstaller
pyinstaller --onefile --noconsole --name "LabelSplitter" label_splitter.py
```

The executable will appear in `dist/LabelSplitter.exe`.
Windows users can also just double-click **`build_exe.bat`**.

## Usage

1. Click **Choose PDF file...** and select your A4 label.
2. Tick the checkboxes for the quadrant(s) you want to keep:

   ```
   +---------------+---------------+
   |   top-left    |   top-right   |
   +---------------+---------------+
   | bottom-left   | bottom-right  |
   +---------------+---------------+
   ```
3. Click **Export to PDF**, pick a destination folder.
4. Each selected quadrant is saved as `<original_name>_<position>.pdf`.

When printing on a thermal label printer:

- Paper size: **A6** (or your roll size, e.g. 100×150 mm).
- Scaling: **Fit to printable area**.
- The cropped PDF will fill the whole label.

## How it works

The app only touches the page's `MediaBox`, `CropBox` and (when supported) `TrimBox`. The PDF stream itself is untouched, so vector graphics, fonts and barcodes remain pixel-perfect — exactly what carriers and scanners want.

## Requirements

- Python 3.8+
- [`pypdf`](https://pypi.org/project/pypdf/) (or legacy `PyPDF2`)
- Tkinter — bundled with the official Python installer on Windows and macOS. On Debian/Ubuntu: `sudo apt install python3-tk`.

## Roadmap

- [ ] Visual preview of the four quadrants before export
- [ ] Multi-page PDF support (split every page)
- [ ] Auto-detect which quadrant contains the label
- [ ] Drag-and-drop file input
- [ ] CLI mode for batch processing

PRs welcome.

## License

[MIT](LICENSE)
