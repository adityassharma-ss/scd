# Load the SCOM PowerShell module
Import-Module OperationsManager

# Connect to SCOM Management Group
$ManagementServer = "YourManagementServerName"  # Replace with your SCOM management server
New-SCOMManagementGroupConnection -ComputerName $ManagementServer

# Get all Windows Servers monitored by SCOM
$WindowsServers = Get-SCOMClassInstance -Class (Get-SCOMClass -Name "Microsoft.Windows.Computer") | 
    Where-Object { $_.DisplayName -like "*Windows*" } |
    Sort-Object DisplayName

# Prepare output file
$outputFile = "C:\SCOM_Thresholds.txt"
$content = New-Object System.Collections.ArrayList

# Add header
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
[void]$content.Add("SCOM Monitored Windows Servers - Configuration Report")
[void]$content.Add("Generated on: $timestamp")
[void]$content.Add("================================================")
[void]$content.Add("")

# Process each Windows Server
foreach ($server in $WindowsServers) {
    [void]$content.Add("SERVER: $($server.DisplayName)")
    [void]$content.Add("------------------------------------------------")
    
    # Fetch and process monitors
    $monitors = Get-SCOMMonitor -Target $server | Sort-Object DisplayName
    if ($monitors) {
        [void]$content.Add("")
        [void]$content.Add("MONITORS:")
        foreach ($monitor in $monitors) {
            [void]$content.Add("  * $($monitor.DisplayName)")
            [void]$content.Add("    - Management Pack: $($monitor.ManagementPackName)")
            [void]$content.Add("    - Enabled: $($monitor.Enabled)")
            
            # Parse monitor configuration
            try {
                [xml]$config = $monitor.Configuration
                $threshold = $config.SelectSingleNode("//Threshold")?.InnerText ?? "N/A"
                $intervalSeconds = $config.SelectSingleNode("//IntervalSeconds")?.InnerText ?? "N/A"
                $timeoutSeconds = $config.SelectSingleNode("//TimeoutSeconds")?.InnerText ?? "N/A"
                
                [void]$content.Add("    - Threshold: $threshold")
                [void]$content.Add("    - Interval Seconds: $intervalSeconds")
                [void]$content.Add("    - Timeout Seconds: $timeoutSeconds")
            }
            catch {
                [void]$content.Add("    - Configuration: Unable to parse")
            }
            [void]$content.Add("")
        }
    }

    # Fetch and process rules
    $rules = Get-SCOMRule -Target $server | Sort-Object DisplayName
    if ($rules) {
        [void]$content.Add("RULES:")
        foreach ($rule in $rules) {
            [void]$content.Add("  * $($rule.DisplayName)")
            [void]$content.Add("    - Management Pack: $($rule.ManagementPackName)")
            [void]$content.Add("    - Enabled: $($rule.Enabled)")
            
            # Parse rule configuration
            try {
                [xml]$config = $rule.Configuration
                $intervalSeconds = $config.SelectSingleNode("//IntervalSeconds")?.InnerText ?? "N/A"
                $timeoutSeconds = $config.SelectSingleNode("//TimeoutSeconds")?.InnerText ?? "N/A"
                
                [void]$content.Add("    - Interval Seconds: $intervalSeconds")
                [void]$content.Add("    - Timeout Seconds: $timeoutSeconds")
            }
            catch {
                [void]$content.Add("    - Configuration: Unable to parse")
            }
            [void]$content.Add("")
        }
    }
    
    [void]$content.Add("================================================")
    [void]$content.Add("")
}

# Write to output file
$content | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "Report generated successfully at $outputFile"
