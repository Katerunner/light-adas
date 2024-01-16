import time

from llmrequest import LLMRequest
from concurrent.futures import ThreadPoolExecutor


class Description:
    def __init__(self, llm_request: LLMRequest, initial_text: str = "Will show some text here"):
        self.text = initial_text
        self.llm_request = llm_request
        self.executor = ThreadPoolExecutor(max_workers=5)  # Persistent thread pool

    def update_text(self, image):
        if image is not None:
            future = self.executor.submit(self.llm_request.make_request_to_chat, image)
            future.add_done_callback(self._update_text_callback)

    def _update_text_callback(self, future):
        try:
            text = future.result()
            self.text = text + " " + str(time.time())
        except Exception as e:
            # Handle exceptions from the future here
            print(f"Error in processing request: {e}")

    def show_text(self):
        return self.text

    def __del__(self):
        self.executor.shutdown(wait=False)
