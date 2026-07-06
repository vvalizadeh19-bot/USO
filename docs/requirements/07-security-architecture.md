# Chapter 7 — Security Architecture

**Version 1.0 Draft**

## 7.1 Security Objectives

The security architecture of the USO Enterprise Platform shall ensure:

- Confidentiality
- Integrity
- Availability
- Accountability
- Traceability
- Least Privilege Access
- Non-Repudiation

The system must protect operational data while maintaining ease of use for
internal Irancell teams and subcontractors.

## 7.2 Security Principles

The platform shall follow these principles:

### SEC-01 — Zero Trust

No user, device, or request is trusted by default. Every request shall be
authenticated and authorized.

### SEC-02 — Least Privilege

Users receive only the minimum permissions required.

Example — a Contractor cannot:

- edit ICT approvals
- edit CRA approvals
- modify CPM
- assign contractors
- approve DT

### SEC-03 — Separation of Duties

Critical operations require different actors.

```
Contractor
   ↓
Submit DT
   ↓
Coordinator
   ↓
Validate DT
   ↓
Project Manager
   ↓
Approve DT
```

No user can complete the whole workflow alone.

### SEC-04 — Complete Auditability

Every important action must be recorded. Nothing disappears. Nothing is
overwritten.

## 7.3 Authentication

**Version 1:** Username, Password, JWT Authentication.

**Version 2:** Microsoft Active Directory, Azure AD, SSO.

### Login Flow

```
User
   ↓
Username + Password
   ↓
Authentication
   ↓
JWT Token
   ↓
Access Platform
```

## 7.4 Password Policy

- **Minimum:** 12 characters
- **Must contain:** Uppercase, Lowercase, Number, Special Character
- **Password History:** Last 5 passwords
- **Password Expiration:** 180 days

## 7.5 Session Management

- **Access Token:** 15 minutes
- **Refresh Token:** 8 hours
- **Automatic Logout:** 30 minutes inactivity
- **Maximum Sessions:** 3 devices

## 7.6 Authorization Model

**Role Based Access Control (RBAC).** Future: Attribute Based Access Control
(ABAC).

**Roles:**

- Administrator
- Project Manager
- Coordinator
- Regional Manager
- Contractor
- Viewer

## 7.7 Permission Matrix

| Module | Admin | PM | Coordinator | Contractor | Regional | Viewer |
|--------|-------|-----|-------------|------------|----------|--------|
| Dashboard | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| CPM Import | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ |
| Assignment | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ |
| Health Check | ✔ | ✔ | View | Edit | View | View |
| Drive Test | ✔ | ✔ | Validate | Submit | View | View |
| Acceptance | ✔ | ✔ | Update | View | View Region | View |
| Letters | ✔ | ✔ | Edit | ✖ | View | View |
| Users | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ |
| Reports | ✔ | ✔ | ✔ | Own | Region | Limited |

## 7.8 Data Visibility Rules

This project requires **row-level security**, not just screen-level security.

**Contractor** — can view only:

- Assigned Work Items
- Own DT history
- Own acceptance progress
- Own reports

Cannot view other contractors' data.

**Regional Manager** — can view only:

- Provinces in assigned region
- Regional KPIs
- Regional acceptance

Cannot modify operational records.

**Viewer** — access is configurable. May view:

- Selected dashboards
- Selected reports
- Selected provinces
- Selected contractors

No editing rights.

**Project Manager** — full operational visibility across all regions.

## 7.9 Data Classification

Operational data is classified into three categories.

**Public (Internal)** — Reference data: Province, Technology, Site Type.

**Confidential** — Operational records: DT Status, Acceptance, Assignments,
Letters.

**Restricted** — Security data: Users, Roles, Permissions, Audit Logs,
Authentication, Passwords.

## 7.10 Encryption

**In Transit:** TLS 1.3, HTTPS Only.

**At Rest:** PostgreSQL Encryption, Encrypted Backups.

**Password Storage:** Never stored. Only hashed. Recommended: Argon2id.

## 7.11 API Security

