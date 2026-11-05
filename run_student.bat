@echo off

echo Starting College Complaint System...
echo.

cd /d "%~dp0"

echo Checking Python...
python --version

echo.
echo Starting Student Portal...
echo.

call venv\Scripts\activate.bat

streamlit run student.py

echo.
echo Program stopped.
pause