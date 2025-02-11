from llama_cpp import Llama

deepseek = Llama(
    model_path=r'C:\Users\hp\.lmstudio\models\lmstudio-community\DeepSeek-R1-Distill-Qwen-7B-GGUF\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf'
)

async def prompt_deepseek(prompt: str):
    output = deepseek.create_completion(
        prompt=prompt,
        max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
        stop=["\n"], # Stop generating just before the model would generate a new question
        echo=True)
    response = ((output['choices'])[0])['text']
    return response