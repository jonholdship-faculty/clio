from clio.summary.openai_summariser import OpenAISummariser
import pandas as pd


df = pd.read_csv("data/Planning Hack Data v0.1.csv")
df = df[["Address", "Application Number", "FullText"]].dropna()
summariser = OpenAISummariser()

df["reason"] = df["FullText"].map(summariser.summarise_document)
df.to_parquet("data/website_data.pq")
