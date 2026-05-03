## Document Information

<!-- source_section_id: section_2 -->

**Table 1: Document Information**

---

## Distribution List

<!-- source_section_id: section_3 -->

**Table 2: Distribution List**

---

## Supporting Documents

<!-- source_section_id: section_4 -->

**Table 3: Supporting Documents**

---

## Overview

<!-- source_section_id: section_6 -->

At Uniper, Azure AD currently synchronizes with On-Premises Active Directory. Role-Based Access Control (RBAC) is an authorization mechanism based on Azure Resource Manager, enabling meticulous access management of Azure resources. By implementing RBAC, Uniper ensures access is restricted by the principles of 'need to know' and 'least privilege', essential for secure cloud resources management. This role-specific access control system directly aligns with organizational roles, optimizing both security and operational efficiency.
```

## 7. Security, HA & DR Considerations

This section details the RBAC requirements, the structured RBAC settings, and maintenance procedures for the RBAC infrastructure within the Enterprise Scale@Uniper's management groups and landing zone subscriptions, ensuring alignment with security principles and controls.

---

## 8. Audience

The primary audience for this document includes UNIPER architects and project management involved in the Enterprise Scale@Uniper initiative.

---

## 9. Risks & Assumptions

**RACI Matrix for Landing Zone Subscriptions:**

_Responsibility Assignment Matrix:_

This matrix specifies the roles and responsibilities associated with the landing zone subscriptions, acknowledging the risks and assumptions based on defined accountabilities.

---

## 10. Design Constraints & Dependencies (OPTIONAL)

**AD Group Creation & Role Assignment:**

_Scope of AD Group Creation and Role Assignment:_

This section elaborates on the constraints and dependencies involved in Active Directory group creation and role assignments within the project scope.

---

## 11. Lifecycle & Evolution Considerations (OPTIONAL)

**Access and Approval for App Team Members:**

_Scope of Access for App Team Members:_

Details the lifecycle management and revision considerations for access rights and approval processes for application team members, including ongoing evaluation and adjustments as necessary.

## In/Out Scope - Creation/Deletion of New AD Group

**Table 7: In/Out Scope Details**

---

## In/Out Scope - Role Assignment

**Table 8: In/Out Scope Details**

---

## In/Out Scope - Custom Role Creation

**Table 9: In/Out Scope Details**

---

## Role-Based Access Control

_Access control focuses on ensuring confidentiality, integrity, and availability of data through the CIA Triad. Role-based access control (RBAC) systematically manages access to information systems and data, enhancing security by only allowing access levels appropriate to each role within an organization._

---

## Azure Enterprise Scale@Uniper Architecture

**Figure 1: ES@Uniper Architecture Overview**

_Remarks: Role assignments can be inherited from the tenant's scope or result from specific policy assignments. These are outlined in Table 29._

## Azure Enterprise Scale@Uniper – HaCT Cloud Engineer RBAC Architecture

**Figure 2: ES@Uniper - HaCT Cloud Engineer Access**

---

## Azure Enterprise Scale@Uniper – Application Team RBAC Architecture

**Figure 3: ES@Uniper - Application Team Access**

*Remark: Detailed explanation regarding the default role is provided under the section 9.*

---

## How are Security AD Groups created?

Application Owners and Team Members order subscriptions by submitting requests to create subscriptions using catalogue services. During the process of deployment of Subscriptions via Infrastructure as Code (IaC), respective AD Groups are created following a standard naming convention pattern, and Application Managers are assigned as Owners/Members of these AD Groups.

*Remarks: Supported by HaCT Automation Team.*

*Detailed explanation about IaC will be covered in the Low-level design of HaCT Platform automation.*

AD Group creation and Role Assignment for the application team are automated.

---

## Naming Convention

**PCFv2 security AD group convention pattern is utilized.**

- **Format:** AZ-<Subscription name>-READER | AZ-<Subscription name>-CONTRIBUTOR

**Examples:**

- **DEV Environment**
  - Subscription Name: "PCFv2-CORP-DEV-C_MA3-DTFU081-01"
  - AD Group Name: AZ-PCFv2-CORP-DEV-C_MA3-DTFU081-01-READER
  - Group Description: [CreatedBy:HaCT][CreatedFor:<EAMID of Application>] Granting Reader access for users on subscription.
  - AD Group Name: AZ-PCFv2-CORP-DEV-C_MA3-DTFU081-01-CONTRIBUTOR
  - Group Description: [CreatedBy:HaCT][CreatedFor:<EAMID of Application>] Granting Contributor access for users on subscription.

- **PROD Environment**
  - Subscription Name: "PCFv2-CORP-PRD-C_MA3-DTFU081-01"
  - AD Group Name: AZ-PCFv2-CORP-PRD-C_MA3-DTFU081-01-READER
  - Group Description: [CreatedBy:HaCT][CreatedFor:<EAMID of Application>] Granting Reader access for users on subscription.

*Remarks: Security AD Groups created are only used for the purpose of ES@Uniper RBAC for application team members.*

---

## RBAC – Application Team

**Table 10: App Team - Default Role Description**

---

### Architecture & Design: Azure AD Group Ownership and Membership Management

_This architecture addresses the efficient management of Azure AD group ownership and membership across various environments to ensure proper role-based access permissions._

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
- References

---

## CORE SECTIONS (MANDATORY)

### 1. Document Metadata

| Field          | Value                           |
|----------------|---------------------------------|
| Architecture ID| ARCH-AZURE-AD-002               |
| Service / Platform | Azure AD Group Management   |
| Author         | Jane Doe                        |
| Reviewers      | Azure Architecture Team        |
| Status         | Approved                        |
| Version        | 1.0                             |
| Last Updated   | 2023-10-01                      |

---

### 2. Problem Statement

_Managing Azure AD group ownership and membership manually across multiple environments (DEV/SANDBOX, UAT/PROD) has been cumbersome, prone to error, and lacks systematic role assignments and compliance checks. This fragmented approach led to inefficiencies and potential security vulnerabilities._

---

### 3. Design Goals & Non-Goals

**Goals**
- Automate the management of Azure AD groups to enhance security and compliance.
- Ensure clear role-based access control across different environments.

**Non-Goals**
- This design does not address individual user account management within Azure AD.

---

### 4. Architecture Overview

The design consists of automated scripts and Azure functions that manage Azure AD group memberships and ownership based on predefined rules and roles specified for different environments.

---

### 5. Design Options Considered

- **Manual Management** – Initially considered due to simplicity, rejected due to high error rate and inefficiency.
- **Partially Automated Management** – Considered but rejected because it did not fully meet the compliance and efficiency requirements.

---

### 6. Chosen Design & Rationale

The fully automated management system was chosen due to its scalability, reduction in human errors, and alignment with compliance requirements. Automation allows for dynamic management of roles based on real-time changes in team structures and projects.

---

### 7. Security, HA & DR Considerations

The system adheres to least privilege access principles, ensuring that permissions are granted strictly as required. High availability and disaster recovery are ensured through Azure's built-in redundancy features and regular backups.

---

### 8. Operational Implications

- **Monitoring and Alerting**: Systematic monitoring of group memberships and automated alerts for any unauthorized changes.
- **Support Complexity**: Reduction in support tickets related to access issues.
- **Ownership and Responsibilities**: Clearly defined via automated role assignments.

---

### 9. Risks & Assumptions

- **Risk**: Potential delays in role updates due to system downtime.
- **Assumption**: Continuous availability of the Azure platform for uninterrupted service.

---

### 13. References

- Azure AD documentation
- Automated Role Management tools

---

> The architecture is recorded and maintained in the version control system to track changes and updates over time.

## HaCT – Automation Service Principal - Role Specific Access

### Document Metadata

| Field | Value |
|-------|-------|
| Architecture ID | ARCH-HaCT-ASP-001 |
| Service / Platform | HaCT Automation Service Principal |
| Author | [Author Name] |
| Reviewers | HaCT Security Team, IAM Governance |
| Status | Draft |
| Version | 1.0 |
| Last Updated | YYYY-MM-DD |

---

### Problem Statement

Existing role assignments for the Automation Service Principal lack specificity and do not align strictly with the necessary permissions required for operational tasks such as subscription lifecycle management and role assignment for Application Teams, leading to potential over-privileging.

---

### Design Goals & Non-Goals

**Goals**
- To explicitly define and restrict the Automation Service Principal roles to only necessary permissions ensuring compliance and security.

**Non-Goals**
- Managing individual user roles and permissions outside of the Automation Service Principal.

---

### Architecture Overview

The architecture defines specific role assignments for the Automation Service Principal to ensure adequate permissions are aligned with operational requirements without over-privileging.

---

### Design Options Considered

- **Broad Access Permissions** – Initially considered to simplify management but rejected due to security concerns of over-privileging.
  
- **Role Specific Access** – Chosen to align permissions more closely with actual needs and security best practices.

---

### Chosen Design & Rationale

The role-specific access was chosen to minimize the security risks associated with broad permissions and to comply with least privilege principle, which is paramount for operational security and efficiency.

---

### Security, HA & DR Considerations

- **Security**: Ensures compliance with least privilege security principle by strictly aligning roles to operational necessities.
- **High Availability** & **Disaster Recovery**: Not directly impacted by this design.

---

### Operational Implications

- **Monitoring and alerting**: Will require updates to ensure that any actions taken under these roles are properly logged and monitored.
- **Support complexity**: Specific roles may require additional training for new users.
- **Ownership and responsibilities**: Clearly delineated in the platform's user management guidelines.

---

### Risks & Assumptions

- **Risk**: Potential delays in operations if the role definition is too restrictive.
- **Assumptions**: All users of the Automation Service Principal are properly trained on their responsibilities.

---

### References

- HaCT Security and IAM Guidelines
- Azure Role-Based Access Control Documentation

---

## Azure AD Role – HaCT Security and IAM Team

### Document Metadata

| Field | Value |
|-------|-------|
| Architecture ID | ARCH-HaCT-IAM-002 |
| Service / Platform | Azure Active Directory - HaCT Team |
| Author | [Author Name] |
| Reviewers | Directory Services, Compliance Team |
| Status | Draft |
| Version | 1.0 |
| Last Updated | YYYY-MM-DD |

---

### Problem Statement

The HaCT Security and IAM Team currently lacks streamlined processes to request and obtain necessary Azure AD roles through the Uniper Directory Service, impeding efficient role management and compliance actions.

---

### Design Goals & Non-Goals

**Goals**
- Establish a standardized approach for the HaCT team to request Azure AD roles necessary for their operations.

**Non-Goals**
- Managing directory services requests for other teams or general staff.

---

### Architecture Overview

Implementation of a cataloged request process facilitated through the Uniper Directory Service, dedicated to the HaCT Security and IAM Team for role assignments in Azure AD.

---

### Operational Implications

- **Responsibilities**: HaCT team to initiate requests following established guidelines.
- **Required tooling**: Access to Uniper Directory Service catalog.

---

### References

- Directory Service - Request Azure / M365 administrator role assignment or removal

---

### Reader-Permissions

- **actions**:

---

### Contributor - Permissions

- **actions**:
- **notactions**:

---

### User Access Administrator -Permissions

- **actions**:

---

### Support Request Contributor-Permissions

- **actions**:

---

### Storage Blob Data Reader-Permissions

- **actions**:
- **notActions**: []

- **dataActions**:

---

```markdown
### Resource Policy Contributor-Permissions

