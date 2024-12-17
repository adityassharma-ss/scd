# Define the Management Group and Management Server
$managementGroup = "YourManagementGroup"  # Replace with your Management Group name
$managementServer = "YourManagementServer"  # Replace with your Management Server name or IP

# Define the server name
$serverName = "awswaqnvaw0005"  # Replace with the server you want to configure

# Define the installation path and download URL for the SCOM agent
$downloadUrl = "https://download.microsoft.com/download/4/3/0/4309b519-1fa3-41fc-8977-70c330fffe27/SCX_2012_R2_3103_2_0_32bit.msi"  # URL for the 32-bit version; use the correct version for your needs
$installerPath = "C:\Temp\SCOMAgent.msi"

# Path to HealthService (SCOM Agent)
$healthServicePath = "C:\Program Files\Microsoft Monitoring Agent\Agent\HealthService.exe"

# Function to download and install the Microsoft Monitoring Agent
function Install-SCOMAgent {
    # Download the SCOM agent installer
    Write-Host "Downloading SCOM Agent..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath
    Write-Host "Download complete."

    # Install the SCOM agent
    Write-Host "Installing SCOM Agent..."
    Start-Process msiexec.exe -ArgumentList "/i", "$installerPath", "/quiet", "/norestart" -Wait
    Write-Host "SCOM Agent installation complete."
}

# Function to configure the SCOM Agent with Management Group and Management Server
function Configure-SCOMAgent {
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

# Check if SCOM agent is already installed
if (Test-Path $healthServicePath) {
    Write-Host "SCOM agent found on server: $serverName"
    Configure-SCOMAgent
} else {
    Write-Host "SCOM agent not installed on this server: $serverName"
    Install-SCOMAgent
    Configure-SCOMAgent
}
