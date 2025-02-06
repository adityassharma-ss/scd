SELECT TOP 10 [DateTime], [SampleValue], [CounterName], [Path]  
FROM [SCOMConfiguration].[dbo].[grafanaPerfReport02]  
WHERE [ManagementPackSystemName] = 'Microsoft.SystemCenter.2007'  
AND [ObjectName] = 'System'  
AND [CounterName] = 'System Up Time'  
AND [Path] IN ($ServerName)  
ORDER BY [DateTime] DESC;
