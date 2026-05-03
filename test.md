## Architecture & Design: Azure Enterprise-Scale / PCF V2 — RBAC (PCFv2)

Uniper requires a defined Azure RBAC model (aligned to least privilege/need-to-know) for Enterprise Scale@Uniper management groups and landing zone subscriptions, including group creation, role assignment, approvals, monitoring, and emergency access.

---

### Table of Contents
- Document Metadata
- Problem Statement
- Design Goals & Non-Goals
- Architecture Overview
- Design Options Considered
- Chosen Design & Rationale
- Security, HA & DR Considerations
- Operational Implications
- Risks & Assumptions
- Design Constraints & Dependencies (OPTIONAL)
- Lifecycle & Evolution Considerations (OPTIONAL)
- Out-of-Scope / Deferred Decisions (OPTIONAL)
- References

---

## CORE SECTIONS (MANDATORY)

### 1. Document Metadata

| Field | Value |
|------|------|
| Architecture ID |  |
| Service / Platform | Azure Enterprise-Scale / PCF V2 (Enterprise Scale@Uniper / PCFv2) |
| Author | Indhumathi Subramanian (Cloud Security & IAM consultant) |
| Reviewers | UNIPER architects; UNIPER Enterprise Scale@Uniper project management |
| Status | Draft |
| Version | 1.0 |
| Last Updated | 2023-02-06 |

**Document Information (Table 1: Document Information)**

| Date | Version | Name | Role | Comments |
| --- | --- | --- | --- | --- |
| 06/02/2023 | 1.0 | Indhumathi Subramanian | Cloud Security & IAM consultant | Initial draft |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

**Distribution List (Table 2: Distribution List)**

| Distributed to | Role | Company |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

**Supporting Documents (Table 3: Supporting Documents)**

| Document Name | Version |
| --- | --- |
| Azure Enterprise-Scale / PCF V2  <br>High Level Design Document <br> | Version 1.0 |

---

### 2. Problem Statement

Uniper has Azure AD at present, which is synced with On-Premises active directory. RBAC is an authorisation system built on Azure Resource Manager that provides fine-grained access management of Azure resources. Using RBAC, you can restrict access based on the need to know and least privilege security principles. Access management for cloud resources is a critical function for UNIPER when using cloud services.

Role-based access control provides each worker privileges based on what role they have in the organization.

A control is a safeguard or countermeasure designed to preserve Confidentiality, Integrity and Availability of data. This, of course, is the CIA Triad.

Access control involves limiting what objects can be available to what subjects according to what rules.

Access controls are not just about restricting access to information systems and data, but also about allowing access. It is about granting the appropriate level of access to authorized personnel and processes and denying access to unauthorized functions or individuals.

Role-based access control provides each application team member/HaCT Cloud Engineer privileges based on what role they have in the organization.

---

### 3. Design Goals & Non-Goals

**Goals**
- Document RBAC requirements, detailed RBAC structure, RBAC configurations and maintenance of these RBAC infrastructure which will be deployed in Enterprise Scale@Uniper, its management groups and landing zone subscriptions.
- Restrict access based on “need to know” and “least privilege” security principles for Azure resources managed under Azure Resource Manager (RBAC).
- Provide a standardized approach for:
  - AD Group creation (including naming conventions and descriptions)
  - Role assignments (default and role-specific)
  - Approval workflow (Four Eye audit process)
  - Monitoring/alerting of critical role assignments and custom role activities
  - Emergency access (“break glass”) account approach
  - Role assignment backup and AD group membership backup reporting
- Ensure access is granted appropriately to authorized personnel and processes and denied to unauthorized functions or individuals.

**Non-Goals**
- Detailed explanation about IaC will be covered in Low level design of HaCT Platform automation.
- Alert rule topic is not completed; Rule name and details are required.
- Remarks – Description about the Initiatives and Policies are explained in the Governance LLD document.

---

### 4. Architecture Overview

**Overview / Purpose / Audience**
- This LLD documents covers RBAC requirements, detailed RBAC structure, RBAC configurations and maintenance of these RBAC infrastructure which will be deployed in Enterprise Scale@Uniper, its management groups and landing zone subscriptions.
- The intended audience for this document will be UNIPER architects and UNIPER Enterprise Scale@Uniper project management.

**Azure Enterprise Scale@Uniper Architecture**
- Figure 1: ES@Uniper Architecture (image ignored)

Remarks: There are role assignments that inherited from the tenant's scope and role assignments that result from policy assignments. The role assignments are tabulated/listed out in the Table 29

**Azure Enterprise Scale@Uniper – HaCT Cloud Engineer RBAC Architecture**
- Figure 2: ES@Uniper - HaCT Cloud Engineer Access (image ignored)

**Azure Enterprise Scale@Uniper – Application Team RBAC Architecture**
- Figure 3: ES@Uniper - Application Team Access (image ignored)

Remark: Detailed explanation regarding the default role is provided under the section 9.

**How are Security AD Groups created?**
- Application Owners and Team Members order subscriptions by submitting requests to create subscriptions using catalogue services.
- During the process of deployment of Subscriptions via IaC *, respective AD Groups are created with the standard naming convention pattern and Application Managers are assigned as Owners/Member of AD Groups.

Remarks: * Owned/Supported HaCT Automation Team

Detailed explanation about IaC will be covered in Low level design of HaCT Platform automation

AD Group creation and Role Assignment for application team are automated.

**Naming Convention**
PCFv2 security AD group convention pattern is used.

AZ-              PCFv2-CORP-DEV-C_MA3-DTFU081-01-           READER

AZ-<Subscription name>-READER

AZ-<Subscription name>-CONTRIBUTOR

Example:

DEV Environment

Subscription Name - "PCFv2-CORP-DEV-C_MA3-DTFU081-01"

AD Group Name - AZ-PCFv2-CORP-DEV-C_MA3-DTFU081-01-READER

Group Description - [CreatedBy:HaCT][CreatedFor:<EAMID of Application>] Granting Reader access for users on subscription.

AD Group Name - AZ-PCFv2-CORP-DEV-C_MA3-DTFU081-01-CONTRIBUTOR

Group Description - [CreatedBy:HaCT][CreatedFor:<EAMID of Application>] Granting Contributor access for users on subscription.

