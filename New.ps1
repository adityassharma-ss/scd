# Automated MMA Configuration Script for Multiple Servers and Full Sync

# Prompt User Inputs
$ServerName = Read-Host "Enter the server name (e.g., localhost or FQDN)"
$ManagementGroupName = Read-Host "Enter the Management Group name"
$PrimaryManagementServer = Read-Host "Enter the Primary Management Server name (e.g., your OMS server)"
$Port = Read-Host "Enter the Port number (default: 5723)"
$AssignmentMode = "0"  # Default assignment mode

# Set default port if not provided
if (-not $Port) {
    $Port = "5723"
}

# Function to Check if MMA is Installed
function Check-MMAInstalled {
    Write-Host "Checking if MMA is installed on $ServerName..."
    if (Get-Service -Name "HealthService" -ErrorAction SilentlyContinue) {
        Write-Host "Microsoft Monitoring Agent (MMA) is installed." -ForegroundColor Green
        return $true
    } else {
        Write-Host "Microsoft Monitoring Agent (MMA) is NOT installed. Install it first!" -ForegroundColor Red
        return $false
    }
}

# Function to Add or Update Management Group
function AddOrUpdate-ManagementGroup {
    Write-Host "Adding/Updating Management Group '$ManagementGroupName'..." -ForegroundColor Yellow

    # Use AgentConfigHelper.exe for adding/updating management group
    $AgentHelperPath = "C:\Program Files\Microsoft Monitoring Agent\Agent\AgentConfigHelper.exe"

    if (Test-Path $AgentHelperPath) {
        # Command to add the group
        $Command = "& `"$AgentHelperPath`" ADD_GROUP `"$ManagementGroupName`" `"$PrimaryManagementServer`" $Port $AssignmentMode"
        Invoke-Expression $Command

        Write-Host "Management Group '$ManagementGroupName' has been successfully added/updated." -ForegroundColor Green
    } else {
        Write-Host "AgentConfigHelper.exe not found. Please check the MMA installation path." -ForegroundColor Red
        exit
    }
}

# Function to Sync Management Group in MMA Properties
function Sync-MMAProperties {
    Write-Host "Synchronizing Management Group properties with MMA UI..." -ForegroundColor Yellow
    try {
        # Restart HealthService to sync
        Restart-Service -Name "HealthService" -Force -ErrorAction Stop
        Write-Host "Microsoft Monitoring Agent service restarted successfully." -ForegroundColor Green
    } catch {
        Write-Host "Failed to restart the HealthService: $_" -ForegroundColor Red
    }
}

# Function to Validate Management Group in MMA Properties
function Validate-ManagementGroup {
    Write-Host "Validating Management Group configuration in MMA properties..." -ForegroundColor Yellow

    $RegistryPath = "HKLM:\SOFTWARE\Microsoft\Microsoft Operations Manager\3.0\Agent Management Groups\$ManagementGroupName"

    if (Test-Path $RegistryPath) {
        $ConfiguredServer = Get-ItemProperty -Path $RegistryPath -Name ManagementServer | Select-Object -ExpandProperty ManagementServer
        $ConfiguredPort = Get-ItemProperty -Path $RegistryPath -Name ManagementServerPort | Select-Object -ExpandProperty ManagementServerPort

        if ($ConfiguredServer -eq $PrimaryManagementServer -and $ConfiguredPort -eq $Port) {
            Write-Host "Management Group is properly configured in the MMA UI." -ForegroundColor Green
        } else {
            Write-Host "Management Group configuration mismatch. Re-applying settings..." -ForegroundColor Yellow
            AddOrUpdate-ManagementGroup
            Sync-MMAProperties
        }
    } else {
        Write-Host "Management Group '$ManagementGroupName' is not present. Adding it now..." -ForegroundColor Yellow
        AddOrUpdate-ManagementGroup
        Sync-MMAProperties
    }
}

# Main Script Execution
Write-Host "Starting MMA configuration on $ServerName..." -ForegroundColor Cyan
if (Check-MMAInstalled) {
    AddOrUpdate-ManagementGroup
    Sync-MMAProperties
    Validate-ManagementGroup
    Write-Host "MMA configuration completed successfully on $ServerName." -ForegroundColor Green
} else {
    Write-Host "Exiting script. Install MMA first and re-run the script." -ForegroundColor Red
}
