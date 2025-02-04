# Import SCOM module (if using SCOM)
Import-Module OperationsManager

# Define Output File
$OutputFile = "C:\DiskAlertRules.csv"

# Fetch All Disk Alerting Rules
$DiskRules = Get-SCOMRule | Where-Object { $_.DisplayName -match "Disk" -or $_.Name -match "Disk" }

# Initialize results array
$Results = @()

foreach ($Rule in $DiskRules) {
    # Get Alert Criteria
    $Criteria = ($Rule | Get-SCOMAlertCriteria)

    # Get Overrides (if any thresholds are customized)
    $Overrides = Get-SCOMOverride | Where-Object { $_.Context -eq $Rule.MonitoringClass }

    # Extract Relevant Data
    $Results += [PSCustomObject]@{
        RuleName        = $Rule.DisplayName
        InternalName    = $Rule.Name
        Description     = $Rule.Description
        Enabled         = $Rule.Enabled
        TargetClass     = $Rule.Target.DisplayName
        MonitoringClass = $Rule.MonitoringClass.DisplayName
        AlertCriteria   = $Criteria
        OverrideRules   = ($Overrides | Select-Object Property, Value -ExpandProperty Value) -join "; "
    }
}

# Export Data to CSV
$Results | Export-Csv -Path $OutputFile -NoTypeInformation

Write-Host "✅ Disk Alert Configuration exported to $OutputFile"
