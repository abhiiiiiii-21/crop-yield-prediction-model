import logging
import json
import os
import sys

from dotenv import load_dotenv

# Add the backend directory to sys.path to allow 'app' module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, ".."))


if backend_dir not in sys.path:
    sys.path.append(backend_dir)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.agents.agent import run_agent

def run(input_data: dict):
    try:
        if not input_data:
            return {"error": "No input provided"}

        logger.info("Received input data")

        result = run_agent(input_data)

        logger.info(f"Agent execution completed")
        logger.info(f"Final Output: {result}")

        return result

    except Exception:
        logger.exception("Error in main.run")
        return {"error": "Something went wrong in backend"}

if __name__ == "__main__":

    sample_input = {
        "crop": "Wheat",
        "season": "Rabi",
        "state": "Punjab",
        "rainfall": 120,
        "temperature": 25,
        "pH": 6.5,
        "fertilizer": 50,
        "query": "How to improve yield?"
    }

    output = run(sample_input)

    print("\n===== RESULT =====")
    print(json.dumps(output.get("final_output", output), indent=2))
