#app.py
#data Controller

from flask import Flask, render_template, request
from models import newFile, responseInterpreter, imageList, deletePhoto
from os.path import splitext

#create Flask app instance
app = Flask(__name__, static_url_path='/static')

#Debug mode on
app.debug = False

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 

@app.errorhandler(404) 
def not_found(e):
	return render_template("404.html") 

@app.errorhandler(413) 
def exceeds(e):
	return render_template("413.html") 

@app.route("/", methods=["POST", "GET"])
def index():
	args = {"method": "GET"}
	if request.method == "POST":
		if request.files and "file" in request.files and request.files["file"]:
			imageFile = request.files["file"]
			imageFileName = request.form.get("fileName") if request.form.get("fileName") else splitext(imageFile.filename)[0]
			imageFileExtension = splitext(imageFile.filename)[1]
			imageFileName = imageFileName + imageFileExtension
			newImageObject = newFile(imageFile, imageFileName)
			responseCode = newImageObject.checkAndUpload()
			del newImageObject
			responseInterpreterInstance = responseInterpreter(responseCode)
			args["responseMessage"] = responseInterpreterInstance.getResponseMessage()
			del responseInterpreterInstance
		if request.form and "delete" in request.form and request.form["delete"]:
			deletePhotoInstance = deletePhoto(request.form["delete"])
			responseCode = deletePhotoInstance.deletePhoto()
			del deletePhotoInstance
			responseInterpreterInstance = responseInterpreter(responseCode)
			args["responseMessage"] = responseInterpreterInstance.getResponseMessage()
			del responseInterpreterInstance			
	imageListInsance = imageList()
	imagesList = imageListInsance.getList()
	if "errorCode" in imagesList[0] and imagesList[0]["errorCode"] == 3:
		responseInterpreterInstance = responseInterpreter(imagesList[0]["errorCode"])
		imagesList[0]["errorMessage"] = responseInterpreterInstance.getResponseMessage()
		del responseInterpreterInstance
	args["imagesList"] = imagesList
	return render_template(
		'index.html',
		args=args
		)
		
@app.route("/readme")
def readme():
	return render_template(
		'instructions.html'
		)

if __name__ == "__main__":
	app.run()
