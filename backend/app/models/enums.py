"""Enumerations that codify the business vocabulary (Chapters 1–2).

Values are the canonical English tokens stored in the database. The CPM importer
maps the raw Persian/packed CPM values onto these enums.
"""
from __future__ import annotations

import enum


class SiteType(str, enum.Enum):
    """Second half of the Work Item business key (§2.5)."""

    NEW_SITE = "New Site"
    ADD_TECH = "Add Tech"        # CPM label; a.k.a. "Add Technology"
    REPEATER = "Repeater"


class Technology(str, enum.Enum):
    G2 = "2G"
    G3 = "3G"
    G4 = "4G"


class VillageType(str, enum.Enum):
    """هدف / اقماری (§1.5 هدف/اقماری)."""

    TARGET = "Target"           # هدف
    SATELLITE = "Satellite"     # اقماری


class WorkItemStatus(str, enum.Enum):
    """Drive-Test lifecycle states (§2.2)."""

    NEW = "New"
    HEALTH_CHECK = "Health Check"
    PROBLEMATIC = "Problematic"
    WAITING_RESOLUTION = "Waiting Resolution"
    READY_FOR_ASSIGNMENT = "Ready for Assignment"
    ASSIGNED = "Assigned to Contractor"
    DT_PERFORMED = "Drive Test Performed"
    COORDINATOR_VALIDATION = "Coordinator Validation"
    RE_DRIVE_TEST = "Re-Drive Test"
    PM_VALIDATION = "PM Validation"
    COMPLETED = "Completed"


class HealthCheckResult(str, enum.Enum):
    READY = "Ready"
    PROBLEMATIC = "Problematic"


class DriveTestStatus(str, enum.Enum):
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    RETURNED = "Returned"


class ApprovalStatus(str, enum.Enum):
    """Per-technology / per-authority acceptance status (§2.16)."""

    APPROVED = "Approved"
    REJECTED = "Rejected"
    PENDING = "Pending"     # blank in CPM = no feedback yet


class AcceptanceAuthority(str, enum.Enum):
    ICT_PROVINCE = "ICT Province"
    ICT_HQ = "ICT HQ"
    CRA_REGION = "CRA Region"
    CRA_HQ = "CRA HQ"


class ChangeRequestStatus(str, enum.Enum):
    """CPM sync decision states (§2.4)."""

    PENDING = "Pending"
    ACCEPTED = "Accepted"
    IGNORED = "Ignored"
    ARCHIVED = "Archived"
