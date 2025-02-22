def chain_of_thought_prompt(user_input):
    prompt = (
        "Think about the following question one step at a time:\n"
        f"{user_input}\n"
        "“Break down your reasoning and provide an answer."
    )
    return prompt