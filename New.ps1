# Import SCOM module (if not loaded)
Import-Module OperationsManager

# Connect to the SCOM Management Group
$ManagementGroup = "<ManagementGroup>"  # Replace with your Management Group name
New-SCOMManagementGroupConnection -ComputerName $ManagementGroup

# Output file
$outputFile = "C:\SCOM_AlertRules_Thresholds.csv"

# Initialize a collection for results
$results = @()

# Get all Windows Server-related rules
$rules = Get-SCOMRule | Where-Object { $_.Target.Name -like "*Windows Server*" }

# Process each rule
foreach ($rule in $rules) {
    $ruleDetails = @{
        RuleName           = $rule.DisplayName
        TargetObject       = $rule.Target.DisplayName
        Category           = $rule.Category
        Enabled            = $rule.Enabled
        AlertSeverity      = $rule.AlertSeverity
        PollingInterval    = $rule.ScheduleDescription
        TriggerCondition   = $rule.ConditionDetectionDisplayName
        AlertDescription   = $rule.Description
    }

    # Add the details to results
    $results += New-Object PSObject -Property $ruleDetails
}

# Export results to CSV
$results | Export-Csv -Path $outputFile -NoTypeInformation -Force

Write-Host "Extraction complete. File saved at: $outputFile"
