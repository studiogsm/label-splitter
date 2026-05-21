# Publishing Label Splitter to GitHub

A short cheat-sheet for getting this project online.

## 1. Create the repository on GitHub

1. Go to <https://github.com/new>.
2. Repository name: **`label-splitter`** (or whatever you prefer).
3. Description: *Split A4 PDF shipping labels into A6 quadrants — ready for thermal label printers.*
4. **Public** (so others can find it) or **Private** — your call.
5. **Do NOT** tick "Initialize with README / .gitignore / license" — we already have those files locally.
6. Click **Create repository**.

GitHub will show you the URL, e.g.:
`https://github.com/<your-username>/label-splitter.git`

## 2. Initialize the local repo and push

Open a terminal (PowerShell or CMD on Windows) in the folder that contains all the project files and run:

```bash
git init
git add label_splitter.py README.md LICENSE .gitignore requirements.txt build_exe.bat
git commit -m "Initial commit - Label Splitter v1.0.0"
git branch -M main
git remote add origin https://github.com/<your-username>/label-splitter.git
git push -u origin main
```

That's it — the project is now live on GitHub.

## 3. (Optional) Add a screenshot

The README references `docs/screenshot.png`. To make it appear:

1. Run the app, take a screenshot of the GUI.
2. In the project folder create a `docs/` subfolder.
3. Save the image as `docs/screenshot.png`.
4. Then:
   ```bash
   git add docs/screenshot.png
   git commit -m "Add screenshot"
   git push
   ```

## 4. (Optional) Create a release with the .exe

If you want non-technical users to download a ready-made executable:

1. Run `build_exe.bat` to produce `dist/LabelSplitter.exe`.
2. On GitHub go to **Releases → Draft a new release**.
3. Tag: `v1.0.0`, title: `Label Splitter 1.0.0`.
4. Drag `LabelSplitter.exe` into the **Assets** section.
5. Publish the release.

Users can now download the EXE directly without installing Python.

## 5. (Optional) Don't have Git installed?

- Download Git from <https://git-scm.com/download/win> and install with defaults.
- Or use **GitHub Desktop** (<https://desktop.github.com>) — point it at this folder, then "Publish repository".

## Common follow-ups

- Want a CI build that auto-produces the .exe on every release? Add a `.github/workflows/build.yml` with PyInstaller on `windows-latest`. Happy to generate one if you ask.
- Want a Polish translation alongside the English UI? You can add a language toggle and ship locale strings in a dict.
