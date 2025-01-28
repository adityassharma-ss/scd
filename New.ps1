# Import SCOM Module
Import-Module OperationsManager

# Connect to SCOM Management Group
$managementServer = "YourSCOMManagementServer"
New-SCOMManagementGroupConnection -ComputerName $managementServer

# List of servers to stop monitoring
$servers = Get-Content -Path "C:\Path\To\servers.txt"

foreach ($server in $servers) {
    try {
        # Get the SCOM Agent by DNS Hostname
        $agent = Get-SCOMAgent -DNSHostName $server -ErrorAction Stop

        # OPTIONAL: Place in Maintenance Mode to suppress alerts during removal
        $healthService = $agent.GetHealthService()
        Start-SCOMMaintenanceMode -Instance $healthService -Duration (New-TimeSpan -Minutes 5) `
            -Reason PlannedOther -Comment "Removing from monitoring" -ErrorAction Stop

        # Remove the agent from SCOM monitoring (does NOT uninstall the agent)
        Remove-SCOMAgent -Agent $agent -Force -ErrorAction Stop
        Write-Host "Successfully stopped monitoring $server." -ForegroundColor Green
    }
    catch {
        Write-Warning "Failed to process $server. Error: $($_.Exception.Message)"
    }
}
