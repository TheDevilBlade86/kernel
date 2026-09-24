# Kernel AI Chatbot 

Kernel is a local, lightweight AI chatbot powered by Python and the **Qwen-2.5-0.5B-Instruct** large language model. It runs completely offline on your local machine with zero external API dependencies.

##  How to Install and Run

### 1. Prerequisites
Make sure you have Python 3.11+ installed on your system. Windows users also require Visual Studio Community Edition with the **"Desktop development with C++"** workload to compile the llama engine.

### 2. Clone the Repository
```bash
git clone https://github.com
cd kernel
```

### 3. Install Dependencies
Install the required Python modules using pip:
```bash
pip install llama-cpp-python huggingface_hub
```

### 4. Setup the Model File
This project uses the `qwen2.5-0.5b-instruct-q4_k_m.gguf` model file. 
* Download the GGUF file from the official Qwen repository on Hugging Face.
* Place the downloaded `.gguf` file directly into the root folder of this project.

### 5. Launch the Chatbot
Run the main script to load the model into your memory and start chatting:
```bash
python main.py
```

##  Built With
* **Python** - Core language logic.
* **llama-cpp-python** - Local inference engine.
* **Qwen 2.5 0.5B** - Base language intelligence layer.
