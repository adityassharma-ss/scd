# Import SCOM Module
Import-Module OperationsManager

# Define output file
$OutputFile = "C:\DiskAlertRules.csv"

# Fetch all alerting rules related to Disk Monitoring
$DiskRules = Get-SCOMRule | Where-Object { $_.DisplayName -match "Disk" -or $_.Name -match "Disk" }

# Initialize results array
$Results = @()

foreach ($Rule in $DiskRules) {
    # Get Monitors Associated with this Rule
    $Monitors = Get-SCOMMonitor | Where-Object { $_.Target -eq $Rule.Target }

    # Get Overrides if any exist
    $Overrides = Get-SCOMOverride | Where-Object { $_.Context -eq $Rule.MonitoringClass }

    foreach ($Monitor in $Monitors) {
        # Extract thresholds (for disk space alerts)
        $Thresholds = ($Monitor | Get-SCOMMonitorProperty -Property "Threshold") -join ", "

        $Results += [PSCustomObject]@{
            RuleName        = $Rule.DisplayName
            InternalName    = $Rule.Name
            Description     = $Rule.Description
            Enabled         = $Rule.Enabled
            TargetClass     = $Rule.Target.DisplayName
            MonitoringClass = $Rule.MonitoringClass.DisplayName
            AlertThreshold  = $Thresholds
            OverrideRules   = ($Overrides | Select-Object Property, Value -ExpandProperty Value) -join "; "
        }
    }
}

# Export results to CSV
$Results | Export-Csv -Path $OutputFile -NoTypeInformation

Write-Host "✅ Disk Alert Configuration exported to $OutputFile"
