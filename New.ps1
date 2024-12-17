Import-Module OperationsManager -ErrorAction Stop

$ManagementServer = "YourSCOMServerName"
$serverListFile = "C:\path\to\serverList.txt"
$outputFile = "C:\path\to\output.txt"
$timeout = 30
$startTime = Get-Date

function Connect-ToSCOM {
    try {
        New-SCOMManagementGroupConnection -ComputerName $ManagementServer -ErrorAction Stop
    }
    catch {
        $elapsedTime = (Get-Date) - $startTime
        if ($elapsedTime.TotalSeconds -gt $timeout) {
            "Connection timeout exceeded after $timeout seconds." | Out-File -FilePath $outputFile -Append
        } else {
            "Error: $_" | Out-File -FilePath $outputFile -Append
        }
    }
}

Connect-ToSCOM

function Check-ServerList {
    try {
        $monitoredServers = Get-SCOMManagedComputer | Select-Object -ExpandProperty Name

        if (-not $monitoredServers) {
            "No monitored servers found in SCOM." | Out-File -FilePath $outputFile -Append
            return
        }

        if (-Not (Test-Path $serverListFile)) {
            "Server list file not found: $serverListFile" | Out-File -FilePath $outputFile -Append
            return
        }

        $serverList = Get-Content -Path $serverListFile
        if (-not $serverList) {
            "Server list file is empty." | Out-File -FilePath $outputFile -Append
            return
        }

        $monitoredCount = 0
        $nonMonitoredCount = 0

        "Server Name, Monitored Status" | Out-File -FilePath $outputFile -Append

        foreach ($server in $serverList) {
            $server = $server.Trim()
            if ($server -eq "") { continue }

            if ($monitoredServers -contains $server) {
                $status = "Monitored"
                $monitoredCount++
            } else {
                $status = "Not Monitored"
                $nonMonitoredCount++
            }

            "$server, $status" | Out-File -FilePath $outputFile -Append
        }

        $summary = @"
------------------------
Summary
------------------------
Total Servers: $($serverList.Count)
Monitored Servers: $monitoredCount
Non-Monitored Servers: $nonMonitoredCount
"@

        $summary | Out-File -FilePath $outputFile -Append
    }
    catch {
        "Error while checking server list: $_" | Out-File -FilePath $outputFile -Append
    }
}

Check-ServerList
