# Import the SCOM module
Import-Module OperationsManager

# Connect to SCOM Management Server
param(
    [Parameter(Mandatory=$true)]
    [string]$ManagementGroup,
    [string]$outputFile = "C:\SCOM_Thresholds_for_Servers.txt"
)

try {
    # Connect to SCOM Management Group with error handling
    Write-Host "Connecting to SCOM Management Group: $ManagementGroup"
    $mgConnection = New-SCOMManagementGroupConnection -ComputerName $ManagementGroup -ErrorAction Stop
} catch {
    Write-Error "Failed to connect to SCOM Management Group: $_"
    exit 1
}

# Initialize the output content array
$outputContent = @()
$counter = 1

# Improved Windows server query
$windowsServers = Get-SCOMClass -Name "Microsoft.Windows.Computer" | Get-SCOMClassInstance

# Verify server count and output details
if ($null -eq $windowsServers -or $windowsServers.Count -eq 0) {
    Write-Error "No Windows servers found. Please verify:
    1. SCOM connection is successful
    2. Windows Computer class instances exist
    3. You have sufficient permissions"
    exit 1
}

Write-Host "Total Windows servers found: $($windowsServers.Count)"

# Create progress bar
$progressCounter = 0
$totalServers = $windowsServers.Count

foreach ($server in $windowsServers) {
    $progressCounter++
    $progressPercentage = ($progressCounter / $totalServers) * 100
    Write-Progress -Activity "Processing Servers" -Status "Processing $($server.DisplayName)" -PercentComplete $progressPercentage
    
    try {
        # Get monitors specific to this server instance
        $serverMonitors = Get-SCOMMonitor | Where-Object { 
            $_.Target.Id -eq $server.Id -or 
            ($_.Target.DisplayName -eq $server.DisplayName)
        }

        foreach ($monitor in $serverMonitors) {
            # Skip if monitor is null
            if ($null -eq $monitor) { continue }

            # Extract configuration details safely
            $thresholds = try {
                $monitor.Configuration.Xml
            } catch {
                "Configuration not available"
            }

            $alertCriteria = try {
                $monitor.AlertSettings.AlertMessage
            } catch {
                "Alert criteria not available"
            }

            # Only add to output if we have meaningful data
            if ($thresholds -ne "Configuration not available" -or $alertCriteria -ne "Alert criteria not available") {
                $details = @"
$counter. Server:            $($server.DisplayName)
    Health State:           $($server.HealthState)
    Monitor Name:           $($monitor.DisplayName)
    Monitor Category:       $($monitor.Category)
    Thresholds:            $thresholds
    Alert Criteria:        $alertCriteria
    Description:           $($monitor.Description)

"@
                $outputContent += $details
                $counter++
            }
        }

    } catch {
        Write-Warning "Error processing server $($server.DisplayName): $_"
        continue
    }
}

# Write the output content to a file
if ($outputContent.Count -gt 0) {
    try {
        $outputContent | Out-File -FilePath $outputFile -Encoding UTF8 -Force
        Write-Host "Processing complete. File saved at: $outputFile"
        Write-Host "Total entries processed: $($counter - 1)"
    } catch {
        Write-Error "Failed to write to output file: $_"
        exit 1
    }
} else {
    Write-Warning "No threshold data found for the monitored servers."
}
