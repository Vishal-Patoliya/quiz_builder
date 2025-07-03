from strands import Agent
from strands_tools import http_request
from strands.models.ollama import OllamaModel
import json

def run_llm(developer_category: str, experience_level: str, note: str):
    agent = Agent(tools=[http_request], model=OllamaModel(host="localhost", model_id="mistral"))

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

    print("Prompt: ", "query")

    result = agent(query)
    response_str = result.message.get("content").__getitem__(0).get("text")
    if is_valid_json(response_str):
        return True, repair_options(json.loads(response_str))
    else:
        return False, response_str

def is_valid_json(json_string):
    try:
        data = json.loads(json_string)

        # Check if top-level is a list
        if not isinstance(data, list) or len(data) == 0:
            return False

        for item in data:
            if not isinstance(item, dict):
                return False
            if not all(key in item for key in ("question", "options", "answer")):
                return False
            if not isinstance(item["options"], list):
                return False
        return True
    except json.JSONDecodeError:
        return False

def repair_options(data):
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "options" in item:
                if (isinstance(item["options"], list) and
                        len(item["options"]) == 1 and
                        isinstance(item["options"][0], str) and
                        "," in item["options"][0]):
                    item["options"] = [opt.strip() for opt in item["options"][0].split(",")]
    return data
