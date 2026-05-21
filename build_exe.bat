@echo off
REM ============================================================
REM  Build script for label_splitter.py -> LabelSplitter.exe
REM  Double-click this file inside the project folder.
REM ============================================================

echo Installing required packages...
pip install --upgrade pypdf pyinstaller

echo.
echo Building EXE...
pyinstaller --onefile --noconsole --name "LabelSplitter" label_splitter.py

echo.
echo ============================================================
echo Done! Your EXE is here:   dist\LabelSplitter.exe
echo ============================================================
pause
