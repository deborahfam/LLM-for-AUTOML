def tree_of_thought_prompt(user_input):
    prompt = (
        "Consider the following question and generate multiple reasoning paths:\n"
        f"{user_input}\n"
        "Evaluate each path and select the best one based on coherence and relevance."
    )
    return prompt