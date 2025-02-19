from crewai_config.crew import LatestAIResearchCrew
from app.models import UserText, CustomUser
import logging

logger = logging.getLogger(__name__)

def process_crewai_task(user_input: str, user_id: int = None):
    try:
        user = None
        if user_id is not None:
            user = CustomUser.objects.filter(id=user_id).first()

        # Log the user query.
        UserText.objects.create(
            user=user,
            content=f"User query: {user_input}"
        )

        # (Optional) Test the DirectAnswerTool for simple queries.
        from app.tools.direct_answer_tool import DirectAnswerTool
        test_tool = DirectAnswerTool()
        test_response = test_tool._run("Capital of France?")
        logger.debug(f"DirectAnswerTool test response: {test_response}")

        # Create and kick off the Crew.
        crew = LatestAIResearchCrew().crew()
        result = crew.kickoff(inputs={"query": user_input})
        raw_output = result.raw
        logger.debug(f"Raw output: {raw_output} (type: {type(raw_output)})")

        # Process the raw output.
        final_text = ""
        if raw_output:
            if isinstance(raw_output, list):
                if len(raw_output) > 0:
                    final_text = " ".join(map(str, raw_output)).strip()
            elif isinstance(raw_output, str):
                final_text = raw_output.strip()
            else:
                final_text = str(raw_output).strip()
        if not final_text:
            final_text = "Final Answer: I'm sorry, I couldn't generate an answer."
        else:
            if not final_text.startswith("Final Answer:"):
                final_text = "Final Answer: " + final_text

        # Process task steps if available.
        steps = getattr(result, "steps", None)
        steps_text = ""
        if steps and isinstance(steps, list):
            steps_text = "\n".join(f"Step {i+1}: {s}" for i, s in enumerate(steps))

        # Log the final answer.
        UserText.objects.create(
            user=user,
            content=f"Final answer: {final_text[:500]}"
        )

        return {
            "status": "completed",
            "result": final_text[:1000],
            "steps": steps_text
        }
    except Exception as e:
        logger.exception("Error in process_crewai_task")
        return {
            "status": "failed",
            "error": str(e)
        }
