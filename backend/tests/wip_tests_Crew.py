from crewai_config.crew import LatestAIResearchCrew


def test_crew():
    # Provide input so that any {query} placeholders are substituted
    crew_instance = LatestAIResearchCrew(
        inputs={"query": "What is the capital of France?"}
    )
    # Kick off the crew and capture the final output
    result = crew_instance.crew().kickoff()
    print("Crew Result:", result)


if __name__ == "__main__":
    test_crew()
