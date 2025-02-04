# Import SCOM module
Import-Module OperationsManager

# Define output file
$OutputFile = "C:\SCOM_DiskAlertRules.csv"

# Fetch all disk space-related monitors
$DiskMonitors = Get-SCOMMonitor | Where-Object { $_.DisplayName -match "Disk Free Space" }

# Initialize results array
$Results = @()

foreach ($Monitor in $DiskMonitors) {
    # Get Associated Overrides
    $Overrides = Get-SCOMOverride | Where-Object { $_.Context -eq $Monitor.Target }

    # Extract thresholds (Warning, Critical)
    $WarningThreshold = "N/A"
    $CriticalThreshold = "N/A"

    if ($Monitor.Configuration -match '<UnderWarningThreshold>(.*?)</UnderWarningThreshold>') {
        $WarningThreshold = $matches[1]
    }

    if ($Monitor.Configuration -match '<OverErrorThreshold>(.*?)</OverErrorThreshold>') {
        $CriticalThreshold = $matches[1]
    }

    # Store data in an array
    $Results += [PSCustomObject]@{
        MonitorName       = $Monitor.DisplayName
        TargetClass       = $Monitor.Target.DisplayName
        HealthState       = $Monitor.HealthState
        WarningThreshold  = $WarningThreshold
        CriticalThreshold = $CriticalThreshold
        Overrides         = ($Overrides | Select-Object Property, Value -ExpandProperty Value) -join "; "
    }
}

# Export results to CSV
$Results | Export-Csv -Path $OutputFile -NoTypeInformation

Write-Host "✅ Disk Space Alert Configuration exported to $OutputFile"
