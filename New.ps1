# Define the Management Group and Management Server
$managementGroup = "YourManagementGroup"  # Replace with your Management Group name
$managementServer = "YourManagementServer"  # Replace with your Management Server name or IP

# Define the server name
$serverName = "awswaqnvaw0005"  # Replace with the server you want to configure

# Path to HealthService (SCOM Agent)
$healthServicePath = "C:\Program Files\Microsoft Monitoring Agent\Agent\HealthService.exe"

# Function to update the agent configuration
function Update-SCOMAgent {
    # Stop the Health Service
    Write-Host "Stopping Health Service..."
    Stop-Service -Name "HealthService" -Force
    Write-Host "Health Service stopped."

    # Add the Management Group and Management Server to the agent configuration
    Write-Host "Configuring Management Group: $managementGroup and Management Server: $managementServer..."
    & "$healthServicePath" /addmanagementgroup:$managementGroup /managementserver:$managementServer
    Write-Host "Successfully configured Management Group and Server."

    # Restart the Health Service
    Write-Host "Starting Health Service..."
    Start-Service -Name "HealthService"
    Write-Host "Health Service started."
}

# Check if HealthService.exe exists to confirm agent installation
if (Test-Path $healthServicePath) {
    Write-Host "SCOM agent found on server: $serverName"
    Update-SCOMAgent
} else {
    Write-Host "SCOM agent not installed on this server: $serverName"
}