PROD Environment

Subscription Name - "PCFv2-CORP-PRD-C_MA3-DTFU081-01"

AD Group Name - AZ-PCFv2-CORP-PRD-C_MA3-DTFU081-01-READER

Group Description - [CreatedBy:HaCT][CreatedFor:<EAMID of Application>] Granting Reader access for users on subscription.

Remarks: Security AD Group created are only used for the purpose of ES@Uniper RBAC for application team members.

**RACI Matrix for Landing Zone subscriptions (Table 4: Responsibility assignment matrix)**

| R = Responsibilities<br>A = Accountable<br>C = Consulted<br>I = Informed | Application Team | HaCT Cloud Engineer |
| --- | --- | --- |
| Requesting for new AD group creation other than default | R, A |  |
| Create of role assignment other than default | R, A | C, I |
| Deletion of role assignment other than default | R, A | C, I |
| Access for Application member | R, A |  |
| Process of Approval flow | R, A |  |
| Custom role creation | C, I | R, A |
| Excluding/Exemption of Policy | C, I | R, A |

**AD Group creation & Role Assignment (Table 5: In/Out Scope - AD Group creation and Role Assignment)**

| HaCT   Responsibilities |
| --- |
| 1. HaCT Team will be creating AD Group and performing default role assignments to Application Team on their ordered subscription.<br>2. AD Group creation and Role Assignments for HaCT Cloud Engineers are performed manually in MVP1.0 roll out by UIT HaCT Security Services uit-hact-security-services@uniper.energy.<br>3. PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services uit-hact-security-services@uniper.energy.<br> |
| 1. HaCT Team will be creating AD Group and performing default role assignments to Application Team on their ordered subscription.<br>2. AD Group creation and Role Assignments for HaCT Cloud Engineers are performed manually in MVP1.0 roll out by UIT HaCT Security Services uit-hact-security-services@uniper.energy.<br>3. PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services uit-hact-security-services@uniper.energy.<br> |
| 1. HaCT Team will be creating AD Group and performing default role assignments to Application Team on their ordered subscription.<br>2. AD Group creation and Role Assignments for HaCT Cloud Engineers are performed manually in MVP1.0 roll out by UIT HaCT Security Services uit-hact-security-services@uniper.energy.<br>3. PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services uit-hact-security-services@uniper.energy.<br> |

**Access and Approval for App Team members (Table 6: In/Out Scope - Access for App Team members)**

| Responsibilities | Responsibilities |
| --- | --- |
| Application Team | HaCT Team |
| Application Manager is responsible to grant access to Application Team member on the required subscription<br>Grant/Revoke access to Application team must be taken care by Application Manager.<br><br>Application Managers must assess permitted users and give application team members access. | HaCT Team will be creating the default AD Groups with access on the subscriptions (section 7.2.), assign App Manager as Owner of AD Groups of Contributor and Reader ad group & Member of Reader AD Group (section 8.2.).<br>Will share the details to App Manager.<br> |

**Creation/Deletion new AD Group (Table 7: In/Out Scope - Creation/Deletion new AD Group)**

| Responsibilities | Responsibilities |
| --- | --- |
| Application Team | HaCT Team |
| Application Team needs to contact the UNIPER Directory Service team. | HaCT is not responsible for creating the AD Group for Enterprise Scale@Uniper except for the default AD Groups. |
| AD Group should be Security type with proper description. | HaCT team will be removing the role assignment of other AD Group type role assignment except Security type ad groups |
| Addition/Removal of Members into the AD Group should be taken care by Application Team or via UNIPER Directory Service team. |  |

**Role Assignment (Table 8: In/Out Scope - Role Assignment)**

| Responsibilities | Responsibilities |
| --- | --- |
| Application Team | HaCT Team |
| App Team's responsible to perform the role assignment for themselves on-demand | HaCT Team will be working on to identify other critical roles. If HaCT identifies Critical role, it will get appended to the list. |
| Application team are requested to use the Least privilege principle and perform the role assignment. Recommendation from HaCT is to check resource specific role and assign what is required to perform the activity.<br>Critical/High Privilege role - “Owner, User Access Administrator, Resource Policy Contributor “are requested not use across ESLZ subscriptions/Resource Groups/Resources | If in case mentioned role assignments are identified during audit process, HaCT Team will removing immediately |
|  | On noticing role assignments apart from Reader for Application team members in PROD subscription, HaCT Team will be removing the respective role assignment. |

**Custom Role Creation (Table 9: In/Out Scope - Custom Role creation)**

| Responsibilities | Responsibilities |
| --- | --- |
| Application Team | HaCT Team |
| Not to create custom role, in most of the use case Contributor access will be sufficient for SPN to deploy/create/modify/update/delete. | When App team creates custom role, Custom role is also will be removed. App Team must place consultation call with HaCT Security & IAM team. In case of valid business justification, Post Service Owner, Application Team will be allowed to create custom role. |
| In case of custom role, request you to take consultation call with HaCT Security & IAM Team |  |

---

### 5. Design Options Considered

---

### 6. Chosen Design & Rationale

**RBAC – Application Team (Table 10: App Team - Default Role Description)**

| Azure | Subscription Name | Role Name |
| --- | --- | --- |

**Azure AD Group Ownership and Membership**
During the deployment of subscription and its respective AD groups, Application Manager will be configured as Owner of Reader and Contributor ad groups.

Table 11: AAD Group Member and Owner

| Role Name | Type | Description |
| --- | --- | --- |
| Reader | Built-in | View all resources but does not allow you to make any changes. |
| Contributor | Built-in | Grants full access to manage all resources but does not allow you to assign roles in Azure RBAC, manage assignments in Azure Blueprints, or share image galleries. |
| User Access Administrator | Built-in | Let’s you manage user access to Azure resources. |
| Support Request Contributor | Built-in | Let’s you create and manage Support requests |
| Storage Blob Data Reader | Built-in | Allows for read access to Azure Storage blob containers and data |

\*Application Manager can add his application team members into the AD Groups depending on the requirement.

**Lower Environment – DEV/SANDBOX (Table 12: Application Team Access - Lower Environment)**

