from clio.summary.openai_summariser import OpenAISummariser
import pandas as pd

df = pd.read_excel("data/master-sheet updated.xlsx").dropna()
print(len(df))
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
    summary_of_summaries = summariser.summarise_summaries(group_df["reason"].values)
    application_types = (
        group_df["application_type"].str.lower().value_counts().to_dict()
    )
    records.append(
        {
            "address": address,
            "summary": summary_of_summaries,
            "total_count": len(group_df),
            "appeals": application_types.get("appeal", 0),
            "enforcements": application_types.get("enforcement", 0),
        }
    )
summary_df = pd.DataFrame.from_records(records)
summary_df.to_parquet("data/summaries.pq")
