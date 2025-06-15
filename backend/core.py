from strands import Agent
from strands_tools import speak, http_request
from strands.models.ollama import OllamaModel
import pyttsx3

def speak_text(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def run_llm(developer_category: str, experience_level: str, note: str):
    agent = Agent(tools=[speak, http_request], model=OllamaModel(host="localhost", model_id="mistral"))

    query = f"""
    I'm {developer_category} with experience {experience_level} level and i'm preparing for interview so just generate 10 MCQ with 3 wrong answers and 1 right answer in valid json format without extra text for interview.{"and " + note if note else ""}.
    Format should be like  {{
      "question": "Which XML attribute is used to specify the height of a view in Android?",
      "options": ["option1"],
      "answer": 0 //index of array
    }}
    Note that questions should be different than past result and experience level mentioned.
    """

    print("Prompt: ", query)
    result = agent(query)

    print("Result: ", result.message.get("content").__getitem__(0).get("text"))
    return result