| Security Principal | DEV & SANDBOX | Scope of Access | PIM (Yes/No) |
| --- | --- | --- | --- |
| User | Reader | Subscription | No |
| User | Contributor | Subscription | No |
| Service Principal | Contributor | Subscription | -NA- |
| Service Principal | User Access Administrator | Subscription | -NA- |

Business Justification/Reason of above role assignments:
- Contributor access granted to application users and service principals to deployment of resources.
- UAM access is assigned to Application SP to create/delete the role assignments to Application team members and SPs.
- PIM is not implemented for Application team members in Lower environment

**Upper Environment – UAT/PROD (Table 13: Application Team Access - Upper Environment)**

| Security Principal | UAT & PROD | Scope of Access | PIM (Yes/No) |
| --- | --- | --- | --- |
| User | Reader | Subscription | No |
| User | Support Request Contributor | Subscription | No |
| Service Principal | Contributor | Subscription | -NA- |
| Service Principal | User Access Administrator | Subscription | -NA- |

Business Justification/Reason of above role assignments:
- Contributor access granted to application service principals to deployment of resources.
- Application team members will have only Reader permissions.
- UAM access is assigned to Application SP to create/delete the role assignments to Application team members and SPs.
- PIM is not implemented for Application team members in PROD environment because they will be assigned with Reader role as this role will not allow them to modify/delete resources.

**HaCT – Cloud Engineer – Default Access (Table 14: Default Access - HaCT Cloud Engineer)**

| HaCT Stream | Access - Role | Scope of Access | PIM (Yes/No) | Security AD Group |
| --- | --- | --- | --- | --- |
| HaCT- Security IAM | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |
| HaCT- Architect | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |
| HaCT- Governance | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |
| HaCT- Network Admins | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |
| HaCT- Monitoring Admin | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |
| HaCT- Automation | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |
| HaCT- Dev team | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |
| HaCT- Database Team | Reader | PCFv2 Management Group | No | AZ-HaCT-USERS-PCFv2-READER |

Business Justification/Reason of above role assignments:
- Default all the HaCT Cloud Engineers must have Reader access from the scope of PCFv2 Management Group to monitor the PCFv2 estate.
- As IaaS components are not involved in PCFv2, we are not granting access to HaCT Infra team

Remarks
- “AZ-HaCT-USERS-PCFv2-READER“ Reader AD Group will grant only access to ES@Uniper and not used in PCFv1.
- AD Group creation and Role Assignment for HaCT Cloud Engineer are manually performed by UIT HaCT Security Services uit-hact-security-services@uniper.energy
- PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services uit-hact-security-services@uniper.energy

**HaCT – Cloud Engineer - Role Specific Access (Table 15: HaCT Cloud Engineer - Role Specific Access)**

| HaCT Stream | Access - Role | Scope of Access | PIM (Yes/No) | PAG - PIM Security AD Group |
| --- | --- | --- | --- | --- |
| HaCT- Security IAM | User Access Administrator | PCFv2 Management Group | Yes | AZ-HaCT-PIM-Security Team |
| HaCT- Governance | Resource Policy Contributor | PCFv2 Management Group | Yes | AZ-HaCT-PIM-Governance Team |
| HaCT- Governance | User Access Administrator | PCFv2 Management Group | Yes | AZ-HaCT-PIM-Governance Team |
| HaCT- Network Admins | Network Contributor | PCFv2 Management Group | Yes | AZ-OurConnectivity-PIM-Cloud Network Team |
| HaCT- Monitoring Admin | Monitoring Contributor | PCFv2 Management Group | Yes | AZ-HaCT-PIM-Monitoring Team |
| HaCT - Contributor | Contributor | PCFv2 Management Group | Yes | AZ-HaCT-PIM-UPCFv2-CONTRIBUTOR |

Business Justification/Reason of above role assignments:
- HaCT- Security IAM – To perform create/delete role assignment across PCFv2
- HaCT- Governance – To deploy/support Policy in PCFv2 estate
- HaCT- Network Admins – To deploy network components like VNet, subnet, VNet Peering, to support Application team member during their Network components deployment
- HaCT- Monitoring Admin – Configure Alerts, alert rule, action groups
- HaCT – Contributor – To create resource group for HaCT internal purpose if required (on-demand).

Remarks
- Except “AZ-HaCT-PIM-UPCFv2-CONTRIBUTOR “all the other PAG AD Groups mentioned in the above Table are used to grant access to HaCT Cloud Engineers in PCFv1 as well as in ES@Uniper.

**HaCT – Automation Service Principal - Role Specific Access (Table 16: HaCT Platform Automation - Service Principal Access)**

| HaCT Stream | Access - Role | Scope of Access | PIM (Yes/No) |
| --- | --- | --- | --- |
| HaCT- Automation - SP | Contributor | PCFv2 Management Group | -NA- |
| HaCT- Automation - SP | User Access Administrator | PCFv2 Management Group | -NA- |

Business Justification/Reason of SP role assignments:
- Contributor – To create subscriptions (subscription-Lifecycle), storage account to store deployment state files
- User Access Administrator – To perform create/delete role assignment of Application Team

**Azure AD Role – HaCT Security and IAM Team**
HaCT team must reach out to UNIPER Directory service team to get the roles assigned.

Catalog to place access request with Uniper Directory Service team is Directory Service - Request Azure / M365 administrator role assignment or removal

Remark: while placing request, select Azure Active Directory (Uniper SE) PROD

Table 17: Azure AD Role - HaCT Security and IAM Team

| Role Name | Type | Description |
| --- | --- | --- |
| Privileged Role Administrator | Built-in | Can manage role assignments in Azure AD, and all aspects of Privileged Identity Management. |
| Groups Administrator | Built-in | Members of this role can create/manage groups, create/manage groups settings like naming and expiration policies, and view groups activity and audit reports. |

**Approval Workflow**
Access approval refers to the process of granting permission or authorization to a user to access a particular resource or system. This is typically done by an authorized individual or team who reviews the request and determines if the user has a legitimate need for access and if granting access is in line with the organization's security policies and procedures. Once the approval is granted, the user is provided with the necessary credentials or permissions to access the resource.

As per HaCT IAM standard, HaCT will be Four Eye audit process, i.e two-step approval process.

