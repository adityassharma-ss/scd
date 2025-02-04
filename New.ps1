# Import SCOM Module
Import-Module OperationsManager -ErrorAction Stop

# Define log file
$LogFile = "C:\SCOM_Reports\SCOM_Alerts.log"

# Function to log messages
function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$Timestamp - $Message" | Out-File -Append -FilePath $LogFile
    Write-Host "$Timestamp - $Message"
}

# Start Logging
Write-Log "=== SCOM Alert Monitoring Started ==="

# Get Active Alerts
try {
    $Alerts = Get-SCOMAlert | Where-Object { $_.ResolutionState -ne 255 }  # Exclude resolved alerts
} catch {
    Write-Log "❌ Error fetching alerts: $_"
    exit
}

# Check if alerts exist
if (-not $Alerts) {
    Write-Log "✅ No active alerts found."
    exit
}

# Process Alerts
Write-Log "⚠️  Found $($Alerts.Count) active alerts!"

foreach ($Alert in $Alerts) {
    $AlertDetails = @"
---------------------------------------------
🔴 Alert Name        : $($Alert.Name)
🔧 Monitoring Rule   : $($Alert.MonitoringRule.DisplayName)
📌 Source           : $($Alert.MonitoringObject.DisplayName)
⚠️  Severity         : $($Alert.Severity)
🚨 Resolution State : $($Alert.ResolutionState)
👤 Owner            : $($Alert.Owner -join ', ')
📝 Description      : $($Alert.Description)
📅 Generated On     : $($Alert.TimeRaised)
---------------------------------------------
"@
    Write-Log $AlertDetails
}

Write-Log "✅ Alert monitoring completed successfully."
