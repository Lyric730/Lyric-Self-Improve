@echo off
set "OBSIDIAN_EXE=F:\Apps\Obsidian\Obsidian.exe"

if not exist "%OBSIDIAN_EXE%" (
  echo Obsidian.exe not found: %OBSIDIAN_EXE%
  exit /b 1
)

start "" "%OBSIDIAN_EXE%"
