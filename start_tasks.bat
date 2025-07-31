@echo off
cd /d "C:\Users\Frede\PycharmProjects\remote_worker\start_tasks.bat"
call venv\Scripts\activate.bat
python run_worker.py
exit