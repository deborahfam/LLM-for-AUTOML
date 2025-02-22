
firworks_ai_api_base = "https://api.fireworks.ai/inference/v1"
openai_api_base = "https://api.openai.com/v1"

MODEL_CONFIGURATIONS = {
    "Llama 3.3 70B Instruct": {
        "api_base": firworks_ai_api_base,
        "model_name": "accounts/fireworks/models/llama-3.3-70b-instruct",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    "Llama 3.1 405B Instruct": {
        "api_base": firworks_ai_api_base,
        "model_name": "accounts/fireworks/models/llama-3.1-405b-instruct",
        "temperature": 0.6,
        "max_tokens": 600,
    },
    "DeepSeek R1": {
        "api_base": firworks_ai_api_base,
        "model_name": "accounts/fireworks/models/deepseek-r1",
        "temperature": 0.5,
        "max_tokens": 700,
    },
    "DeepSeek V3": {
        "api_base": firworks_ai_api_base,
        "model_name": "accounts/fireworks/models/deepseek-v3",
        "temperature": 0.8,
        "max_tokens": 800,
    },
    "Llama 3.1 8B Instruct": {
        "api_base": firworks_ai_api_base,
        "model_name": "accounts/fireworks/models/llama-3.1-8b-instruct",
        "temperature": 0.9,
        "max_tokens": 900,
    },
    "DeepSeek R1 Distill Llama 8B": {
        "api_base": firworks_ai_api_base,
        "model_name": "accounts/fireworks/models/deepseek-r1-distill-llama-8b",
        "temperature": 0.4,
        "max_tokens": 400,
    },
}
