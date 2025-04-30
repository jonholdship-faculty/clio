from datetime import date
from fastapi import FastAPI
import pandas as pd
from typing import Union

from clio.api.models import ApplicationSummary

app = FastAPI()
data = pd.read_parquet("data/website_data.pq")


@app.get("/list/{query_str}", response_model=list[str])
def list_addresses(query_str: str) -> list[str]:
    idx = data["address"].str.lower().str.contains(query_str.lower())
    return data.loc[idx, "address"].unique()


@app.get("/address/{address}", response_model=list[ApplicationSummary])
def query_address(address: str):
    rows = data.loc[data["address"].str.lower().str.contains(address.lower())]
    return [
        ApplicationSummary(
            decision_date=date.fromisoformat("2023-01-01"),
            application_ref=row["application_number"],
            address=row["address"],
            type="test type",
            decision_type=row["outcome"],
            reason=row["reason"],
        )
        for _, row in rows.iterrows()
    ]
