@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

REM ============================================================
REM  push_to_github.bat
REM
REM  One-shot script to publish the label-splitter project on
REM  GitHub. Run it from the project folder (B:\Claude\label-splitter).
REM
REM  Before running:
REM    1. Install Git for Windows  ->  https://git-scm.com/download/win
REM    2. Create an empty repo on GitHub (no README/license/.gitignore)
REM    3. Copy its HTTPS URL, e.g.
REM         https://github.com/your-username/label-splitter.git
REM ============================================================

cd /d "%~dp0"

echo.
echo === Step 1/6: checking Git ===
where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH.
    echo Download it from https://git-scm.com/download/win and re-run this script.
    pause
    exit /b 1
)
git --version

echo.
echo === Step 2/6: configuring identity (only if not set globally) ===
for /f "delims=" %%a in ('git config --global --get user.email 2^>nul') do set GIT_EMAIL=%%a
if "%GIT_EMAIL%"=="" (
    git config --global user.email "k.zarzecki@wezafon.pl"
    git config --global user.name  "Krystian Zarzecki"
    echo Identity set: Krystian Zarzecki ^<k.zarzecki@wezafon.pl^>
) else (
    echo Identity already configured: %GIT_EMAIL%
)
git config --global init.defaultBranch main

echo.
echo === Step 3/6: cleaning any broken .git folder ===
if exist ".git" (
    echo Removing existing .git folder...
    rmdir /s /q ".git"
)

echo.
echo === Step 4/6: initialising repo and committing ===
git init
git add .
git status --short
git commit -m "Initial commit - Label Splitter v1.0.0"
git branch -M main

echo.
echo === Step 5/6: GitHub remote URL ===
set /p REPO_URL=Paste your GitHub repo URL (e.g. https://github.com/USERNAME/label-splitter.git):
if "%REPO_URL%"=="" (
    echo [ERROR] No URL provided. Aborting before push.
    pause
    exit /b 1
)

git remote remove origin 2>nul
git remote add origin %REPO_URL%
git remote -v

echo.
echo === Step 6/6: pushing to GitHub ===
echo A browser window may open for authentication (Git Credential Manager).
echo If asked for a password, paste a Personal Access Token (PAT), NOT your GitHub password.
echo Generate a PAT at: https://github.com/settings/tokens  (scope: repo)
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Common causes:
    echo   - Wrong URL
    echo   - Authentication problem (use a PAT, not the account password)
    echo   - The remote repo is not empty (delete and recreate it)
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  DONE! Repo published at: %REPO_URL%
echo ============================================================
pause
