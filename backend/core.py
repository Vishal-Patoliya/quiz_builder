# Import required modules and tools
import os
import logging
import json
from dotenv import load_dotenv
from strands import Agent  # Core agent framework
from strands_tools import http_request  # Tool to perform HTTP requests
from strands.models.ollama import OllamaModel  # Specific LLM model from Ollama
from backend.utils import validate_quiz_options_format, is_valid_json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    filename="application.log",  # Log file name
    filemode="a"  # Append to the log file
)

# Primary function to run LLM with custom query
def run_llm(developer_category: str, experience_level: str, note: str):
    # Initialize the Agent with HTTP request tool and specified LLM model
    agent = Agent(tools=[http_request], model=OllamaModel(host=os.environ["HOST"], model_id=os.environ["MODEL_ID"]))

    # Form the prompt to generate MCQs with clear formatting instructions
    query = f"""
    You are an expert technical interviewer.
    Generate 10 **unique** multiple choice questions (MCQs) for a {developer_category} with {experience_level} experience{" and " + note if note else ""}.
    Ensure these questions are different based on experience mentioned.
    Each question must have exactly 4 options (3 wrong, 1 right), and your response should be **strictly valid JSON**, in the following format:
    {{
        "question": "Your question text?",
        "options": ["wrong1", "wrong2", "correct", "wrong3"],
        "answer": 0 //Index of array
    }}
    Do **not** include any explanations or introductory text. Only return valid JSON array as output.
    """

    # Send query to LLM and retrieve the result
    logging.debug("Sending query to the LLM.", query)
    result = agent(query)

    # Extract response string from agent output
    response_str = result.message.get("content").__getitem__(0).get("text")
    logging.debug("Response received: %s", response_str)

    # Check if the response is valid JSON, and if so, attempt to repair malformed options if necessary
    if is_valid_json(response_str):
        logging.info("Valid JSON response received.")
        return True, validate_quiz_options_format(json.loads(response_str))
    else:
        logging.warning("Invalid JSON response received.")
        return False, response_str
