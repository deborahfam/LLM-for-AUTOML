def auto_refinement_prompt(initial_response):
    prompt = (
        "You have provided the following response:\n"
        f"{initial_response}\n"
        "Review this response for clarity and accuracy. Make iterative corrections to refine it."
    )
    return prompt