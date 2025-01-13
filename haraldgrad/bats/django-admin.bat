@echo off
@chcp 65001 > nul
SET /P appName="Введите имя для приложения:"
python ..\manage.py startapp %appName%
pause