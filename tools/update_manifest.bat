@echo off
setlocal

echo Running manifest generator...

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set PACK_VERSION=%%i
echo Using pack version: %PACK_VERSION%

python generate_manifest.py ^
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

PAUSE