**Actions:**
- TBD

---

### Network Contributor-Permissions

**Actions:**
- TBD

---

### Monitoring Contributor-Permissions

**Actions:**
- TBD

---

### Alert Rule

**Role Assignments of Critical/High Priority Across UPCFv2 Environment**

**Condition:**
- When critical role assignments are performed in UPCFv2 environment.

**Scope:**
- Across all scopes (Management Group, Subscription, Resource Group, Resource) in UPCFv2.

---

### Action Group

**Security and IAM Team Distribution List:**

- UIT HaCT Security Services <uit-hact-security-services@uniper.energy>
```

### Resource Group

<!-- source_section_id: section_51 -->

_The specific placement of Alert rules requires confirmation from the Monitoring Team._

| Detail | Description |
|--------|-------------|
| Location | TBD |

---

### Alert Rule

<!-- source_section_id: section_53 -->

_Custom roles are monitored within the UPCFv2 environment to ensure security and compliance._

#### Condition

- Alert is triggered when custom roles are created in the UPCFv2 environment.

#### Scope

- This rule applies across all levels: Management Group, Subscription, Resource Group, and Resource within the UPCFv2 environment.

---

### Action Group

<!-- source_section_id: section_54 -->

_Contacts for the Security and IAM Team regarding alert handling._

**Distribution List:**

- UIT HaCT Security Services <uit-hact-security-services@uniper.energy>

---

### Resource Group

<!-- source_section_id: section_55 -->

_The specific placement of Alert rules requires confirmation from the Monitoring Team._

| Detail | Description |
|--------|-------------|
| Location | TBD |

---

### Alert Rule

<!-- source_section_id: section_57 -->

_Monitors for critical resource deployments across the PCFv2 and ESLZ environments._

#### Condition

- Activation when there are critical resource deployments across the ESLZ environment.

#### Scope

- Applies to all entity levels in the UPCFv2 environment: Management Group, Subscription, Resource Group, and Resource.

### Action Group

**Security and IAM Team Distribution List:**

- UIT HaCT Security Services <uit-hact-security-services@uniper.energy>

---

### Resource Group

**Note:** Placement of alert rules is under confirmation by the Monitoring Team.

- TBD

**Additional Information:**
- [ ] Completion of alert rule topic is pending. Rule name and details are required.

---

## Introduction

Uniper employs Conditional Access and Azure Identity Protection policies for enforcing Azure Multi-Factor Authentication (MFA), blocking unsupported and non-compliant device platforms, and preventing risky sign-in attempts. In extreme situations, such as during a natural disaster, access to mobile phones or other networks may be compromised. This poses a significant risk of blocking out both users and administrators. To mitigate this risk, the concept of emergency access accounts, often termed as "break glass accounts," plays a vital role in the organization's disaster recovery plan. These accounts are highly privileged and are intended for use exclusively when standard administrative accounts are unable to sign in, ensuring access to systems or services is maintained.

---

## AS-IS – Break-Glass Account Architecture

### Figure 4: Break-Glass Account Access Framework

---

### Account Configuration

**Break Glass Accounts Overview:**

The "break glass accounts" are highly privileged, cloud-only accounts that are exempt from typical identity-protection services. In a crisis, this exemption ensures that these accounts can still log into the Azure environment, maintaining critical access.

**Table 21: Break-Glass Account Configuration**

---

```markdown
## Architecture & Design: Azure Role Assignment Monitoring and Emergency Account Handling

