# Chapter 2 — Business Process & Business Rules

## 2.1 Overview

The USO Enterprise Platform manages the complete lifecycle of a Work Item from
the moment it appears in the CPM master file until all required regulatory
approvals are completed.

The platform replaces multiple independent Excel trackers with a single workflow
engine. A Work Item progresses through predefined business states, each owned by
specific user roles.

## 2.2 Business Lifecycle

A Work Item shall follow the lifecycle below.

### Drive Test Life Cycle

```
CPM Import
      │
      ▼
New Work Item
      │
      ▼
Health Check
      │
      ├──────────────► Problematic
      │                    │
      │                    ▼
      │              Waiting Resolution
      │
      ▼
Ready for Assignment
      │
      ▼
Assigned to Contractor
      │
      ▼
Drive Test Performed
      │
      ▼
Coordinator Validation
      │
      ├──── Reject ───► Re-Drive Test
      │
      ▼
PM Validation
      │
      ▼
Completed
```

### Acceptance Life Cycle

```
Drive Test Performed
      │
      ▼
Work item submission to ICT HQ
      │
Obtain ICT & CRA approval
      │
      ▼
Completed
```

## 2.3 Master Data Source

The CPM file is the only master source for infrastructure information.

The CPM file owns:

- Site ID
- Village ID
- Province
- Site Type
- Requested Technology
- Assignment Date (Official Assignment)
- On-Air Date

No user may manually create a Work Item. **All Work Items originate from CPM.**

## 2.4 CPM Synchronization Rules

The system shall compare every imported CPM file against the database.

For each incoming record:

- **New Record** — Create a new Work Item.
- **Existing Record (No Change)** — Ignore.
- **Existing Record (Changed)** — Create a Change Request and notify the Project
  Manager. PM may choose:
  - Accept Change
  - Ignore Change
  - Archive Existing Version

All decisions shall be stored in history.

## 2.5 Work Item Definition

A Work Item represents one executable deployment.

**Primary Business Key:** Site ID + Site Type

Examples:

```
E1990 + New Site
E1990 + Add Technology
```

Each Work Item has only one lifecycle.

## 2.6 Village Mapping

Each Work Item may contain one or more Villages.

```
Work Item
   ↓
Village A
Village B
Village C
```

Villages are imported exclusively from CPM. Village additions or removals
require PM approval.

## 2.7 Health Check

Health Check is performed by the assigned contractor.

**Purpose:** Determine whether the site is technically ready for Drive Test.

**Possible Results:**

- Ready
- Problematic

Problematic sites require a category.

## 2.8 Problem Categories

Initial categories:

- Temporary Power
- NWG Responsibility
- MS Responsibility
- Project Responsibility

The system shall allow administrators to add new categories without software
modification.

## 2.9 Assignment Process

Two assignment types exist.

### Work Item Assignment

- **Owner:** ICT
- Stored only for reporting.
- Cannot be edited.

### Contractor Assignment

**First Assignment (Initial Assignment):**

```
Project Manager >> Subcontractor >> Health Check (Ready or Problematic) >> Return to Project Manager
```

**Second Assignment (Official Assignment):**

```
Project Manager >> Subcontractor >> Perform DT
```

- **Owner:** Project Manager
- Assigns Work Item to one contractor.
- Assignment records include: Assignment Date, Assigned By, Contractor, Remarks,
  History.

## 2.10 Assignment Rules

One active contractor per Work Item.

If reassigned:

- Previous assignment becomes inactive.
- History remains permanently stored.

## 2.11 Drive Test

The contractor performs one Drive Test for the Work Item.

Contractor updates:

- Drive Test Date
- Status
- Comment

## 2.12 Drive Test Validation

Coordinator reviews submitted DT.

**Possible outcomes:**

- Approved
- Rejected
- Returned

If **rejected**, the workflow returns to Drive Test.

## 2.13 PM Validation

Coordinator approval alone is insufficient. **PM must approve.**

Only then: `Drive Test Status = Completed`.

## 2.14 Acceptance Scope

