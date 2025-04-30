from datetime import date
from fastapi import FastAPI
import pandas as pd
from typing import Union

from clio.api.models import ApplicationSummary

app = FastAPI()
data = pd.read_parquet("data/website_data.pq")


@app.get("/list/{query_str}", response_model=list[str])
def list_addresses(query_str: str) -> list[str]:
    idx = data["Address"].str.lower().str.contains(query_str.lower())
    return data.loc[idx, "Address"].unique()


@app.get("/address/{address}", response_model=list[ApplicationSummary])
def query_address(address: str):
    return [
        ApplicationSummary(
            decision_date=date.fromisoformat("2023-01-01"),
            application_ref="test1",
            address=address,
            type="application",
            decision_type="refusal",
            reason="test case 1",
        ),
        ApplicationSummary(
            decision_date=date.fromisoformat("2023-01-01"),
            application_ref="test2",
            address=address,
            type="appeal",
            decision_type="appeal_allowed",
            reason="test case 2",
        ),
        ApplicationSummary(
            decision_date=date.fromisoformat("2023-01-01"),
            application_ref="test3",
            address=address,
            type="application",
            decision_type="approval",
            reason="test case 3",
        ),
    ]
