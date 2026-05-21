"""
Label Splitter - split an A4 PDF label into four A6 quadrants.

Select any combination of the four quadrants (top-left, top-right,
bottom-left, bottom-right) and export each one as a separate PDF file -
ready to print on an A6 / 100x150 mm thermal label printer.

Requirements:
    pip install pypdf

Build a single-file Windows .exe with PyInstaller:
    pip install pyinstaller
    pyinstaller --onefile --noconsole --name "LabelSplitter" label_splitter.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import copy

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    # fallback for older installs
    from PyPDF2 import PdfReader, PdfWriter


APP_TITLE = "Label Splitter - A4 to A6"
VERSION = "1.0.0"


class PDFQuadrantSplitter:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.input_file = None

        # checkbox variables
        self.var_tl = tk.BooleanVar(value=True)   # top-left
        self.var_tr = tk.BooleanVar(value=False)  # top-right
        self.var_bl = tk.BooleanVar(value=False)  # bottom-left
        self.var_br = tk.BooleanVar(value=False)  # bottom-right

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root,
            text="Split an A4 PDF label into A6 quadrants",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=12)

        # file selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=5, fill="x", padx=20)

        tk.Button(
            file_frame,
            text="Choose PDF file...",
            command=self.select_file,
            width=18,
        ).pack(side="left")

        self.file_label = tk.Label(file_frame, text="No file selected", fg="gray", anchor="w")
        self.file_label.pack(side="left", padx=10, fill="x", expand=True)

        # checkboxes laid out like a sheet of A4
        cb_frame = tk.LabelFrame(
            self.root,
            text="Select quadrants to export",
            padx=20,
            pady=15,
            font=("Segoe UI", 10),
        )
        cb_frame.pack(pady=15, padx=20, fill="x")

        tk.Checkbutton(
            cb_frame, text="Top-left", variable=self.var_tl, font=("Segoe UI", 11)
        ).grid(row=0, column=0, padx=20, pady=8, sticky="w")
        tk.Checkbutton(
            cb_frame, text="Top-right", variable=self.var_tr, font=("Segoe UI", 11)
        ).grid(row=0, column=1, padx=20, pady=8, sticky="w")
        tk.Checkbutton(
            cb_frame, text="Bottom-left", variable=self.var_bl, font=("Segoe UI", 11)
        ).grid(row=1, column=0, padx=20, pady=8, sticky="w")
        tk.Checkbutton(
            cb_frame, text="Bottom-right", variable=self.var_br, font=("Segoe UI", 11)
        ).grid(row=1, column=1, padx=20, pady=8, sticky="w")

        # quick selection
        quick_frame = tk.Frame(self.root)
        quick_frame.pack(pady=5)
        tk.Button(quick_frame, text="Select all", command=self.select_all).pack(side="left", padx=5)
        tk.Button(quick_frame, text="Clear all", command=self.deselect_all).pack(side="left", padx=5)

        # export button
        tk.Button(
            self.root,
            text="Export to PDF",
            command=self.export,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=6,
        ).pack(pady=15)

        # status
        self.status = tk.Label(self.root, text="", fg="green")
        self.status.pack()

        # version footer
        tk.Label(
            self.root,
            text=f"v{VERSION}",
            fg="gray",
            font=("Segoe UI", 8),
        ).pack(side="bottom", pady=5)

    def select_all(self):
        for v in (self.var_tl, self.var_tr, self.var_bl, self.var_br):
            v.set(True)

    def deselect_all(self):
        for v in (self.var_tl, self.var_tr, self.var_bl, self.var_br):
            v.set(False)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Select a PDF label",
            filetypes=[("PDF files", "*.pdf")],
        )
        if path:
            self.input_file = path
            self.file_label.config(text=os.path.basename(path), fg="black")
            self.status.config(text="")

    def export(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select a PDF file first.")
            return

        selections = {
            "top_left":     self.var_tl.get(),
            "top_right":    self.var_tr.get(),
            "bottom_left":  self.var_bl.get(),
            "bottom_right": self.var_br.get(),
        }

        if not any(selections.values()):
            messagebox.showwarning("Notice", "Select at least one quadrant.")
            return

        output_dir = filedialog.askdirectory(title="Choose output folder")
        if not output_dir:
            return

        try:
            reader = PdfReader(self.input_file)
            page = reader.pages[0]

            mb = page.mediabox
            x0 = float(mb.left)
            y0 = float(mb.bottom)
            x1 = float(mb.right)
            y1 = float(mb.top)
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2

            # (left, bottom, right, top) per quadrant
            quadrants = {
                "top_left":     (x0,    mid_y, mid_x, y1),
                "top_right":    (mid_x, mid_y, x1,    y1),
                "bottom_left":  (x0,    y0,    mid_x, mid_y),
                "bottom_right": (mid_x, y0,    x1,    mid_y),
            }

            base_name = os.path.splitext(os.path.basename(self.input_file))[0]
            saved = []

            for name, selected in selections.items():
                if not selected:
                    continue

                writer = PdfWriter()
                new_page = copy.deepcopy(page)
                box = quadrants[name]

                new_page.mediabox.lower_left = (box[0], box[1])
                new_page.mediabox.upper_right = (box[2], box[3])
                new_page.cropbox.lower_left = (box[0], box[1])
                new_page.cropbox.upper_right = (box[2], box[3])
                try:
                    new_page.trimbox.lower_left = (box[0], box[1])
                    new_page.trimbox.upper_right = (box[2], box[3])
                except Exception:
                    pass

                writer.add_page(new_page)

                out_path = os.path.join(output_dir, f"{base_name}_{name}.pdf")
                with open(out_path, "wb") as f:
                    writer.write(f)
                saved.append(out_path)

            self.status.config(text=f"Saved {len(saved)} file(s)", fg="green")
            messagebox.showinfo(
                "Success",
                f"Saved {len(saved)} file(s) in:\n{output_dir}",
            )

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")


def main():
    root = tk.Tk()
    app = PDFQuadrantSplitter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
