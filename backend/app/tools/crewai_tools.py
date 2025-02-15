import random
from typing import Type, ClassVar
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
from app.services.vector_store import ChromaVectorStore

# ------------------------------
# StoreTextTool
# ------------------------------
class StoreTextInput(BaseModel):
    text: str = Field(..., description="User text to store in Chroma DB")

class StoreTextTool(BaseTool):
    name: str = "store_text_tool"
    description: str = "Store user-provided text into Chroma DB for semantic retrieval"
    args_schema: Type[BaseModel] = StoreTextInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, text: str) -> str:
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        vs.store_text(text)
        return f"Stored text: {text[:50]}..."

# ------------------------------
# RetrieveTextTool
# ------------------------------
class RetrieveTextInput(BaseModel):
    query: str = Field(..., description="Search query to find relevant text in Chroma DB")

class RetrieveTextTool(BaseTool):
    name: str = "retrieve_text_tool"
    description: str = "Retrieve relevant text from Chroma DB"
    args_schema: Type[BaseModel] = RetrieveTextInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        results = vs.search_similar(query, n_results=3)
        docs = results.get("documents", [])
        if not docs or not docs[0]:
            return "No similar text found."
        return f"Found {len(docs[0])} doc(s):\n\n" + "\n---\n".join(docs[0])

# ------------------------------
# FindJobsTool
# ------------------------------
class FindJobsInput(BaseModel):
    keyword: str = Field(..., description="Keyword for imaginary job listings")

class FindJobsTool(BaseTool):
    name: str = "find_jobs_tool"
    description: str = "Returns up to 3 imaginary jobs for a given keyword"
    args_schema: Type[BaseModel] = FindJobsInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, keyword: str) -> str:
        sample_jobs = [
            f"{keyword.capitalize()} Engineer at XYZ Inc. - 3+ years required",
            f"Senior {keyword.capitalize()} Specialist at ABC LLC - Remote possible",
            f"{keyword.capitalize()} Associate at ACME Startup - Great for new grads",
        ]
        random.shuffle(sample_jobs)
        return "\n".join(sample_jobs)



# # backend/app/tools/crewai_tools.py

# import random
# from typing import Type, ClassVar
# from pydantic import BaseModel, Field, ConfigDict
# from crewai.tools import BaseTool
# from app.services.vector_store import ChromaVectorStore

# # ------------------------------
# # StoreTextTool
# # ------------------------------

# class StoreTextInput(BaseModel):
#     text: str = Field(..., description="User text to store in Chroma DB")

# class StoreTextTool(BaseTool):
#     name: str = "store_text_tool"
#     description: str = "Store user-provided text into Chroma DB for semantic retrieval"
#     args_schema: Type[BaseModel] = StoreTextInput

#     model_config = ConfigDict(
#         check_fields=False,
#         extra="allow",
#         arbitrary_types_allowed=True,
#     )

#     def _run(self, text: str) -> str:
#         vs = ChromaVectorStore(persist_directory=".chroma-local")
#         vs.store_text(text)
#         return f"Stored text: {text[:50]}..."

# # ------------------------------
# # RetrieveTextTool
# # ------------------------------

# class RetrieveTextInput(BaseModel):
#     query: str = Field(..., description="Search query to find relevant text in Chroma DB")

# class RetrieveTextTool(BaseTool):
#     name: str = "retrieve_text_tool"
#     description: str = "Retrieve relevant text from Chroma DB"
#     args_schema: Type[BaseModel] = RetrieveTextInput

#     model_config = ConfigDict(
#         check_fields=False,
#         extra="allow",
#         arbitrary_types_allowed=True,
#     )

#     def _run(self, query: str) -> str:
#         vs = ChromaVectorStore(persist_directory=".chroma-local")
#         results = vs.search_similar(query, n_results=3)
#         docs = results.get("documents", [])
#         if not docs:
#             return "No similar text found."
#         return f"Found {len(docs)} doc(s):\n\n" + "\n---\n".join(docs)

# # ------------------------------
# # FindJobsTool
# # ------------------------------

# class FindJobsInput(BaseModel):
#     keyword: str = Field(..., description="Keyword for imaginary job listings")

# class FindJobsTool(BaseTool):
#     name: str = "find_jobs_tool"
#     description: str = "Returns up to 3 imaginary jobs for a given keyword"
#     args_schema: Type[BaseModel] = FindJobsInput

#     model_config = ConfigDict(
#         check_fields=False,
#         extra="allow",
#         arbitrary_types_allowed=True,
#     )

#     def _run(self, keyword: str) -> str:
#         sample_jobs = [
#             f"{keyword.capitalize()} Engineer at XYZ Inc. - 3+ years required",
#             f"Senior {keyword.capitalize()} Specialist at ABC LLC - Remote possible",
#             f"{keyword.capitalize()} Associate at ACME Startup - Great for new grads",
#         ]
#         random.shuffle(sample_jobs)
#         return "\n".join(sample_jobs)

# # ------------------------------
# # JobParserTool
# # ------------------------------

# class JobParserInput(BaseModel):
#     job_posting: str = Field(..., description="Raw text of a job posting")

# class JobParserTool(BaseTool):
#     model_config = ConfigDict(
#         check_fields=False,
#         extra="allow",
#         arbitrary_types_allowed=True,
#     )

#     name: ClassVar[str] = "job_parser_tool"
#     description: ClassVar[str] = "Useful for analyzing text of a job posting. Extract top skills, etc."
#     args_schema: ClassVar[Type[BaseModel]] = JobParserInput

#     def _run(self, job_posting: str):
#         lines = job_posting.split('\n')
#         highlights = [line.strip() for line in lines if "required" in line.lower() or "must" in line.lower()]
#         if not highlights:
#             highlights.append("No explicit 'required' lines found.")
#         return f"Key lines found: {highlights}"

#     async def _arun(self, job_posting: str):
#         return self._run(job_posting)

# # ------------------------------
# # ResumeParserTool
# # ------------------------------

# class ResumeParserInput(BaseModel):
#     resume_text: str = Field(..., description="Raw text of the user resume")

# class ResumeParserTool(BaseTool):
#     model_config = ConfigDict(
#         check_fields=False,
#         extra="allow",
#         arbitrary_types_allowed=True,
#     )

#     name: ClassVar[str] = "resume_parser_tool"
#     description: ClassVar[str] = "Analyzes or rewrites a user resume. May highlight missing keywords."
#     args_schema: ClassVar[Type[BaseModel]] = ResumeParserInput

#     def _run(self, resume_text: str):
#         if len(resume_text) < 50:
#             return "Resume is too short, recommended to expand."
#         return "Resume length is decent. Possibly add more job-specific keywords."

#     async def _arun(self, resume_text: str):
#         return self._run(resume_text)
