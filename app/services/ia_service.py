from google import genai
import json
from app.core.config import settings
from app.schemas.post import PostCreate
from app.schemas.image import ImageCreate
from app.services.image_service import generar_imagen_pollinations

client = genai.Client(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """
Tu tarea es generar un artículo de blog profesional con:

1. MÍNIMO 3 párrafos extensos.
2. EXACTAMENTE 3 prompts para imágenes relevantes.
3. Devuelve JSON ESTRICTO:

{
 "title": "...",
 "body": "...",
 "seo_description": "...",
 "image_prompts": ["...", "...", "..."]
}
"""

def generate_blog_post(prompt: str, base_url: str) -> PostCreate:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[SYSTEM_PROMPT, f"Prompt del usuario: {prompt}"],
        config={"response_mime_type": "application/json"}
    )

    data = json.loads(response.text)

    prompts = data.get("image_prompts") or []

    images = []
    for p in prompts:
        filename = generar_imagen_pollinations(p)
        if filename:
            images.append(
                ImageCreate(url=f"{base_url}/static/images/{filename}")
            )

    return PostCreate(
        title=data["title"],
        body=data["body"],
        seo_description=data.get("seo_description"),
        images=images
    )
