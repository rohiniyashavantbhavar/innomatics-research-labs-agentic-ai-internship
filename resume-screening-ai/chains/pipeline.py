from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint

from prompts.extract_prompt import extract_prompt
from prompts.match_prompt import match_prompt
from prompts.score_prompt import score_prompt
from prompts.explain_prompt import explain_prompt

# Use free HuggingFace model
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    temperature=0.5,
    max_new_tokens=512
)

chat_model = ChatHuggingFace(llm=llm)

pipeline = (
    extract_prompt
    | chat_model
    | match_prompt
    | chat_model
    | score_prompt
    | chat_model
    | explain_prompt
    | chat_model
)
