import json
import requests    
def generate_procedure(nl_input, matched_objects, environment):
    prompt = f"""
    Given this environment: {environment}
    And this instruction: "{nl_input}"
    And these matched objects: {matched_objects}
    Output the action plan step by step in JSON like:
    {{
        "steps": [
            {{"action": "move_to", "target": "cup1"}},
            {{"action": "grasp", "object": "cup1"}},
            {{"action": "move_to", "target": "box1"}},
            {{"action": "release", "object": "cup1"}}
        ],
        "confidence": 0.85,
        "reasoning": "...",
        "need_more_info": false
    }}
    """
    response = call_llm(prompt) 
    return json.loads(response)
