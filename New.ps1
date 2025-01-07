Get-SCOMMonitor | Where-Object {$_.DisplayName -match "URL|Web|HTTP"} | Select-Object DisplayName
