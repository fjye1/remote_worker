@echo off
echo %TIME% Script starting >> "%USERPROFILE%\Desktop\task_log.txt"
cd /d "C:\Users\Frede\PycharmProjects\Remote_Worker"
echo %TIME% Running script >> "%USERPROFILE%\Desktop\task_log.txt"
"venv\Scripts\python.exe" run_worker.py >> "%USERPROFILE%\Desktop\worker_log.txt" 2>&1
echo %TIME% Script completed >> "%USERPROFILE%\Desktop\task_log.txt"