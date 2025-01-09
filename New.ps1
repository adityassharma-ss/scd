Import-Module OperationsManager
New-SCOMManagementGroupConnection -ComputerName "Your-SCOM-Server"

# Get alerts for the specific server
$alerts = Get-SCOMAlert | Where-Object {$_.NetbiosComputerName -eq "AWSSPCPNVALT003"}

# Export alerts to CSV
$alerts | Select-Object Name, Severity, ResolutionState, TimeRaised, Description | Export-Csv -Path "C:\Alerts_AWSSPCPNVALT003.csv" -NoTypeInformation
