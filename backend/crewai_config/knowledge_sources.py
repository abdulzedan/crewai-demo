import os
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

JOB_POSTINGS_TEXT = """\
Sr. Python Developer - 5+ years required. Must have Django experience.
Data Scientist - must have ML background, advanced stats, etc.
Software Engineer - required to have strong system design, etc.
"""

job_postings_source = StringKnowledgeSource(
    content=JOB_POSTINGS_TEXT,
    metadata={"category": "job_postings"}
)
