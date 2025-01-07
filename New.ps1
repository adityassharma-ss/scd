New-SCOMOverride -Monitor (Get-SCOMMonitor -DisplayName "URLGenie Error Code Monitor") `
    -Parameter "StatusThreshold" `
    -Value 400 `
    -ManagementPack (Get-SCOMManagementPack -DisplayName "Overrides Management Pack") `
    -Target (Get-SCOMClassInstance -Name "YourTargetObjectName")


    New-SCOMOverride -Monitor (Get-SCOMMonitor -DisplayName "URLGenie Error Code Monitor") `
    -Parameter "Enabled" `
    -Value $false `
    -ManagementPack (Get-SCOMManagementPack -DisplayName "Overrides Management Pack") `
    -Target (Get-SCOMClassInstance -Name "YourTargetObjectName")


    Set-SCOMClassInstance -Instance (Get-SCOMClassInstance -Name "YourTargetObjectName") -RecalculateHealth



    Invoke-Command -ComputerName "TargetServerName" -ScriptBlock {
    Restart-Service HealthService
}
