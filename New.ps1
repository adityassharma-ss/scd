# Load SCOM module
Import-Module OperationsManager

# Connect to SCOM Management Server
$ManagementServer = "<SCOM_Management_Server>"  # Replace with your SCOM management server name
New-SCOMManagementGroupConnection -ComputerName $ManagementServer

# Set the date range for December (any year)
$StartDate = Get-Date "2024-12-01"
$EndDate = Get-Date "2024-12-31"

# Fetch all alerts related to Windows Servers during December
$Alerts = Get-SCOMAlert |
    Where-Object {
        $_.MonitoringObjectPath -like "*Windows*" -and
        $_.TimeRaised -ge $StartDate -and
        $_.TimeRaised -le $EndDate
    }

# Define the output file path
$OutputFilePath = "C:\Temp\WindowsServerAlerts_December.txt"

# Create and write structured data to the file
$FileContent = @()
$FileContent += "Alerts for Windows Servers (December 2024)"
$FileContent += "-----------------------------------------"
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
