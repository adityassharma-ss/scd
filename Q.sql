WITH cte_netcool AS (
    SELECT
        DATEADD(MINUTE, DATEDIFF(MINUTE, GETDATE(), GETUTCDATE()), [FIRSTOCCURRENCE]) as UTC_FIRSTOCCURRENCE,
        [FIRSTOCCURRENCE] as FIRSTOCCURRENCE,
        [ALERTKEY] AS AlertKey,
        [AlertGroup] as AlertGroup,
        [INCIDENTNUMBER] as [Incident Number],
        [SUPPRESSESCL] AS SupprEscl,
        [EVENTID] as EVENTID,
        [ConfigurationItem] as ConfigurationItem,
        [Node] as Node,
        [Agent] as Agent,
        [Summary] as Summary,
        [MANAGER]
    FROM
        [netcool].[dbo].[REPORTER_STATUS]
    WHERE
        [MANAGER] in ('SCOM Probe: JNJWEBPING', 'SCOM Probe: JNJWEBPING-2016') 
        AND [ConfigurationItem] like 'http://VHCITSHAWBOG9/SIGN_ING/ASSETS%'
)
SELECT
    [FIRSTOCCURRENCE] as time,
    DATEDIFF(second, '1970-01-01', [FIRSTOCCURRENCE]) AS unix_timestamp,
    [AlertKey],
    [AlertGroup],
    [Incident Number] as IncidentNumber,
    [SupprEscl],
    [EVENTID],
    [ConfigurationItem],
    [Node],
    [Agent],
    [MANAGER],
    [Summary]
FROM
    cte_netcool
WHERE
    FIRSTOCCURRENCE BETWEEN '2025-01-07T07:26:33Z' AND '2025-01-07T10:26:33Z'
ORDER BY
    FIRSTOCCURRENCE ASC