First Approval from HaCT Head and second approval from respective Service Owner,

Table 18: HaCT Head - Approver

| HaCT Head |
| --- |
| Whillans, Mathew <mathew.whillans@uniper.energy> |

Table 19: HaCT Stream - Service Owners

| HaCT Stream Lead | HaCT Stream Lead |
| --- | --- |
| Database | Wittich, Mark <mark.wittich@uniper.energy> |
| Automation | Richards, Gareth <gareth.richards@uniper.energy> |
| Development | Schmitz, Carsten <carsten.schmitz@uniper.energy> |
| Architect | Stolcz, Tamas <Tamas.Stolcz2@uniper.energy> |
| Infrastructure | Arunachalam, Selvam <selvam.arunachalam@uniper.energy> |
| Network | Abbott, Steve <steve.abbott@uniper.energy> |
| Operations | Sidhu, Amerdeep <Amerdeep.Sidhu.ext@uniper.energy> |
| Security & IAM | Heil, Sebastian <sebastian.heil@uniper.energy> |
| Monitoring | Arunachalam, Selvam <selvam.arunachalam@uniper.energy> |
| Optimization | Steinemann, Daniel <Daniel.Steinemann.ext@uniper.energy> |
| Governance | Daniel Steinemann/Sebastian Heil |
| Scrum Board | Röckel, Heike <Heike.Roeckel@uniper.energy> |

**Permission – Azure RBAC for PCFv2 (Table 20: Role Description)**

| Role Name | Type | Description |
| --- | --- | --- |
| Reader | Built-in | View all resources but does not allow you to make any changes. |
| Contributor | Built-in | Grants full access to manage all resources but does not allow you to assign roles in Azure RBAC, manage assignments in Azure Blueprints, or share image galleries. |
| User Access Administrator | Built-in | Let’s you manage user access to Azure resources. |
| Resource Policy Contributor | Built-in | Users with rights to create/modify resource policy, create support ticket and read resources/hierarchy. |
| Network Contributor | Built-in | Let’s you manage networks, but not access to them. |
| Monitoring Contributor | Built-in | Can read all monitoring data and update monitoring settings. |
|  |  |  |

**Permission Details of role**
This section is about the permission details of each role from the section 5 and section 6

Reader-Permissions  
actions:

| "*/read" |
| --- |

Contributor - Permissions  
actions:

| “*” |
| --- |

notactions:

| "Microsoft.Authorization/*/Delete",<br>"Microsoft.Authorization/*/Write",<br>"Microsoft.Authorization/elevateAccess/Action",<br>"Microsoft.Blueprint/blueprintAssignments/write",<br>"Microsoft.Blueprint/blueprintAssignments/delete",<br>"Microsoft.Compute/galleries/share/action" |
| --- |

User Access Administrator -Permissions  
actions:

| "*/read",<br>"Microsoft.Authorization/*",<br>"Microsoft.Support/*" |
| --- |

Support Request Contributor-Permissions  
actions:

| "Microsoft.Authorization/*/read",<br>"Microsoft.Resources/subscriptions/resourceGroups/read",<br>"Microsoft.Support/*" |
| --- |

Storage Blob Data Reader-Permissions  
actions:

| "Microsoft.Storage/storageAccounts/blobServices/containers/read",<br>"Microsoft.Storage/storageAccounts/blobServices/generateUserDelegationKey/action" |
| --- |

notActions: []

dataActions:

| "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read" |
| --- |

Resource Policy Contributor-Permissions  
actions:

