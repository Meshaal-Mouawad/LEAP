# KPI: Complaint Reopen Rate Pct
# Description: Measures the percentage of closed customer complaint cases reopened during the reporting period.
# Objective: Detect weak complaint closure quality and recurring unresolved customer issues.
# Formula: (reopened_complaints / closed_complaints) * 100
# Input: reopened_complaints and closed_complaints from CRM service case records.
# Unit: %
# Data Source: CRM service-management case table crm_customer_cases.
# Used In: Customer Experience Quality Dashboard
# Comments: Synthetic test values: reopened_complaints=18 and closed_complaints=640 for May.
def complaint_reopen_rate_pct(reopened_complaints: int, closed_complaints: int) -> float | None:
    if closed_complaints == 0:
        return None
    return (reopened_complaints / closed_complaints) * 100
