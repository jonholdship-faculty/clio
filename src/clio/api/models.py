from datetime import date
from sqlmodel import SQLModel


class ApplicationSummary(SQLModel):
    decision_date: date
    application_ref: str
    address: str
    type: str  # application, appeal, enforcement
    decision_type: str  # approval_with_conditions, approval, refusal, appeal_allowed, appeal_dismissed, no_further_action, breach_of_condition, enforcement_notice_served
    reason: str
    overall_summary: str
    total_applications: int
    appeals: int
    enforcements: int
