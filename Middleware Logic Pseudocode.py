"""
Middleware Logic Algorithm -- Python Pseudocode
"""
def process_user_command(user_command, environment_json, llm_model):
    """
    Step 1: Parse user command and match it with known environment objects.
    """
    matched_objects = match_objects(user_command, environment_json)

    """
    Step 2: Use LLM to perform chain-of-thought reasoning and generate procedure steps.
    """
    reasoning_output = llm_generate_procedure(
        user_command=user_command,
        objects=matched_objects,
        model=llm_model
    )

    # Evaluate the confidence level of the LLM output
    confidence = evaluate_confidence(reasoning_output)

    if confidence == "low":
        if reasoning_output.requires_more_info:
            # Step 3A: Missing information → ask the user for clarification
            question = reasoning_output.query_to_user
            user_response = ask_user(question)
            return process_user_command(user_response, environment_json, llm_model)

        elif reasoning_output.unfeasible:
            # Step 3B: Action not feasible → explain the reason and ask for confirmation
            explain_to_user(reasoning_output.reason)
            confirmation = wait_for_user_confirmation()
            if confirmation:
                return process_user_command(user_command, environment_json, llm_model)
            else:
                return {"status": "aborted", "reason": reasoning_output.reason}

        else:
            # Fallback case: Unknown error with low confidence
            return {"status": "low_confidence", "output": reasoning_output.raw}

    elif confidence == "high":
        # Step 4: Convert reasoning result into final Output JSON format
        output_json = reasoning_output.to_execution_format()
        return output_json
