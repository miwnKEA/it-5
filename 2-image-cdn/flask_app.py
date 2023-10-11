# install modules using pip

# pip install flask flask-cors cloudinary
# pip3 install flask flask-cors cloudinary

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

CORS(app)

# insert your Cloudinary API credentials here
cloudinary.config(cloud_name = "xxx", api_key="xxx", api_secret="xxx")

# create endpoint for index page
@app.route('/', methods=['GET'])
def index():
    images = cloudinary.api.resources()
    list = []
    for i in images['resources']:
        list.append(i['url'])
    return render_template('index.html', list=list)

# create POST endpoint for uploading images to Cloudinary
@app.route("/upload", methods=['POST'])
def upload_file():
    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            return jsonify(upload_result)

# create GET endpoint to return a JSON list of all images uploaded to Cloudinary
@app.route('/images', methods=['GET'])
def get_images():
    images = cloudinary.api.resources()
    list = []
    for i in images['resources']:
        list.append(i['url'])
    return jsonify(list)

if __name__ == '__main__':
    app.run()

# print(dir(images)) 

# print(images.keys()) 

# print(images.items()) 

# print(images['resources'])