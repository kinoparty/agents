import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Авторизация в Google Cloud происходит автоматически
client = genai.Client()

@app.route('/', methods=['GET', 'POST'])
def run_agent():
    # Пытаемся получить промт из JSON-запроса, если он есть
    user_prompt = "Придумай одну бизнес-идею на стыке ИИ и экологии."
    if request.is_json:
        request_json = request.get_json(silent=True)
        if request_json and 'prompt' in request_json:
            user_prompt = request_json['prompt']
    elif request.args and 'prompt' in request.args:
        user_prompt = request.args.get('prompt')

    try:
        # Запуск модели Gemini 1.5 Flash
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction="Ты — опытный ИИ-агент. Твоя цель — давать автономные решения.",
                temperature=0.7,
            )
        )
        return jsonify({"status": "success", "agent_response": response.text}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Сервер автоматически запустится на порту, который требует Google Cloud (8080)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
import functions_framework
from google import genai
from google.genai import types

client = genai.Client()

@functions_framework.http
def run_agent(request):
    request_json = request.get_json(silent=True)
    user_prompt = "Придумай одну бизнес-идею на стыке ИИ и экологии."

    if request_json and 'prompt' in request_json:
        user_prompt = request_json['prompt']

    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction="Ты — опытный ИИ-агент. Твоя цель — давать автономные решения.",
                temperature=0.7,
            )
        )
        return {"status": "success", "agent_response": response.text}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
