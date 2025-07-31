@echo off
cd /d "C:\Path\To\Your\Project"
call venv\Scripts\activate.bat
python run_worker.py
exit