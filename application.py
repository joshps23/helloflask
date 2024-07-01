from flask import Flask, render_template, Response,jsonify,request,session
import random
import datetime
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import os

import cv2

# YOLO_Video is the python file which contains the code for our object detection model
#Video Detection is the Function which performs Object Detection on Input Video
from YOLO_Video import video_detection

from wtforms import FileField, SubmitField
application = Flask(__name__)
app=application
app.config['SECRET_KEY'] = 'anewflaskapp'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
  file = FileField("File",validators=[InputRequired()])
  submit = SubmitField("Run")

def generate_frames(path_x = ''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

@app.route('/')
def hello_world():
  random_number = random.randint(1, 100)
  current_year = datetime.datetime.now().year
  return render_template("index.html", num=random_number, yr=current_year)

@app.route('/anotherpage')
def get_another_page():
  return render_template("anotherpage.html")

@app.route('/videoanalysis', methods=['GET','POST'])
def get_video_analysis():
  form = UploadFileForm()
  if form.validate_on_submit():
      # Our uploaded video file path is saved here
      file = form.file.data
      file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                              secure_filename(file.filename)))  # Then save the file
      # Use session storage to save video file path
      session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                            secure_filename(file.filename))
  return render_template("videoanalysis.html", form=form)

@app.route('/video')
def video():
    #return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
  app.run(debug=True,host="0.0.0.0",port=5000)