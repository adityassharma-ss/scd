# Enable verbose output
$VerbosePreference = "Continue"

# Load the SCOM PowerShell module
Write-Verbose "Attempting to load OperationsManager module..."
try {
    Import-Module OperationsManager -ErrorAction Stop
    Write-Verbose "Successfully loaded OperationsManager module"
} catch {
    Write-Error "Failed to load OperationsManager module: $_"
    exit
}

# Connect to SCOM Management Group
$ManagementServer = "YourManagementServerName"  # Replace with your SCOM management server
Write-Verbose "Attempting to connect to SCOM Management Server: $ManagementServer"
try {
    New-SCOMManagementGroupConnection -ComputerName $ManagementServer -ErrorAction Stop
    Write-Verbose "Successfully connected to SCOM Management Server"
} catch {
    Write-Error "Failed to connect to SCOM Management Server: $_"
    exit
}

# Get all Windows Servers monitored by SCOM
Write-Verbose "Fetching Windows Servers from SCOM..."
try {
    $SCOMClass = Get-SCOMClass -Name "Microsoft.Windows.Computer" -ErrorAction Stop
    Write-Verbose "Found SCOM Class: $($SCOMClass.DisplayName)"
    
    $WindowsServers = Get-SCOMClassInstance -Class $SCOMClass | 
        Where-Object { $_.DisplayName -like "*Windows*" } |
        Sort-Object DisplayName
    
    Write-Verbose "Found $($WindowsServers.Count) Windows Servers"
    
    if ($WindowsServers.Count -eq 0) {
        Write-Warning "No Windows Servers found in SCOM!"
    }
} catch {
    Write-Error "Failed to fetch Windows Servers: $_"
    exit
}

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
    Write-Verbose "Processing server: $($server.DisplayName)"
    [void]$content.Add("SERVER: $($server.DisplayName)")
    [void]$content.Add("------------------------------------------------")
    
    # Fetch and process monitors
    Write-Verbose "Fetching monitors for $($server.DisplayName)"
    try {
        $monitors = Get-SCOMMonitor -Target $server -ErrorAction Stop | Sort-Object DisplayName
        Write-Verbose "Found $($monitors.Count) monitors"
        
        if ($monitors) {
            [void]$content.Add("")
            [void]$content.Add("MONITORS:")
            foreach ($monitor in $monitors) {
                Write-Verbose "Processing monitor: $($monitor.DisplayName)"
                [void]$content.Add("  * $($monitor.DisplayName)")
                [void]$content.Add("    - Management Pack: $($monitor.ManagementPackName)")
                [void]$content.Add("    - Enabled: $($monitor.Enabled)")
                
                # Parse monitor configuration
                if ($monitor.Configuration) {
                    try {
                        [xml]$config = $monitor.Configuration
                        Write-Verbose "Successfully parsed monitor configuration XML"
                        
                        $thresholdNode = $config.SelectSingleNode("//Threshold")
                        $threshold = if ($thresholdNode) { $thresholdNode.InnerText } else { "N/A" }
                        
                        $intervalNode = $config.SelectSingleNode("//IntervalSeconds")
                        $intervalSeconds = if ($intervalNode) { $intervalNode.InnerText } else { "N/A" }
                        
                        $timeoutNode = $config.SelectSingleNode("//TimeoutSeconds")
                        $timeoutSeconds = if ($timeoutNode) { $timeoutNode.InnerText } else { "N/A" }
                        
                        [void]$content.Add("    - Threshold: $threshold")
                        [void]$content.Add("    - Interval Seconds: $intervalSeconds")
                        [void]$content.Add("    - Timeout Seconds: $timeoutSeconds")
                    }
                    catch {
                        Write-Warning "Failed to parse monitor configuration for $($monitor.DisplayName): $_"
                        [void]$content.Add("    - Configuration: Unable to parse")
                    }
                } else {
                    Write-Verbose "No configuration found for monitor: $($monitor.DisplayName)"
                    [void]$content.Add("    - Configuration: None")
                }
                [void]$content.Add("")
            }
        } else {
            Write-Verbose "No monitors found for $($server.DisplayName)"
            [void]$content.Add("No monitors found")
        }
    } catch {
        Write-Warning "Failed to fetch monitors for $($server.DisplayName): $_"
        [void]$content.Add("Error fetching monitors: $_")
    }

    # Fetch and process rules
    Write-Verbose "Fetching rules for $($server.DisplayName)"
    try {
        $rules = Get-SCOMRule -Target $server -ErrorAction Stop | Sort-Object DisplayName
        Write-Verbose "Found $($rules.Count) rules"
        
        if ($rules) {
            [void]$content.Add("RULES:")
            foreach ($rule in $rules) {
                Write-Verbose "Processing rule: $($rule.DisplayName)"
                [void]$content.Add("  * $($rule.DisplayName)")
                [void]$content.Add("    - Management Pack: $($rule.ManagementPackName)")
                [void]$content.Add("    - Enabled: $($rule.Enabled)")
                
                # Parse rule configuration
                if ($rule.Configuration) {
                    try {
                        [xml]$config = $rule.Configuration
                        Write-Verbose "Successfully parsed rule configuration XML"
                        
                        $intervalNode = $config.SelectSingleNode("//IntervalSeconds")
                        $intervalSeconds = if ($intervalNode) { $intervalNode.InnerText } else { "N/A" }
                        
                        $timeoutNode = $config.SelectSingleNode("//TimeoutSeconds")
                        $timeoutSeconds = if ($timeoutNode) { $timeoutNode.InnerText } else { "N/A" }
                        
                        [void]$content.Add("    - Interval Seconds: $intervalSeconds")
                        [void]$content.Add("    - Timeout Seconds: $timeoutSeconds")
                    }
                    catch {
                        Write-Warning "Failed to parse rule configuration for $($rule.DisplayName): $_"
                        [void]$content.Add("    - Configuration: Unable to parse")
                    }
                } else {
                    Write-Verbose "No configuration found for rule: $($rule.DisplayName)"
                    [void]$content.Add("    - Configuration: None")
                }
                [void]$content.Add("")
            }
        } else {
            Write-Verbose "No rules found for $($server.DisplayName)"
            [void]$content.Add("No rules found")
        }
    } catch {
        Write-Warning "Failed to fetch rules for $($server.DisplayName): $_"
        [void]$content.Add("Error fetching rules: $_")
    }
    
    [void]$content.Add("================================================")
    [void]$content.Add("")
}

# Write to output file
Write-Verbose "Writing report to $outputFile"
try {
    $content | Out-File -FilePath $outputFile -Encoding UTF8 -ErrorAction Stop
    Write-Host "Report generated successfully at $outputFile"
} catch {
    Write-Error "Failed to write report to file: $_"
}
