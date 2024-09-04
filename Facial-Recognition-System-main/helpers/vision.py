import os
import time
from ultralytics import YOLO
import camera_server
# model = YOLO("yolov8n-cls.pt")  # pass any model type
import threading
import contants as CONSTANTS


class YoloClassification:
    def __init__(self) -> None:
        self.model = YOLO("YOLOv8n-cls.pt")  # load an official model
        self.is_server_running= False
        # self.server_host=CONSTANTS.CAM_SERVER_HOST
        # self.server_port = CONSTANTS.CAM_SERVER_PORT   #http://127.0.0.1:5000/video
        self.live_url = CONSTANTS.CAM_SERVER_URL
        self.start_server()

    def start_server(self):
        # return

        def run_server():
            os.system("python3.10 helpers/camera_server.py")
        server = threading.Thread(target=run_server)
        server.start()

        self.is_server_running = True
        print("[OK]Live camera server started!")
        

    def classify_image(self, image_path="https://ultralytics.com/images/bus.jpg", stream = False):
        results = self.model(image_path, show=True, stream=stream)
        # time.sleep(10)
        # names = results.names
        # probs = results.probs
        # orig_shape = results.orig_shape
        # speed = results.speed
        # print(probs)
        return results
    
    def classify_live(self):
        # frame = live_video_stream.stream_frames_for_direct_integration()
        # while True:
        results = self.model(self.live_url, stream=True, show=False)
        for result in results:
            result.show()


    



if __name__ == "__main__":
    yolo = YoloClassification()
    # live_video_stream = VideoStream()
    yolo.classify_live()

    # results = yolo.classify_image(live_video_stream.stream_frames_for_direct_integration(), stream=True)

    # # print("Number of results", len(results))

    # for result in results:
    #     probs = result.probs  # Probs object for classification outputs
    #     names = result.names
    #     orig_shape = result.orig_shape
    #     speed = result.speed
    #     # print(probs)
    #     result.show()  # display to screen

    # print(results)
