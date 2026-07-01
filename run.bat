@echo off
cd /d %~dp0

echo ==========================
echo RetailRocket Dashboard
echo ==========================

py -m pip install -r requirements.txt
py -m streamlit run 4_app/app.py

pause
