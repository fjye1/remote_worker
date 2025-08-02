@echo off
REM Change directory to your local project folder
cd /d "C:\Users\Frede\PycharmProjects\Remote_Worker"

REM Activate your virtual environment
call .venv\Scripts\activate.bat

REM Run your script
python run_worker.py

REM Pause so you can see any errors (remove this line when stable)
pause