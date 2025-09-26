import os
from PIL import Image
from io import BytesIO
import requests
from urllib.parse import quote
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

def generate_image(attributes: str, primary_object: str, context: str, style_notes: str):
    final_prompt = f"Create an image of a {attributes} {primary_object} {context}. "
    if style_notes:
        final_prompt += f"Style: {style_notes}. "

    enhanced_prompt = (
        f"{final_prompt}, "
        "high resolution, highly detailed, sharp focus, "
        "professional photography, cinematic lighting, "
        "8k uhd, ray tracing, ambient lighting"
    )

    negative_prompt = (
        "blurry, low quality, low resolution, "
        "watermark, signature, oversaturated, "
        "distorted, deformed, pixelated"
    )

    base_url = "https://image.pollinations.ai/prompt"
    encoded_prompt = quote(enhanced_prompt)
    url = f"{base_url}/{encoded_prompt}"

    params = {
        "width": 1024,
        "height": 1024,
        "model": "flux-pro",
        "sampler": "DPM++ SDE Karras",
        "enhance": True,
        "nologo": True,
        "negative_prompt": negative_prompt,
        "upscale": True,
        "upscale_amount": "2",
    }

    try:
        response = requests.get(url, params=params, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


