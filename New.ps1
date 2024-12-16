Import-Module OperationsManager

$inputFile = "C:\Scripts\server_list.txt"
$outputFile = "C:\Scripts\monitoring_status.csv"

New-SCOMManagementGroupConnection -ComputerName "SCOMManagementServer"

$serverList = Get-Content -Path $inputFile
$results = @()

foreach ($serverName in $serverList) {
    $monitored = Get-SCOMManagedComputer | Where-Object { $_.DisplayName -eq $serverName }

    if ($monitored) {
        $status = "Monitored"
    } else {
        $status = "Not Monitored"
    }

    $results += [PSCustomObject]@{
        ServerName = $serverName
        Status     = $status
    }
}

$results | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8

Write-Output "Monitoring status exported to $outputFile"
