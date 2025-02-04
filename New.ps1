# Import SCOM module
Import-Module OperationsManager

# Define output file
$OutputFile = "C:\DiskAlertRules.csv"

# Get all monitors related to Disk
$DiskMonitors = Get-SCOMMonitor | Where-Object { $_.DisplayName -match "Disk" -or $_.Target.DisplayName -match "Disk" }

# Initialize results array
$Results = @()

foreach ($Monitor in $DiskMonitors) {
    # Get associated rules
    $Rules = Get-SCOMRule | Where-Object { $_.Target -eq $Monitor.Target }

    foreach ($Rule in $Rules) {
        # Get Override values if any
        $Overrides = Get-SCOMOverride | Where-Object { $_.Context -eq $Monitor.Target }

        # Get Default Threshold (if applicable)
        $Threshold = "N/A"
        if ($Monitor.Configuration -match '<Threshold>(.*?)</Threshold>') {
            $Threshold = $matches[1]
        }

        $Results += [PSCustomObject]@{
            MonitorName     = $Monitor.DisplayName
            RuleName        = $Rule.DisplayName
            RuleID          = $Rule.Id
            Enabled         = $Monitor.Enabled
            TargetClass     = $Monitor.Target.DisplayName
            Threshold       = $Threshold
            OverrideRules   = ($Overrides | Select-Object Property, Value -ExpandProperty Value) -join "; "
        }
    }
}

# Export results to CSV
$Results | Export-Csv -Path $OutputFile -NoTypeInformation

Write-Host "✅ Disk Alert Configuration exported to $OutputFile"
