# Output file path
$outputFile = "C:\SCOM_Thresholds.txt"

# Initialize output content
$outputContent = @()

# Get all monitors and rules
$monitors = Get-SCOMMonitor
$rules = Get-SCOMRule

# Counter for numbering
$counter = 1

# Process monitors
foreach ($monitor in $monitors) {
    if ($monitor.Enabled -eq $true) {
        $thresholds = $monitor.Configuration
        $details = @"
$counter. Monitor Name:    $($monitor.DisplayName)
    Target Object:       $($monitor.Target.DisplayName)
    Threshold:           $thresholds
    Polling Interval:    $($monitor.ScheduleDescription)
    Alert Severity:      $($monitor.AlertSeverity)
    Description:         $($monitor.Description)

"@
        $outputContent += $details
        $counter++
    }
}

# Process rules
foreach ($rule in $rules) {
    if ($rule.Enabled -eq $true) {
        $thresholds = $rule.Configuration
        $details = @"
$counter. Rule Name:       $($rule.DisplayName)
    Target Object:       $($rule.Target.DisplayName)
    Threshold:           $thresholds
    Polling Interval:    $($rule.ScheduleDescription)
    Alert Severity:      $($rule.AlertSeverity)
    Description:         $($rule.Description)

"@
        $outputContent += $details
        $counter++
    }
}

# Write to file
$outputContent | Out-File -FilePath $outputFile -Encoding UTF8 -Force

Write-Host "Threshold and polling details saved to: $outputFile"
