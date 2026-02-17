from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)  # ✅ Allow frontend requests

# --- Vastu Rules Dataset ---
vastu_rules = {
    "kitchen": {
        "ideal": ["Southeast"],
        "remedy_en": ["Use red/yellow tones", "Place stove facing East"],
        "remedy_hi": ["लाल/पीले रंग का प्रयोग करें", "चूल्हा पूर्व दिशा की ओर रखें"]
    },
    "bedroom": {
        "ideal": ["Southwest"],
        "remedy_en": ["Keep bed head towards South", "Avoid mirrors facing bed"],
        "remedy_hi": ["बिस्तर का सिर दक्षिण दिशा में रखें", "बिस्तर के सामने दर्पण न रखें"]
    }
}

def detect_language(message):
    hindi_keywords = ["namaste", "नमस्ते", "हाँ", "नहीं", "रसोईघर", "शयनकक्ष"]
    for word in hindi_keywords:
        if word.lower() in message.lower():
            return "hi"
    return "en"

@app.route("/")
def home():
    return "🪔 AI Vastu API Running Successfully!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"response": "Please send a message"}), 400

        lang = detect_language(message)
        tokens = message.lower().split()
        room = None
        direction = None

        for r in vastu_rules.keys():
            if r in tokens:
                room = r

        for d in ["north","south","east","west","southeast","southwest","northeast","northwest"]:
            if d in tokens:
                direction = d.capitalize()

        if room and direction:
            ideal = vastu_rules[room]["ideal"]

            if direction in ideal:
                if lang == "hi":
                    response = f"✅ उत्तम! {room} {direction} दिशा में है।"
                else:
                    response = f"✅ Perfect! {room.capitalize()} in {direction} is ideal."
            else:
                if lang == "hi":
                    remedy = random.choice(vastu_rules[room]["remedy_hi"])
                    response = f"⚠️ {room} {direction} दिशा में उचित नहीं। उपाय: {remedy}"
                else:
                    remedy = random.choice(vastu_rules[room]["remedy_en"])
                    response = f"⚠️ {room.capitalize()} in {direction} is not ideal. Remedy: {remedy}"
        else:
            if lang == "hi":
                response = "कृपया अपना कमरा और उसकी दिशा बताएं."
            else:
                response = "Please tell me your room and its direction."

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
