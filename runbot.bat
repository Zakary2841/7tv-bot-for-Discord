@echo off
cd %~dp0
:runbot
python runbot.py %*
timeout /t 10
cls
goto runbot