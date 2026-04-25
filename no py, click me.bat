@echo off
chcp 65001 >nul
title Khoi Chay He Thong POS
color 0A

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ========================================================
    echo Phat hien may chua co Python! 
    echo He thong dang tu dong tai va cai dat Python 3.10 chinh chu tu Microsoft...
    echo (Vui long nhan "Yes" neu Windows hien bang hoi quyen)
    echo ========================================================
    winget install -e --id Python.Python.3.10 --accept-package-agreements --accept-source-agreements
    echo.
    echo ========================================================
    echo DA CAI DAT PYTHON THANH CONG!
    echo Vui long TAT CUA SO NAY va bam mo lai file start.bat 1 lan nua de chay.
    echo ========================================================
    pause
    exit
)

if not exist "venv\Scripts\activate.bat" (
    echo Lan dau tien chay: Dang tao moi truong va tai thu vien...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install setuptools<70.0
    pip install cmake
    pip install -r env.txt
) else (
    echo Moi truong da san sang!
    call venv\Scripts\activate.bat
)

python app.py