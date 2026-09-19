import requests
# import google.generativeai as genai

from app.config import settings


# ==========================================================
# LLM Provider Registry
# ==========================================================

def generate(prompt: str):

    providers = {

        "ollama": call_ollama,

        # "gemini": call_gemini,

    }

    provider = providers.get(
        settings.LLM_PROVIDER.lower()
    )

    if provider is None:

        raise Exception(

            f"Unsupported provider: {settings.LLM_PROVIDER}"

        )

    return provider(prompt)


# ==========================================================
# OLLAMA
# ==========================================================

def call_ollama(prompt: str):

    try:

        response = requests.post(

            f"{settings.OLLAMA_URL}/api/generate",

            json={

                "model": settings.OLLAMA_MODEL,

                "prompt": prompt,

                "stream": False,

            },

            timeout=120,

        )

        response.raise_for_status()

        data = response.json()

        if "response" not in data:

            raise Exception(
                "Invalid Ollama response"
            )

        return data["response"]

    except requests.exceptions.RequestException as e:

        raise Exception(

            f"Ollama Error: {str(e)}"

        )


# ==========================================================
# GEMINI
# ==========================================================

# def call_gemini(prompt: str):

#     try:

#         if not settings.GOOGLE_API_KEY:

#             raise Exception(
#                 "GOOGLE_API_KEY is missing."
#             )

#         genai.configure(
#             api_key=settings.GOOGLE_API_KEY
#         )

#         model = genai.GenerativeModel(
#             settings.GEMINI_MODEL
#         )

#         response = model.generate_content(
#             prompt
#         )

#         return response.text

#     except Exception as e:

#         raise Exception(

#             f"Gemini Error: {str(e)}"

#         )