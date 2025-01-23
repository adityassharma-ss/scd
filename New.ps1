# Automated MMA Configuration Script

# User Input
$ServerName = Read-Host "Enter the server name (e.g., localhost)"
$ManagementGroupName = Read-Host "Enter the Management Group name"
$PrimaryManagementServer = Read-Host "Enter the Primary Management Server name"
$Port = Read-Host "Enter the Port number (default is 5723)"

# Default port if not provided
if (-not $Port) {
    $Port = "5723"
}

# Function to Check MMA Installation
function Check-MMAInstalled {
    if (Get-Service "HealthService" -ErrorAction SilentlyContinue) {
        Write-Host "Microsoft Monitoring Agent (MMA) is installed on $ServerName." -ForegroundColor Green
        return $true
    } else {
        Write-Host "Microsoft Monitoring Agent (MMA) is NOT installed. Please install it first!" -ForegroundColor Red
        return $false
    }
}

# Function to Configure Management Group
function Configure-ManagementGroup {
    $RegistryBasePath = "HKLM:\SOFTWARE\Microsoft\Microsoft Operations Manager\3.0\Agent Management Groups"
    $RegistryPath = "$RegistryBasePath\$ManagementGroupName"

    # Check if the Management Group already exists
    if (Test-Path $RegistryPath) {
        Write-Host "Management Group '$ManagementGroupName' already exists. Verifying details..." -ForegroundColor Yellow

        # Check if the server and port match
        $ExistingServer = (Get-ItemProperty -Path $RegistryPath -Name ManagementServer -ErrorAction SilentlyContinue).ManagementServer
        $ExistingPort = (Get-ItemProperty -Path $RegistryPath -Name ManagementServerPort -ErrorAction SilentlyContinue).ManagementServerPort

        if ($ExistingServer -eq $PrimaryManagementServer -and $ExistingPort -eq $Port) {
            Write-Host "Management Group is already correctly configured." -ForegroundColor Green
        } else {
            Write-Host "Updating Management Group details..." -ForegroundColor Yellow
            Set-ItemProperty -Path $RegistryPath -Name ManagementServer -Value $PrimaryManagementServer
            Set-ItemProperty -Path $RegistryPath -Name ManagementServerPort -Value $Port
            Write-Host "Management Group updated successfully." -ForegroundColor Green
        }
    } else {
        Write-Host "Adding new Management Group '$ManagementGroupName'..." -ForegroundColor Yellow
        New-Item -Path $RegistryBasePath -Name $ManagementGroupName -Force | Out-Null
        Set-ItemProperty -Path $RegistryPath -Name ManagementServer -Value $PrimaryManagementServer
        Set-ItemProperty -Path $RegistryPath -Name ManagementServerPort -Value $Port
        Write-Host "Management Group added successfully." -ForegroundColor Green
    }
}

# Function to Restart MMA Service
function Restart-MMAService {
    Write-Host "Restarting Microsoft Monitoring Agent service..." -ForegroundColor Yellow
    try {
        Restart-Service "HealthService" -Force -ErrorAction Stop
        Write-Host "Service restarted successfully." -ForegroundColor Green
    } catch {
        Write-Host "Failed to restart the service. Please restart it manually." -ForegroundColor Red
    }
}

# Function to Check MMA Service Status
function Check-MMAServiceStatus {
    $Service = Get-Service "HealthService" -ErrorAction SilentlyContinue
    if ($Service.Status -eq "Running") {
        Write-Host "Microsoft Monitoring Agent service is running." -ForegroundColor Green
    } else {
        Write-Host "Microsoft Monitoring Agent service is not running. Attempting to start it..." -ForegroundColor Yellow
        Start-Service "HealthService" -ErrorAction SilentlyContinue
        if ((Get-Service "HealthService").Status -eq "Running") {
            Write-Host "Service started successfully." -ForegroundColor Green
        } else {
            Write-Host "Failed to start the service. Please start it manually." -ForegroundColor Red
        }
    }
}

# Main Script Execution
if (Check-MMAInstalled) {
    Configure-ManagementGroup
    Restart-MMAService
    Check-MMAServiceStatus
    Write-Host "Configuration completed successfully on $ServerName." -ForegroundColor Green
} else {
    Write-Host "Exiting script. Install Microsoft Monitoring Agent and re-run." -ForegroundColor Red
}
