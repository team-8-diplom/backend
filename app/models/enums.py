from enum import StrEnum


class ApplicationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class TopicStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
    ASSIGNED = "assigned"


class UserRole(StrEnum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"