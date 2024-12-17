# Set the Management Server and Management Group
$managementServer = "YourPrimaryManagementServer" # Replace with your Management Server name or IP address
$managementGroup = "YourManagementGroup"         # Replace with your Management Group name

# Path to the HealthService.exe (SCOM Agent)
$healthServicePath = "C:\Program Files\Microsoft Monitoring Agent\Agent\HealthService.exe"

# Function to update the agent configuration
function Update-SCOMAgent {
    try {
        Write-Host "Updating $hostname to Management Group: $managementGroup with Management Server: $managementServer"
        
        # Stop the Health Service before making changes
        Stop-Service -Name "HealthService" -Force
        Write-Host "Stopped Health Service."

        # Add the Management Group and Primary Management Server
        & "$healthServicePath" /addmanagementgroup:$managementGroup /managementserver:$managementServer
        Write-Host "Successfully added $hostname to $managementGroup with Management Server $managementServer."

        # Restart the Health Service after making the changes
        Start-Service -Name "HealthService"
        Write-Host "Started Health Service."
    } catch {
        Write-Host "Error: $_"
    }
}

# Check if HealthService.exe exists to ensure the agent is installed
if (Test-Path $healthServicePath) {
    Update-SCOMAgent
} else {
    Write-Host "SCOM agent not found on this server. Please install the Microsoft Monitoring Agent first."
}
