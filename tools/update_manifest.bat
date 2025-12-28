@echo off
setlocal

cd /d "%~dp0"

cd ..

echo Running manifest generator...

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set PACK_VERSION=%%i
echo Using pack version: %PACK_VERSION%

python tools\generate_manifest.py ^
   --base-url "https://raw.githubusercontent.com/ThatGuyJack01/GodSMP-Pack/main/mods" ^
   --pack-version %PACK_VERSION%

if errorlevel 1 (
  echo.
  echo Manifest generation failed.
  pause
  exit /b 1
)

echo.
echo Manifest generated successfully.

git add "mods" "manifest.json"

git commit -m "%PACK_VERSION%"
if errorlevel 1 (
  echo.
  echo (No changes to commit.)
)

git push
if errorlevel 1 (
  echo.
  echo Push failed.
  pause
  exit /b 1
)

echo.
echo Committed and pushed: %PACK_VERSION%

PAUSE