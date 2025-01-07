# Import SCOM module
Import-Module OperationsManager

# Reset the specific monitor
$monitor = Get-SCOMMonitor -Name "*HTTP*Error*"
$instance = Get-SCOMClassInstance -Name "vmcitsnaw00g9"
Reset-SCOMMonitoringState -Instance $instance -Monitor $monitor -Confirm:$false
