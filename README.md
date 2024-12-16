# Step 1: Import SCOM Module
Import-Module OperationsManager

# Step 2: Input and Output File Paths
$inputFile = "C:\Scripts\server_list.csv"  # Path to your input file
$outputFile = "C:\Scripts\monitoring_status.csv"  # Path for the output file

# Step 3: Connect to the SCOM Management Server
# Replace with your SCOM Management Server name
New-SCOMManagementGroupConnection -ComputerName "SCOMManagementServer"

# Step 4: Import Server List
$serverList = Import-Csv -Path $inputFile

# Step 5: Create an Empty Array for Results
$results = @()

# Step 6: Check Each Server in the List
foreach ($server in $serverList) {
    $serverName = $server.Servers  # Get server name from the CSV file
    
    # Check if the server is monitored
    $monitored = Get-SCOMManagedComputer | Where-Object { $_.DisplayName -eq $serverName }

    if ($monitored) {
        $status = "Monitored"
    } else {
        $status = "Not Monitored"
    }

    # Add the result to the array
    $results += [PSCustomObject]@{
        ServerName = $serverName
        Status     = $status
    }
}

# Step 7: Export the Results to a CSV File
$results | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8

Write-Output "Monitoring status exported to $outputFile"
