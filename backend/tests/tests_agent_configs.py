#!/usr/bin/env python
import os
import sys
from pathlib import Path
import pytest

# Set up the project root and update sys.path.
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Set CREWAI_CONFIG_PATH to the YAML config directory.
config_path = project_root / "backend" / "crewai_config" / "config"
os.environ["CREWAI_CONFIG_PATH"] = str(config_path)

from crewai_config.crew import LatestAIResearchCrew

def test_agent_configs():
    """
    Test the configuration of agents by instantiating the research crew and verifying
    that each agent's role and goal are non-empty strings.
    """
    crew_instance = LatestAIResearchCrew()
    manager = crew_instance.manager()
    web_researcher = crew_instance.web_researcher()
    aggregator = crew_instance.aggregator()
    synthesizer = crew_instance.synthesizer()

    for agent_name, agent in [
        ("Manager", manager),
        ("Web Researcher", web_researcher),
        ("Aggregator", aggregator),
        ("Synthesizer", synthesizer)
    ]:
        assert isinstance(agent.role, str) and agent.role, f"{agent_name} role should be a non-empty string"
        assert isinstance(agent.goal, str) and agent.goal, f"{agent_name} goal should be a non-empty string"

if __name__ == "__main__":
    pytest.main()
