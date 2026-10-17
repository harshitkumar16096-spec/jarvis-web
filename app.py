
import os
from flask import Flask, request, jsonify
from google import genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://harshitkumar16096-spec.github.io"])

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "assistant": "JARVIS"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "API key not configured"}), 500

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message
        )
        return jsonify({"reply": response.text})
    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({"error": "AI request failed"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  
