# Import SCOM module
Import-Module OperationsManager

# Define the output file
$outputFile = "C:\MonitorDetails.txt"

# Connect to the SCOM management group
$ManagementGroup = Get-SCOMManagementGroupConnection

# Fetch all monitors
$monitors = Get-SCOMMonitor

# Initialize output content
$outputContent = @()

# Iterate through each monitor and gather details
foreach ($monitor in $monitors) {
    $monitorDetails = @{
        Name             = $monitor.DisplayName
        Target           = $monitor.Target
        Type             = $monitor.MonitorType
        InheritedFrom    = $monitor.InheritsFrom
        ManagementPack   = $monitor.ManagementPackName
        Enabled          = $monitor.Enabled
        IntervalSeconds  = ""
        Threshold        = ""
        TimeoutSeconds   = ""
        Configuration    = $monitor.Configuration
    }

    # Extract specific configurations (if available)
    if ($monitor.Configuration -match "<IntervalSeconds>(\d+)</IntervalSeconds>") {
        $monitorDetails.IntervalSeconds = $matches[1]
    }
    if ($monitor.Configuration -match "<Threshold>(\d+)</Threshold>") {
        $monitorDetails.Threshold = $matches[1]
    }
    if ($monitor.Configuration -match "<TimeoutSeconds>(\d+)</TimeoutSeconds>") {
        $monitorDetails.TimeoutSeconds = $matches[1]
    }

    # Add structured details to output content
    $outputContent += "---------------------------------------------"
    $outputContent += "Monitor Name      : $($monitorDetails.Name)"
    $outputContent += "Target            : $($monitorDetails.Target)"
    $outputContent += "Type              : $($monitorDetails.Type)"
    $outputContent += "Inherited From    : $($monitorDetails.InheritedFrom)"
    $outputContent += "Management Pack   : $($monitorDetails.ManagementPack)"
    $outputContent += "Enabled           : $($monitorDetails.Enabled)"
    $outputContent += "Interval Seconds  : $($monitorDetails.IntervalSeconds)"
    $outputContent += "Threshold         : $($monitorDetails.Threshold)"
    $outputContent += "Timeout Seconds   : $($monitorDetails.TimeoutSeconds)"
    $outputContent += "Configuration     : $($monitorDetails.Configuration)"
    $outputContent += "---------------------------------------------"
}

# Write the structured details to a file
$outputContent | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "Monitor details have been exported to $outputFile"
