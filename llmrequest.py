import base64

import cv2
from openai import OpenAI

# Sign detection
# DEFAULT_INSTRUCTION = """
# You are a driving assistant. You receive frontal image as input
# and output only the sign names that affects ego vehicle. Your
# output is very short, precise and strict. If there are no signs,
# you output 'BLANK'. The country of driving - Slovenia. Speed limit
# sings are of most importance - make sure to correctly determine those.
# """.strip()

# Lane detection
DEFAULT_INSTRUCTION = """
You are a system that detects a road layout based on the dash cam image.
You output an array of 6 values like this: "[0, 0, 1, 1, 1, 0]". This array
shows that there is one lane in opposite direction to the ego vehicle and two
lanes in the forward direction. First three values represent the presence of the 
opposite lane, when the third values - is the closest opposite lane to centerline.
Last three values represent the presence of lanes in direction of ego vehicle, where
the fourth value of the array is the closes lane to centerline. You output only array.
If you are not sure, about the lane presence, put 'x' in that lane position. Few more examples:
"[0, 0, 0, 1, 0, 0]" - one-way road;
"[0, 0, 1, 1, 0, 0]" - simple two-way, one lane each direction;
"[0, 1, 1, 1, 1, 0]" - four lane two-way road, two lanes each direction;
"[x, 1, 1, 1, 1, x]" - four lane two-way road, two lanes each direction, but you not sure about the lanes on the edge;
If something is wrong, you output "[x, x, x, x, x, x]". You do not speak language, only output 6 values array.
Lane - is considered to present if there is a lane that a vehicle can and may drive on it. Sidewalks, bike lanes, rails
do not count as lanes and there should labeled as 0.
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
