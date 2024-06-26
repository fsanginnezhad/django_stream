# stream/consumers.py

import base64
import cv2
import numpy as np
from channels.generic.websocket import WebsocketConsumer

class VideoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        header, data = text_data.split(',', 1)
        img_data = base64.b64decode(data)
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')

        self.send(text_data=frame_data)