| "*/read",<br>"Microsoft.Authorization/policyassignments/*”,<br>"Microsoft.Authorization/policydefinitions/*”,<br>"Microsoft.Authorization/policyexemptions/*”,<br>"Microsoft.Authorization/policysetdefinitions/*”,<br>"Microsoft.PolicyInsights/*”,<br>"Microsoft.Support/*”<br> |
| --- |

Network Contributor-Permissions  
actions:

| "Microsoft.Authorization/*/read”,<br>"Microsoft.Insights/alertRules/*”,<br>"Microsoft.Network/*”,<br>"Microsoft.ResourceHealth/availabilityStatuses/read”,<br>"Microsoft.Resources/deployments/*”,<br>"Microsoft.Resources/subscriptions/resourceGroups/read”,<br>"Microsoft.Support/*” |
| --- |

Monitoring Contributor-Permissions  
actions:

| "*/read”,<br>"Microsoft.AlertsManagement/alerts/*”,<br>"Microsoft.AlertsManagement/alertsSummary/*”,<br>"Microsoft.Insights/actiongroups/*”,<br>"Microsoft.Insights/activityLogAlerts/*”,<br>"Microsoft.Insights/AlertRules/*”,<br>"Microsoft.Insights/components/*”,<br>"Microsoft.Insights/createNotifications/*”,<br>"Microsoft.Insights/dataCollectionEndpoints/*”,<br>"Microsoft.Insights/dataCollectionRules/*”,<br>"Microsoft.Insights/dataCollectionRuleAssociations/*”,<br>"Microsoft.Insights/DiagnosticSettings/*”,<br>"Microsoft.Insights/eventtypes/*”,<br>"Microsoft.Insights/LogDefinitions/*”,<br>"Microsoft.Insights/metricalerts/*”,<br>"Microsoft.Insights/MetricDefinitions/*”,<br>"Microsoft.Insights/Metrics/*”,<br>"Microsoft.Insights/notificationStatus/*”,<br>"Microsoft.Insights/Register/Action”,<br>"Microsoft.Insights/scheduledqueryrules/*”,<br>"Microsoft.Insights/webtests/*”,<br>"Microsoft.Insights/workbooks/*”,<br>"Microsoft.Insights/workbooktemplates/*”,<br>"Microsoft.Insights/privateLinkScopes/*”,<br>"Microsoft.Insights/privateLinkScopeOperationStatuses/*”,<br>"Microsoft.OperationalInsights/workspaces/write”,<br>"Microsoft.OperationalInsights/workspaces/intelligencepacks/*”,<br>"Microsoft.OperationalInsights/workspaces/savedSearches/*”,<br>"Microsoft.OperationalInsights/workspaces/search/action”,<br>"Microsoft.OperationalInsights/workspaces/sharedKeys/action”,<br>"Microsoft.OperationalInsights/workspaces/storageinsightconfigs/*”,<br>"Microsoft.Support/*”,<br>"Microsoft.WorkloadMonitor/monitors/*”,<br>"Microsoft.AlertsManagement/smartDetectorAlertRules/*”,<br>"Microsoft.AlertsManagement/actionRules/*”,<br>"Microsoft.AlertsManagement/smartGroups/*”,<br>"Microsoft.AlertsManagement/migrateFromSmartDetection/*”<br> |
| --- |

**Monitoring / Alerting requirements (as provided)**
Alert Rule  
Role assignments of critical/high priority performed across UPCFv2 environment

Condition  
When critical role assignments are performed in UPCFv2 environment

Scope  
Across all scopes (Management Group, Subscription, Resource Group, Resource) in UPCFv2

Action Group  
Security and IAM Team Distribution List:  
UIT HaCT Security Services <uit-hact-security-services@uniper.energy>

Resource Group  
(where Alert rules are placed, Monitoring Team has to confirm us.)
- < TBD >

Alert Rule  
Custom roles are created performed across UPCFv2 environment

Condition  
When custom roles are created in UPCFv2 environment

Scope  
Across all scopes (Management Group, Subscription, Resource Group, Resource) in UPCFv2

Action Group  
Security and IAM Team Distribution List:  
UIT HaCT Security Services <uit-hact-security-services@uniper.energy>

Resource Group  
(where Alert rules are placed, Monitoring Team has to confirm us.)
- < TBD >

Alert Rule  
When there are critical resource deployments across PCFv2 environment.

Condition  
When there are critical resource deployments across ESLZ environment

Scope  
Across all scopes (Management Group, Subscription, Resource Group, Resource) in UPCFv2

Action Group  
Security and IAM Team Distribution List:  
UIT HaCT Security Services <uit-hact-security-services@uniper.energy>

Resource Group  
(where Alert rules are placed, Monitoring Team has to confirm us.)
- < TBD >

[Alert rule topic is not completed, Rule name and details are required]

**Break-Glass (Emergency Access)**
Introduction  
Uniper uses Conditional Access and Azure Identity Protection policies to enforce Azure Multi-Factor Authentication (MFA), to block unsupported and incompliant device platforms and to block risky sign-in attempts.

During unforeseen circumstances such as a natural disaster emergency, during which a mobile phone or other networks might be unavailable

In the worst case, these scenarios can block out users and administrator.

Emergency access accounts, often referred to as “break glass accounts”, is an important part of an organization’s disaster recovery plan. These accounts are highly privileged and should only be used when normal admin accounts can’t sign in to gain access to a system or service.

AS-IS – Break-Glass account Architecture  
Figure 4: Break-Glass account Access Framework (image ignored)

Account Configuration  
The "break glass accounts," also known as emergency access accounts, are highly privileged cloud-only accounts that are not covered by any identity-protection services. In an emergency, this makes sure that at least these accounts can log in to the Azure environment.

Table 21: Break-Glass account configuration

| Category | Current Configuration |
| --- | --- |
| Password | The password for each emergency access account must be set to ‘never expire’ |
| Password | A high complex password with at least 16 characters must be set. |
| Azure AD Role | Global Administrator |
| Azure AD Role | The role assignment must not be set to be eligible in Privileged Access<br>Management (PIM), but assigned permanently. |
| Multi-Factor Authentication | Not configured MFA |
| Multi-Factor Authentication | accounts are not connected with an employee mobile, hardware token or other employee-specific<br>credentials |
| Conditional Access | excluded from any Conditional Access policy |
| Directory synchronization | cloud-only accounts which are not synchronized with the on-premises Active Directory. |
| Cleanup tasks | excluded from any expiration and credential cleanup tasks |

SMEs: Who They Are and How to Contact Them  
AAD Break-Glass account - Username & Password

As a Global Administrator in Azure Active Directory (Azure AD), one can elevate their access as User Access Administrator which is used to role assignment to HaCT Team members. AAD Break Glass account is assigned with Global Admin access.

Username - The emergency access accounts, also named “break glass accounts”, are high privileged cloud only accounts which are excluded from any identity protection service. This ensures at least these accounts are able to sign-in to the Azure environment in case of emergency.

Break-Glass account - AZ-HACT-EAA-BrkGlass@uniper.onmicrosoft.com

Password - The password for the Break-Glass account is shared between two teams. First part of the password is with HaCT Internal members who will be available 24/7 availability. Second half of the password is with “Service Management and Integration” (SMI) team. This team offers 24/7 availability by this it can be ensured, that the 2nd password part can be accessed at any time.

Table 22: PoC for Emergency account

Validation – Break Glass account  
The procedure should be trained at least twice a year to make sure that everyone involved is aware of what to do in case of an emergency. As a result, every time it cannot be ruled out that one individual has access to both parts of the password, the password is changed.

Discuss and Plan with Service Owner on validation/training of Break Glass account.

**Azure Role Assignments Backup (daily)**
Purpose
- To have historic data of all Azure Role Assignments on a particular day
- Quickly view and compare the Role assignment changes between a time
- Easily find out all the Role Assignments done for a particulate User/Group/Service Principle or on an Azure Resource
- Analysis for Role Assignment clean-up

Technical Details
This is achieved through a PowerShell Script. The script is configured via an Azure DevOps pipeline. It scheduled to run daily and when the run is completed it generates an Excel file with all current Role assignment details on UPCFv2 Management group, and then upload the excel file to an Azure Storage Account.  
There is a service principle configured which has Reader access to UPCFv2 Management Group.

Azure Resources
A report will be uploaded to a container. The information about the storage account and related container is provided below.

- Storage Account: hactsecuritysto001
- Storage Container: upcfv2roleassignments
- DevOps Git URL: RoleAssignments - Repos (azure.com)
- DevOps Pipeline: Pipelines - Runs for Azure Role Assignment Backup UPCFv2

Scheduler/Pipeline Trigger Details
- Days: Monday - Sunday
- Time: 4.00 PM CET

Service Principal details  
Below is the Service Principle used for this purpose:  
Name: Cloud Security Services | PROD | BSN0003595 | General Automation

Service Principal Azure RBAC Permissions  
The service principle has below 2 access granted to perform the required operations:
- Reader access at “UPCFv2 Enterprise Scale” UPCFv2 Management Group → to view all Role assignments
- Storage Account Contributor access at Storage account hactsecuritysto001 → to upload the csv files as a Blob to Storage container

Service Principal Azure AD API Permissions
- Microsoft Graph - "Directory.Read.All" for Service Principal in Azure AD.

**AD Group Membership Backup (daily)**
Purpose
- To have historic data of all members of AD groups which has role assignment across PCFv2 estate on a particular day
- Quickly view and compare the memberships of AD Groups changes between a time period
- Analysis of Members of AD Groups and cleanup.

Technical Details
This is achieved through a PowerShell Script. The script is configured via an Azure DevOps pipeline. It scheduled to run daily and when the run is completed it generates an Excel file with all lists of members of AD Group which has role assignment across all scope from PCFv2 environment and then upload the excel file to an Azure Storage Account.  
There is a service principle configured which has Reader access to UPCFv2 Management Group.

Azure Resources
A report will be uploaded to a container. The information about the storage account and related container is provided below.

- Storage Account: hactsecuritysto001
- Storage Container: <TBD>
- DevOps Git URL: <TBD>
- DevOps Pipeline: <TBD>

Scheduler/Pipeline Trigger Details
- Days : Monday - Sunday
- Time : 4.00 PM CET

Service Principal Details  
Below is the Service Principle used for this purpose:  
Name: Cloud Security Services | PROD | BSN0003595 | General Automation

Service Principal Azure RBAC Permissions  
The service principle has below 2 access granted to perform the required operations:
- Reader access at “UPCFv2 Enterprise Scale” UPCFv2 Management Group → to view all Role assignments
- Storage Account Contributor access at Storage account hactsecuritysto001 → to upload the csv files as a Blob to Storage container

Service Principal Azure AD API Permissions
- Microsoft Graph - "Directory.Read.All" for Service Principal in Azure AD.

---

### 7. Security, HA & DR Considerations

**Security - Microsoft Defender for Cloud**
Services used in the platform should be secured according to Microsoft Best Practices.

Defender for Cloud periodically analyses the compliance status of your resources to identify potential security misconfigurations and weaknesses. Recommendations are the result of assessing your resources against the relevant policies and identifying resources that aren't meeting your defined requirements.

Defender for Cloud makes its security recommendations based on your chosen initiatives. When a policy from your initiative is compared against your resources and finds one or more that aren't compliant, it's presented as a recommendation in Defender for Cloud.

Across the UNIPER PCFv2 estate, Defender for Cloud offers unified security administration and threat protection. Monitor the security posture for most commonly/widely used resources we are implementing the best practises by Policy initiatives. Governance policies are used to moderate and control decision-making, to ensure compliance when necessary and to guide the creation and implementation of other resources.

Below is the list of Policy Initiatives,

A security initiative is a collection of Azure Policy definitions, or rules, are grouped together towards a specific goal or purpose.

Security recommendations are implemented by initiatives/policies to our subscriptions.

Policies and Initiatives  
Remarks – Description about the Initiatives and Policies are explained in the Governance LLD document.

Guest account permission on azure resources (Table 23: Security Initiative - Guest Account Permission)

| Initiatives Name | Policy Display Name |
| --- | --- |
| Name: gov initiative security compliance | · gov policy Guest accounts with write permissions on Azure resources should be removed_disabled |
| Name: gov initiative security compliance | · gov policy Guest accounts with owner permissions on Azure resources should be removed_disabled |

Audit for compliance of minimum TLS version (Table 24:  Security Initiative - Audit on TLS version)

| Initiatives Name | Policy Display Name |
| --- | --- |
| Name: gov initiative security tls compliance | · gov policy dbformysql security mintlsversion 1.2_deny |
| Name: gov initiative security tls compliance | · gov policy postgresql security mintlsversion 1.2_deny |
| Name: gov initiative security tls compliance | · gov policy storage security mintlsversion 1.2_deny |
| Name: gov initiative security tls compliance | · gov policy web sites security mintlsversion 1.2_deployifnotexists |
| Name: gov initiative security tls compliance | · gov policy sql security mintlsversion 1.2_deny |

Security features – Storage Account (Table 25: Security Initiative - Storage Account)

| Initiatives Name | Policy Display Name |
| --- | --- |
| Name: gov initiative storage account | · gov policy Storage accounts should restrict network access using virtual network rules_deny |
| Name: gov initiative storage account | · gov policy public network access should be disabled for azure file sync_deny |
| Name: gov initiative storage account | · gov policy storage account public access should be disallowed_deny |
| Name: gov initiative storage account | · gov policy secure transfer to storage accounts should be enabled_deny |
| Name: gov initiative storage account | · gov policy storage accounts should have the specified minimum tls version_deny |
| Name: gov initiative storage account | · gov policy Storage Account should have soft delete enabled_deny |

Network Policy (Table 26:  Security Initiative - Network Policy)

| Initiatives Name | Policy Display Name |
| --- | --- |
| Name: gov initiative network policy | · gov policy network interfaces should disable ip forwarding_deny |
| Name: gov initiative network policy | · gov policy azure web application firewall should be enabled for azure front door entry-points_deny |
| Name: gov initiative network policy | · gov policy web application firewall (waf) should be enabled for application gateway_deny |

SQL Policy Initiatives (Table 27:  Security Initiative - SQL PAAS)

| Initiatives Name | Policy Display Name |
| --- | --- |
| Name: gov initiative sql policy | · gov policy azure sql database should have azure active directory only authentication enabled_deny |
| Name: gov initiative sql policy | · gov policy azure sql managed instance should have azure active directory only authentication enabled_deny |
| Name: gov initiative sql policy | · gov policy public network access on azure sql database should be disabled_deny |
| Name: gov initiative sql policy | · gov policy enforce ssl connection should be enabled for postgresql database servers_deny |
| Name: gov initiative sql policy | · gov policy enforce ssl connection should be enabled for mysql database servers_deny |
| Name: gov initiative sql policy | · gov policy private endpoint connections on azure sql database should be enabled_deny |
| Name: gov initiative sql policy | · gov policy private endpoint should be enabled for mysql servers_deny |
| Name: gov initiative sql policy | · gov policy Private endpoint should be enabled for PostgreSQL servers_deny |

KeyVault - Policy Initiatives (Table 28:  Security Initiative – KeyVault)

| Initiatives Name | Policy Display Name |
| --- | --- |
| Name: gov initiative keyvault policy | · gov policy key vaults should have purge protection enabled_deny |
| Name: gov initiative keyvault policy | · gov policy key vaults should have soft delete enabled_deny |

**Role Assignment – scope – Tenant**
Below is the list of role assignments which are inherited from the scope of Tenant.

Table 29: Existing - Role Assignment

| DisplayName | RoleDefinitionName | ObjectType | Comments |
| --- | --- | --- | --- |
| 89c1d63b423a47d58f7f2929 | Website Contributor | ServicePrincipal | Policy Assignment |
| 8f78da66f15a4bbe8e13fbec | Backup Contributor | ServicePrincipal | Policy Assignment |
| 8f78da66f15a4bbe8e13fbec | Virtual Machine Contributor | ServicePrincipal | Policy Assignment |
| 93f538cecd934a278ee7ddd3 | Contributor | ServicePrincipal | Policy Assignment |
| AZ-F_OI2-E3-Security Administrator-CDC-Team | HaCT | Security Administrator | Defender for Cloud Alerts | Group | Uniper CDC Team access |
| AZ-F_OI3-B4-Cost-Management-Reader | HaCT-Cost Management Reader | Group | Application Managers are granted with Cost Management access |
| AZ-HaCT-PIM-Owner | Owner | Group | Subscription Owner |
| AZ-HaCT-PIM-Security Team | User Access Administrator | Group | HaCT Security and IAM Team |
| AZ-HaCT-PIM-UAM Access | User Access Administrator | Group | Subscription Owner |
| AZ-Tenant Root Management Group Reader-HaCT | Reader | Group | Azure LightHouse AD Groups from scope of Tenant |
| AZ-Tenant Root Management Group Reader-Others | Reader | Group | Azure LightHouse AD Groups from scope of Tenant |
| azmonreschealth-prd-logicapp-001 | Reader | ServicePrincipal | * |
| azmonreschealth-rich | Reader | ServicePrincipal | * |
| b418938ccd924c8eada965a6 | Website Contributor | ServicePrincipal | Policy Assignment |
| Cloud Security Services | PROD | BSN0003595 | General Automation | Reader | ServicePrincipal | Security and IAM Pipeline Devops service principal |
| Cloud Security Services | PROD | BSN0003595 | General Automation | Reader | ServicePrincipal | Security and IAM Pipeline Devops service principal |
| CloudWorks Automation Services | PROD | bsn0001358 | CloudWorks ESLZ Automation | Contributor | ServicePrincipal | HaCT Automation team's service principal |
| CMCAzurePortal | PROD | 200188 | Reader | ServicePrincipal | HaCT Automation team's service principal |
| testexport | Reader | ServicePrincipal | * |
| reservationchecker | Reader | ServicePrincipal | * |
| cmdbextract | Azure Kubernetes Service RBAC Reader | ServicePrincipal | * |
| cmdbextract | Website Contributor | ServicePrincipal | * |
| cmdbextract | Reader | ServicePrincipal | * |
| cmdbextract | Virtual Machine Contributor | ServicePrincipal | * |
| cmdbextract2 | Azure Kubernetes Service Cluster User Role | ServicePrincipal | * |
| cmdbextract2 | Azure Kubernetes Service Contributor Role | ServicePrincipal | * |
| cmdbextract2 | Azure Kubernetes Service Cluster Admin Role | ServicePrincipal | * |
| cmdbextract2 | Azure Kubernetes Service RBAC Cluster Admin | ServicePrincipal | * |
| cmdbextract2 | Reader | ServicePrincipal | * |
| cmdbextract2 | Virtual Machine Contributor | ServicePrincipal | * |
| cmdbextract3 | Reader | ServicePrincipal | * |
| cmdbextract3 | Virtual Machine Contributor | ServicePrincipal | * |
| cmdbkaren | Reader | ServicePrincipal | * |
| d62fc8165cfa45c3b2596861 | Contributor | ServicePrincipal | Policy Assignment |
| Mandiant ASM | Reader | ServicePrincipal | * |
| Stolcz, Tamas, T13508@uniper.energy | Owner | User | Subscription Owner |
| Stolcz, Tamas (CMC - Service Admin), tamas.stolcz_outlook.com#EXT#@Uniper.onmicrosoft.com | Owner | User | Subscription Owner |

Remarks: * - The justification for the role assignment must be examined and documented.

**Important Note**
- Security AD Group created are only used for the purpose of ES@Uniper RBAC for application team members.
- AD Group creation and Role Assignment for application team are automated.
- PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services uit-hact-security-services@uniper.energy
- AD Group creation and Role Assignment for HaCT Cloud Engineer are manually performed by UIT HaCT Security Services uit-hact-security-services@uniper.energy
- Application Managers must assess permitted users and give application team members access.

**HA & DR**
Emergency access accounts (“break glass accounts”) are described as an important part of an organization’s disaster recovery plan. These accounts are highly privileged and should only be used when normal admin accounts can’t sign in to gain access to a system or service.

---

### 8. Operational Implications

- AD Group creation and Role Assignment for application team are automated (during subscription deployment via IaC; Owned/Supported HaCT Automation Team).
- AD Group creation and Role Assignment for HaCT Cloud Engineer are manually performed by UIT HaCT Security Services <uit-hact-security-services@uniper.energy> (noted for MVP1.0 roll out).
- PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services <uit-hact-security-services@uniper.energy>.
- Application Manager operational responsibilities:
  - Responsible to grant access to Application Team member on the required subscription.
  - Grant/Revoke access to Application team must be taken care by Application Manager.
  - Application Managers must assess permitted users and give application team members access.
  - Application Manager is configured as Owner of Reader and Contributor AD groups; can add application team members into the AD Groups depending on requirement.
- Request and approval operations:
  - HaCT IAM standard: Four Eye audit process, i.e two-step approval process:
    - First Approval from HaCT Head
    - Second approval from respective Service Owner
- Monitoring/Alerting operations (TBDs exist):
  - Critical/high priority role assignments alerting across UPCFv2 across all scopes; action group distribution list UIT HaCT Security Services <uit-hact-security-services@uniper.energy>; Resource Group for alert rules is <TBD> pending Monitoring Team confirmation.
  - Custom role creation alerting across UPCFv2 across all scopes; action group distribution list UIT HaCT Security Services <uit-hact-security-services@uniper.energy>; Resource Group is <TBD>.
  - Critical resource deployments alerting across UPCFv2 across all scopes; action group distribution list UIT HaCT Security Services <uit-hact-security-services@uniper.energy>; Resource Group is <TBD>. Note: alert rule topic not completed; rule name and details required.
- Reporting/backup operations (Azure DevOps pipelines and storage):
  - Azure Role Assignments backup daily at 4.00 PM CET (Mon–Sun) producing Excel; uploads to Storage Account hactsecuritysto001, Container upcfv2roleassignments; uses Service Principal “Cloud Security Services | PROD | BSN0003595 | General Automation” with Reader on UPCFv2 MG and Storage Account Contributor on hactsecuritysto001; Microsoft Graph permission Directory.Read.All.
  - AD group membership backup daily at 4.00 PM CET (Mon–Sun) producing Excel; uploads to Storage Account hactsecuritysto001; Container/Git URL/Pipeline are <TBD>; uses same Service Principal and permissions.
- Directory Service operational dependency:
  - HaCT team must reach out to UNIPER Directory service team to get Azure AD roles assigned using catalog: “Directory Service - Request Azure / M365 administrator role assignment or removal”
  - Remark: while placing request, select Azure Active Directory (Uniper SE) PROD
- Break Glass operational validation:
  - The procedure should be trained at least twice a year.
  - Every time it cannot be ruled out that one individual has access to both parts of the password, the password is changed.
  - Discuss and Plan with Service Owner on validation/training of Break Glass account.

---

### 9. Risks & Assumptions

- Risk / Audit note: Tenant-scope inherited role assignments list includes entries marked with “*”; the justification for the role assignment must be examined and documented.
- Risk: Use of critical/high privilege roles (“Owner, User Access Administrator, Resource Policy Contributor”) across ESLZ subscriptions/resource groups/resources is requested not to be used; if identified during audit process, HaCT Team will remove immediately.
- Risk: On noticing role assignments apart from Reader for Application team members in PROD subscription, HaCT Team will be removing the respective role assignment.
- Risk: If App team creates custom role, custom role will be removed; App Team must place consultation call with HaCT Security & IAM team; in case of valid business justification, Post Service Owner, Application Team will be allowed to create custom role.
- Assumption: Subscriptions are deployed via IaC and during deployment, respective AD Groups are created with the standard naming convention pattern and Application Managers are assigned as Owners/Member of AD Groups.
- Assumption: PIM is not implemented for Application team members in Lower environment and in PROD environment (as per stated justifications/role patterns).
- Assumption/Dependency: Monitoring Team has to confirm Resource Group where alert rules are placed (currently <TBD>).
- Assumption: “AZ-HaCT-USERS-PCFv2-READER“ Reader AD Group will grant only access to ES@Uniper and not used in PCFv1.
- Break glass risk/assumption: Conditional Access / Identity Protection enforcement (MFA, blocking unsupported/incompliant devices, blocking risky sign-ins) can block users/administrators in extreme scenarios; emergency access accounts are needed and are cloud-only, excluded from identity protection services, excluded from Conditional Access, and have no MFA.

---

## OPTIONAL SECTIONS (USE WHEN APPLICABLE)

### 10. Design Constraints & Dependencies (OPTIONAL)

- HaCT team must reach out to UNIPER Directory service team to get the Azure AD roles assigned.
- Catalog dependency: Directory Service - Request Azure / M365 administrator role assignment or removal (Remark: select Azure Active Directory (Uniper SE) PROD).
- Some monitoring configuration elements are explicitly TBD:
  - Resource Group where Alert rules are placed: <TBD> (Monitoring Team has to confirm).
  - Alert rule topic not completed; rule name and details required.
- IaC details are deferred to Low level design of HaCT Platform automation.

**Abbreviations (Table 40)**

| Abbreviation | Description |
| --- | --- |
| HaCT | Hosting & Cloud Technology |
| SMI | Service Management and Integration |
| UAM | User Access Administrator |
| RBAC | Role Based Access Control |
| PAG | Privileges Access Group |
| PIM | Privileged Identity Management |
| Azure AD | Azure Active Directory |
| SME | Subject Matter Experts |
| MVP | Minimum Viable Product |
| Azure SP | Azure Service Principal |
| IaC | Infrastructure as Code |

---

### 11. Lifecycle & Evolution Considerations (OPTIONAL)

- AD Group creation and Role Assignments for HaCT Cloud Engineers are performed manually in MVP1.0 roll out by UIT HaCT Security Services <uit-hact-security-services@uniper.energy>.
- HaCT Team will be working on to identify other critical roles. If HaCT identifies Critical role, it will get appended to the list.
- Break glass validation/training should occur at least twice a year; password changes occur when separation of password halves cannot be ensured.

---

### 12. Out-of-Scope / Deferred Decisions (OPTIONAL)

- Detailed explanation about IaC will be covered in Low level design of HaCT Platform automation.
- Remarks – Description about the Initiatives and Policies are explained in the Governance LLD document.
- Alert rule topic is not completed, Rule name and details are required.
- AD group membership backup: Storage Container, DevOps Git URL, DevOps Pipeline are <TBD>.
- Resource Group (where Alert rules are placed, Monitoring Team has to confirm us.): <TBD> (listed multiple times).

---

### 13. References

- Azure Enterprise-Scale / PCF V2 High Level Design Document — Version 1.0
- DevOps Git URL: RoleAssignments - Repos (azure.com)
- DevOps Pipeline: Pipelines - Runs for Azure Role Assignment Backup UPCFv2
- Directory Service catalog: Directory Service - Request Azure / M365 administrator role assignment or removal

> Change history is maintained via Git commit and pull request history.
