# Import SCOM module
Import-Module OperationsManager

# Connect to SCOM
$ManagementGroup = "<ManagementGroup>"  # Replace with your Management Group
New-SCOMManagementGroupConnection -ComputerName $ManagementGroup

# Output file
$outputFile = "C:\SCOM_Thresholds_Debugged.txt"

# Initialize counter and output
$counter = 1
$outputContent = @()

# Fetch rules and monitors
$rules = Get-SCOMRule
$monitors = Get-SCOMMonitor

# Debug counts
Write-Host "Total rules: $($rules.Count)"
Write-Host "Total monitors: $($monitors.Count)"

# Process monitors
foreach ($monitor in $monitors) {
    try {
        Write-Host "Processing Monitor: $($monitor.DisplayName)"
        $thresholds = $monitor.Configuration
        $details = @"
$counter. Monitor Name:    $($monitor.DisplayName)
    Target Object:       $($monitor.Target.DisplayName)
    Threshold:           $thresholds
    Polling Interval:    $($monitor.ScheduleDescription)
    Alert Severity:      $($monitor.AlertSeverity)
    Description:         $($monitor.Description)

"@
        Write-Host $details
        $outputContent += $details
        $counter++
    } catch {
        Write-Warning "Failed to process monitor: $($monitor.DisplayName)"
    }
}

# Process rules
foreach ($rule in $rules) {
    try {
        Write-Host "Processing Rule: $($rule.DisplayName)"
        $thresholds = $rule.Configuration
        $details = @"
$counter. Rule Name:       $($rule.DisplayName)
    Target Object:       $($rule.Target.DisplayName)
    Threshold:           $thresholds
    Polling Interval:    $($rule.ScheduleDescription)
    Alert Severity:      $($rule.AlertSeverity)
    Description:         $($rule.Description)

"@
        Write-Host $details
        $outputContent += $details
        $counter++
    } catch {
        Write-Warning "Failed to process rule: $($rule.DisplayName)"
    }
}

# Write output to file
$outputContent | Out-File -FilePath $outputFile -Encoding UTF8 -Force

Write-Host "Processing complete. File saved at: $outputFile"
