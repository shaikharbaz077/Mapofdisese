from app import app
from flask import Flask,request,render_template,Response,redirect, url_for, escape
import requests
import json
import base64
from werkzeug import secure_filename
from .helper import read_base64_image
from .helper import gen_prediction
from .helper import gen_probabilities
import os

image_64_encode = ""
filename_src = ""
my_list = []
res=0
UPLOAD_FOLDER = 'files/imgs/'

@app.route('/')
@app.route('/index')
def index():
    return "DermAI Inference Server"

@app.route('/upload')
def upload_file2():
   return render_template('fileupload.html')

@app.route('/makeprep',methods = ['GET', 'POST'])
def makereq():

	if request.method == 'POST':
	    fs = request.files['file']
	    filename = secure_filename(fs.filename)

	    filename_path = os.path.join('/home/ubpc/Documents/kk/derm-ai-master/app/files/imgs/', filename)
	    print("--------------------------------file path is : %s" % filename_path )
	    global filename_src
	    filename_src = filename_path
	    fs.save(filename_path)

        #enconding image base64
        image = open('/home/ubpc/Documents/kk/derm-ai-master/app/files/imgs/%s' % filename, 'rb') #open binary file in read mode
        image_read = image.read()
        global image_64_encode
        image_64_encode = base64.encodestring(image_read)
        #making post request
        print("-------------request gone to post predict-------------")
        #requests.post("http://127.0.0.1:5000/predictx")
        #, data={'image':image_64_encode}
        #funcz()
        return redirect('http://127.0.0.1:5000/predict')
        #print("-------------request gone to post predict-------------")
        #print(r.status_code, r.reason)
        
        
@app.route('/predict', methods=['GET'])
def predict():
    print("-------------1-------------")
    #data = json.loads(request.data)
    #base64_str = data.get('image')
    base64_str = image_64_encode
    rgb_image = read_base64_image(base64_str)
    print("-------------2-------------")

    probas = gen_probabilities(rgb_image)
    print("-------------3-------------")
    klass, score = gen_prediction(probas)
    print("-------------4-------------")

    response = {'class': klass, 'score': score}
    print("-------------7-------------")
    response = json.dumps(response)
    print("-------------6-------------")
    print("res ------------")
    print(response)#, filename_res=filename_src
    return render_template('result.html',response=response)
    #return Response(response=response)
