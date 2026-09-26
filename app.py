import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured in .env")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.1-flash-lite"


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]},
                {"role": "user", "parts": [{"text": message}]},
            ],
        )
        reply = response.text or "I couldn't generate a response right now."
        return jsonify({"reply": reply})
    except Exception:
        return jsonify({
            "error": "Sorry, I couldn't process your request right now."
        }), 500


if __name__ == "__main__":
    app.run()
