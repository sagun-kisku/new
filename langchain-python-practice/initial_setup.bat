@echo off

REM Step 1: Create python virtual environment
echo Creating Python virtual environment.......
python -m venv venv

REM Step 2: Activate virtual environment
echo Activating the virtual environment........
call .\venv\Scripts\activate.bat

REM Step 3: Upgrading pip
echo Upgrading the pip
python.exe -m pip install --upgrade pip

REM Step 4: Install requirements
echo Installing requirements file
pip install -r requirements.txt

