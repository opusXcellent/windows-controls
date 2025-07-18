# windows-controls

PowerShell Admin Setup

# Create folder
New-Item -ItemType Directory -Force -Path "C:\ParentalControl"

# Copy files
Copy-Item ".\parental_control_monitor.py" "C:\ParentalControl\parental_control_monitor.py"
Copy-Item ".\timer_overlay.pyw" "C:\ParentalControl\timer_overlay.pyw"
Copy-Item ".\user_time_limits.json" "C:\ParentalControl\user_time_limits.json"

# Protect folder
icacls "C:\ParentalControl" /inheritance:r /grant:r "Administrators:F"

# Setup task for monitor
$action1 = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\ParentalControl\parental_control_monitor.py"
$trigger1 = New-ScheduledTaskTrigger -AtLogOn
$principal1 = New-ScheduledTaskPrincipal -GroupId "Users" -RunLevel Highest
Register-ScheduledTask -TaskName "ParentalControlMonitor" -Action $action1 -Trigger $trigger1 -Principal $principal1 -Force

# Setup task for timer overlay
$action2 = New-ScheduledTaskAction -Execute "pythonw.exe" -Argument "C:\ParentalControl\timer_overlay.pyw"
$trigger2 = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "ParentalControlTimerOverlay" -Action $action2 -Trigger $trigger2 -Principal $principal1 -Force
