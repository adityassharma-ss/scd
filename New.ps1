Import-Module OperationsManager

New-SCOMManagementGroupConnection -ComputerName "Your-SCOM-Server"

$serverName = "AWSSPCPNVALT003"

$allAlerts = Get-SCOMAlert | Where-Object {
    $_.NetbiosComputerName -eq $serverName
}

$diskAlerts = $allAlerts | Where-Object {
    $_.Name -like "*Disk*" -or $_.Description -like "*disk*"
}

$currentDiskUsage = Get-PSDrive | Where-Object {
    $_.Provider -eq "FileSystem"
} | ForEach-Object {
    [PSCustomObject]@{
        Drive         = $_.Name
        UsedSpaceGB   = [math]::round(($_.Used / 1GB), 2)
        FreeSpaceGB   = [math]::round(($_.Free / 1GB), 2)
        TotalSpaceGB  = [math]::round(($_.Used + $_.Free) / 1GB, 2)
    }
}

$outputFile = "C:\ServerReport_$serverName.txt"

@"
##########################################
# Server Report for $serverName
##########################################
"@ | Out-File -FilePath $outputFile -Encoding UTF8

"### All Alerts for $serverName ###" | Out-File -Append -FilePath $outputFile
$allAlerts | Format-Table Name, Severity, ResolutionState, TimeRaised, Description -AutoSize | Out-String | Out-File -Append -FilePath $outputFile

"`n### Disk Space Alerts for $serverName ###" | Out-File -Append -FilePath $outputFile
$diskAlerts | Format-Table Name, Severity, ResolutionState, TimeRaised, Description -AutoSize | Out-String | Out-File -Append -FilePath $outputFile

"`n### Current Disk Usage for $serverName ###" | Out-File -Append -FilePath $outputFile
$currentDiskUsage | Format-Table Drive, UsedSpaceGB, FreeSpaceGB, TotalSpaceGB -AutoSize | Out-String | Out-File -Append -FilePath $outputFile

Write-Host "Structured report generated: $outputFile"
