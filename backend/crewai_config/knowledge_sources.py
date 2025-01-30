# backend/crewai_config/knowledge_sources.py

import os
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
# or from crewai.knowledge.source.crew_docling_source import CrewDoclingSource

# Example: Suppose we have some plain text with sample job data
JOB_POSTINGS_TEXT = """\
Sr. Python Developer - 5+ years required. Must have Django experience.
Data Scientist - must have ML background, advanced stats, etc.
Software Engineer - required to have strong system design, etc.
"""

job_postings_source = StringKnowledgeSource(
    content=JOB_POSTINGS_TEXT,
    # chunk_size=4000,
    # chunk_overlap=200,
    metadata={"category": "job_postings"}
)
