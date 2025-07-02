# llm/dummy_llm.py

from openai import OpenAI

# Setup client for local LLM
client = OpenAI(
    base_url="http://172.17.30.133:1234/v1",
    api_key="lm-studio"  
)

MODEL = "deepseek-r1-distill-llama-8b"

def generate_robotic_steps(user_command: str, environment_json: str) -> str:
    """
    Send a prompt to the local LLM to generate robotic movement steps based on user command and environment data.

    Parameters:
    - user_command: The natural language input from the user.
    - environment_json: The stringified content of environment.json.

    Returns:
    - A string of structured JSON-like plan for robot execution.
    """

    system_prompt = (
        "You are a Robotic Arm Controller. Your job is to convert human commands "
        "into a series of step-by-step movements, based on the environment configuration provided.\n\n"
        "## Environment:\n"
        f"{environment_json}\n\n"
        "## Command:\n"
        f"{user_command}\n\n"
        "## Instructions:\n"
        "Think step-by-step, reason through the goal, check for obstacles and generate valid JSON output "
        "with clear explanations. Follow this format:\n"
        '''{
    "step 1": {
        "start point": {"x": float, "y": float, "z": float},
        "end point": "none" | {"x": float, "y": float, "z": float},
        "motion": "fetch" | "move",
        "object": "object_name",
        "parameters": { "max_pressure": "value or unknown" },
        "explaination": "text",
        "action": "act" | "refine"
    },
    ...
}'''
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_command}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return response.choices[0].message.content.strip()