This architecture ensures the secure and controlled access and monitoring of Azure Role Assignments and establishes a robust emergency access protocol using AAD Break-Glass accounts.

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
- References

---

### 1. Document Metadata

| Field            | Value                                      |
|------------------|--------------------------------------------|
| Architecture ID  | ARCH-AZURE-SEC-002                         |
| Service / Platform | Azure Security and Role Management       |
| Author           | [Author Name]                              |
| Reviewers        | Azure Security Team, Compliance Officers   |
| Status           | Approved                                   |
| Version          | 1.0                                        |
| Last Updated     | YYYY-MM-DD                                 |

---

### 2. Problem Statement

The management of Azure Role Assignments lacked centralized monitoring and control, leading to potential security and compliance risks. Furthermore, the absence of a standardized emergency access protocol posed a threat to continuity and security compliance under crisis scenarios.

---

### 3. Design Goals & Non-Goals

**Goals**
- Ensure all Azure Role Assignments are tracked and monitored daily.
- Establish a secure, compartmentalized emergency access procedure using Break-Glass accounts.

**Non-Goals**
- Automating role assignments based on usage patterns.
- Integrating third-party identity management solutions.

---

### 4. Architecture Overview

The architecture consists of two main components:
1. **Azure Role Monitoring**: Utilizes a PowerShell script driven by Azure DevOps to generate daily reports of all Azure Role Assignments, storing these reports in a secure Azure Storage Account.
2. **Emergency Account Handling (Break-Glass Account)**: Strategically assigns account password components to different teams ensuring high availability and control during emergencies.

