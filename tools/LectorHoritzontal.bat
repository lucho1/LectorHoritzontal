@echo off

python ../scripts/main.py
if errorlevel 1 (
    echo Couldn't run Lector Horitzontal! D:
)

pause
