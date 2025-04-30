from clio.summary.openai_summariser import OpenAISummariser


test_doc = """
outcome fail
this building is in a conservation area
"""


summariser = OpenAISummariser()
summariser.summarise_document(test_doc)
