@echo off
cd %~dp0
:runbot
python runbot.py %*
pause
cls
goto runbot