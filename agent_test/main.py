import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Считываем ключ
api_key = os.environ.get("GEMINI_API_KEY", "")
if api_key.startswith("AQ"):
    os.environ["GCP_CREDENTIALS"] = api_key

client = genai.Client()

@app.route('/', methods=['GET', 'POST'])
def run_agent():
    user_prompt = "Придумай одну бизнес-идею на стыке ИИ и экологии."
    if request.is_json:
        request_json = request.get_json(silent=True)
        if request_json and 'prompt' in request_json:
            user_prompt = request_json['prompt']
    elif request.args and 'prompt' in request.args:
        user_prompt = request.args.get('prompt')

    try:
        # Используем новейшую базовую модель gemini-2.0-flash
        response = client.models.generate_content(
            model='gemini-2.0-flash',
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
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Считываем ключ. Если он начинается на AQ, библиотека google-genai 
# использует его через специальную системную переменную авторизации Google
api_key = os.environ.get("GEMINI_API_KEY", "")
if api_key.startswith("AQ"):
    os.environ["GCP_CREDENTIALS"] = api_key

# Создаем чистый клиент без передачи ключа напрямую в аргументы
client = genai.Client()

@app.route('/', methods=['GET', 'POST'])
def run_agent():
    user_prompt = "Придумай одну бизнес-идею на стыке ИИ и экологии."
    if request.is_json:
        request_json = request.get_json(silent=True)
        if request_json and 'prompt' in request_json:
            user_prompt = request_json['prompt']
    elif request.args and 'prompt' in request.args:
        user_prompt = request.args.get('prompt')

    try:
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
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Считываем ваш ключ из настроек облака
api_key = os.environ.get("GEMINI_API_KEY", "")

# Если ключ корпоративный (на AQ), настраиваем облачную авторизацию
if api_key.startswith("AQ"):
    os.environ["GEMINI_API_KEY"] = api_key
    client = genai.Client()
else:
    # Иначе запускаем как обычный API ключ
    client = genai.Client(api_key=api_key)

@app.route('/', methods=['GET', 'POST'])
def run_agent():
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
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
