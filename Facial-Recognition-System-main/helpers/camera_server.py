import time
import cv2
import threading
import contants as CONSTANTS
from flask import Flask, render_template, Response, request

app = Flask(__name__)

video_stream = None


@app.route('/')
def index():
    return "this server is running"

#serve video
@app.route('/video')
def video_feed():
    return Response(video_stream.generate_frames_for_web(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/speak', methods=['POST', 'GET'])
# def speak_now():
#     return speak.speak(request)




class VideoStream:
    def __init__(self):
        self.lock = threading.Lock()
        self.active_clients = 0
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

    def __del__(self):
        if self.cap is not None:
            self.cap.release()

    # def start_camera(self):
    #     if self.cap is None or not self.cap.isOpened():
    #         self.cap = cv2.VideoCapture(0)
    #         self.cap.set(3, 640)
    #         self.cap.set(4, 480)
    #         print("Camera started.")

    # def stop_camera(self):
    #     if self.cap is not None and self.cap.isOpened():
    #         self.cap.release()
    #         # self.cap = None
    #         print("Camera stopped.")

    def get_frame(self):
        with self.lock:
            ret, frame = self.cap.read()
            if not ret:
                return None
            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()

    def generate_frames_for_web(self):
        with self.lock:
            self.active_clients += 1
            if self.active_clients == 1:
                # self.start_camera()
                pass
        
        try:
            while True:
                frame = self.get_frame()
                if frame is None:
                    break
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        finally:
            with self.lock:
                self.active_clients -= 1
                if self.active_clients == 0:
                    self.cap.release()
                    self.cap = cv2.VideoCapture(0)
                    self.cap.set(3, 640)
                    self.cap.set(4, 480)


        


def run(host=CONSTANTS.CAM_SERVER_HOST, port = CONSTANTS.CAM_SERVER_PORT):
    global video_stream
    video_stream = VideoStream()
    app.run(debug=False, host= host, port = port)



if __name__ == '__main__':
    run()
    # host='127.0.0.1'
    # port = 5000
    # video_stream = VideoStream()
    # app.run(debug=True, host= host, port = port)
