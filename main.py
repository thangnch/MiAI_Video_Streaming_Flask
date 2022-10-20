from flask import Flask, render_template, Response
from webcam import Webcam
from YOLO import YoloDetect
app = Flask(__name__)

webcam = Webcam()
yolo = YoloDetect()

@app.route("/")
def index():
    return render_template("index.html")

def read_from_webcam():
    while True:
        # Đọc ảnh từ class Webcam
        image = next(webcam.get_frame())

        # Nhận diện qua model YOLO
        image = yolo.detect(image)

        # Trả về cho web bằng lệnh yeild
        yield b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n--frame\r\n'


@app.route("/image_feed")
def image_feed():
    return Response( read_from_webcam(), mimetype="multipart/x-mixed-replace; boundary=frame" )

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False)