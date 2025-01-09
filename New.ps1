# Import SCOM module
Import-Module OperationsManager

# Connect to the SCOM management group
New-SCOMManagementGroupConnection -ComputerName "Your-SCOM-Server"

# Get alerts for the specific server
$alerts = Get-SCOMAlert | Where-Object {$_.NetbiosComputerName -eq "AWSSPCPNVALT003"}

# Select relevant fields and export to a text file
$alerts | ForEach-Object {
    "Alert Name: $($_.Name)"
    "Severity: $($_.Severity)"
    "Resolution State: $($_.ResolutionState)"
    "Time Raised: $($_.TimeRaised)"
    "Description: $($_.Description)"
    "------------------------------------------"
} | Out-File -FilePath "C:\Alerts_AWSSPCPNVALT003.txt" -Encoding UTF8