---

### 5. Design Options Considered

- **Automated Role Assignment Monitoring using third-party tools**: Considered for its extensive features but rejected due to increased operational complexity and vendor lock-in concerns.
- **Centralized Emergency Access with single team access**: Rejected to avoid single points of failure and insider threat risks.

---

### 6. Chosen Design & Rationale

The chosen design effectively balances security, operational simplicity, and compliance requirements. It leverages existing Azure services and internal team structures to ensure robust handling and oversight of role assignments and emergency access.

---

### 7. Security, HA & DR Considerations

- **Security**: Implements strict access controls and audits on the Break-Glass account and the Azure Role Assignments.
- **High Availability**: The distribution of the Break-Glass password ensures 24/7 availability across multiple teams.
- **Disaster Recovery**: Routine validations and training ensure preparedness for emergency account activations.

---

### 8. Operational Implications

- **Monitoring and Alerting**: Daily reports and change logs enable proactive monitoring and incident response.
- **Support Complexity**: Defined roles and responsibilities streamline support and operational tasks.
- **Required Tooling or Skills**: Teams require familiarity with PowerShell, Azure DevOps, and Azure security best practices.

---

### 9. Risks & Assumptions

- **Risk**: Unauthorized access if both parts of the Break-Glass account password are compromised.
- **Assumption**: Operational integrity and confidentiality are maintained within the divided teams handling the Break-Glass account details.

---

### 13. References

