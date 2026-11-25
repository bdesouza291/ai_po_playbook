@echo off
rem Thin wrapper: finds a working Python and runs scripts\pdlc.py with the same arguments.
rem Exists so permission rules (and people) have one command to use, whatever the interpreter is called.
python -c "import sys" >nul 2>&1
if not errorlevel 1 goto usepython
python3 -c "import sys" >nul 2>&1
if not errorlevel 1 goto usepython3
py -3 -c "import sys" >nul 2>&1
if not errorlevel 1 goto usepy
echo pdlc: no working Python (python, python3 or py) found on PATH. 1>&2
exit /b 127
:usepython
python "%~dp0pdlc.py" %*
exit /b %errorlevel%
:usepython3
python3 "%~dp0pdlc.py" %*
exit /b %errorlevel%
:usepy
py -3 "%~dp0pdlc.py" %*
exit /b %errorlevel%
