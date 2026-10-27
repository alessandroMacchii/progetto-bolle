@echo off
setlocal
title Carico merci - prova online
cd /d "%~dp0"

rem Come "Avvia carico merci.bat", ma rende l'app raggiungibile da internet con
rem un link Cloudflare protetto da password. Link e password li stampa sotto.

where python >nul 2>nul
if errorlevel 1 (
  echo   [X] Python non e' installato, o non e' nel PATH.
  echo       Scaricalo da https://www.python.org/downloads/ e durante
  echo       l'installazione spunta "Add python.exe to PATH".
  pause
  exit /b 1
)

python -c "import fastapi, fitz, openpyxl, dotenv" >nul 2>nul
if errorlevel 1 (
  echo   Prima accensione: installo le librerie. Ci vuole un minuto.
  python -m pip install --disable-pip-version-check -r requirements.txt
  if errorlevel 1 (
    echo   [X] Installazione fallita. Copia l'errore qui sopra.
    pause
    exit /b 1
  )
)

rem Online la modalita' prova non ha senso: senza chiave non si parte.
if not exist ".env" (
  echo   [X] Manca il file .env con la chiave API: copia .env.example in .env
  echo       e inserisci la chiave prima di mettere l'app online.
  pause
  exit /b 1
)

python -m bolle.online

echo.
echo   Prova online chiusa: il link non funziona piu'.
pause
