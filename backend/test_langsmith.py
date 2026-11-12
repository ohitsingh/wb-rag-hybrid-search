from langsmith import traceable


@traceable
def hello():
    return "Hello LangSmith"


hello()

print("Done")
