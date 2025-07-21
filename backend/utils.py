import re
import logging
import json

def validate_input(user_input):
    """
    validate_input user input to prevent injection attacks.

    Args:
        user_input (str): The raw input provided by the user.

    Returns:
        str: The sanitized input.
    """
    if not user_input:
        return ""

    # Remove potentially harmful characters
    sanitized_input = re.sub(r"[^a-zA-Z0-9\s.,!?-]", "",
                             user_input)  # Allow only alphanumeric, spaces, and basic punctuation
    sanitized_input = sanitized_input.strip()  # Remove leading/trailing whitespace
    logging.info(f"Sanitized user input: {sanitized_input}")
    return sanitized_input

# Helper function to repair malformed 'answers' entries
def validate_quiz_options_format(data):
    """
    Validate and resolve malformed question where the 'options' list was incorrectly returned as a single comma-separated string.

    Args:
        data (list): List of question dictionaries

    Returns:
        list: Cleaned-up list of question dictionaries
    """
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "options" in item:
                if (isinstance(item["options"], list) and
                        len(item["options"]) == 1 and
                        isinstance(item["options"][0], str) and
                        "," in item["options"][0]):
                    item["options"] = [opt.strip() for opt in item["options"][0].split(",")]
    logging.info("Options are in valid format")
    return data


# Helper function to validate JSON format
def is_valid_json(json_string):
    """
    Checks if the input string is a valid JSON array of MCQ dictionaries.

    Args:
        json_string (str): JSON string to validate

    Returns:
        bool: True if valid, else False
    """

    logging.info("Validating JSON string.")
    try:
        data = json.loads(json_string)

        # Check if top-level is a list
        if not isinstance(data, list) or len(data) == 0:
            logging.warning("JSON is not a list or is empty.")
            return False

        for item in data:
            if not isinstance(item, dict):
                logging.warning("Item in JSON is not a dictionary.")
                return False
            if not all(key in item for key in ("question", "options", "answer")):
                logging.warning("Required keys missing in item: %s", item)
                return False
            if not isinstance(item["options"], list):
                logging.warning("Options field is not a list.")
                return False
        logging.info("JSON validation successful.")
        return True
    except json.JSONDecodeError as e:
        logging.error("JSONDecodeError: Failed to parse JSON string. Error: %s", str(e))
        return False
    except Exception as e:
        logging.error("Unexpected error during JSON validation: %s", str(e))
        return False