#models.py
#Data Model

from PIL import ImageChops, Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from glob import glob
import io
from os.path import join, splitext, basename, getsize, getmtime
from os import remove
import time

class newFile():
	def __init__(self, tempFile, tempFileName):
		self.fileToUpload = tempFile
		self.fileToUploadName = tempFileName
		self.imagesFolder = "static/data/images/"
		self.thumbnailsFolder = "static/data/thumbnails/"
		self.allowedSize = 8 * 1024 * 1024
		self.thumbnailSize = (120,120)
	def __del__(self):
		self.fileToUpload = None
		self.imagesFolder = None
		self.thumbnailsFolder = None
		self.allowedSize = None
		self.thumbnailSize = None
	
	def storeThumbnail(self):
		self.fileToUpload.stream.seek(0)
		uploadingImage = Image.open(io.BytesIO(self.fileToUpload.stream.read()))
		uploadingImage.thumbnail(self.thumbnailSize)
		uploadingImage.save(f"{self.thumbnailsFolder}thumbnail_{self.fileToUploadName}")
		uploadingImage.close()
	def uploadImage(self):
		self.fileToUpload.stream.seek(0)
		self.fileToUpload.save(f"{self.imagesFolder}{self.fileToUploadName}")
		self.fileToUpload.close()
	def getUploadedImages(self):
		existingImages = glob(self.imagesFolder + "*.*")
		return existingImages
		
	def alreadyExists(self):
		existingImages = self.getUploadedImages()
		imageExists = False
		self.fileToUpload.stream.seek(0)
		checkingImage = Image.open(io.BytesIO(self.fileToUpload.stream.read()))
		for existingImage in existingImages:
			existingImageFile = Image.open(existingImage)
			imageExists = ImageChops.difference(checkingImage.convert("RGB"), existingImageFile.convert("RGB")).getbbox() is None
			existingImageFile.close()
			if imageExists:
				break
		checkingImage.close()
		return imageExists
	
	# Checks if the file to be uploaded is standard raster image
	# Vector image formats should be rejected as wrong images
	# For example .svg vector image format seems to be rejected
	def isImage(self):
		isImage = False
		self.fileToUpload.stream.seek(0)
		try:
			checkingImage = Image.open(io.BytesIO(self.fileToUpload.stream.read()))
			isImage = checkingImage.verify() is None
			checkingImage.close()
		except:
			isImage = False
		return isImage

	def checkAndUpload(self):
		responseCode = 0 # No errors code
		# Doing tests on uploaded file
		responseCode = 0 if self.isImage() else 1 # Check if file is raster image file, which obviously photo should be
		if responseCode != 1:
			responseCode = 2 if self.alreadyExists() else 0 # Check if file already exists
		if responseCode == 0:
			self.storeThumbnail()
			self.uploadImage()
		del self.fileToUpload # Remove link to file stream when not needed anymore
		return responseCode # Return error code to be able to display a message for the User to see on a Web Page

class responseInterpreter():
	def __init__(self, responseCode):
		responseMessage = {
			0: "Image successfully uploaded",
			1: "File type is not a raster image",
			2: "Image already exists",
			3: "No images available",
			4: "Image removed successfully",
			5: "Error removing Image"
		}
		self.responseMessage = responseMessage[responseCode]

	def getResponseMessage(self):
		return self.responseMessage

class imageList():
	def __init__(self):
		self.imagesFolder = "static/data/images/"
		self.thumbnailsFolder = "static/data/thumbnails/"
	
	def __del__(self):
		self.imagesFolder = None
		self.thumbnailsFolder = None
	
	def getExifDict(self, filePath):
		returned = {}
		EXIFParser = createParser(filePath)
		EXIFMetadata = extractMetadata(EXIFParser)
		# PIL EXIF parsing module has a bug when it can not parse non JPG files properply
		# Also PIL EXIF parsing module has a bug when it can not parse heavilly incorrect EXIF in correct file
		# So we using hachoir module and hope to get at least common data set, which probaly be enough in our case
		for item in sorted(EXIFMetadata):
			if len(item.values ) > 0:
				returned[item.key] = item.values[0].value
		return returned
	
	def getList(self):
		returned = []
		existingImages = sorted(glob(self.imagesFolder + "*.*"))
		existingThumbnails = sorted(glob(self.thumbnailsFolder + "*.*"))
		imageCount = 0
		for existingImage in existingImages:
			imagesData = {}
			imagesData["thumbnail"] = existingThumbnails[imageCount] if existingThumbnails[imageCount] else ""
			imagesData["normal"] = existingImage if existingImage else ""
			imagesData["name"] = basename(existingImage) if existingImage else ""
			imagesData["size"] = getsize(existingImage)if existingImage else 0
			fileDate = getmtime(existingImage)
			imagesData["UploadedDate"] = time.strftime('%Y-%m-%d', time.localtime(fileDate))
			exifDict = self.getExifDict(existingImage)
			imagesData["DateCreated"] = exifDict["date_time_digitized"].strftime('%Y-%m-%d') if "date_time_digitized" in exifDict else "Not Available"
			imagesData["CameraMake"] = exifDict["camera_manufacturer"] if "camera_manufacturer" in exifDict else "Not Available"
			imagesData["CameraModel"] = exifDict["camera_model"] if "camera_model" in exifDict else "Not Available"
			returned.append(imagesData)
			imageCount = imageCount + 1
		if len(returned) <= 0:
			imagesListError = {}
			imagesListError["errorCode"] = 3
			returned.append(imagesListError)
		return returned

class deletePhoto():
	def __init__(self, imageName):
		self.imagesFolder = "static/data/images/"
		self.thumbnailsFolder = "static/data/thumbnails/"
		self.photoName = imageName
		
	def __del__(self):
		self.imagesFolder = None
		self.thumbnailsFolder = None
		self.photoName = None
	
	def deletePhoto(self):
		existingImages = sorted(glob(self.imagesFolder + "*.*"))
		existingThumbnails = sorted(glob(self.thumbnailsFolder + "*.*"))
		returned = 4
		try:
			for existingImage in existingImages:
				if basename(existingImage) == self.photoName:
					remove(existingImage)
					break
			for existingThumbnail in existingThumbnails:
				if basename(existingThumbnail) == f"thumbnail_{self.photoName}":
					remove(existingThumbnail)
					break
			returned = 4
		except:
			returned = 5
		
		return returned
