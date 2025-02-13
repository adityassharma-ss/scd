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
    Write-Host "Processing server: $($server.DisplayName)" -ForegroundColor Gray
    
    # Get all logical disks for the server
    $disks = Get-SCOMMonitoringObject -Class (Get-SCOMClass -Name "Microsoft.Windows.LogicalDisk") | 
             Where-Object { $_.Path -match $server.DisplayName }
    
    foreach ($disk in $disks) {
        try {
            # Get disk space metrics
            $diskProperties = $disk.GetMonitoringPropertyCollection()
            
            # Get free space percentage
            $freeSpacePercentage = $diskProperties | 
                Where-Object { $_.Name -eq "PercentFreeSpace" } | 
                Select-Object -ExpandProperty Value
            
            # Get total size and free space
            $totalSize = $diskProperties | 
                Where-Object { $_.Name -eq "Size" } | 
                Select-Object -ExpandProperty Value
            
            $freeSpace = $diskProperties | 
                Where-Object { $_.Name -eq "FreeSpace" } | 
                Select-Object -ExpandProperty Value
            
            if ($null -ne $freeSpacePercentage) {
                $freePercent = [math]::Round($freeSpacePercentage, 2)
                $totalSizeMB = [math]::Round($totalSize / 1MB, 2)
                $freeSpaceMB = [math]::Round($freeSpace / 1MB, 2)
                
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
                        DriveLetter = $disk.DisplayName
                        TotalSizeGB = [math]::Round($totalSizeMB / 1024, 2)
                        FreeSpaceGB = [math]::Round($freeSpaceMB / 1024, 2)
                        FreeSpacePercent = $freePercent
                        CurrentStatus = $currentStatus
                        ProposedStatus = $proposedStatus
                        LastUpdated = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                    }
                    
                    if ($currentStatus -ne "Healthy") { $currentBreaches += $result }
                    if ($proposedStatus -ne "Healthy") { $proposedBreaches += $result }
                    
                    # Write immediate feedback for breaches
                    Write-Host "  Drive $($disk.DisplayName) - Free Space: $freePercent% - Status: $proposedStatus" -ForegroundColor Yellow
                }
            }
        }
        catch {
            Write-Warning "Error processing disk $($disk.DisplayName) on server $($server.DisplayName): $_"
            continue
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
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$csvPath = "C:\SCOM_Disk_Space_Analysis_$timestamp.csv"
$proposedBreaches | Export-Csv -Path $csvPath -NoTypeInformation

Write-Host "`n✅ Detailed report saved to: $csvPath" -ForegroundColor Green
Write-Host "`nTotal servers analyzed: $($servers.Count)"
Write-Host "Total current breaches: $($currentBreaches.Count)"
Write-Host "Total proposed breaches: $($proposedBreaches.Count)"
