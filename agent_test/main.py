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
