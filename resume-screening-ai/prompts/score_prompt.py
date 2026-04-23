from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate(
    input_variables=["match_data"],
    template="""
Based on the match data, assign a score from 0 to 100.

Match Data:
{match_data}

Return only the numeric score.
"""
)