def is_robot_relevant_command(input_text, filter_model=None):
    """
    Use custom model or keyword matching to determine if command is for the robotic arm.
    """
    if filter_model:
        return filter_model.predict(input_text)  # Placeholder for custom intent model

    keywords = ["grab", "move", "pick", "place", "lift", "deliver", "transfer"]
    return any(kw in input_text.lower() for kw in keywords)