# Spermatophyta Explorer — Mobile/Web

## Struktur
- frontend/index.html — aplikasi siswa yang responsif untuk HP
- backend/main.py — FastAPI + proxy Pl@ntNet
- backend/requirements.txt — dependensi
- run_windows.bat — menjalankan server di Windows

## 1. Siapkan API key
Jangan menaruh API key di `frontend/index.html`.
Set environment variable:
Windows PowerShell:
    $env:PLANTNET_API_KEY="API_KEY_ANDA"

## 2. Jalankan
Dari folder proyek:
    py -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r backend\requirements.txt
    python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

Buka laptop:
    http://127.0.0.1:8000

## 3. Akses dari HP di Wi-Fi yang sama
Cari IPv4 laptop dengan:
    ipconfig

Misalnya IPv4 laptop = 192.168.1.10
Buka pada HP:
    http://192.168.1.10:8000

Jika tidak terbuka, izinkan Python/Uvicorn pada Windows Firewall untuk jaringan Private.

## 4. Untuk dipakai 38 siswa dari internet
Jangan menggunakan IP lokal. Deploy folder backend + frontend ke hosting/server yang mendukung Python/FastAPI dan set `PLANTNET_API_KEY` sebagai secret/environment variable.

## Catatan
Pl@ntNet mendukung maksimal 5 foto untuk satu individu tanaman dalam satu permintaan dan format JPG/PNG. Versi awal ini menggunakan 1 foto per identifikasi untuk membuat alur HP sederhana. 
