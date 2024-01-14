from llmrequest import LLMRequest


class Description:
    def __init__(self, llm_request: LLMRequest, initial_text: str = "Will show some text here"):
        self.text = initial_text
        self.open_to_request = True
        self.llm_request = llm_request

    def update_text(self, image):
        if image is not None and self.open_to_request:
            self.open_to_request = False
            # time.sleep(2)  # Some time-consuming process here
            text = self.llm_request.make_request_to_chat(image)
            self.text = text
            self.open_to_request = True

    def show_text(self):
        return self.text
