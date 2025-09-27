import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
print("🔑 GEMINI_API_KEY loaded:", os.getenv("GEMINI_API_KEY") is not None)

# Flask app with templates/static folders
app = Flask(__name__, template_folder="templates", static_folder="static")

# In-memory chat history
chat_history = []

def get_ai_response(user_query):
    global chat_history

    chat_history.append({"role": "user", "content": user_query})

    conversation = ""
    for msg in chat_history:
        if msg["role"] == "user":
            conversation += f"User: {msg['content']}\n"
        else:
            conversation += f"Bot: {msg['content']}\n"

    prompt = f"""
    You are a **college admission assistant**.

    Rules:
    - Always reply with a structured **HTML table** when asked about colleges:
      <table border="1" cellspacing="0" cellpadding="5">
        <tr>
          <th>College / University</th>
          <th>Type</th>
          <th>Approx Fees</th>
          <th>Highlights</th>
          <th>Placement / Notes</th>
        </tr>
        ...
      </table>

    - Include at least 5-6 colleges.
    - If the user asks for "top colleges with 4+ rating", interpret as well-known colleges.
    - If not about colleges, reply:
      "⚠️ I can only help with college-related queries like MCA, B.Tech, MBA admissions, etc."

    Conversation so far:
    {conversation}

    Latest question: {user_query}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    bot_reply = response.text if response.text else "⚠️ Sorry, I couldn’t understand that."

    chat_history.append({"role": "bot", "content": bot_reply})
    return bot_reply

# Serve index.html from templates folder
@app.route("/")
def serve_index():
    return render_template("index.html")

# Chat API
@app.route("/get", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("message") if data else None

    if not user_query:
        return jsonify({"response": "⚠️ Please enter a message."})

    return jsonify({"response": get_ai_response(user_query)})

if __name__ == "__main__":
    app.run(debug=True)
