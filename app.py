#from app import app
from flask import Flask,request,render_template,Response,redirect, url_for, escape
import requests
import json
import urllib2
import base64
import cStringIO
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
from werkzeug import secure_filename
from helper import read_base64_image
from helper import gen_prediction
from helper import gen_probabilities
import os

app = Flask(__name__)

image_64_encode = ""
filename_src = ""
my_list = []
res=0
UPLOAD_FOLDER = '/app/files/imgs/'

cloudinary.config( 
  cloud_name = "dx7b1x3es", 
  api_key = "336942238365418", 
  api_secret = "kLZBMLP0pJlgnTL10U0ICeLu7J4" 
)

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
	    #os.path.join

        
        cloudinary.uploader.upload(fs,folder = "uploadimgs/", public_id = filename)

	    #filename_path = os.path.abspath('/app/files/imgs/'+filename)
        print("--------------------------------file path is : %s" % filename )
        global filename_src
        #filename_src = filename_path
        #fs.save(filename_path)

        #enconding image base64
        #image = open('/app/files/imgs/%s' % filename, 'rb') #open binary file in read mode
        #image_read = ("https://res.cloudinary.com/dx7b1x3es/image/upload/v1521697833/uploadimgs/"+filename+".jpg")
        image_read =  urllib2.urlopen("https://res.cloudinary.com/dx7b1x3es/image/upload/v1521697833/uploadimgs/"+filename+".jpg").read()
      
        global image_64_encode
        #image_read
        image_64_encode = base64.encodestring(image_read)
        print("image 64 read is")
        print(image_64_encode)
        #making post request
        print("-------------request gone to post predict-------------")
        #requests.post("http://127.0.0.1:5000/predictx")
        #, data={'image':image_64_encode}
        #funcz()
        return redirect('https://skindiseasepredictionbymohmmad.herokuapp.com/predict')
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

if __name__ == "__main__":
	app.run()
