# Load the Operations Manager PowerShell module
Import-Module OperationsManager -ErrorAction Stop

# Define paths and variables
$ManagementServer = "YourSCOMServerName" # Replace with your SCOM server name
$serverListFile = "D:\serverList\serverList.txt" # Path to the list of servers
$outputDirectory = "D:\serverList" # Directory for output files
$monitoredOutputFile = "$outputDirectory\MSSQLDB-monitoredServers.txt" # File for monitored servers
$nonMonitoredOutputFile = "$outputDirectory\MSSQLDB-nonMonitoredServers.txt" # File for non-monitored servers
$summaryOutputFile = "$outputDirectory\MSSQLDB-summary.txt" # Summary report file

# Create output directory if it doesn't exist
if (-Not (Test-Path -Path $outputDirectory)) {
    New-Item -Path $outputDirectory -ItemType Directory
}

# Connect to the SCOM Management Server
try {
    New-SCOMManagementGroupConnection -ComputerName $ManagementServer -ErrorAction Stop
    "Successfully connected to SCOM" | Out-File -FilePath $summaryOutputFile -Append
} catch {
    "Failed to connect to SCOM. Error: $_" | Out-File -FilePath $summaryOutputFile -Append
    exit
}

# Get the list of monitored servers from SCOM
try {
    $monitoredServers = Get-SCOMManagedComputer | ForEach-Object { ($_.Name.Split('.')[0]).ToLower().Trim() }
    if ($monitoredServers.Count -eq 0) {
        "No monitored servers were found. Possible connection issue." | Out-File -FilePath $summaryOutputFile -Append
        exit
    } else {
        "Successfully retrieved monitored servers: $($monitoredServers.Count) found." | Out-File -FilePath $summaryOutputFile -Append
    }
} catch {
    "Error while fetching monitored servers: $_" | Out-File -FilePath $summaryOutputFile -Append
    exit
}

# Read server list from file
try {
    if (-Not (Test-Path -Path $serverListFile)) {
        "Server list file not found: $serverListFile" | Out-File -FilePath $summaryOutputFile -Append
        exit
    }

    $serverList = Get-Content -Path $serverListFile | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ -ne "" }
    if ($serverList.Count -eq 0) {
        "Server list file is empty or invalid." | Out-File -FilePath $summaryOutputFile -Append
        exit
    }

    "Successfully loaded server list: $($serverList.Count) servers found." | Out-File -FilePath $summaryOutputFile -Append
} catch {
    "Error while reading server list: $_" | Out-File -FilePath $summaryOutputFile -Append
    exit
}

# Initialize counts and file outputs
$monitoredCount = 0
$nonMonitoredCount = 0

# Clear output files if they exist
Clear-Content -Path $monitoredOutputFile -ErrorAction SilentlyContinue
Clear-Content -Path $nonMonitoredOutputFile -ErrorAction SilentlyContinue

# Write headers for output files
"Server Name" | Out-File -FilePath $monitoredOutputFile -Append
"Server Name" | Out-File -FilePath $nonMonitoredOutputFile -Append

# Check each server's monitoring status
foreach ($server in $serverList) {
    if ($server -eq "") { continue }

    if ($monitoredServers -contains $server) {
        $monitoredCount++
        $server | Out-File -FilePath $monitoredOutputFile -Append
    } else {
        $nonMonitoredCount++
        $server | Out-File -FilePath $nonMonitoredOutputFile -Append
    }
}

# Write summary report
$summary = @"
------------------------
Summary
------------------------
Total Servers in list: $($serverList.Count)
Monitored Servers: $monitoredCount
Non-Monitored Servers: $nonMonitoredCount

Monitored Servers List: $monitoredOutputFile
Non-Monitored Servers List: $nonMonitoredOutputFile
------------------------
"@

$summary | Out-File -FilePath $summaryOutputFile -Append

# Final message
"Script execution completed. Check summary report: $summaryOutputFile" | Out-File -FilePath $summaryOutputFile -Append
