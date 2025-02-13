# Import SCOM PowerShell module (needed for remote execution)
Import-Module OperationsManager

# Set SCOM Management Server (Update this with your actual SCOM server)
$ManagementServer = "SCOM-MGMT-Server"

# Connect to SCOM Management Server
New-SCOMManagementGroupConnection -ComputerName $ManagementServer

# Define threshold values
$warningThreshold = 15  # New Warning threshold (was 10)
$criticalThreshold = 10 # New Critical threshold (was 5)
$severeCriticalThreshold = 5  # Severe critical threshold

# Get all monitored Windows Servers
$servers = Get-SCOMMonitoringObject -Class (Get-SCOMClass -Name "Microsoft.Windows.Server.Computer")

# Initialize an array to store results
$results = @()

# Iterate through each server to check disk space
foreach ($server in $servers) {
    # Get all logical disks for the server
    $disks = Get-SCOMMonitoringObject -Class (Get-SCOMClass -Name "Microsoft.Windows.LogicalDisk") | 
             Where-Object { $_.Path -match $server.DisplayName }

    foreach ($disk in $disks) {
        # Get free space percentage
        $diskHealth = $disk.GetMonitoringPerformanceData() | Where-Object { $_.CounterName -eq "Free Megabytes" }
        $totalSize = $diskHealth | Where-Object { $_.InstanceName -eq "_Total" } | Select-Object -ExpandProperty CookedValue
        $freeSpace = $diskHealth | Where-Object { $_.InstanceName -ne "_Total" } | Select-Object -ExpandProperty CookedValue

        if ($totalSize -and $freeSpace) {
            $freePercent = [math]::Round(($freeSpace / $totalSize) * 100, 2)

            # Determine severity
            $status = "Healthy"
            if ($freePercent -le $warningThreshold -and $freePercent -gt $criticalThreshold) { $status = "Warning" }
            elseif ($freePercent -le $criticalThreshold -and $freePercent -gt $severeCriticalThreshold) { $status = "Critical" }
            elseif ($freePercent -le $severeCriticalThreshold) { $status = "Severe Critical" }

            # Store result in an array
            $results += [PSCustomObject]@{
                ServerName = $server.DisplayName
                Disk = $disk.Path
                TotalSizeMB = $totalSize
                FreeSpaceMB = $freeSpace
                FreeSpacePercent = $freePercent
                Status = $status
            }
        }
    }
}

# Define CSV file path
$csvPath = "C:\SCOM_Disk_Space_Report.csv"

# Export results to CSV
$results | Export-Csv -Path $csvPath -NoTypeInformation

# Display completion message
Write-Host "`n✅ Report saved to: $csvPath" -ForegroundColor Green

