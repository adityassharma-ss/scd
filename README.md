# Implementation Document: SCOM Monitoring Addition
**Change Task:** CTASK000000138105  
**Change Request:** CHG000000031781  
**Priority:** 4-Low  
**Risk Level:** High  
**Project:** Diamond Project - MTO Cutover (JNJ to Kenvue Environment)

## 1. Overview
### 1.1 Purpose
This document outlines the implementation procedure for adding 8 servers to SCOM monitoring for the PAS-X BRAZIL-PROD environment as part of the Diamond Project cutover from JNJ to Kenvue environment.

### 1.2 Scope


### 1.3 Target Servers
1. 

## 2. Prerequisites
### 2.1 System Requirements
- Windows Server operating system
- Network connectivity to SCOM Management Server
- Minimum 4GB RAM
- 2GB free disk space
- .NET Framework 4.5 or higher

### 2.2 Access Requirements
- Local Administrator access on target servers
- SCOM Administrator privileges
- Change window approval
- Backup verification

## 3. Implementation Procedure
### 3.1 Pre-Implementation Checks
1. Verify server accessibility
   - Ping test
   - Remote Desktop connectivity
   - Service account access validation
   
2. System State Verification
   - Check CPU/Memory utilization
   - Verify disk space
   - Document current monitoring status

### 3.2 SCOM Agent Installation
1. Management Server Preparation
   - Login to SCOM Management Server
   - Download agent installation package
   - Verify package version compatibility

2. Agent Deployment
   ```powershell
   # Run on each target server
   msiexec /i MOMAgent.msi /qn MANAGEMENT_GROUP=ProdGroup MANAGEMENT_SERVER_DNS=SCOM.kenvue.com ACTIONS_USE_COMPUTER_ACCOUNT=1
   ```

3. Agent Configuration
   ```powershell
   # Configure Agent Settings
   Set-SCOMAgentConfiguration -AgentName $serverName -Parameter "HeartbeatInterval" -Value 300
   ```

### 3.3 Monitoring Configuration
1. Management Pack Configuration
   - Import required management packs
   - Configure monitoring templates
   - Set up alert thresholds

2. Alert Rules Setup
   - CPU monitoring (>80% threshold)
   - Memory utilization (>90% threshold)
   - Disk space monitoring (<10% free space)
   - Service availability monitoring

## 4. Verification Steps
### 4.1 Agent Health Check
- Verify agent installation status
- Check agent heartbeat
- Validate management server communication

### 4.2 Monitoring Validation
- Test alert generation
- Verify performance data collection
- Check reporting functionality

## 5. Post-Implementation Tasks
### 5.1 Documentation Updates
- Update CMDB with new configurations
- Document installed agent versions
- Record any deviations from standard configuration

### 5.2 Monitoring Period
- 24-hour observation period
- Performance impact assessment
- Alert pattern analysis

## 6. Rollback Procedure
### 6.1 Rollback Triggers
- System performance degradation
- Alert storm
- Communication failures

### 6.2 Rollback Steps
```powershell
# Uninstall SCOM Agent
msiexec /x {786970C5-E6F6-4A41-B238-AE25D4B91EEA} /qn

# Remove Registry Keys
Remove-Item -Path "HKLM:\SOFTWARE\Microsoft\Microsoft Operations Manager\*" -Recurse
```

## 7. Contacts and Escalation Path
### 7.1 Primary Contacts
- Implementation Team: WINDOWS L1
- Technical Lead: [Name]
- Project Manager: [Name]

### 7.2 Escalation Path
1. Level 1: WINDOWS L1 Team
2. Level 2: SCOM Administration Team
3. Level 3: Infrastructure Management Team

## 8. Sign-off Requirements
- Implementation Engineer
- Technical Lead
- Change Manager
- Application Owner

## 9. Success Criteria
- All 8 servers showing "Healthy" status in SCOM
- Performance data being collected successfully
- Alerts generating and resolving as expected
- No impact on application performance
- All documentation updated and verified
