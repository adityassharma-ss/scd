# Import the Operations Manager module
Import-Module OperationsManager -ErrorAction Stop

# Define Management Servers
$ManagementServers = @("awswcanvaw0003", "awswcanvaw0002")

# Define log file
$LogFile = "C:\SCOM_Reports\SCOM_DiskAlerts.log"

# Function to log messages
function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$Timestamp - $Message" | Out-File -Append -FilePath $LogFile
    Write-Host "$Timestamp - $Message"
}

# Start Logging
Write-Log "=== SCOM Disk Space Monitoring Started ==="

# Fetch all monitored Windows servers
try {
    $Servers = Get-SCOMClassInstance -Class (Get-SCOMClass -Name "Microsoft.Windows.Computer") | Where-Object { $_.DisplayName -match "awswcanvaw" }
} catch {
    Write-Log "❌ Error fetching monitored servers: $_"
    exit
}

if (-not $Servers) {
    Write-Log "⚠️ No servers found matching AWSW primary management group."
    exit
}

Write-Log "✅ Found $($Servers.Count) monitored servers."

# Define Alert Thresholds
$WarningThreshold = 20  # Warning if free space < 20%
$CriticalThreshold = 10 # Critical if free space < 10%

# Fetch Disk Data from Monitored Servers
foreach ($Server in $Servers) {
    $ServerName = $Server.DisplayName
    Write-Log "🔍 Checking disk space on $ServerName..."

    try {
        # Fetch Logical Disks monitored by SCOM
        $Disks = Get-SCOMClassInstance -Class (Get-SCOMClass -Name "Microsoft.Windows.LogicalDisk") | Where-Object { $_.Path -match $ServerName }
        
        if (-not $Disks) {
            Write-Log "⚠️ No disks found for $ServerName. Skipping."
            continue
        }

        foreach ($Disk in $Disks) {
            $DiskName = $Disk.DisplayName
            $FreeSpaceMB = [math]::Round($Disk.'Free Megabytes', 2)
            $TotalSpaceMB = [math]::Round($Disk.'Size Megabytes', 2)
            $FreePercentage = [math]::Round(($FreeSpaceMB / $TotalSpaceMB) * 100, 2)

            $AlertMessage = @"
---------------------------------------------
🖥️  Server       : $ServerName
💾 Disk         : $DiskName
📊 Total Space : $TotalSpaceMB MB
🆓 Free Space  : $FreeSpaceMB MB ($FreePercentage%)
---------------------------------------------
"@

            # Check Threshold and Simulate Alerting Logic
            if ($FreePercentage -lt $CriticalThreshold) {
                Write-Log "🚨 CRITICAL ALERT: $DiskName on $ServerName is below $CriticalThreshold% free space!"
                Write-Log $AlertMessage
            } elseif ($FreePercentage -lt $WarningThreshold) {
                Write-Log "⚠️ WARNING: $DiskName on $ServerName is below $WarningThreshold% free space."
                Write-Log $AlertMessage
            } else {
                Write-Log "✅ OK: $DiskName on $ServerName has sufficient free space ($FreePercentage%)."
            }
        }
    } catch {
        Write-Log "❌ Error checking disks on $ServerName: $_"
    }
}

Write-Log "✅ SCOM Disk Monitoring Completed."
