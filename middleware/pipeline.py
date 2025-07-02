import json
from input_layer.intent_filter import is_robot_relevant_command


def parse_and_clean_command(input_text):
    return {
        "action": "move",
        "source": "handy",
        "target": "fruit",
        "context": "avoid collision"
    }


def match_objects(parsed, env):
    matched = []
    for obj_id, obj in env.items():
        if parsed["source"] in obj["name"] or parsed["target"] in obj["name"]:
            matched.append(obj)
    return matched


def build_prompt(command, matched_objects, env):
    return f"""
You are a robotic arm control assistant. Based on the following environment and user instruction, generate a plan.

Environment: {json.dumps(env)}
Instruction: {command}
Output format must be Output.json style.
"""


def call_llm(prompt, model):
    # Placeholder for LLM call
    return model.generate(prompt)  # Assume a .generate() method for simplicity


def parse_llm_output_to_plan(text):
    try:
        json_part = text[text.index('{'):text.rindex('}')+1]
        return json.loads(json_part)
    except:
        return {"error": "Could not parse LLM output as JSON"}


def run_middleware(input_text, env_json, llm_model):
    parsed_command = parse_and_clean_command(input_text)
    matched_objects = match_objects(parsed_command, env_json)

    if not matched_objects:
        return {"status": "fail", "reason": "No relevant objects matched in environment."}

    prompt = build_prompt(parsed_command, matched_objects, env_json)
    llm_output = call_llm(prompt, llm_model)

    if "low confidence" in llm_output.lower():
        return {"status": "uncertain", "reason": "LLM uncertain. Please clarify."}
    elif "unfeasible" in llm_output.lower():
        return {"status": "rejected", "reason": "Command not feasible. Awaiting confirmation."}

    plan = parse_llm_output_to_plan(llm_output)
    return {"status": "success", "plan": plan}
