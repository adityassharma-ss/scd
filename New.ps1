# Load SCOM module
Import-Module OperationsManager

# Connect to SCOM Management Server
$ManagementServer = "<SCOM_Management_Server>"  # Replace with your SCOM server name
New-SCOMManagementGroupConnection -ComputerName $ManagementServer

# Set the date range for the query
$StartDate = Get-Date "2024-12-20"
$EndDate = Get-Date "2024-12-28"

# Fetch all alerts for Windows Servers in the specified date range
$Alerts = Get-SCOMAlert |
    Where-Object {
        ($_.TimeRaised -ge $StartDate) -and
        ($_.TimeRaised -le $EndDate) -and
        ($_.MonitoringObjectPath -like "*Windows*")  # Filter for Windows servers
    }

# Define the output file path
$OutputFilePath = "C:\Temp\WindowsServerAlerts_Dec20_Dec28.txt"

# Create and write structured data to the file
$FileContent = @()
$FileContent += "Alerts for Windows Servers (Dec 20 - Dec 28, 2024)"
$FileContent += "---------------------------------------------------"
$FileContent += "TimeRaised          | MonitoringObjectPath    | AlertName                  | Severity | ResolutionState"
$FileContent += "-----------------------------------------------------------------------------------------------"

foreach ($Alert in $Alerts) {
    $Line = "{0,-20} | {1,-25} | {2,-25} | {3,-8} | {4}" -f `
        $Alert.TimeRaised.ToString("yyyy-MM-dd HH:mm:ss"), `
        $Alert.MonitoringObjectPath, `
        $Alert.Name, `
        $Alert.Severity, `
        $Alert.ResolutionState
    $FileContent += $Line
}

# Write the content to the text file
Set-Content -Path $OutputFilePath -Value $FileContent

Write-Host "Alerts fetched and saved to $OutputFilePath"
