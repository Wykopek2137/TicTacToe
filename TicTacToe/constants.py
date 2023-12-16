import os

class Constants():
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.IMAGE_PATH = os.path.join(base_path, "img", "chatgpt_logo.gif")
        self.AUDIO_PATH = os.path.join(base_path, "audio", "barka.mp3")
        self.ICON_PATH = os.path.join(base_path, "img", "icon_ttc.ico")
