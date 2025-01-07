Get-SCOMMonitor | Where-Object {$_.DisplayName -match "URL|Web|HTTP"} | ForEach-Object {
    $monitor = $_
    $config = Get-SCOMMonitorConfiguration -Monitor $monitor
    [PSCustomObject]@{
        DisplayName       = $monitor.DisplayName
        Target            = $monitor.Target.DisplayName
        IntervalSeconds   = $config | Where-Object { $_.Property -eq "IntervalSeconds" } | Select-Object -ExpandProperty Value
        ManagementPack    = $monitor.ManagementPack.DisplayName
    }
}
