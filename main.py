from llama_cpp import Llama

print("Loading Kernel into memory...")

# Initialize the model with verbose=False to clear the terminal screen
llm = Llama(
    model_path="./qwen2.5-0.5b-instruct-q4_k_m.gguf",
    n_ctx=2048,     # Context window size
    verbose=False   # Suppresses the massive technical system logs
)

print("\nKernel is online! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("\nShutting down Kernel. Goodbye!")
        break
        
    # Format the prompt using Qwen's specific ChatML tags
    prompt = f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
    
    # Generate the AI response
    output = llm(
        prompt,
        max_tokens=512,
        stop=["<|im_end|>"],
        echo=False
    )
    
    # Extract and clean the text response from the output data dictionary
    response = output["choices"][0]["text"].strip()
    print(f"Kernel: {response}\n")
