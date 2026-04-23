from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
Compare the resume data with job description.

Return:
- Matching skills
- Missing skills
- Match percentage

Resume Data:
{resume_data}

Job Description:
{job_description}
"""
)