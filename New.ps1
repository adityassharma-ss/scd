# Import SCOM PowerShell module
Import-Module OperationsManager

# Set SCOM Management Server
$ManagementServer = "SCOM-MGMT-Server"

# Connect to SCOM Management Server
New-SCOMManagementGroupConnection -ComputerName $ManagementServer

# Define current and proposed thresholds
$currentWarningThreshold = 10    # Current Warning threshold
$currentCriticalThreshold = 5    # Current Critical threshold
$proposedWarningThreshold = 15   # Proposed Warning threshold
$proposedCriticalThreshold = 10  # Proposed Critical threshold
$severeCriticalThreshold = 5     # Severe Critical threshold

# Get all monitored Windows Servers
$servers = Get-SCOMMonitoringObject -Class (Get-SCOMClass -Name "Microsoft.Windows.Server.Computer")

# Initialize arrays to store results
$currentBreaches = @()
$proposedBreaches = @()

# Iterate through each server to check disk space
foreach ($server in $servers) {
    # Get all logical disks for the server
    $disks = Get-SCOMMonitoringObject -Class (Get-SCOMClass -Name "Microsoft.Windows.LogicalDisk") | 
             Where-Object { $_.Path -match $server.DisplayName }
    
    foreach ($disk in $disks) {
        # Get free space percentage
        $diskHealth = $disk.GetMonitoringPerformanceData() | 
                     Where-Object { $_.CounterName -eq "Free Megabytes" }
        
        $totalSize = $diskHealth | 
                    Where-Object { $_.InstanceName -eq "_Total" } | 
                    Select-Object -ExpandProperty CookedValue
        
        $freeSpace = $diskHealth | 
                    Where-Object { $_.InstanceName -ne "_Total" } | 
                    Select-Object -ExpandProperty CookedValue
        
        if ($totalSize -and $freeSpace) {
            $freePercent = [math]::Round(($freeSpace / $totalSize) * 100, 2)
            
            # Check current thresholds
            $currentStatus = "Healthy"
            if ($freePercent -le $currentWarningThreshold -and $freePercent -gt $currentCriticalThreshold) {
                $currentStatus = "Warning"
            }
            elseif ($freePercent -le $currentCriticalThreshold) {
                $currentStatus = "Critical"
            }
            
            # Check proposed thresholds
            $proposedStatus = "Healthy"
            if ($freePercent -le $proposedWarningThreshold -and $freePercent -gt $proposedCriticalThreshold) {
                $proposedStatus = "Warning"
            }
            elseif ($freePercent -le $proposedCriticalThreshold -and $freePercent -gt $severeCriticalThreshold) {
                $proposedStatus = "Critical"
            }
            elseif ($freePercent -le $severeCriticalThreshold) {
                $proposedStatus = "Severe Critical"
            }
            
            # Store results if there's a breach in either current or proposed thresholds
            if ($currentStatus -ne "Healthy" -or $proposedStatus -ne "Healthy") {
                $result = [PSCustomObject]@{
                    ServerName = $server.DisplayName
                    Disk = $disk.Path
                    TotalSizeMB = $totalSize
                    FreeSpaceMB = $freeSpace
                    FreeSpacePercent = $freePercent
                    CurrentStatus = $currentStatus
                    ProposedStatus = $proposedStatus
                }
                
                if ($currentStatus -ne "Healthy") { $currentBreaches += $result }
                if ($proposedStatus -ne "Healthy") { $proposedBreaches += $result }
            }
        }
    }
}

# Generate summary report
Write-Host "`nCurrent Threshold Breaches:" -ForegroundColor Yellow
Write-Host "Warning (≤ 10%): $($currentBreaches.Where({$_.CurrentStatus -eq 'Warning'}).Count) servers"
Write-Host "Critical (≤ 5%): $($currentBreaches.Where({$_.CurrentStatus -eq 'Critical'}).Count) servers"

Write-Host "`nProposed Threshold Breaches:" -ForegroundColor Cyan
Write-Host "Warning (≤ 15%): $($proposedBreaches.Where({$_.ProposedStatus -eq 'Warning'}).Count) servers"
Write-Host "Critical (≤ 10%): $($proposedBreaches.Where({$_.ProposedStatus -eq 'Critical'}).Count) servers"
Write-Host "Severe Critical (≤ 5%): $($proposedBreaches.Where({$_.ProposedStatus -eq 'Severe Critical'}).Count) servers"

# Export detailed results
$csvPath = "C:\SCOM_Disk_Space_Analysis.csv"
$proposedBreaches | Export-Csv -Path $csvPath -NoTypeInformation
Write-Host "`n✅ Detailed report saved to: $csvPath" -ForegroundColor Green
