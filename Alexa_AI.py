
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from google import genai

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alexa AI Assistant</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0; min-height: 100vh; padding: 20px;
    display: grid; place-items: center;
    font-family: Arial, sans-serif; color: #f8fafc;
    background: linear-gradient(135deg, #08111f, #123451);
}
.app {
    width: 100%; max-width: 760px; height: 90vh;
    min-height: 520px; display: flex; flex-direction: column;
    overflow: hidden; border: 1px solid #34516a;
    border-radius: 24px; background: #122235;
    box-shadow: 0 24px 70px #0006;
}
header { text-align: center; padding: 22px; background: #172d43; }
.orb {
    height: 66px; width: 66px; margin: 0 auto 10px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #c4fbff, #20b9e8 45%, #3157c8 75%);
    box-shadow: 0 0 28px #21b9e866;
}
h1 { margin: 5px; font-size: 25px; }
header p { margin: 6px; color: #b9cbd9; }
#chat {
    flex: 1; overflow-y: auto; padding: 20px;
    display: flex; flex-direction: column; gap: 12px;
}
.msg {
    max-width: 86%; padding: 12px 15px;
    border-radius: 16px; line-height: 1.5;
    white-space: pre-wrap; overflow-wrap: anywhere;
}
.bot { align-self: flex-start; background: #263d52; }
.user { align-self: flex-end; background: #1269b3; }
.controls { padding: 15px; background: #172d43; }
form { display: flex; gap: 9px; }
input {
    min-width: 0; flex: 1; border: 1px solid #506b80;
    border-radius: 12px; padding: 13px;
    background: #0d1b2a; color: white; font-size: 16px;
}
button {
    border: 0; border-radius: 12px; padding: 12px 16px;
    background: #21c1e8; color: #062438;
    font-weight: bold; cursor: pointer;
}
button:disabled { opacity: .55; cursor: wait; }
.actions {
    display: flex; justify-content: center;
    gap: 10px; margin-top: 11px; flex-wrap: wrap;
}
.actions button { background: #314b62; color: white; }
#status { text-align: center; font-size: 13px; color: #a9c4d8; margin-top: 10px; }
@media(max-width: 520px) {
    body { padding: 0; }
    .app { height: 100vh; min-height: 0; border-radius: 0; }
    header { padding: 16px; }
    #chat { padding: 13px; }
}
</style>
</head>
<body>
<main class="app">
<header>
    <div class="orb"></div>
    <h1>Alexa AI</h1>
    <p>Your personal AI voice assistant</p>
</header>

<section id="chat" aria-live="polite">
    <div class="msg bot">Hello! I'm Alexa AI. Type a question or tap Speak to talk to me.</div>
</section>

<section class="controls">
    <form id="chatForm">
        <input id="question" placeholder="Ask Alexa anything..." autocomplete="off" required>
        <button id="send" type="submit">Send</button>
    </form>
    <div class="actions">
        <button id="mic" type="button">🎙 Speak</button>
        <button id="stop" type="button">🔇 Stop speaking</button>
        <button id="clear" type="button">Clear chat</button>
    </div>
    <div id="status">Ready to help</div>
</section>
</main>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("question");
const statusBox = document.getElementById("status");
const sendButton = document.getElementById("send");

function addMessage(text, role) {
    const item = document.createElement("div");
    item.className = "msg " + role;
    item.textContent = text;
    chat.appendChild(item);
    chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-IN";
    utterance.rate = 1;
    window.speechSynthesis.speak(utterance);
}

async function ask(question) {
    question = question.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";
    sendButton.disabled = true;
    statusBox.textContent = "Alexa is thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({question})
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Request failed");

        addMessage(data.answer, "bot");
        speak(data.answer);
        statusBox.textContent = "Ready to help";
    } catch (error) {
        addMessage(error.message, "bot");
        statusBox.textContent = "Request failed";
    } finally {
        sendButton.disabled = false;
        input.focus();
    }
}

document.getElementById("chatForm").addEventListener("submit", event => {
    event.preventDefault();
    ask(input.value);
});

document.getElementById("stop").addEventListener("click", () => {
    window.speechSynthesis.cancel();
    statusBox.textContent = "Speech stopped";
});

document.getElementById("clear").addEventListener("click", () => {
    chat.replaceChildren();
    window.speechSynthesis.cancel();
    statusBox.textContent = "Chat cleared";
});

document.getElementById("mic").addEventListener("click", () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        statusBox.textContent = "Voice input is not supported. Try Chrome or type your question.";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => statusBox.textContent = "Listening...";
    recognition.onresult = event => {
        input.value = event.results[0][0].transcript;
        ask(input.value);
    };
    recognition.onerror = event => statusBox.textContent = "Microphone error: " + event.error;
    recognition.onend = () => {
        if (statusBox.textContent === "Listening...") {
            statusBox.textContent = "Ready to help";
        }
    };

    recognition.start();
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    if client is None:
        return jsonify({
            "error": "GEMINI_API_KEY is missing. Check your .env file."
        }), 500

    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()[:4000]

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    # Handle simple commands locally
    lower = question.lower()

    if "time" in lower and len(lower) < 100:
        return jsonify({
            "answer": "The time is " + datetime.now().strftime("%I:%M %p")
        })

    if ("date" in lower or "what day" in lower) and len(lower) < 100:
        return jsonify({
            "answer": "Today is " + datetime.now().strftime("%A, %d %B %Y")
        })

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=(
                "You are Alexa AI, a friendly voice assistant. "
                "Answer clearly and naturally in a few sentences. "
                "User question: " + question
            )
        )

        return jsonify({
            "answer": response.text or "Sorry, I couldn't generate an answer."
        })

    except Exception as error:
        print("Gemini API error:", repr(error))
        return jsonify({
            "error": "AI service unavailable. Check the terminal and try again."
        }), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
