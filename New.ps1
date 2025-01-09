
# Import SCOM module
Import-Module OperationsManager

# Connect to the SCOM management group
New-SCOMManagementGroupConnection -ComputerName "Your-SCOM-Server"

# Server to query
$serverName = "AWSSPCPNVALT003"

# Fetch all alerts for the server
$allAlerts = Get-SCOMAlert | Where-Object {
    $_.NetbiosComputerName -eq $serverName
}

# Fetch disk space-specific alerts for the server
$diskAlerts = $allAlerts | Where-Object {
    $_.Name -like "*Disk*" -or $_.Description -like "*disk*"
}

# Get current disk usage for the server
$currentDiskUsage = Get-PSDrive | Where-Object {
    $_.Provider -eq "FileSystem"
} | ForEach-Object {
    @{
        Drive = $_.Name
        UsedSpaceGB = [math]::round(($_.Used / 1GB), 2)
        FreeSpaceGB = [math]::round(($_.Free / 1GB), 2)
        TotalSpaceGB = [math]::round(($_.Used + $_.Free) / 1GB, 2)
    }
}

# Output all data to a single file
$outputFile = "C:\ServerReport_$serverName.txt"

# Write all alerts
"### All Alerts for $serverName ###" | Out-File -FilePath $outputFile -Encoding UTF8
$allAlerts | ForEach-Object {
    "Alert Name: $($_.Name)"
    "Severity: $($_.Severity)"
    "Resolution State: $($_.ResolutionState)"
    "Time Raised: $($_.TimeRaised)"
    "Description: $($_.Description)"
    "------------------------------------------"
} | Out-File -Append -FilePath $outputFile

# Write disk space-specific alerts
"`n### Disk Space Alerts for $serverName ###" | Out-File -Append -FilePath $outputFile
$diskAlerts | ForEach-Object {
    "Alert Name: $($_.Name)"
    "Severity: $($_.Severity)"
    "Resolution State: $($_.ResolutionState)"
    "Time Raised: $($_.TimeRaised)"
    "Description: $($_.Description)"
    "------------------------------------------"
} | Out-File -Append -FilePath $outputFile

# Write current disk usage
"`n### Current Disk Usage for $serverName ###" | Out-File -Append -FilePath $outputFile
$currentDiskUsage | ForEach-Object {
    "Drive: $($_.Drive)"
    "Used Space: $($_.UsedSpaceGB) GB"
    "Free Space: $($_.FreeSpaceGB) GB"
    "Total Space: $($_.TotalSpaceGB) GB"
    "------------------------------------------"
} | Out-File -Append -FilePath $outputFile

# Inform the user
Write-Host "Report generated: $outputFile"
