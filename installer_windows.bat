@echo off
setlocal enabledelayedexpansion
title Arena CLI V2 - Installateur

echo.
echo  ==========================================
echo   Arena.ai CLI V2 - Installation
echo  ==========================================
echo.

REM Verifie Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Telecharge-le sur https://www.python.org/downloads/
    echo Coche bien "Add Python to PATH" pendant l'installation !
    pause
    exit /b 1
)

echo [OK] Python detecte: 
python --version
echo.

echo [1/4] Creation de l'environnement virtuel (.venv)...
python -m venv .venv
if errorlevel 1 (
    echo [ERREUR] Echec de la creation de l'environnement virtuel.
    pause
    exit /b 1
)

echo [2/4] Mise a jour de pip...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet

echo [3/4] Installation des dependances (requirements.txt)...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERREUR] pip a echoue. Verifie ta connexion internet.
    pause
    exit /b 1
)

echo [4/4] Telechargement du navigateur Chromium (Playwright)...
python -m playwright install chromium
if errorlevel 1 (
    echo [ERREUR] Echec telechargement Chromium.
    pause
    exit /b 1
)

echo.
echo  ==========================================
echo   Installation terminee !
echo  ==========================================
echo.
echo  Pour utiliser Arena CLI :
echo.
echo    Premiere fois (connexion) :
echo      .venv\Scripts\activate
echo      python arena.py --login
echo.
echo    Ensuite pour chatter :
echo      .venv\Scripts\activate
echo      python arena.py
echo.
pause
