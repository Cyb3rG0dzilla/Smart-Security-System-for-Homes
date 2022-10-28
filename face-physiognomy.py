import os

from flask import Flask, Response, render_template, request
from utils.camera import FileUpload, VideoCamera

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/image_upload', methods=['GET', 'POST'])
def image_upload():
    image = request.files['image']
    image.save('static/created_images/image.jpg')
    f = FileUpload()
    pred = f.get_roi()
    return render_template('image_upload.html', data=pred)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port, debug = True)
