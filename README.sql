SELECT 
    $_timeEpoch([DateTime]) AS time, 
    CASE 
        WHEN [SampleValue] > 0 THEN 'Up' 
        ELSE 'Down' 
    END AS value, 
    [CounterName] AS metric
FROM 
    [SCOMConfiguration].[dbo].[grafanaPerfReport02]
WHERE 
    [ManagementPackSystemName] = 'Microsoft.SystemCenter.2007'
    AND [ObjectName] = 'System'
    AND [CounterName] = 'System Up Time'
    AND [Path] IN ($ServerName)
ORDER BY 
    [DateTime] ASC
