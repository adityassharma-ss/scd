# Import SCOM PowerShell module
Import-Module OperationsManager

# Script Parameters
param(
    [string]$OutputPath = "C:\SCOM_Reports",
    [string]$ReportName = "DiskSpaceAlerts_$(Get-Date -Format 'yyyyMMdd')",
    [int]$DaysToCheck = 7
)

# Create output directory if it doesn't exist
if (!(Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null
}

# Initialize logging
$LogFile = Join-Path $OutputPath "DiskMonitor.log"
function Write-Log {
    param($Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "$Timestamp - $Message"
    Add-Content -Path $LogFile -Value $LogEntry
    Write-Host $LogEntry
}

try {
    Write-Log "Starting disk space alert collection from SCOM"

    # Connect to SCOM Management Server
    $ManagementServer = Get-SCOMManagementServer | Where-Object {$_.IsGateway -eq $false} | Select-Object -First 1
    
    if (!$ManagementServer) {
        throw "No SCOM Management Server found"
    }

    # Get active alerts from recent days
    $StartDate = (Get-Date).AddDays(-$DaysToCheck)
    $Alerts = Get-SCOMAlert | Where-Object {
        $_.ResolutionState -ne 255 -and
        $_.TimeRaised -gt $StartDate -and
        ($_.MonitoringObjectDisplayName -match "Logical Disk" -or
         $_.MonitoringObjectDisplayName -match "Storage Space")
    }

    # Get all disk monitors for threshold information
    $DiskMonitors = Get-SCOMMonitor | Where-Object {
        $_.DisplayName -match "Logical Disk Free Space"
    }

    # Prepare report data
    $ReportData = foreach ($Alert in $Alerts) {
        $Monitor = $DiskMonitors | Where-Object {$_.Id -eq $Alert.MonitoringRuleId}
        
        # Extract thresholds from monitor configuration
        $WarningThreshold = "N/A"
        $CriticalThreshold = "N/A"
        
        if ($Monitor) {
            $Config = $Monitor.Configuration
            if ($Config -match '<WarningThreshold>(.*?)</WarningThreshold>') {
                $WarningThreshold = $matches[1]
            }
            if ($Config -match '<CriticalThreshold>(.*?)</CriticalThreshold>') {
                $CriticalThreshold = $matches[1]
            }
        }

        # Create report entry
        [PSCustomObject]@{
            TimeGenerated = $Alert.TimeRaised
            Server = $Alert.MonitoringObjectDisplayName.Split('\')[0]
            Drive = ($Alert.MonitoringObjectDisplayName -split '\\')[-1]
            AlertName = $Alert.Name
            Severity = switch($Alert.Severity) {
                0 { "Information" }
                1 { "Warning" }
                2 { "Critical" }
                default { "Unknown" }
            }
            WarningThreshold = $WarningThreshold
            CriticalThreshold = $CriticalThreshold
            Description = $Alert.Description -replace '\s+', ' '
            RepeatCount = $Alert.RepeatCount
            ResolutionState = switch($Alert.ResolutionState) {
                0 { "New" }
                1 { "Acknowledged" }
                254 { "Resolved" }
                255 { "Closed" }
                default { $Alert.ResolutionState }
            }
        }
    }

    # Export to CSV
    $CSVPath = Join-Path $OutputPath "$ReportName.csv"
    $ReportData | Export-Csv -Path $CSVPath -NoTypeInformation
    Write-Log "Exported alert data to $CSVPath"
    Write-Log "Total alerts exported: $($ReportData.Count)"

} catch {
    $ErrorMessage = "Error: $_"
    Write-Log $ErrorMessage
    throw $ErrorMessage
} finally {
    Write-Log "Script execution completed"
}
