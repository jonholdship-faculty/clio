from clio.summary.openai_summariser import OpenAISummariser

# Sample individual decision summaries
sample_summaries = [
    "Refused due to conflict with Local Plan policies H3 and DE1. The proposed layout failed to provide adequate amenity space and separation distances between habitable rooms, and created safety risks due to contrived access.",
    "Granted subject to conditions. The proposal for variation of condition was found to have no adverse impact on highway safety or residential amenity, and remained within the scope of the original Environmental Impact Assessment.",
    "Appeal allowed. The Inspector concluded that the proposed boundary fencing would not harm local character and would not materially affect highway safety. Conditions imposed to control future alterations."
]

# Run the test
summariser = OpenAISummariser()
insight = summariser.summarise_summaries(sample_summaries)

print("\n📝 Site Insight Summary:")
print(insight)
