from clio.summary.openai_summariser import OpenAISummariser
import pandas as pd


df = pd.read_csv("data/Planning Hack Data v0.1.csv")

print(df.columns)


summariser = OpenAISummariser()

json_records = df["FullText"].map(summariser.summarise_document)
output_df = pd.DataFrame.from_records(json_records)
print(output_df)
