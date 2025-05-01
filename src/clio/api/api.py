from datetime import date
from fastapi import FastAPI
import pandas as pd
from typing import Union

from clio.api.models import ApplicationSummary

app = FastAPI()
data = pd.read_parquet("data/website_data.pq")
summary_data = pd.read_parquet("data/summaries.pq")


@app.get("/list/{query_str}", response_model=list[str])
def list_addresses(query_str: str) -> list[str]:
    idx = data["address"].str.lower().str.contains(query_str.lower())
    return data.loc[idx, "address"].unique()


@app.get("/address/{address}", response_model=list[ApplicationSummary])
def query_address(address: str):
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
            approvalrate=summary["approval_rate"].values[0],
        )
        for _, row in rows.iterrows()
    ]
