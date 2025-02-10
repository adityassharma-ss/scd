# Load the SCOM module
Import-Module OperationsManager

# Connect to SCOM Management Server (Optional, modify as needed)
New-SCOMManagementGroupConnection -ComputerName "YourSCOMServer"

# Get all Web URL Monitoring Objects
$monitoredObjects = Get-SCOMMonitoringObject | Where-Object { $_.DisplayName -match "^https?://" }

# Create an empty array for results
$results = @()

# Process each monitored object
foreach ($object in $monitoredObjects) {
    $results += [PSCustomObject]@{
        URL         = $object.DisplayName
        State       = $object.HealthState
        Path        = $object.FullName
    }
}

# Define Excel File Path
$ExcelFile = "C:\SCOM_Monitored_URLs.xlsx"

# Create Excel COM Object
$Excel = New-Object -ComObject Excel.Application
$Excel.Visible = $false
$Excel.DisplayAlerts = $false
$Workbook = $Excel.Workbooks.Add()
$Sheet = $Workbook.Sheets.Item(1)

# Add Headers
$Sheet.Cells.Item(1,1) = "URL"
$Sheet.Cells.Item(1,2) = "State"
$Sheet.Cells.Item(1,3) = "Path"

# Format Headers
$HeaderRange = $Sheet.Range("A1:C1")
$HeaderRange.Font.Bold = $true
$HeaderRange.Interior.ColorIndex = 15  # Light Gray Background

# Insert Data
$row = 2
foreach ($entry in $results) {
    $Sheet.Cells.Item($row,1) = $entry.URL
    $Sheet.Cells.Item($row,2) = $entry.State
    $Sheet.Cells.Item($row,3) = $entry.Path
    $row++
}

# Autofit Columns
$Sheet.Columns.AutoFit()

# Save and Close Excel
$Workbook.SaveAs($ExcelFile)
$Excel.Quit()

# Cleanup COM Objects
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Sheet) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Workbook) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Excel) | Out-Null

Write-Host "Exported $($results.Count) URLs to $ExcelFile"
