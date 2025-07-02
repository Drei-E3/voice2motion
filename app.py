from input_layer.intent_filter import is_robot_relevant_command
from middleware.pipeline import run_middleware
from utils.env_loader import load_environment

class DummyLLM:
    def generate(self, prompt):
        return """{
            \"step 1\": {"motion": "fetch", "object": "handy", "start point": {"x": 0, "y": 0, "z": 0}, "end point": null, "explanation": "Fetch 'handy'.", "action": "act"},
            \"step 2\": {"motion": "move", "object": "handy", "start point": {"x": 0, "y": 0, "z": 0}, "end point": {"x": -5, "y": -5, "z": -5}, "explanation": "Move to fruit.", "action": "act"}
        }"""

if __name__ == "__main__":
    user_input = "Can you move the handy next to the fruit?"

    if not is_robot_relevant_command(user_input):
        print({"status": "ignored", "reason": "Command not intended for robotic arm."})
    else:
        env = load_environment()
        result = run_middleware(user_input, env, llm_model=DummyLLM())
        print(result)