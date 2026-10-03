@echo off
echo ==========================================
echo SPERMATOPHYTA EXPLORER - START SERVER
echo ==========================================
if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate
python -m pip install -r backend\requirements.txt
set /p PLANTNET_API_KEY=Masukkan API key Pl@ntNet: 
set PLANTNET_PROJECT=k-world-flora
echo.
echo Server berjalan di http://127.0.0.1:8000
echo Untuk HP, server harus diakses dari jaringan yang sama dan firewall Windows mengizinkan port 8000.
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause
