# save this as `gemini_image_gen.py`

import base64
from io import BytesIO
from typing import Optional

from google import genai
from google.genai import types
from PIL import Image

# Configure once globally (avoid putting API key in code if sharing)


def generate_image_from_prompt(
    prompt: str, filename: Optional[str] = "gemini_image.png"
):
    """
    Generates an image using Gemini image model based on the given prompt.

    Args:
        prompt (str): Description of the image to generate.
        filename (Optional[str]): Name of the file to save the image (default: "gemini_image.png").

    Returns:
        str: Path to the saved image if successful, or None if no image was returned.
    """
    client = genai.Client(api_key="")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )

        for part in response.candidates[0].content.parts:
            if part.text:
                print("[INFO]", part.text)
            elif part.inline_data:
                image = Image.open(BytesIO(part.inline_data.data))
                if filename:
                    image.save(filename)
                    print(f"[✔] Image saved as {filename}")
                image.show()
                return filename
    except Exception as e:
        print(f"[ERROR] {e}")

    return None


if __name__ == "__main__":
    generate_image_from_prompt("a cat drinking tea with a tophat", "cat.png")
