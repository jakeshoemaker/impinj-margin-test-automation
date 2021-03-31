
@ECHO OFF
ECHO Activating Automation Environment 

ECHO This is a margin test automation tool, Starting margin test now!
START /wait C:\Users\jshoemaker\Desktop\tagtest_tool\MarginTest\bin\Debug\netcoreapp3.1\MarginTest.exe 192.3.2.101 20 25 1 3 DOPE 0
CALL activate tagtest_tool
python C:\Users\jshoemaker\Desktop\tagtest_tool\main.py --tag-names DOPE
PAUSE
python C:\Users\jshoemaker\Desktop\tagtest_tool\aggregate.py
CALL conda deactivate tagtest_tool

