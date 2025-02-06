SELECT 
    'Status' AS metric, 
    CASE 
        WHEN MAX([SampleValue]) > 0 THEN 'Up' 
        ELSE 'Down' 
    END AS value 
FROM 
    [SCOMConfiguration].[dbo].[grafanaPerfReport02]
WHERE 
    [ManagementPackSystemName] = 'Microsoft.SystemCenter.2007'
    AND [ObjectName] = 'System'
    AND [CounterName] = 'System Up Time'
    AND [Path] IN ($ServerName)