Acceptance is managed per **Site ID + Village ID**, not per Work Item.

This distinction is fundamental.

```
One Work Item
   ↓
Many Villages
   ↓
Each Village
   ↓
Independent Acceptance
```

## 2.15 Acceptance Authorities

Acceptance is performed independently by:

- ICT Province
- ICT HQ
- CRA Region
- CRA HQ

Each authority may issue different official letters.

## 2.16 Technology Approval

Each Village stores approval for **2G, 3G, 4G**. Each technology has independent
status.

**Possible values:**

- **Approved** — Indicated by the technology name itself; for example, a value
  of `2G` means 2G is approved. Otherwise it is rejected for that technology. A
  blank means no feedback / pending. The same rule applies to all technologies.
- **Rejected**
- **Pending** — waiting for feedback

## 2.17 Village Status

**Village Overall Status**

ICT phase:

- Approved
- Rejected
- Pending

CRA phase:

- Approved
- Rejected
- Pending

## 2.18 Site Completion Rule

A Work Item becomes **Fully Accepted** only when **ALL villages** AND **ALL
requested technologies** have reached **Approved**.

## 2.19 Letter Registration

Each approval letter stores:

- Letter Number
- Letter Date
- Authority
- Province / Region
- PDF/Picture Attachment (optional)
- Comment

One letter may approve one or many villages.

## 2.20 Acceptance Rejection

Rejected villages shall remain visible. Coordinator attempts resubmission using
existing DT.

If unsuccessful, a new DT is required.

History shall preserve every attempt.

## 2.21 Notification Rules

System notifications shall be generated automatically for:

- New CPM Changes
- Assignment Required
- Health Check Completed
- DT Submitted
- DT Rejected
- PM Approval Required
- Village Rejected
- Village Approved
- ICT Waiting
- CRA Waiting
- Contractor Reassignment
- CPM Conflict

## 2.22 Action Center

Every logged-in user shall immediately see **"My Pending Actions"**.

Examples:

**Coordinator**

- 23 DT waiting validation
- 54 ICT letters pending
- 12 CRA letters pending

**Contractor**

- 15 Assigned
- 6 Ready
- 3 Blocked
- 9 Waiting Validation

**PM**

- 4 CPM changes
- 16 PM approvals
- 9 Assignment requests
- 5 DT conflicts

## 2.23 Audit Rules

Every modification shall store:

- Timestamp
- User
- Previous Value
- New Value
- Reason
- Module
- IP Address (optional)

**History cannot be edited.**

## 2.24 Soft Delete

Operational records shall never be physically deleted. Soft Delete shall be
used. Deleted records remain recoverable.

## 2.25 Archive

Completed historical versions may be archived.

- Archived data remains searchable.
- Archived data is excluded from operational dashboards.

## 2.26 Business KPIs

The platform shall automatically calculate:

- Total Sites
- Total Villages
- On-Air Sites
- Ready for DT
- Assigned
- DT Completed
- DT Remaining
- DT Blocked
- ICT Approved
- CRA Approved
- Fully Accepted
- Partial Acceptance
- Contractor Productivity
- Province Completion
- Region Completion
- Monthly DT
- Yearly DT
- Monthly Acceptance
- Yearly Acceptance
- Block Categories
- Aging Analysis
- Backlog Trend

## 2.27 Business Automation

The system shall automatically determine:

- Ready for DT
- Ready for Submission
- Waiting ICT
- Waiting CRA
- Acceptance Complete
- PM Action Required
- Coordinator Action Required
- Contractor Action Required
- CPM Conflict
- Dashboard Counters
- Notifications

No manual status update shall be required where the system can derive the state
automatically.

## 2.28 Future Extension Rules

The architecture shall support future modules without modifying existing
business logic.

Future modules include:

- Budget Management
- Battery Tracking
- Permanent Power Tracking
- Invoice Management
- AMP Integration
- API Integration
- AI Analytics
- Executive KPI Engine

Each future module shall reference existing entities rather than duplicate
operational data.
