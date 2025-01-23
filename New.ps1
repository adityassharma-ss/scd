# MMA Configuration Script

# Logging Function
function Write-Log {
    param(
        [Parameter(Mandatory=$true)][string]$Message,
        [Parameter(Mandatory=$false)][string]$Type = "Info"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    switch ($Type) {
        "Success" { Write-Host "[$timestamp] [SUCCESS] $Message" -ForegroundColor Green }
        "Error" { Write-Host "[$timestamp] [ERROR] $Message" -ForegroundColor Red }
        "Warning" { Write-Host "[$timestamp] [WARNING] $Message" -ForegroundColor Yellow }
        default { Write-Host "[$timestamp] [INFO] $Message" }
    }
}

# Check MMA Installation Function
function Verify-MMAInstallation {
    $mmaServices = @(
        "Microsoft Monitoring Agent",
        "HealthService"
    )

    foreach ($serviceName in $mmaServices) {
        $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        if ($service) {
            Write-Log "MMA Service '$serviceName' found" -Type "Success"
            return $true
        }
    }

    Write-Log "Microsoft Monitoring Agent services not found" -Type "Error"
    return $false
}

# Configure Management Group Function
function Configure-ManagementGroup {
    param(
        [Parameter(Mandatory=$true)][string]$ManagementGroupName,
        [Parameter(Mandatory=$true)][string]$PrimaryManagementServer,
        [Parameter(Mandatory=$false)][string]$Port = "5723"
    )

    try {
        # Path to AgentConfig.exe
        $agentConfigPath = "C:\Program Files\Microsoft Monitoring Agent\Agent\AgentConfig.exe"
        
        if (-not (Test-Path $agentConfigPath)) {
            Write-Log "AgentConfig.exe not found. Check MMA installation." -Type "Error"
            return $false
        }

        # Unregister existing management groups
        Start-Process $agentConfigPath -ArgumentList "/d" -Wait -NoNewWindow

        # Configure new management group
        $configResult = Start-Process $agentConfigPath -ArgumentList "/c:$ManagementGroupName /s:$PrimaryManagementServer /p:$Port" -Wait -NoNewWindow -PassThru

        if ($configResult.ExitCode -eq 0) {
            Write-Log "Management Group configured successfully" -Type "Success"
            return $true
        }
        else {
            Write-Log "Management Group configuration failed. Exit Code: $($configResult.ExitCode)" -Type "Error"
            return $false
        }
    }
    catch {
        Write-Log "Error configuring Management Group: $_" -Type "Error"
        return $false
    }
}

# Main Execution Function
function Main {
    # Elevation check
    if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Log "Please run as Administrator" -Type "Error"
        return
    }

    # Verify MMA Installation
    if (-not (Verify-MMAInstallation)) {
        Write-Log "Cannot proceed. MMA not installed." -Type "Error"
        return
    }

    # User Input
    $ManagementGroupName = Read-Host "Enter Management Group Name"
    $PrimaryManagementServer = Read-Host "Enter Primary Management Server Name"
    $Port = Read-Host "Enter Port (default 5723)" 
    $Port = if ([string]::IsNullOrWhiteSpace($Port)) { "5723" } else { $Port }

    # Configure Management Group
    $configSuccess = Configure-ManagementGroup -ManagementGroupName $ManagementGroupName `
                                               -PrimaryManagementServer $PrimaryManagementServer `
                                               -Port $Port

    # Restart Service if Configuration Successful
    if ($configSuccess) {
        try {
            Restart-Service "HealthService" -Force
            Write-Log "HealthService restarted successfully" -Type "Success"
        }
        catch {
            Write-Log "Failed to restart HealthService" -Type "Error"
        }
    }
}

# Run the script
Main
