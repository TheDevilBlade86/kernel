from huggingface_hub import hf_hub_download

print("Downloading model... This may take a few minutes.")
model_path = hf_hub_download(
    repo_id="MaziyarPanahi/Meta-Llama-3-8B-Instruct-GGUF",
    filename="Meta-Llama-3-8B-Instruct.Q4_K_M.gguf",
    local_dir="."
)
print(f"Model downloaded successfully to: {model_path}")
