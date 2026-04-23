from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate(
    input_variables=["score", "match_data"],
    template="""
Explain why this score was given.

Score: {score}
Match Data: {match_data}

Give clear reasoning.
"""
)