# Load the SCOM PowerShell module
Import-Module OperationsManager

# Connect to SCOM Management Group
$ManagementServer = "YourManagementServerName"  # Replace with your SCOM management server
New-SCOMManagementGroupConnection -ComputerName $ManagementServer

# Get all Windows Servers monitored by SCOM
$WindowsServers = Get-SCOMClassInstance -Class (Get-SCOMClass -Name "Microsoft.Windows.Computer") | Where-Object {
    $_.DisplayName -like "*Windows*"
}

# Prepare output file
$outputFile = "C:\SCOM_Thresholds.txt"
$content = @()
$content += "SCOM Monitored Windows Servers - Thresholds and Configurations`r`n"
$content += "=================================================================`r`n"

# Iterate through each Windows Server
foreach ($server in $WindowsServers) {
    $content += "Server: $($server.DisplayName)`r`n"
    $content += "-------------------------------------------------------------`r`n"

    # Fetch associated monitors
    $monitors = Get-SCOMMonitor -Target $server
    foreach ($monitor in $monitors) {
        $content += "    - Monitor Name       : $($monitor.DisplayName)`r`n"
        $content += "      Management Pack    : $($monitor.ManagementPackName)`r`n"
        $content += "      Enabled            : $($monitor.Enabled)`r`n"

        # Parse monitor configuration
        if ($monitor.Configuration -match '<Threshold>(\d+)</Threshold>') {
            $threshold = $matches[1]
        } else {
            $threshold = 'N/A'
        }
        $content += "      Threshold          : $threshold`r`n"

        if ($monitor.Configuration -match '<IntervalSeconds>(\d+)</IntervalSeconds>') {
            $intervalSeconds = $matches[1]
        } else {
            $intervalSeconds = 'N/A'
        }
        $content += "      Interval Seconds   : $intervalSeconds`r`n"

        if ($monitor.Configuration -match '<TimeoutSeconds>(\d+)</TimeoutSeconds>') {
            $timeoutSeconds = $matches[1]
        } else {
            $timeoutSeconds = 'N/A'
        }
        $content += "      Timeout Seconds    : $timeoutSeconds`r`n"
    }

    # Fetch associated rules
    $rules = Get-SCOMRule -Target $server
    foreach ($rule in $rules) {
        $content += "    - Rule Name          : $($rule.DisplayName)`r`n"
        $content += "      Management Pack    : $($rule.ManagementPackName)`r`n"
        $content += "      Enabled            : $($rule.Enabled)`r`n"

        # Parse rule configuration
        if ($rule.Configuration -match '<IntervalSeconds>(\d+)</IntervalSeconds>') {
            $intervalSeconds = $matches[1]
        } else {
            $intervalSeconds = 'N/A'
        }
        $content += "      Interval Seconds   : $intervalSeconds`r`n"

        if ($rule.Configuration -match '<TimeoutSeconds>(\d+)</TimeoutSeconds>') {
            $timeoutSeconds = $matches[1]
        } else {
            $timeoutSeconds = 'N/A'
        }
        $content += "      Timeout Seconds    : $timeoutSeconds`r`n"
    }

    $content += "`r`n"
}

# Write to output file
Set-Content -Path $outputFile -Value $content

Write-Host "Data successfully written to $outputFile"
