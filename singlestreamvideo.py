import cv2


class SingleStreamVideo:
    def __init__(self, filepath: str):
        self.video_source = filepath
        self.cam, self.height, self.width, self.frame_rate = self.open_reset_video()

    def open_reset_video(self):
        cam = cv2.VideoCapture(self.video_source)
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_rate = cam.get(cv2.CAP_PROP_FPS)
        return cam, height, width, frame_rate

    def get_frame(self):
        ret, frame = self.cam.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None
