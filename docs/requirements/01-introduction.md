# Chapter 1 — Introduction

## 1.1 Purpose

The purpose of this document is to define the complete functional and
non-functional requirements of the USO Enterprise Platform (UEP).

The platform is designed to replace multiple disconnected Excel trackers, manual
email communications, and decentralized approval processes with a centralized
web-based system that manages the complete lifecycle of USO project execution.

The system will provide a single source of truth for:

- Drive Test activities
- Project manager management
  - Project Delivery
  - Assignment management
- Contractor management
- Acceptance workflow
  - ICT approvals
  - CRA approvals
- Executive dashboards
- Project reporting
- Future operational modules

This document serves as the baseline specification for software development,
testing, deployment, maintenance, and future enhancement.

## 1.2 Background

The current operational process relies heavily on manual activities performed
across multiple Excel spreadsheets owned by different stakeholders.

These spreadsheets are exchanged through email and updated independently by:

- Project Support Office (our team)
- Drive Test Contractors
- ICT Coordinators
- CRA Coordinators
- Regional Managers
- Project Manager

The lack of a centralized platform creates significant operational challenges.
Examples include:

- duplicate data
- inconsistent status
- manual lookup operations
- difficult reporting
- poor traceability
- delayed decision making
- lack of ownership visibility

As the project has been running for several years and manages approximately
**500 new sites annually**, the existing approach is no longer sustainable.

## 1.3 Business Problem

The current business process suffers from several operational inefficiencies.

### Manual Data Synchronization

Acceptance information is received from multiple independent organizations.
Each organization delivers data using different Excel formats. Project
coordinators manually perform dozens of lookup operations before updating the
master tracker.

### Multiple Sources of Truth

Different teams maintain independent trackers. Examples include:

- CPM Master File (main database of project)
- Drive Test Tracker (our database tracker)
- ICT Tracker
- CRA Tracker
- Contractor Progress Files

These files frequently become inconsistent.

### Lack of Process Visibility

Project Managers cannot immediately answer questions such as:

- Which contractor is delayed?
- Which region has the highest backlog?
- Which villages are waiting for ICT?
- Which sites are blocked because of temporary power?
- Which approvals are missing?

### Reporting Complexity

Generating management reports requires manual Excel processing that may take
several hours or even days.

### No Ownership Tracking

Responsibilities across different teams are unclear. The organization lacks a
centralized Action Center identifying pending activities for each user.

## 1.4 Business Objectives

The primary objective of the platform is to establish a centralized operational
system that manages the entire lifecycle of every USO Work Item.

| ID | Objective |
|------|-----------|
| **BO-01** | Eliminate Excel as the operational working environment. |
| **BO-02** | Centralize all operational data into a single database. |
| **BO-03** | Provide real-time dashboards for all stakeholders. |
| **BO-04** | Reduce manual reporting effort. |
| **BO-05** | Improve transparency of responsibilities. |
| **BO-06** | Track every operational activity using complete audit history. |
| **BO-07** | Automate workflow progression wherever business rules allow. |
| **BO-08** | Support future business modules without redesigning the architecture. |

## 1.5 Project Scope

The initial release shall support the following business domains.

### Included

- Drive Test Management
- Login Page
- Assignment Management
- Health Check
- ICT Acceptance
- CRA Acceptance
- Letter Tracking
- Contractor Management
- Executive Dashboard
- Regional Dashboard
- Coordinator Dashboard
- Reports
- Notification Center
- Action Center
- Administration
- Role Management
- User Management
- Master Data Import
- History Tracking
- Audit Log

## 1.7 Stakeholders

| Stakeholder | Responsibility |
|-------------|----------------|
| Admin | System Administration |
| Project Manager | Project Governance |
| Coordinator | Acceptance & DT Coordination |
| Contractor | DT Execution |
| Regional Manager | Regional Follow-up |
| Viewer | Read-only Access |

## 1.8 Definitions

| Term | Definition |
|------|------------|
| Site | Physical telecom location |
| Village | Coverage area served by a Site |
| Work Item | Unique execution unit identified by (Site ID + Site Type) |
| Acceptance | Government approval process |
| ICT | Ministry ICT Organization |
| CRA | Communications Regulatory Authority |
| DT | Drive Test |
| CPM | Master source system for project deployment |
| Assignment | Official notification assigning a Work Item (1. Site assignment to MTN and 2. Site assignment to DT contractor) |
| Health Check | Contractor validation before DT |
| Approval | Final government confirmation |
| Rejection | Government refusal requiring corrective action |

## 1.9 Design Principles

The platform shall be developed according to the following architectural
principles:

- **Single Source of Truth** — Only one database stores operational information.
- **Database-Driven Workflow** — Workflow progression is determined by database
  state rather than user assumptions.
- **Event-Based Processing** — Business actions generate events that update
  workflow status automatically.
- **Auditability** — Every change performed by every user shall be permanently
  recorded.
- **Scalability** — The architecture shall support future modules without
  redesign.
- **Security** — Role-Based Access Control (RBAC) shall govern every operation.
- **Extensibility** — Business logic shall remain independent from presentation
  and reporting.

## 1.10 Success Criteria

The project shall be considered successful when:

- Excel is no longer required for daily operations.
- Every stakeholder uses the platform as the primary operational system.
- Management dashboards are generated in real time.
- Approval tracking becomes fully transparent.
- Responsibility for every pending activity is clearly identified.
- Historical changes are preserved.
- The system supports future operational modules without architectural
  modification.
