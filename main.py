import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk


class Video:
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
            return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return None


class VideoApp:
    def __init__(self, window, window_title, video_source):
        self.delay = None
        self.photo = None
        self.window = window
        self.window.title(window_title)

        self.video = Video(video_source)

        self.collection = []

        self.playing = False  # Flag to control playback
        self.last_time_stamp = time.time()

        self.canvas = tk.Canvas(window, width=self.video.width, height=self.video.height)
        self.canvas.pack()

        self.btn_play = tk.Button(window, text="Play", width=50, command=self.play_video)
        self.btn_play.pack(anchor=tk.CENTER, expand=True)

        # Ensure the main event loop is initiated
        self.window.mainloop()

    def play_video(self):
        if not self.playing:
            self.playing = True
            self.update()  # Start the video update loop
            self.btn_play.config(text="Pause")
        else:
            self.playing = False
            self.btn_play.config(text="Play")

    def update(self):
        if self.playing:
            frame = self.video.get_frame()

            if frame is None:
                self.playing = False
                return

            self.photo = ImageTk.PhotoImage(image=frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # Calculate or set a default delay
            delay_seconds = 1 / self.video.frame_rate - (time.time() - self.last_time_stamp)
            delay_seconds = delay_seconds if delay_seconds > 0 else 0
            self.delay = int(delay_seconds * 1000)
            self.window.after(self.delay, self.update)
            self.last_time_stamp = time.time()


# Create a window and pass it to the video app
root = tk.Tk()
app = VideoApp(root, "Python Video Player", "video.mp4")
