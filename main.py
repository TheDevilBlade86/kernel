from llama_cpp import Llama

print("Loading Kernel into memory...")
# Initialize the model (adjust repo path if name changes)
llm = Llama(
    model_path="./Meta-Llama-3-8B-Instruct.Q4_K_M.gguf",
    n_ctx=2048,  # Context window size
)

print("\nKernel is online! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
        
    # Format the prompt for an AI assistant
    prompt = f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
    
    # Generate response
    output = llm(
        prompt,
        max_tokens=512,
        stop=["<|im_end|>"],
        echo=False
    )
    
    response = output["choices"][0]["text"].strip()
    print(f"Kernel: {response}\n")
