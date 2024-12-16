# Import Operations Manager Module
Import-Module OperationsManager -ErrorAction Stop

# Set the SCOM Management Server name or IP address
$ManagementServer = "YourSCOMServerName"  # Replace with actual server name or IP address

# Set the timeout for the connection attempt (in seconds)
$timeout = 30
$startTime = Get-Date

# Set the path for the output text file
$outputFile = "C:\path\to\output.txt"  # Replace with the desired file path

# Function to check connection status with timeout
function Connect-ToSCOM {
    try {
        # Attempt to connect to the SCOM Management Server
        Write-Output "Attempting to connect to $ManagementServer..."
        New-SCOMManagementGroupConnection -ComputerName $ManagementServer -ErrorAction Stop
        Write-Output "Successfully connected to SCOM Management Server: $ManagementServer"
    }
    catch {
        $elapsedTime = (Get-Date) - $startTime
        if ($elapsedTime.TotalSeconds -gt $timeout) {
            Write-Output "Connection timeout exceeded after $timeout seconds."
        } else {
            Write-Output "Error: $_"
        }
    }
}

# Call the function to connect to SCOM
Connect-ToSCOM

# Retrieve and check the list of monitored servers
function Get-MonitoredServers {
    try {
        Write-Output "Retrieving monitored servers list..."
        $monitoredServers = Get-SCOMManagedComputer

        if ($monitoredServers) {
            $serverCount = $monitoredServers.Count
            Write-Output "Monitored Servers Count: $serverCount"

            # Save to file
            $output = "Monitored Servers Count: $serverCount`r`n"
            $output | Out-File -FilePath $outputFile -Append

            Write-Output "Monitored Servers:"
            $monitoredServers | ForEach-Object {
                $serverDetails = "$($_.Name) - Status: $($_.Status)"
                Write-Output $serverDetails
                $serverDetails | Out-File -FilePath $outputFile -Append
            }
        } else {
            Write-Output "No monitored servers found."
            "No monitored servers found." | Out-File -FilePath $outputFile -Append
        }
    }
    catch {
        Write-Output "Error retrieving monitored servers: $_"
        "Error retrieving monitored servers: $_" | Out-File -FilePath $outputFile -Append
    }
}

# Retrieve and output the list of monitored servers and their count to file
Get-MonitoredServers
