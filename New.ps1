# Comprehensive MMA Configuration Script

# Logging Function
function Write-LogMessage {
    param(
        [Parameter(Mandatory=$true)][string]$Message,
        [Parameter(Mandatory=$false)][string]$Type = "Info"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Type] $Message"
    
    switch ($Type) {
        "Success" { Write-Host $logMessage -ForegroundColor Green }
        "Warning" { Write-Host $logMessage -ForegroundColor Yellow }
        "Error" { Write-Host $logMessage -ForegroundColor Red }
        default { Write-Host $logMessage }
    }
    
    $logPath = "C:\Logs\MMAConfiguration.log"
    if (-not (Test-Path (Split-Path $logPath))) {
        New-Item -ItemType Directory -Path (Split-Path $logPath) -Force | Out-Null
    }
    Add-Content -Path $logPath -Value $logMessage
}

# Function to Configure MMA via Command Line Tool
function Configure-MMAManagementGroup {
    param(
        [Parameter(Mandatory=$true)][string]$ServerName,
        [Parameter(Mandatory=$true)][string]$ManagementGroupName,
        [Parameter(Mandatory=$true)][string]$PrimaryManagementServer,
        [Parameter(Mandatory=$false)][string]$Port = "5723"
    )

    # Path to MMA Configuration Tool
    $MMAConfigToolPath = "$env:ProgramFiles\Microsoft Monitoring Agent\Agent\MonitoringHost.exe"
    
    # Check if MMA is installed
    if (-not (Test-Path $MMAConfigToolPath)) {
        Write-LogMessage "Microsoft Monitoring Agent is not installed." -Type "Error"
        return $false
    }

    try {
        # Unregister existing management groups (optional but recommended)
        & "$env:ProgramFiles\Microsoft Monitoring Agent\Agent\AgentConfig.exe" /d

        # Configure new management group
        $configCommand = "& '$env:ProgramFiles\Microsoft Monitoring Agent\Agent\AgentConfig.exe' /c:$ManagementGroupName /s:$PrimaryManagementServer /p:$Port"
        Write-LogMessage "Executing configuration command: $configCommand" -Type "Info"
        
        $result = Invoke-Expression $configCommand
        
        # Check configuration result
        if ($LASTEXITCODE -eq 0) {
            Write-LogMessage "Management Group configured successfully." -Type "Success"
            return $true
        }
        else {
            Write-LogMessage "Failed to configure Management Group. Exit Code: $LASTEXITCODE" -Type "Error"
            return $false
        }
    }
    catch {
        Write-LogMessage "Configuration error: $_" -Type "Error"
        return $false
    }
}

# Main Configuration Function
function Main-MMAConfiguration {
    # Ensure administrative privileges
    if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-LogMessage "Please run this script as an Administrator." -Type "Error"
        return
    }

    # User Inputs
    $ServerName = Read-Host "Enter the server name (e.g., localhost)"
    $ManagementGroupName = Read-Host "Enter the Management Group name"
    $PrimaryManagementServer = Read-Host "Enter the Primary Management Server name"
    $Port = Read-Host "Enter the Port number (default is 5723)"
    
    # Set default port if not provided
    if ([string]::IsNullOrWhiteSpace($Port)) {
        $Port = "5723"
    }

    # Configure Management Group
    $configResult = Configure-MMAManagementGroup -ServerName $ServerName `
                                                 -ManagementGroupName $ManagementGroupName `
                                                 -PrimaryManagementServer $PrimaryManagementServer `
                                                 -Port $Port

    # Restart MMA Service
    if ($configResult) {
        try {
            Write-LogMessage "Restarting Microsoft Monitoring Agent service..." -Type "Info"
            Restart-Service "HealthService" -Force
            Write-LogMessage "Microsoft Monitoring Agent service restarted successfully." -Type "Success"
        }
        catch {
            Write-LogMessage "Failed to restart MMA service: $_" -Type "Error"
        }
    }
}

# Execute the configuration
Main-MMAConfiguration
