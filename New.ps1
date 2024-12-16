# Import Operations Manager Module
Import-Module OperationsManager -ErrorAction Stop

# Set the SCOM Management Server name or IP address
$ManagementServer = "YourSCOMServerName"  # Replace with actual server name or IP address

# Set the timeout for the connection attempt (in seconds)
$timeout = 30
$startTime = Get-Date

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
            Write-Output "Monitored Servers:"
            $monitoredServers | ForEach-Object {
                Write-Output "$($_.Name) - Status: $($_.Status)"
            }
        } else {
            Write-Output "No monitored servers found."
        }
    }
    catch {
        Write-Output "Error retrieving monitored servers: $_"
    }
}

# Retrieve and output the list of monitored servers
Get-MonitoredServers
