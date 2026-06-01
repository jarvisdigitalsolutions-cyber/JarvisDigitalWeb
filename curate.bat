@echo off
REM Quick Auto-Curate Launcher
REM Uso: curate.bat [v1|v2|mp] [--dry-run]

setlocal enabledelayedexpansion

cd /d "D:\Proyecto\PS5-COLLECTION"

set VERSION=mp
set DRYRUN=

if "%1"=="v1" set VERSION=v1
if "%1"=="v2" set VERSION=v2
if "%1"=="mp" set VERSION=mp
if "%2"=="--dry-run" set DRYRUN=--dry-run

echo.
echo ====================================
echo 🎮 PS5 COLLECTION AUTO-CURATE
echo ====================================
echo.
echo Version: %VERSION%
echo Dry-run: %DRYRUN%
echo.

if "%VERSION%"=="v1" (
    echo 📊 Ejecutando: v1 (PS5 ONLY)
    echo    (55%% rating, 30%% recency, 15%% discount)
    echo.
    python scripts/auto_curate.py %DRYRUN%
) else if "%VERSION%"=="v2" (
    echo 🚀 Ejecutando: v2 (PS5 ONLY MEJORADO)
    echo    (40%% rating, 25%% recency, 15%% discount, 15%% popularity, 5%% exclusive)
    echo.
    python scripts/auto_curate_v2.py --version v2 %DRYRUN%
) else (
    echo 🎮 Ejecutando: MULTIPLATFORM (PS5, PS4, PS3)
    echo    (40%% rating, 25%% recency, 15%% discount, 15%% popularity, 5%% exclusive)
    echo    (3 semanas de predicción)
    echo.
    python scripts/auto_curate_multiplatform.py --weeks-forecast 3 %DRYRUN%
)

echo.
echo ✅ Completado
echo.
pause
