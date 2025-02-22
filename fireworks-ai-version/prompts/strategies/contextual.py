def contextual_prompt(context, user_input):
    prompt = f"Context: {context}\n"
    prompt += f"Now, answer the following question:\n{user_input}"
    return prompt