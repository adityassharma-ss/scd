# Automated MMA Configuration Script

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
    
    # Optional: Log to a file
    $logPath = "C:\Logs\MMAConfiguration.log"
    if (-not (Test-Path (Split-Path $logPath))) {
        New-Item -ItemType Directory -Path (Split-Path $logPath) -Force | Out-Null
    }
    Add-Content -Path $logPath -Value $logMessage
}

# Function to Validate Input
function Validate-Input {
    param(
        [Parameter(Mandatory=$true)][string]$Prompt,
        [Parameter(Mandatory=$false)][switch]$AllowEmpty = $false
    )

    do {
        $input = Read-Host $Prompt
        if ($AllowEmpty -or (-not [string]::IsNullOrWhiteSpace($input))) {
            return $input
        }
        Write-Host "Input cannot be empty. Please try again." -ForegroundColor Yellow
    } while ($true)
}

# Main Configuration Function
function Configure-MMAAgent {
    # Ensure script runs with administrative privileges
    if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-LogMessage "Please run this script as an Administrator." -Type "Error"
        return $false
    }

    # User Inputs
    $ServerName = Validate-Input "Enter the server name (e.g., localhost or server FQDN)"
    $ManagementGroupName = Validate-Input "Enter the Management Group name"
    $PrimaryManagementServer = Validate-Input "Enter the Primary Management Server name"
    $Port = Validate-Input "Enter the Port number (default is 5723)" -AllowEmpty
    
    # Set default port if not provided
    if ([string]::IsNullOrWhiteSpace($Port)) {
        $Port = "5723"
    }

    # Check MMA Installation
    try {
        $mmaService = Get-Service "HealthService" -ErrorAction Stop
    }
    catch {
        Write-LogMessage "Microsoft Monitoring Agent (MMA) is NOT installed on $ServerName." -Type "Error"
        return $false
    }

    # Configure Registry
    $RegistryPath = "HKLM:\SOFTWARE\Microsoft\Microsoft Operations Manager\3.0\Agent Management Groups\$ManagementGroupName"

    try {
        # Ensure the Management Groups key exists
        if (-not (Test-Path "HKLM:\SOFTWARE\Microsoft\Microsoft Operations Manager\3.0\Agent Management Groups")) {
            New-Item -Path "HKLM:\SOFTWARE\Microsoft\Microsoft Operations Manager\3.0\Agent Management Groups" -Force | Out-Null
        }

        # Create or update Management Group
        if (-not (Test-Path $RegistryPath)) {
            New-Item -Path $RegistryPath -Force | Out-Null
            Write-LogMessage "Created new Management Group '$ManagementGroupName'." -Type "Info"
        }

        # Set Management Group Properties
        Set-ItemProperty -Path $RegistryPath -Name "ManagementServer" -Value $PrimaryManagementServer -Force
        Set-ItemProperty -Path $RegistryPath -Name "ManagementServerPort" -Value $Port -Force
        Set-ItemProperty -Path $RegistryPath -Name "ServerName" -Value $ServerName -Force

        Write-LogMessage "Management Group '$ManagementGroupName' configured successfully for $ServerName." -Type "Success"

        # Restart MMA Service
        Write-LogMessage "Restarting Microsoft Monitoring Agent service..." -Type "Info"
        Restart-Service "HealthService" -Force
        Write-LogMessage "Microsoft Monitoring Agent service restarted successfully." -Type "Success"

        return $true
    }
    catch {
        Write-LogMessage "Configuration failed: $_" -Type "Error"
        return $false
    }
}

# Execute Configuration
try {
    $result = Configure-MMAAgent
    
    if ($result) {
        Write-LogMessage "MMA Configuration completed successfully." -Type "Success"
        Read-Host "Press Enter to exit"
    }
    else {
        Write-LogMessage "MMA Configuration failed. Please check the log file." -Type "Error"
        Read-Host "Press Enter to exit"
    }
}
catch {
    Write-LogMessage "An unexpected error occurred: $_" -Type "Error"
    Read-Host "Press Enter to exit"
}
