# Import SCOM module (if not already loaded)
Import-Module OperationsManager

# Connect to the SCOM Management Group
$ManagementGroup = "<ManagementGroup>"  # Replace with your Management Group Name
New-SCOMManagementGroupConnection -ComputerName $ManagementGroup

# Output file path
$outputFile = "C:\SCOM_Rules_and_Thresholds.txt"

# Initialize a counter for numbering and a collection for results
$counter = 1
$outputContent = @()

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
        # Construct the text format for each rule
        $ruleDetails = @"
$counter. Rule Name:        $($rule.DisplayName)
    Rule ID:             $($rule.Id)
    Target Object:       $($rule.Target.DisplayName)
    Category:            $($rule.Category)
    Enabled:             $($rule.Enabled)
    Polling Interval:    $($rule.ScheduleDescription)
    Alert Severity:      $($rule.AlertSeverity)
    Description:         $($rule.Description)

"@
        # Add details to the output collection
        $outputContent += $ruleDetails
        $counter++
    } catch {
        Write-Warning "Error processing rule: $($rule.DisplayName)"
    }
}

# Write the output to the text file
$outputContent | Out-File -FilePath $outputFile -Encoding UTF8 -Force

Write-Host "Extraction complete. File saved at: $outputFile"
