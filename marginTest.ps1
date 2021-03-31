############################################
##############  INITIALIZING  ##############
############################################

$hostname = Read-Host "Please enter the hostname"
$start_power = Read-Host "Please enter the starting power"
$end_power = Read-Host "Please enter the end power"
$step_size = Read-Host "Please enter the power step size in dBM"
$power_duration = Read-Host "Please enter the Duration for each power step"
$tag_name = Read-Host "Please enter the name of the Tag"
$target_epc = Read-Host "Please enter the epc of the tag you are testing like so: '0000 1111 2222 3333'"

$pwd = $PSScriptRoot
$marginTestPath = Join-Path -Path $pwd -ChildPath "\MarginTest\bin\Debug\netcoreapp3.1\MarginTest.exe"
$python1Path = Join-Path -Path $pwd -ChildPath "main.py"
$python2Path = Join-Path -Path $pwd -ChildPath "aggregate.py"
$batchPath = Join-Path -Path $pwd -ChildPath "marginTest.bat"
$batch = "
@ECHO OFF
ECHO Activating Automation Environment 

ECHO This is a margin test automation tool, Starting margin test now!
START /wait $marginTestPath $hostname $start_power $end_power $step_size $power_duration $tag_name $target_epc
CALL activate tagtest_tool
python $python1Path --tag-names $tag_name
PAUSE
python $python2Path
CALL conda deactivate tagtest_tool
"

#########################################
##############  EXECUTING  ##############
#########################################


Set-Content -Path $batchPath -Value $batch
Start-Process $batchPath