Get-WmiObject -Namespace "root\Microsoft\OperationsManager" -Class "MSFT_HealthService" | Select-Object Name, PrincipalName, AuthenticationType
