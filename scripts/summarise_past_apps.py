from clio.summary.openai_summariser import OpenAISummariser
import pandas as pd

df = pd.read_csv("data/Planning Hack Data v0.1.csv", quotechar='"')
df = df[["Address", "Application Number", "FullText", "Outcome"]].dropna()

df2 = pd.read_excel("data/Planning Hack Data v0.2.xlsx")
df2 = df2[["Address", "Application Number", "FullText", "Outcome"]].dropna()

df = pd.concat([df, df2]).reset_index(drop=True)
df = df.rename(
    {
        "Address": "address",
        "Application Number": "application_number",
        "FullText": "full_text",
        "Outcome": "outcome",
    },
    axis=1,
)

summariser = OpenAISummariser()

df["reason"] = df.apply(
    lambda row: summariser.summarise_document(
        document_text=row["full_text"], outcome=row["outcome"]
    ),
    axis=1,
)

df.to_parquet("data/website_data.pq")

records = []
for address, group_df in df.groupby("address"):
    summary_of_summaries = summariser.summarise_summarys(group_df["reason"].values)
    records.append(
        {
            "address": address,
            "summary": summary_of_summaries,
        }
    )
summary_df = pd.DataFrame.from_records(records)
summary_df.to_parquet("data/summaries.pq")
