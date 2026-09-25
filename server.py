import os
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from llama_cpp import Llama

app = Flask(__name__)

# Route to serve the local logo asset to the front-end cleanly
@app.route('/logo.png')
def serve_logo():
    return send_from_directory(os.getcwd(), 'logo.png')

print("Loading Kernel Engine...")
llm = Llama(
    model_path="./qwen2.5-0.5b-instruct-q4_k_m.gguf",
    n_ctx=2048,
    verbose=False
)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kernel AI Console</title>
    <style>
        body {
            background-color: #0B0A08;
            color: #E6E1DA;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* 💾 Left Sidebar Navigation Menu */
        .sidebar {
            width: 260px;
            background-color: #141311;
            border-right: 1px solid #22201C;
            display: flex;
            flex-direction: column;
            padding: 5rem 1rem 1rem 1rem;
            box-sizing: border-box;
        }

        .new-chat-btn {
            background-color: #1F1D19;
            color: #E6E1DA;
            border: 1px solid #2F2C26;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            transition: background 0.2s;
        }

        .new-chat-btn:hover { background-color: #2B2822; }

        /* 🏷️ Top-Left Floating Branding Header (With Curved Image Custom Fixes) */
        .brand-header {
            position: absolute;
            top: 1rem;
            left: 1rem;
            z-index: 10;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.25rem;
            font-weight: 600;
            color: #F5F2EB;
        }

        /* Enforces a perfect circle on the logo asset to hide raw edges */
        .brand-logo-img {
            width: 32px;
            height: 32px;
            object-fit: cover;
            border-radius: 50%; 
            border: 1px solid #2F2C26;
        }

        /* 🎛️ Top-Right Modern Functional Menu Action Button Trigger */
        .top-right-menu {
            position: absolute;
            top: 1rem;
            right: 1.5rem;
            z-index: 10;
            background: transparent;
            border: none;
            color: #8C857B;
            font-size: 1.5rem;
            cursor: pointer;
            transition: color 0.2s;
            padding: 0.5rem;
        }

        .top-right-menu:hover {
            color: #F5F2EB;
        }

        /* 🖥️ Workstage Viewport Canvas */
        .main-workspace {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 2rem;
            box-sizing: border-box;
            position: relative;
        }

        .greeting-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            flex: 1;
            text-align: center;
        }

        .greeting-text {
            font-size: 2.5rem;
            font-weight: 500;
            color: #F5F2EB;
            margin: 0;
            letter-spacing: -0.02em;
        }

        .chat-stream {
            width: 100%;
            max-width: 720px;
            flex: 1;
            overflow-y: auto;
            padding: 2rem 0;
            display: none;
            flex-direction: column;
            gap: 1.5rem;
        }

        .msg {
            padding: 1rem 1.25rem;
            border-radius: 12px;
            line-height: 1.6;
            max-width: 85%;
        }

        .user-msg {
            background-color: #1F1D19;
            border: 1px solid #2F2C26;
            align-self: flex-end;
            color: #F5F2EB;
        }

        .assistant-msg {
            background-color: transparent;
            align-self: flex-start;
            color: #E6E1DA;
            padding-left: 0;
        }

        /* 💬 Claude-Style Input Tray Navigation Layout */
        .input-tray {
            width: 100%;
            max-width: 720px;
            background-color: #141311;
            border: 1px solid #22201C;
            border-radius: 16px;
            padding: 1rem 1.2rem;
            box-sizing: border-box;
        }

        .chat-input {
            width: 100%;
            background: transparent;
            border: none;
            color: #F5F2EB;
            font-size: 1.05rem;
            outline: none;
        }

        /* 🌀 Animated Pulse Loading Sequence Dots */
        .loading-dots {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 1rem 0;
            align-self: flex-start;
        }

        .dot {
            width: 8px;
            height: 8px;
            background-color: #8C857B;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out both;
        }

        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1.0); }
        }
    </style>
</head>
<body>

    <!-- Upper Boundary Brand Matrix -->
    <div class="brand-header">
        <img src="/logo.png" class="brand-logo-img" alt="Kernel Logo">
        <span>Kernel</span>
    </div>

    <!-- ⚙️ Top Right Clean Menu Overlay Trigger Button -->
    <button class="top-right-menu" onclick="alert('Menu options: Profile, Settings, Key Configurations coming soon!')">⋮</button>

    <div class="sidebar">
        <button class="new-chat-btn" onclick="resetChat()">+ New Chat</button>
    </div>

    <div class="main-workspace">
        <div class="greeting-container" id="greetingCanvas">
            <h2 class="greeting-text">You're here!</h2>
        </div>

        <div class="chat-stream" id="chatArea"></div>

        <div class="input-tray">
            <input type="text" class="chat-input" id="userInput" placeholder="How can Kernel help you today?" onkeydown="if(event.key === 'Enter') sendMessage()">
        </div>
    </div>

    <script>
        function resetChat() {
            document.getElementById('chatArea').innerHTML = '';
            document.getElementById('chatArea').style.display = 'none';
            document.getElementById('greetingCanvas').style.display = 'flex';
        }

        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const chatArea = document.getElementById('chatArea');
            const greetingCanvas = document.getElementById('greetingCanvas');
            const query = inputField.value.trim();
            if (!query) return;

            greetingCanvas.style.display = 'none';
            chatArea.style.display = 'flex';

            // 1. Add User query text block
            chatArea.innerHTML += `<div class="msg user-msg">${query}</div>`;
            inputField.value = '';
            
            // 2. Inject the Animated Typing Loader Component placeholder
            const loaderId = 'loader_' + Date.now();
            chatArea.innerHTML += `
                <div class="loading-dots" id="${loaderId}">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            `;
            chatArea.scrollTop = chatArea.scrollHeight;

            // 3. Request inference back-end data pipelines 
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: query })
            });
            const data = await response.json();

            // 4. Tear down active animated indicator and display clean response strings
            document.getElementById(loaderId).remove();
            chatArea.innerHTML += `<div class="msg assistant-msg">${data.response}</div>`;
            chatArea.scrollTop = chatArea.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    system_instruction = (
        "You are Kernel, a high-performance local AI companion built entirely by jisha. "
        "Keep your responses sharp, helpful, direct, and completely devoid of generic corporate AI disclaimers."
    )
    prompt = f"<|im_start|>system\n{system_instruction}<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
    output = llm(prompt, max_tokens=512, stop=["<|im_end|>"], echo=False)
    response = output["choices"][0]["text"].strip()
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
