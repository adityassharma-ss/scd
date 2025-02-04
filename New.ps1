# Import SCOM module (ensure it's available)
Import-Module OperationsManager -ErrorAction Stop

# Script parameters
param (
    [string]$OutputPath = "C:\SCOM_Reports",
    [string]$OutputFile = "DiskAlertRules.csv",
    [switch]$IncludeDisabled = $false,
    [switch]$ExportToHTML = $false
)

# Ensure output directory exists
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath | Out-Null
}

$FullOutputPath = Join-Path $OutputPath $OutputFile

# Initialize logging
$LogFile = Join-Path $OutputPath "DiskMonitor.log"
function Write-Log {
    param([string]$Message)
    $LogMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
    Add-Content -Path $LogFile -Value $LogMessage
    Write-Host $Message
}

try {
    Write-Log "🔍 Fetching SCOM disk monitor configuration..."

    # Get all disk space-related monitors
    $DiskMonitors = Get-SCOMMonitor | Where-Object { 
        $_.DisplayName -match "Disk Free Space" -or 
        $_.DisplayName -match "Logical Disk" -or
        $_.DisplayName -match "Storage Space"
    }

    if (-not $DiskMonitors) {
        throw "⚠ No disk monitors found in SCOM!"
    }

    # Initialize results array
    $Results = @()

    foreach ($Monitor in $DiskMonitors) {
        # Get Overrides (error handling included)
        $Overrides = try {
            Get-SCOMOverride | Where-Object { $_.Context -eq $Monitor.Target }
        } catch {
            Write-Log "⚠ Error fetching overrides for $($Monitor.DisplayName): $_"
            $null
        }

        # Extract thresholds (Warning, Critical, Free Space, Time)
        $Configuration = $Monitor.Configuration
        $Thresholds = @{
            Warning       = "N/A"
            Critical      = "N/A"
            FreeSpace     = "N/A"
            TimeThreshold = "N/A"
        }

        $ThresholdPatterns = @{
            Warning       = '<UnderWarningThreshold>(.*?)</UnderWarningThreshold>'
            Critical      = '<OverErrorThreshold>(.*?)</OverErrorThreshold>'
            FreeSpace     = '<MinimumFreeSpace>(.*?)</MinimumFreeSpace>'
            TimeThreshold = '<TimeThreshold>(.*?)</TimeThreshold>'
        }

        foreach ($pattern in $ThresholdPatterns.GetEnumerator()) {
            if ($Configuration -match $pattern.Value) {
                $Thresholds[$pattern.Key] = $matches[1]
            }
        }

        # Get Monitor State and Enabled Status
        $MonitorState = try {
            Get-SCOMMonitoringObject | Where-Object { $_.DisplayName -eq $Monitor.DisplayName } | Select-Object -ExpandProperty HealthState
        } catch {
            Write-Log "⚠ Error getting state for $($Monitor.DisplayName): $_"
            "Unknown"
        }

        # Store data in an array
        $Results += [PSCustomObject]@{
            MonitorName       = $Monitor.DisplayName
            TargetClass       = $Monitor.Target.DisplayName
            HealthState       = $MonitorState
            Enabled           = $Monitor.Enabled
            WarningThreshold  = $Thresholds.Warning
            CriticalThreshold = $Thresholds.Critical
            MinimumFreeSpace  = $Thresholds.FreeSpace
            TimeThreshold     = $Thresholds.TimeThreshold
            LastModified      = $Monitor.LastModified
            Overrides         = if ($Overrides) { ($Overrides | Select-Object Property, Value | ForEach-Object { "$($_.Property)=$($_.Value)" }) -join "; " } else { "None" }
        }
    }

    # Filter disabled monitors if not included
    if (-not $IncludeDisabled) {
        $Results = $Results | Where-Object { $_.Enabled -eq $true }
    }

    # Export results to CSV
    $Results | Export-Csv -Path $FullOutputPath -NoTypeInformation

    # Generate HTML report if requested
    if ($ExportToHTML) {
        $HTMLPath = $FullOutputPath -replace '\.csv$', '.html'
        $HTMLContent = $Results | ConvertTo-Html -Title "SCOM Disk Monitor Configuration Report" -Pre "<h1>SCOM Disk Monitor Configuration Report</h1><p>Generated on $(Get-Date)</p>"
        $HTMLContent | Out-File $HTMLPath
        Write-Log "📄 HTML report exported to $HTMLPath"
    }

    Write-Log "✅ Export completed successfully to $FullOutputPath"
} catch {
    Write-Log "❌ Error: $_"
    throw $_
}
