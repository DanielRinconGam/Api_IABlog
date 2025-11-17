import requests, os, uuid
from fastapi import HTTPException
from urllib.parse import quote


def generar_imagen_pollinations(prompt: str) -> str:
    """
    Genera una imagen usando el endpoint estable de Pollinations.
    Guarda la imagen localmente y devuelve el nombre del archivo.
    """

    try:
        safe_prompt = quote(prompt)

        # ENDPOINT ESTABLE
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"

        response = requests.get(image_url, timeout=60)

        if response.status_code != 200:
            raise Exception(f"Error HTTP {response.status_code}")

        # Path real dentro del contenedor
        save_dir = "/app/app/static/images"
        os.makedirs(save_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.jpg"
        path = f"{save_dir}/{filename}"

        with open(path, "wb") as f:
            f.write(response.content)

        return filename

    except Exception as e:
        print("Error generando imagen:", e)
        raise HTTPException(500, f"Error al generar/guardar imagen: {e}")
