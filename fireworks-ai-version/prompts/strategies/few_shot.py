def few_shot_prompt(examples, user_input):
    prompt = "Here are some examples:\n"
    for example in examples:
        prompt += f"Example: {example['input']} Answer: {example['output']}."
    prompt += f"Now, answer the following question:\n{user_input}"
    return prompt