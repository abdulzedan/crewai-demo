#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Since this file is in backend/tests/, the project root is three levels up.
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Set CREWAI_CONFIG_PATH to the YAML config directory.
# Your YAML files are in: backend/crewai_config/config/
config_path = project_root / "backend" / "crewai_config" / "config"
os.environ["CREWAI_CONFIG_PATH"] = str(config_path)
print(f"[TEST DEBUG] CREWAI_CONFIG_PATH is: {os.environ['CREWAI_CONFIG_PATH']}")

from crewai_config.crew import LatestAIResearchCrew

def test_agent_configs():
    crew_instance = LatestAIResearchCrew()
    manager = crew_instance.manager()
    generalist = crew_instance.generalist()
    web_researcher = crew_instance.web_researcher()
    aggregator = crew_instance.aggregator()
    synthesizer = crew_instance.synthesizer()
    
    print("Manager role:", manager.role)
    print("Manager goal:", manager.goal)
    print("Generalist role:", generalist.role)
    print("Generalist goal:", generalist.goal)
    print("Web Researcher role:", web_researcher.role)
    print("Web Researcher goal:", web_researcher.goal)
    print("Aggregator role:", aggregator.role)
    print("Aggregator goal:", aggregator.goal)
    print("Synthesizer role:", synthesizer.role)
    print("Synthesizer goal:", synthesizer.goal)


if __name__ == "__main__":
    test_agent_configs()
