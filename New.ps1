# Import SCOM module
Import-Module OperationsManager

# Connect to SCOM
$ManagementGroup = "<Your Management Group>"  # Replace with your Management Group
New-SCOMManagementGroupConnection -ComputerName $ManagementGroup

# Output file
$outputFile = "C:\SCOM_Thresholds_for_Servers.txt"

# Initialize counter and output content
$counter = 1
$outputContent = @()

# Fetch all Windows servers (you can filter these by class if needed)
$windowsServers = Get-SCOMAgent | Where-Object {$_.OperatingSystem -like "Windows*"}

# Debugging output for monitored servers
Write-Host "Total monitored Windows servers: $($windowsServers.Count)"

# Loop through each Windows server
foreach ($server in $windowsServers) {
    try {
        Write-Host "Processing server: $($server.FullName)"
        
        # Fetch the rules applied to the server
        $serverRules = Get-SCOMMonitor | Where-Object {$_.Target -eq $server}

        # Process each rule
        foreach ($rule in $serverRules) {
            Write-Host "Fetching rule: $($rule.DisplayName)"
            
            # Assuming threshold data is stored in 'Configuration' or 'Thresholds'
            $thresholds = $rule.Configuration  # Or a specific property that holds thresholds
            $alertCriteria = $rule.ScheduleDescription # Or other fields

            # Structure the data for output
            $details = @"
$counter. Server:           $($server.FullName)
    Rule:                 $($rule.DisplayName)
    Thresholds:           $thresholds
    Alert Criteria:       $alertCriteria
    Description:          $($rule.Description)

"@
            $outputContent += $details
            $counter++
        }

    } catch {
        Write-Warning "Failed to process server: $($server.FullName)"
    }
}

# Write output to the file
$outputContent | Out-File -FilePath $outputFile -Encoding UTF8 -Force

Write-Host "Processing complete. File saved at: $outputFile"
