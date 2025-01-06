# Import SCOM module (if not already loaded)
Import-Module OperationsManager

# Connect to the SCOM Management Group
$ManagementGroup = "<ManagementGroup>"  # Replace with your Management Group Name
New-SCOMManagementGroupConnection -ComputerName $ManagementGroup

# Output file path
$outputFile = "C:\SCOM_Rules_and_Thresholds.csv"

# Initialize a collection for results
$results = @()

# Get all rules from SCOM
$rules = Get-SCOMRule

# Check if rules exist
if ($rules -eq $null -or $rules.Count -eq 0) {
    Write-Host "No rules found in the SCOM management group."
    exit
}

# Process each rule and extract details
foreach ($rule in $rules) {
    try {
        $ruleDetails = @{
            RuleName           = $rule.DisplayName
            RuleID             = $rule.Id
            TargetObject       = $rule.Target.DisplayName
            Category           = $rule.Category
            Enabled            = $rule.Enabled
            PollingInterval    = $rule.ScheduleDescription
            AlertSeverity      = $rule.AlertSeverity
            Description        = $rule.Description
        }

        # Add the details to the results array
        $results += New-Object PSObject -Property $ruleDetails
    } catch {
        Write-Warning "Error processing rule: $($rule.DisplayName)"
    }
}

# Export results to CSV
if ($results.Count -gt 0) {
    $results | Export-Csv -Path $outputFile -NoTypeInformation -Force
    Write-Host "Extraction complete. File saved at: $outputFile"
} else {
    Write-Host "No data to export. Please verify the rules in your SCOM environment."
}
