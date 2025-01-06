# Import the SCOM module
Import-Module OperationsManager

# Connect to SCOM Management Server
$ManagementGroup = "<Your Management Group>"  # Replace with your Management Group name
New-SCOMManagementGroupConnection -ComputerName $ManagementGroup

# Output file path
$outputFile = "C:\SCOM_Thresholds_for_Servers.txt"

# Initialize the output content array
$outputContent = @()
$counter = 1

# Fetch all Windows servers monitored by SCOM
$windowsServers = Get-SCOMAgent | Where-Object { $_.OperatingSystem -like "Windows*" }

# Check if any servers are found
if ($windowsServers.Count -eq 0) {
    Write-Host "No Windows servers found. Check the SCOM connection and agents."
    exit
}

Write-Host "Total Windows servers monitored: $($windowsServers.Count)"

# Iterate through each Windows server
foreach ($server in $windowsServers) {
    Write-Host "Processing server: $($server.FullName)"
    
    try {
        # Fetch all monitors and rules for the server
        $serverMonitors = Get-SCOMMonitor | Where-Object { $_.Target -eq $server.GetType().Name }

        # Iterate over each monitor to extract relevant threshold and alert data
        foreach ($monitor in $serverMonitors) {
            Write-Host "Fetching monitor: $($monitor.DisplayName)"
            
            # Fetch thresholds (This depends on the monitor type, might need more customization)
            $thresholds = $monitor.Configuration  # Assuming the thresholds are in 'Configuration'
            $alertCriteria = $monitor.ScheduleDescription  # Assuming alert criteria can be found here
            
            # If no threshold or criteria found, continue to next monitor
            if (-not $thresholds -or -not $alertCriteria) {
                continue
            }
            
            # Format the data for this server and monitor
            $details = @"
$counter. Server:            $($server.FullName)
    Monitor Name:            $($monitor.DisplayName)
    Thresholds:              $thresholds
    Alert Criteria:          $alertCriteria
    Description:             $($monitor.Description)

"@
            $outputContent += $details
            $counter++
        }

    } catch {
        Write-Warning "Failed to process server: $($server.FullName)"
    }
}

# Write the output content to a file
if ($outputContent.Count -gt 0) {
    $outputContent | Out-File -FilePath $outputFile -Encoding UTF8 -Force
    Write-Host "Processing complete. File saved at: $outputFile"
} else {
    Write-Host "No threshold data found for the monitored servers."
}
