import base64

import cv2
from openai import OpenAI

DEFAULT_INSTRUCTION = """
You are a driving assistant. You receive frontal image as input
and output only the sign names that affects ego vehicle. Your
output is very short, precise and strict. If there are no signs,
you output 'BLANK'. The country of driving - Slovenia. Speed limit
sings are of most importance - make sure to correctly determine those.
""".strip()


class LLMRequest:
    def __init__(self, model: str = "gpt-4-vision-preview", api_key: str = None, instruction=DEFAULT_INSTRUCTION):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.instruction = instruction

    @staticmethod
    def encode_image_array(image_array):
        # Ensure the image is in the correct format
        retval, buffer = cv2.imencode('.jpg', image_array)
        if retval:
            # Convert to base64 encoding and return as string
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            return image_base64
        else:
            raise ValueError("Could not encode image")

    def make_request_to_chat(self, image):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.instruction},
                    {"role": "user", "content": [
                        # {"type": "text", "text": "What’s in this image?"},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{self.encode_image_array(image)}"
                        }, }, ],
                     }],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return "Request Error Occurred"
