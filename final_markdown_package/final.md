# SOP: <SOP Name>

## Table of Contents

- [1. Document Metadata](#1-document-metadata)
  - [1.1. Target Audience](#11-target-audience)
- [2. Purpose & Scope](#2-purpose-scope)
  - [2.1. Document Purpose](#21-document-purpose)
  - [2.2. When/Why Custom role creation](#22-whenwhy-custom-role-creation)
- [3. Definitions & Abbreviations (Optional)](#3-definitions-abbreviations-optional)
- [4. Triggers & Preconditions](#4-triggers-preconditions)
- [5. Step-by-Step Procedure](#5-step-by-step-procedure)
  - [5.1. Process of Custom Role implementation](#51-process-of-custom-role-implementation)
    - [5.1.1. Due Diligence Phase](#511-due-diligence-phase)
    - [5.1.2. Analyse/POC Phase](#512-analysepoc-phase)
    - [5.1.3. CR creation](#513-cr-creation)
    - [5.1.4. Implementation Phase](#514-implementation-phase)
  - [5.2. How to create custom roles](#52-how-to-create-custom-roles)
  - [5.3. Naming Convention of Custom role](#53-naming-convention-of-custom-role)
- [6. Validation & Rollback](#6-validation-rollback)
- [7. Roles & Responsibilities (RACI Matrix - Optional)](#7-roles-responsibilities-raci-matrix---optional)
- [8. Controls & Compliance](#8-controls-compliance)
- [9. Exceptions & Escalation](#9-exceptions-escalation)
- [10. Tooling & Systems](#10-tooling-systems)
  - [10.1. Backup – Custom Role](#101-backup-custom-role)
- [11. Linked Documentation (Optional)](#11-linked-documentation-optional)
- [12. Change History](#12-change-history)
  - [12.1. Document History, Version and Authors](#121-document-history-version-and-authors)
    - [12.1.1. Document Version and Authors](#1211-document-version-and-authors)
    - [12.1.2. Uniper Review/Approvals](#1212-uniper-reviewapprovals)
- [13. Source-only sections](#13-source-only-sections)
  - [13.1. Contents](#131-contents)
  - [13.2. Disclaimer](#132-disclaimer)
  - [13.3. Monitoring – Custom Role](#133-monitoring-custom-role)

---


## 1. Document Metadata

| Field | Value |
|------|------|
| Document ID |  |
| Domain | Public Cloud Framework (PCFv1) |
| Owning Team | HaCT Security and IAM Team |
| Document Owner | Indhumathi Subramanian |
| Technical Owner | Sebastian Heil |
| Audience | UNIPER architects and HaCT Security and IAM Team |
| Status | Draft |
| Version | 0.1 |
| Last Updated |  |
| Review Cycle |  |

;

![Figure 1](images/source_000_figure_1.png)

Public Cloud Framework version 1.0 and ES@UNIPER

HaCT RBAC – Custom Role

### 1.1. Target Audience

The intended audience for this document will be UNIPER architects and HaCT Security and IAM Team.

## 2. Purpose & Scope

### 2.1. Document Purpose

### 2.2. When/Why Custom role creation

If the Azure built-in roles don't meet the specific needs of your organization, we can create custom roles based on the requirements. Just like built-in roles, you can assign custom roles to users, groups, and service principals.

## 3. Definitions & Abbreviations (Optional)

## 4. Triggers & Preconditions

## 5. Step-by-Step Procedure

### 5.1. Process of Custom Role implementation

Below different steps of implementing new/updating custom role in PCFv1.

Due Diligence Phase

Analyse/POC Phase

CR creation

Implementation Phase

#### 5.1.1. Due Diligence Phase

Identify the permissions, user details, scope that Application team requires to perform their support/maintenance/enhancement activity on their application resource.

Prepare the permissions list that we have to include in the custom role. We can refer MS documents Azure resource provider operations or and  [azadvertizer.net](https://www.azadvertizer.net/azrolesadvertizer_all.html)   to compare permissions  of the  existing built-in role in azure.

Key point:  Users at any cost shouldn’t be able to modify/delete/write permissions to compute & network components in PCFv1.

#### 5.1.2. Analyse/POC Phase

Conduct an analysis of the existing built-in roles before proceeding with the creation of custom roles. Built-in roles should be used instead of custom roles if possible.

Always adhere to the principle of using the least privilege and just enough access model when designing custom roles.

Prepare a strong testcase to perform end to end testing of the custom role.

Before proceeding with a custom role update, please verify if there are any existing security principals with role assignments. If you find any security principals associated with the custom role being modified, thoroughly analyse whether the newly added actions, notactions, or scope may have any adverse effects. Performing an end-to-end analysis is highly recommended in such cases to ensure a comprehensive understanding of potential impacts.

After validation in R&D, a demo/session must be conducted with the service owner for approval to implement in PROD environment.

#### 5.1.3. CR creation

Ensure to create Change Request for update/New custom role in PREPROD/PROD subscriptions/Management group.

Here are the sample CRs,

| S.No | Activity | Activity | Sample CRs | Mandatory documents |
| --- | --- | --- | --- | --- |
| 1 | Create new custom role |  |  | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role in PCF MG. Post validating the permissions in POC/RnD environment | Create new custom role in MG Scope | CHG0054299 | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role in PCF MG. Post validating the permissions in POC/RnD environment | + role assignment | CHG0054299 | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
| 2 | Update custom role with new permission |  |  | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role is in PCF MG (POC,PREPROD and PROD subscriptions) | addition of Action | CHG0055401 | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role is in PCF MG (POC,PREPROD and PROD subscriptions) | addition of NotAction | CHG0055401 | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role is in PCF MG (POC,PREPROD and PROD subscriptions) | addition of Assignable scope | CHG0055401 | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role is in PCF MG (POC,PREPROD and PROD subscriptions) | removal of action | - | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role is in PCF MG (POC,PREPROD and PROD subscriptions) | removal of notAction | - | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |
|  | Note : When the custom role is in PCF MG (POC,PREPROD and PROD subscriptions) | removal of assignable scope | - | While creating CR:<br>1. Implementation Plan<br>2. BackOut Plan<br>During CR implementation:<br>3. Snapshots of before and after changes/update |

Table 1

Document of Implementation plan, BackOut Plan must be placed in the below shared path,

Share Path Link to place document – [CR Documents](https://uniper.sharepoint.com.mcas.ms/sites/CloudWorksTeam/HaCT/Forms/AllItems.aspx?id=%2Fsites%2FCloudWorksTeam%2FHaCT%2FCloud%20Dev%2C%20Sec%20and%20Compliance%2FSecurity%2FOps%2FCR%20Documents&viewid=3305bd1d%2Da258%2D4b01%2Dacde%2Dc9a0cf7707bd).

#### 5.1.4. Implementation Phase

Ensure to capture "before" and "after" implementation changes in custom roles or role assignments.

Document the snapshots and attach in the CTASK.

### 5.2. How to create custom roles

Follow MS document and create the custom role [Azure custom roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles).

### 5.3. Naming Convention of Custom role

Below are the naming conventions of the custom role.

Example:

|                       Reader                          |                     Network Resource

|                       Operator                      |                   VM and VMSS

|  | \| | Job Name | \| | Resource/Action Name |
| --- | --- | --- | --- | --- |

Table 2

## 6. Validation & Rollback

## 7. Roles & Responsibilities (RACI Matrix - Optional)

## 8. Controls & Compliance

## 9. Exceptions & Escalation

## 10. Tooling & Systems

### 10.1. Backup – Custom Role

Description:

In Azure environment, Custom Roles are generally created/updated based on Application access requirements. This Automation performs daily sync of all Azure Custom Roles in the PCF Management Group to Azure DevOps GIT Repository

Technical Details:

This is achieved through an Azure DevOps Pipeline. The Pipeline has 2 tasks -

1) Getting the unique custom role definitions in PCF Management Group → This is done using a PowerShell script which generated individual Json files for each custom role definitions

2) Syncing the Json files to GIT Repository → This is done using a series of GIT commands. The Json files are synced to a folder named AzureCustomRoles

It is scheduled to run daily and when the run is completed the GIT Repo is updated with all latest changes made in Azure for the custom roles.

Azure Resources:

Azure DevOps Project: [HaCT Security Services](https://dev.azure.com/uniperteamservices/HaCT%20Security%20Services)

GIT Repo: [HaCT Security Services - Repo](https://dev.azure.com/uniperteamservices/HaCT%20Security%20Services/_git/HaCT%20Security%20Services)

PowerShell Script to get the role definitions: [Get-AzureCustomRoles.ps1 - Repos](https://dev.azure.com/uniperteamservices/HaCT%20Security%20Services/_git/HaCT%20Security%20Services?path=/Get-AzureCustomRoles.ps1)

Azure Build Pipeline: [Pipelines - Runs for Azure Custom Role Definitions Sync](https://dev.azure.com/uniperteamservices/HaCT%20Security%20Services/_build?definitionId=3727)

Output folder in GIT Repo: [AzureCustomRoles](https://dev.azure.com/uniperteamservices/_git/HaCT%20Security%20Services?path=/AzureCustomRoles)

## 11. Linked Documentation (Optional)

## 12. Change History

### 12.1. Document History, Version and Authors

#### 12.1.1. Document Version and Authors

| Date | Version | Name | Role | Comments |
| --- | --- | --- | --- | --- |
| 27-July-2023 | 0.1 | Indhumathi Subramanian |  | Initial draft |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

Table 3

#### 12.1.2. Uniper Review/Approvals

| Approval/Review Date | Version | Name | Role |
| --- | --- | --- | --- |
| Review | 0.1 | Sebastian Heil | Cloud Security Architect |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

Table 4

## 13. Source-only sections

### 13.1. Contents

### 13.2. Disclaimer

### 13.3. Monitoring – Custom Role

In PCFv1 we don’t have monitoring setup for custom role create/delete/update.

<Will be implemented sooner>