- Azure Security Center Documentation
- Internal Emergency Access Protocol SOP
- Azure Compliance Guidelines
```

### Scheduler/Pipeline Trigger Details

**Frequency**: Daily  
**Days**: Monday - Sunday  
**Time**: 4:00 PM CET  

---

### Service Principal Details

**Name**: Cloud Security Services | PROD | BSN0003595 | General Automation  

---

### Service Principal Azure RBAC Permissions

The service principal is granted the following access rights to perform necessary operations:

- **Reader Access**: At "UPCFv2 Enterprise Scale" UPCFv2 Management Group to view all role assignments.
- **Storage Account Contributor Access**: At Storage account `hactsecuritysto001` to upload CSV files as a Blob to the storage container.

---

### Service Principal Azure AD API Permissions

- Microsoft Graph – "Directory.Read.All" for the Service Principal in Azure AD.

---

### Purpose

The purpose of this setup is:
- To maintain historic data of all members of AD groups which have role assignments across the PCFv2 estate on a specified day.
- To enable quick viewing and comparison of the memberships of AD groups over different time periods.
- To facilitate the analysis and cleanup of members in AD groups.

### 4. Architecture Overview

**PowerShell Automation Script in Azure DevOps**
The architecture involves a PowerShell script managed via an Azure DevOps pipeline. This script automates the daily generation of reports detailing the members of AD Groups across all scope of the PCFv2 environment. The result is an Excel file uploaded to an Azure Storage Account for easy access and manageability.

---

### 5. Design Options Considered

**Manual Reporting**
- Considered for its simplicity but rejected for its lack of scalability and increased risk of human error.

**Third-Party Solutions**
- Considered for comprehensive features but not chosen due to higher costs and dependency on external vendors.

---

### 6. Chosen Design & Rationale

The decision to use a PowerShell script executed via an Azure DevOps pipeline was made to streamline operations and ensure consistency in the reporting process. The automation minimizes human error and allows for scalability as the system's needs grow. Additionally, using Azure Storage provides a secure and centralized location for accessing reports.

---

### 7. Security, HA & DR Considerations

**Security**
- Implemented through restricted access using service principles with minimal necessary permissions.

**High Availability and Disaster Recovery**
- Azure Storage ensures high availability and durability of the data. Regular backups and geo-redundancy options further support disaster recovery efforts.

---

### 8. Operational Implications

**Monitoring and Alerting**
- The system uses Azure DevOps monitoring tools to track the health and performance of the pipeline and alerts the team to any issues in real-time.

**Support Complexity**
- Requires basic knowledge of PowerShell scripting and Azure DevOps operations.

**Ownership and Responsibilities**
- Managed by the cloud security services team, ensuring updates and maintenance are handled promptly.

---

### 9. Risks & Assumptions

**Risks**
- Dependency on the reliability of Azure DevOps and Azure Storage could pose a single point of failure.

**Assumptions**
- The environment will maintain stable internet connectivity and Azure services will be available without significant downtime.

---

### 10. Design Constraints & Dependencies 

**Constraints**
- Limited to the tools and permissions available within the Azure environment.

**Dependencies**
- Relies on the proper configuration of Azure DevOps and the availability of Azure Storage services.

---

### 11. Lifecycle & Evolution Considerations

The architecture is designed to be robust with potential scalability as the organization's needs grow. Future modifications may include adding more sophisticated error handling and expanding the types of reports generated.

---

### 13. References

- Azure DevOps Documentation
- Microsoft Azure Storage Solutions Documentation

## Architecture & Design: Azure AD API & Microsoft Defender for Cloud Security Implementations

_This architecture provides a secure and compliant design for managing permissions and security policies in Azure services, addressing the need for systematic control and security oversight._

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
- References

---

### 1. Document Metadata

| Field | Value |
|------|------|
| Architecture ID | ARCH-SEC-002 |
| Service / Platform | Azure AD & Microsoft Defender for Cloud |
| Author | Security Architecture Team |
| Reviewers | IT Security Governance, Azure SMEs |
| Status | Approved |
| Version | 1.0 |
| Last Updated | 2023-11-15 |

---

### 2. Problem Statement

Existing permissions and security management frameworks in Azure services lacked structured policies, resulting in a non-uniform security posture and potential compliance risks.

---

### 3. Design Goals & Non-Goals

**Goals**
- Ensure compliant and granular permission assignments for service principals in Azure AD.
- Uniform security policy application across all Azure resources using Microsoft Defender for Cloud.
- Enhance monitoring and enforce best practices through security initiatives and policies.

**Non-Goals**
- Direct handling of non-Azure related security or compliance requirements.
- Immediate remediation of identified security misconfigurations.

---

### 4. Architecture Overview

The architecture utilizes Microsoft Graph API to manage Azure AD service principal permissions and integrates Microsoft Defender for Cloud for centralized security management and compliance assessments.

---

### 5. Design Options Considered

- **Direct API Management without Microsoft Graph**: Considered due to direct API access but rejected for less manageable permission granularity and higher maintenance.
- **Using Third-party Security Solutions**: Evaluated for extended features but not chosen due to higher integration complexity and cost implications.

---

### 6. Chosen Design & Rationale

The design was chosen because it leverages native Azure services like Microsoft Graph and Defender for Cloud which are robust and integrated directly into the Azure ecosystem. This approach supports better scalability, compliance adherence, and maintenance.

---

### 7. Security, HA & DR Considerations

- **Security**: Permissions are managed through tightly controlled roles and policies ensuring that only necessary permissions are granted.
- **High Availability & Disaster Recovery**: Leverages Azure's native capabilities to ensure availability and resilience.

---

### 8. Operational Implications

- **Monitoring and Alerting**: Continuous monitoring through Azure Monitor and integration with Defender for Cloud alerts.
- **Support Complexity**: Centralized through Azure support and governance frameworks, reducing operational overhead.
- **Ownership and Responsibilities**: Clearly defined within the IT Security and Azure operations teams.

---

### 9. Risks & Assumptions

- **Risks**: Potential delays in role updates could lead to temporary compliance deviations.
- **Assumptions**: All Azure resources comply with current Azure policies and are continuously monitored.

---

### 13. References

- Azure Active Directory Service Principals documentation
- Microsoft Defender for Cloud official docs
- Governance and Compliance documentation in LLD

---

> Note: For detailed explanations about security initiatives related to guest account permissions and TLS compliance, refer to the Governance LLD document.

### Security features – Storage Account

_Table outlining specific security initiatives for Storage Account management._

| **Table 25** | Security Initiative - Storage Account |
|--------------|---------------------------------------|

---

### Network Policy

_Table detailing network policies as part of security initiatives._

| **Table 26** | Security Initiative - Network Policy |
|--------------|--------------------------------------|

---

### SQL Policy Initiatives

_Table identifying security policy initiatives for SQL Platform as a Service (PaaS)._

| **Table 27** | Security Initiative - SQL PAAS |
|--------------|-------------------------------|

---

### KeyVault - Policy Initiatives

_Table listing policy initiatives pertinent to KeyVault management and security._

| **Table 28** | Security Initiative – KeyVault |
|--------------|--------------------------------|

---

### Role Assignment – scope – Tenant

_List of role assignments inherited from the Tenant scope._

| **Table 29** | Existing - Role Assignment|
|--------------|---------------------------|
| Remarks      | * The justification for the role assignment must be examined and documented. |

---

## Important Note

Security AD Group created are only used for the purpose of ES@Uniper RBAC for application team members.

AD Group creation and Role Assignment for application team are automated.

PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services uit-hact-security-services@uniper.energy

AD Group creation and Role Assignment for HaCT Cloud Engineer are manually performed by UIT HaCT Security Services uit-hact-security-services@uniper.energy

Application Managers must assess permitted users and give application team members access.

---

# Preserved Tables from Source Document

### Source Table 1

| Date       | Version | Name                   | Role                             | Comments    |
|------------|---------|------------------------|----------------------------------|-------------|
| 06/02/2023 | 1.0     | Indhumathi Subramanian | Cloud Security & IAM consultant  | Initial draft |

### Source Table 2

| Distributed to | Role | Company |
|----------------|------|---------|
|                |      |         |

### Source Table 3

| Document Name                                      | Version  |
|----------------------------------------------------|----------|
| Azure Enterprise-Scale / PCF V2 High Level Design Document | Version 1.0 |

### Source Table 4

| R = Responsibilities<br>A = Accountable<br>C = Consulted<br>I = Informed | Application Team | HaCT Cloud Engineer |
|-------------------------------------------------------------------------|------------------|---------------------|
| Requesting for new AD group creation other than default                 | R, A             |                     |
| Creation of role assignment other than default                         | R, A             | C, I                |
| Deletion of role assignment other than default                         | R, A             | C, I                |
| Access for Application member                                          | R, A             |                     |
| Process of Approval flow                                               | R, A             |                     |
| Custom role creation                                                   | C, I             | R, A                |
| Excluding/Exemption of Policy                                          | C, I             | R, A                |

### Source Table 5

| HaCT Responsibilities |
|-----------------------|
| 1. HaCT Team will be creating AD Group and performing default role assignments to Application Team on their ordered subscription.<br>2. AD Group creation and Role Assignments for HaCT Cloud Engineers are performed manually in MVP1.0 roll out by UIT HaCT Security Services uit-hact-security-services@uniper.energy.<br>3. PIM implementation of Role Specific access for HaCT Cloud Engineers are manually done by UIT HaCT Security Services uit-hact-security-services@uniper.energy. |

### Source Table 6

| Responsibilities       | Responsibilities                                                                                                                                                    |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Application Team       | Application Manager is responsible to grant access to Application Team member on the required subscription<br>Grant/Revoke access to Application team must be taken care by Application Manager. |
| HaCT Team              | HaCT Team will be creating the default AD Groups with access on the subscriptions, assign App Manager as Owner of AD Groups of Contributor and Reader ad group & Member of Reader AD Group. Will share the details to App Manager. |

### Source Table 7

| Responsibilities       | Responsibilities                                                                                                                                                            |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Application Team       | Application Team needs to contact the UNIPER Directory Service team.<br>AD Group should be Security type with proper description.<br>Addition/Removal of Members into the AD Group should be taken care by Application Team or via UNIPER Directory Service team. |
| HaCT Team              | HaCT is not responsible for creating the AD Group for Enterprise Scale@Uniper except for the default AD Groups.<br>HaCT team will be removing the role assignment of other AD Group type role assignment except Security type ad groups |

### Source Table 8

| Responsibilities       | Responsibilities                                                                                                                                                                                 |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Application Team       | App Team's responsible to perform the role assignment for themselves on-demand<br>Application team are requested to use the Least privilege principle and perform the role assignment. Recommendation from HaCT is to check resource specific role and assign what is required to perform the activity.<br>Critical/High Privilege role - “Owner, User Access Administrator, Resource Policy Contributor “are requested not use across ESLZ subscriptions/Resource Groups/Resources |
| HaCT Team              | If in case mentioned role assignments are identified during audit process, HaCT Team will removing immediately<br>On noticing role assignments apart from Reader for Application team members in PROD subscription, HaCT Team will be removing the respective role assignment. |

### Source Table 9

| Responsibilities       | Responsibilities                                                                                                                                                  |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Application Team       | Not to create custom role, in most of the use case Contributor access will be sufficient for SPN to deploy/create/modify/update/delete. In case of custom role, request you to take consultation call with HaCT Security & IAM Team |
| HaCT Team              | When App team creates custom role, Custom role is also will be removed. App Team must place consultation call with HaCT Security & IAM team. In case of valid business justification, Post Service Owner, Application Team will be allowed to create custom role. |

### Source Table 10

| Azure           | Subscription Name | Role Name |
|-----------------|-------------------|-----------|

### Source Table 11

| Role Name            | Type     | Description                                                                                                                                                   |
|----------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Reader               | Built-in | View all resources but does not allow you to make any changes.                                                                                                |
| Contributor          | Built-in | Grants full access to manage all resources but does not allow you to assign roles in Azure RBAC, manage assignments in Azure Blueprints, or share image galleries. |
| User Access Administrator | Built-in | Let’s you manage user access to Azure resources.                                                                                                            |
| Support Request Contributor | Built-in | Let’s you create and manage Support requests                                                                                                                 |
| Storage Blob Data Reader | Built-in | Allows for read access to Azure Storage blob containers and data                                                                                          |

### Source Table 12

|                      | Reader - AD Group | Contributor - AD Group |
|----------------------|-------------------|----------------------|
| Owner                | App Manager       | App Manager          |
| Member               | App Manager, *    | *                    |

### Source Table 13

| Security Principal | DEV & SANDBOX   | Scope of Access | PIM (Yes/No) |
|--------------------|-----------------|-----------------|--------------|
| User               | Reader          | Subscription    | No           |
| User               | Contributor     | Subscription    | No           |
| Service Principal  | Contributor     | Subscription    | -NA-         |
| Service Principal  | User Access Administrator | Subscription    | -NA-         |

### Source Table 14

| Security Principal | UAT & PROD       | Scope of Access | PIM (Yes/No) |
|--------------------|------------------|-----------------|--------------|
| User               | Reader           | Subscription    | No           |
| User               | Support Request Contributor | Subscription    | No           |
| Service Principal  | Contributor      | Subscription    | -NA-         |
| Service Principal  | User Access Administrator | Subscription    | -NA-         |

### Source Table 15

| HaCT Stream      | Access - Role    | Scope of Access         | PIM (Yes/No) | Security AD Group             |
|------------------|------------------|-------------------------|--------------|-------------------------------|
| HaCT- Security IAM | Reader           | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |
| HaCT- Architect  | Reader           | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |
| HaCT- Governance | Reader           | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |
| HaCT- Network Admins | Reader       | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |
| HaCT- Monitoring Admin | Reader     | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |
| HaCT- Automation | Reader           | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |
| HaCT- Dev team   | Reader           | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |
| HaCT- Database Team | Reader        | PCFv2 Management Group  | No           | AZ-HaCT-USERS-PCFv2-READER    |

### Source Table 16

| HaCT Stream         | Access - Role           | Scope of Access         | PIM (Yes/No) | PAG - PIM Security AD Group      |
|---------------------|-------------------------|-------------------------|--------------|----------------------------------|
| HaCT- Security IAM  | User Access Administrator | PCFv2 Management Group | Yes          | AZ-HaCT-PIM-Security Team        |
| HaCT- Governance    | Resource Policy Contributor | PCFv2 Management Group | Yes          | AZ-HaCT-PIM-Governance Team      |
| HaCT- Governance    | User Access Administrator | PCFv2 Management Group | Yes          | AZ-HaCT-PIM-Governance Team      |
| HaCT- Network Admins | Network Contributor   | PCFv2 Management Group  | Yes          | AZ-OurConnectivity-PIM-Cloud Network Team |
| HaCT- Monitoring Admin | Monitoring Contributor | PCFv2 Management Group | Yes          | AZ-HaCT-PIM-Monitoring Team      |
| HaCT - Contributor  | Contributor            | PCFv2 Management Group  | Yes          | AZ-HaCT-PIM-UPCFv2-CONTRIBUTOR   |

### Source Table 17

| HaCT Stream         | Access - Role           | Scope of Access         | PIM (Yes/No) |
|---------------------|-------------------------|-------------------------|--------------|
| HaCT- Automation - SP | Contributor           | PCFv2 Management Group  | -NA-         |
| HaCT- Automation - SP | User Access Administrator | PCFv2 Management Group | -NA-         |

### Source Table 18

| Role Name                 | Type     | Description                                                                                                    |
|---------------------------|----------|----------------------------------------------------------------------------------------------------------------|
| Privileged Role Administrator | Built-in | Can manage role assignments in Azure AD, and all aspects of Privileged Identity Management.                    |
| Groups Administrator      | Built-in | Members of this role can create/manage groups, create/manage groups settings like naming and expiration policies, and view groups activity and audit reports. |

### Source Table 19

| HaCT Head |
|-----------|
| Whillans, Mathew <mathew.whillans@uniper.energy> |

### Source Table 20

| HaCT Stream Lead | HaCT Stream Lead                                                                       |
|------------------|----------------------------------------------------------------------------------------|
| Database         | Wittich, Mark <mark.wittich@uniper.energy>                                             |
| Automation       | Richards, Gareth <gareth.richards@uniper.energy>                                       |
| Development      | Schmitz, Carsten <carsten.schmitz@uniper.energy>                                       |
| Architect        | Stolcz, Tamas <Tamas.Stolcz2@uniper.energy>                                             |
| Infrastructure   | Arunachalam, Selvam <selvam.arunachalam@uniper.energy>                                  |
| Network          | Abbott, Steve <steve.abbott@uniper.energy>                                             |
| Operations       | Sidhu, Amerdeep <Amerdeep.Sidhu.ext@uniper.energy>                                     |
| Security & IAM   | Heil, Sebastian <sebastian.heil@uniper.energy>                                         |
| Monitoring       | Arunachalam, Selvam <selvam.arunachalam@uniper.energy>                                  |
| Optimization     | Steinemann, Daniel <Daniel.Steinemann.ext@uniper.energy>                               |
| Governance       | Daniel Steinemann/Sebastian Heil                                                       |
| Scrum Board      | Röckel, Heike <Heike.Roeckel@uniper.energy>                                            |

### Source Table 21

| Role Name              | Type     | Description                                                                                                                                                                                         |
|------------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Reader                 | Built-in | View all resources but does not allow you to make any changes.                                                                                                                                       |
| Contributor            | Built-in | Grants full access to manage all resources but does not allow you to assign roles in Azure RBAC, manage assignments in Azure Blueprints, or share image galleries.                                    |
| User Access Administrator | Built-in | Let’s you manage user access to Azure resources.                                                                                                                                                    |
| Resource Policy Contributor | Built-in | Users with rights to create/modify resource policy, create support ticket and read resources/hierarchy.                                                                                              |
| Network Contributor    | Built-in | Let’s you manage networks, but not access to them.                                                                                                                                                  |
| Monitoring Contributor | Built-in | Can read all monitoring data and update monitoring settings. 
