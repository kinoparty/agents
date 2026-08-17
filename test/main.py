import os
from flask import Flask, request
import telebot
from google import genai
from google.genai import types

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GOOGLE_CLOUD_API_KEY = os.environ.get("GOOGLE_CLOUD_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

client = genai.Client(vertexai=True, api_key=GOOGLE_CLOUD_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(message.text)]
            )
        ]
        
        tools = [
            types.Tool(google_search=types.GoogleSearch()),
        ]
        
        tool_config = types.ToolConfig(
            retrieval_config=types.RetrievalConfig(),
        )
        
        generate_content_config = types.GenerateContentConfig(
            max_output_tokens=65535,
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
            ],
            tools=tools,
            tool_config=tool_config,
        )
        
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model="gemini-3.7-flash",
            contents=contents,
            config=generate_content_config,
        ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
            response_text += chunk.text

        bot.reply_to(message, response_text if response_text else "...")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'Invalid request', 403

@app.route("/", methods=["GET"])
def index():
    return "Agent Connector is running.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
