import random

# --- Vastu Rules Dataset (English + Hindi) ---
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

# --- Memory ---
user_house = {}
last_followup = None

def detect_language(message):
    """Simple detection: if Hindi keywords present, return 'hi', else 'en'"""
    hindi_keywords = ["namaste", "नमस्ते", "हाँ", "नहीं", "रसोईघर", "शयनकक्ष"]
    for word in hindi_keywords:
        if word.lower() in message.lower():
            return "hi"
    return "en"

def vastu_chat():
    global last_followup
    print("🪔 Welcome to AI Vastu Expert Chatbot 🪔")
    print("Type 'exit' to quit.\n")
    
    while True:
        message = input("You: ").strip()
        if message.lower() == "exit":
            print("🙏 Thank you! Goodbye!\n🙏 धन्यवाद! अलविदा!")
            break
        
        lang = detect_language(message)
        response = ""
        
        # Greeting handling
        if "namaste" in message.lower() or "नमस्ते" in message:
            if lang == "hi":
                response = "🙏 नमस्ते! मैं आपका वास्तु सलाहकार हूँ।"
            else:
                response = "🙏 Namaste! I am your Vastu consultant."
            print("Bot:", response, "\n")
            continue
        
        # Room + direction detection
        tokens = message.lower().split()
        room = None
        direction = None
        for r in vastu_rules.keys():
            if r in tokens or (lang=="hi" and ("रसोईघर" in message and r=="kitchen")) or (lang=="hi" and ("शयनकक्ष" in message and r=="bedroom")):
                room = r
        for d in ["north","south","east","west","southeast","southwest","northeast","northwest"]:
            if d in tokens:
                direction = d.capitalize()
        
        if room and direction:
            user_house[room] = direction
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
                response = "कृपया अपना कमरा और उसकी दिशा बताएं (जैसे: 'मेरा रसोईघर दक्षिण-पूर्व में है')."
            else:
                response = "Please tell me your room and its direction (e.g., 'My kitchen is in Southeast')."
        
        print("Bot:", response, "\n")

if __name__ == "__main__":
    vastu_chat()