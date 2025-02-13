SELECT
    vme.Path AS 'Server Name',
    perf.ObjectName AS 'Object',
    perf.CounterName AS 'Counter',
    perf.InstanceName AS 'Instance',
    ROUND(AVG(Perf.SampleValue), 2) AS 'Avg Free Space (%)',
    COUNT(*) AS 'Sample Count'
FROM PerformanceDataAllView perf
JOIN vManagedEntity vme ON perf.ManagedEntityRowId = vme.ManagedEntityRowId
WHERE perf.CounterName = 'Free Space (%)'
AND vme.Path LIKE '%.yourdomain.com%'  -- Filter by your domain (optional)
GROUP BY vme.Path, perf.ObjectName, perf.CounterName, perf.InstanceName
HAVING ROUND(AVG(Perf.SampleValue), 2) <= 15 -- Adjust threshold as needed
ORDER BY [Avg Free Space (%)] ASC;
