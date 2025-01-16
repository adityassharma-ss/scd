# Define the management server
$managementServerName = "awswcanvaw0002"

# Define the output file
$outputFile = "C:\SCOM_ManagedServers_Config.txt"

# Initialize the output content
$content = @"
Managed Servers Under Management Server: $managementServerName
===============================================================
"@

# Get the management server
$managementServer = Get-SCOMManagementServer | Where-Object { $_.Name -eq $managementServerName }

if (!$managementServer) {
    Write-Host "Management Server '$managementServerName' not found!" -ForegroundColor Red
    exit
}

# Get all agents reporting to the management server
$agents = Get-SCOMAgent | Where-Object { $_.PrimaryManagementServer -eq $managementServer }

if ($agents.Count -eq 0) {
    Write-Host "No agents found under management server '$managementServerName'!" -ForegroundColor Red
    exit
}

# Loop through each agent and fetch configurations
foreach ($agent in $agents) {
    $serverName = $agent.ComputerName
    $content += "Server Name: $serverName`r`n"
    $content += "  - Health State   : $($agent.HealthService.HealthState)`r`n"

    # Fetch rules applied to this server
    $rules = Get-SCOMRule | Where-Object { $_.Target -eq $agent.GetMonitoringClass() }
    if ($rules.Count -gt 0) {
        $content += "  - Associated Rules:`r`n"
        foreach ($rule in $rules) {
            $content += "      - Rule Name          : $($rule.DisplayName)`r`n"
            $content += "        Management Pack    : $($rule.ManagementPackName)`r`n"
            $content += "        Interval Seconds   : $($rule.Configuration -match '<IntervalSeconds>(\d+)</IntervalSeconds>' ? $matches[1] : 'N/A')`r`n"
            $content += "        Timeout Seconds    : $($rule.Configuration -match '<TimeoutSeconds>(\d+)</TimeoutSeconds>' ? $matches[1] : 'N/A')`r`n"
        }
    } else {
        $content += "  - No rules associated with this server.`r`n"
    }

    # Fetch monitors applied to this server
    $monitors = Get-SCOMMonitor | Where-Object { $_.Target -eq $agent.GetMonitoringClass() }
    if ($monitors.Count -gt 0) {
        $content += "  - Associated Monitors:`r`n"
        foreach ($monitor in $monitors) {
            $content += "      - Monitor Name       : $($monitor.DisplayName)`r`n"
            $content += "        Management Pack    : $($monitor.ManagementPackName)`r`n"
            $content += "        Threshold          : $($monitor.Configuration -match '<Threshold>(\d+)</Threshold>' ? $matches[1] : 'N/A')`r`n"
            $content += "        Interval Seconds   : $($monitor.Configuration -match '<IntervalSeconds>(\d+)</IntervalSeconds>' ? $matches[1] : 'N/A')`r`n"
            $content += "        Timeout Seconds    : $($monitor.Configuration -match '<TimeoutSeconds>(\d+)</TimeoutSeconds>' ? $matches[1] : 'N/A')`r`n"
        }
    } else {
        $content += "  - No monitors associated with this server.`r`n"
    }

    $content += "`r`n" # Add spacing between servers
}

# Write the content to the output file
$content | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "Managed server configurations written to $outputFile"
