SELECT
    $_timeEpoch([DateTime]),
    CASE 
        WHEN [SampleValue] > 0 THEN 1  -- Up
        ELSE 0  -- Down
    END as status
FROM
    [SCOMConfiguration].[dbo].[grafana PerfReport02]
WHERE
    [ManagementPackSystemName] = 'Microsoft.SystemCenter.2007'
    AND [ObjectName] = 'System'
    AND [CounterName] = 'System Up Time'
    AND [Path] IN ($ServerName)
ORDER BY
    [DateTime] ASC
