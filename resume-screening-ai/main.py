import os

# Set HuggingFace key
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "Your-api-key"

# (Optional but required for assignment)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "Your-api-key"

from chains.pipeline import pipeline

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

resume = load_file("data/strong_resume.txt")
job_description = load_file("data/job_description.txt")

result = pipeline.invoke({
    "resume": resume,
    "job_description": job_description
})

print("\n===== FINAL OUTPUT =====\n")
print(result)
