from mcp.server.fastmcp import FastMCP
import pandas as pd
from datetime import date
from sqlmodel import SQLModel
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Create an MCP server
mcp = FastMCP("Planning Restrictions Checker")

# Load the data
data = pd.read_parquet(PROJECT_ROOT / "data" / "website_data.pq")
summary_data = pd.read_parquet(PROJECT_ROOT / "data" / "summaries.pq")

class ApplicationSummary(SQLModel):
    decision_date: date
    application_ref: str
    address: str
    type: str  # application, appeal, enforcement
    decision_type: str  # approval_with_conditions, approval, refusal, appeal_allowed, appeal_dismissed, no_further_action, breach_of_condition, enforcement_notice_served
    reason: str

@mcp.tool(description="Get all supported addresses for the planning restrictions checker")
def list_addresses() -> list[str]:
    """List all supported addresses"""
    return data["address"].unique()

@mcp.tool(description="Get a list of addresses that match the query string")
def list_addresses_for_query(query_str: str) -> list[str]:
    """List addresses that match the query string"""
    idx = data["address"].str.lower().str.contains(query_str.lower())
    return data.loc[idx, "address"].unique()


@mcp.tool(description="Get a list of planning restrictions for an address")
def get_planning_restrictions(address: str) -> list[str]:
    """Get planning restrictions for an address"""
    rows = data.loc[data["address"].str.lower().str.contains(address.lower())]
    summary = summary_data.loc[
        summary_data["address"].str.lower().str.contains(address.lower())
    ]
    return [
        ApplicationSummary(
            decision_date=date.fromisoformat("2023-01-01"),
            application_ref=row["application_number"],
            address=row["address"],
            type=row["application_type"],
            decision_type=row["outcome"],
            reason=row["reason"],
            overall_summary=summary["summary"].values[0],
            total_applications=summary["total_count"].values[0],
            appeals=summary["appeals"].values[0],
            enforcements=summary["enforcements"].values[0],
        )
        for _, row in rows.iterrows()
    ]

