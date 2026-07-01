@echo off
cd /d %~dp0

echo ==========================
echo RetailRocket Dashboard
echo ==========================

pip install -r requirements.txt

streamlit run 4_app/app.py

pause