Every API requires:

- JWT Token
- Permission Check
- Input Validation
- Output Filtering
- Rate Limiting
- Audit

Example:

```
GET /api/work-items
   ↓
Authenticate
   ↓
Authorize
   ↓
Filter by Role
   ↓
Return
```

## 7.12 Input Validation

Every request validated by **Pydantic**.

Examples:

- **Site ID** — Required, Max Length, Regex
- **Letter Number** — Required, Unique, Length Validation

Reject invalid data before reaching the database.

## 7.13 SQL Injection Protection

The platform shall exclusively use **SQLAlchemy ORM**. Raw SQL is prohibited
except for optimized reporting queries. All queries are parameterized.

## 7.14 File Upload Security

- **Supported:** PDF, Excel
- **Maximum Size:** 20 MB
- Virus scanning (future)
- Executable files are prohibited.

## 7.15 Audit Log

Every critical action records: Timestamp, User, IP, Browser, Action, Module, Old
Value, New Value, Reason.

Audit entries are immutable.

## 7.16 Data Recovery

- **Deleted records:** Soft Delete, Recoverable.
- **Archived records:** Searchable, Recoverable.

## 7.17 Security Events

Generate alerts for:

- Multiple failed logins
- Unauthorized access attempts
- Role changes
- CPM imports
- Bulk updates
- Mass deletions
- Permission changes

## 7.18 Rate Limiting

- **Login:** 5 attempts / 15 minutes
- **API:** 100 requests / minute / user
- **Exports:** 10 exports / hour

## 7.19 Security Headers

Nginx shall enforce:

- HSTS
- CSP
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

## 7.20 Backup Security

Backups:

- Encrypted
- Compressed
- Offsite copy
- Daily verification
- 365-day retention

## 7.21 Logging & Monitoring

Application logs include:

- Request ID
- User ID
- Execution Time
- HTTP Status
- Error Code
- Module
- Correlation ID

Future integration: Grafana, Prometheus, Loki.

## 7.22 Disaster Recovery

| Metric | Target |
|--------|--------|
| RPO | 24 Hours |
| RTO | 4 Hours |

## 7.23 Compliance

The platform should align with:

- OWASP Top 10
- OWASP ASVS Level 2
- NIST Password Guidelines

Although the system is internal, it should follow internationally recognized
secure development practices.

## 7.24 Security Architecture Diagram

```
                 Browser
                    │
               HTTPS (TLS)
                    │
             React Frontend
                    │
              JWT Authentication
                    │
              API Gateway (FastAPI)
                    │
      ┌─────────────┼─────────────┐
      │             │             │
 Authentication  Authorization  Validation
      │             │             │
      └─────────────┼─────────────┘
                    │
             Business Services
                    │
              PostgreSQL Database
                    │
                 Audit Logs
```

## 7.25 Security Review — New Recommendations

While documenting the security model, five architectural improvements were
identified that were not part of the original discussions but would
significantly strengthen the platform.

### Recommendation 1 — Dynamic Permission Engine

Do not hardcode permissions in backend code. Store them in the database so Admin
can modify permissions without deployment.

### Recommendation 2 — Field-Level Security

Some users may access a Work Item but should not see specific fields (e.g.,
invoice amounts in the future Budget module or internal PM notes). Permissions
should be applicable at the field level.

### Recommendation 3 — Digital Approval Workflow

For sensitive actions (PM approval, CPM change acceptance), require explicit
confirmation and record a digital approval event. This provides stronger
accountability than a simple button click.

### Recommendation 4 — Immutable Event Store

Beyond Audit Logs, maintain an append-only Event Store capturing every domain
event (AssignmentCreated, DTValidated, ICTApproved, etc.). This enables future
event sourcing, analytics, and AI training without relying solely on current
table state.

### Recommendation 5 — Security Dashboard

Create an internal dashboard displaying:

- Failed login attempts
- Pending approvals
- CPM conflicts
- Bulk operations
- Recent permission changes
- Active sessions

This gives administrators operational visibility into security-related
activities.
