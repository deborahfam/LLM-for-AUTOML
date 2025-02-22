def one_shot_prompt(example, user_input):
    prompt = f"Example: {example['input']}\Answer: {example['output']}\n"
    prompt += f"Now, answer the following question:\n{user_input}"
    return prompt