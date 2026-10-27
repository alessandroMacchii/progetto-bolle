@echo off
setlocal
title Carico merci - revisione bolle
cd /d "%~dp0"

echo.
echo   CARICO MERCI - revisione bolle
echo   ==============================
echo.

rem --- Python c'e'? -----------------------------------------------------------
where python >nul 2>nul
if errorlevel 1 (
  echo   [X] Python non e' installato, o non e' nel PATH.
  echo       Scaricalo da https://www.python.org/downloads/ e durante
  echo       l'installazione spunta "Add python.exe to PATH".
  echo.
  pause
  exit /b 1
)

rem --- dipendenze installate? solo alla prima accensione -----------------------
python -c "import fastapi, fitz, openpyxl" >nul 2>nul
if errorlevel 1 (
  echo   Prima accensione: installo le librerie. Ci vuole un minuto.
  echo.
  python -m pip install --disable-pip-version-check -r requirements.txt
  if errorlevel 1 (
    echo.
    echo   [X] Installazione fallita. Copia l'errore qui sopra.
    pause
    exit /b 1
  )
  echo.
)

rem --- chiave API presente? ----------------------------------------------------
rem Senza .env l'app non puo' leggere le scansioni vere. Invece di morire con un
rem errore parte in modalita' prova sulle 14 pagine di esempio, e si vede: la
rem pillola del motore in alto a sinistra diventa arancione e dice "mock".
if not exist ".env" (
  echo   [!] Manca il file .env con ANTHROPIC_API_KEY.
  echo       Parto in MODALITA' PROVA: righe di esempio, nessun costo,
  echo       la lettura delle scansioni vere non e' attiva.
  echo       Per attivarla: copia .env.example in .env e metti la chiave.
  echo.
  set BOLLE_EXTRACTOR=mock
)

rem --- apri il browser quando il server e' in piedi ----------------------------
start "" powershell -NoProfile -WindowStyle Hidden -Command ^
  "Start-Sleep -Seconds 4; Start-Process 'http://127.0.0.1:8000'"

echo   Server su http://127.0.0.1:8000
echo   Il browser si apre da solo fra qualche secondo.
echo.
echo   PER CHIUDERE: Ctrl+C qui dentro, oppure chiudi questa finestra.
echo.

python -m bolle.app

echo.
echo   Server fermato.
pause
