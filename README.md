# codesamples-python3-flask-file-upload
Python 3 Flask File Uploading App in virtualenv
# Description
File Uploading web application in style of Photo Storage 
# Purposes
To demonstrate ability to create web application on Python Flask as part of homework to get Python Developer position
# Requirements
1) Python 3
2) Flask
3) virtualenv
4) hachoir to get EXIF data from not only jpg files and corrupted EXIF data
5) pillow or PIL to detect if file is image or getting various Image parameters

# Installation instructions (approximate, not the last ones to follow):
1) sudo pip3 install virtualenv
2) mkdir Python3_FileUpload_Flask
3) cd Python3_FileUpload_Flask
4) virtualenv Python3_FileUpload_Flask
5) source Python3_FileUpload_Flask/bin/activate
6) pip install flask  hachoir pillow
7) copy the file contents from github into Python3_FileUpload_Flask/ (just near the second folder Python3_FileUpload_Flask in Python3_FileUpload_Flask folder)
8) Overall you structure should be similar to the one in github except for the files created by virtualenv
9) sudo ufw allow 5000
10) python app.py
11) [optional, done playing?] deactivate
12) [optional] You may also clone the project into you project, but you would need to create your own virtuenv in there or install requirements into your virtual environment Linux OS, [update] which is more preferable way now as you will get a precise version of virtualenv setup for the project - unless you want this project on non Debian based OS - in this case consult virtualenv documentation for your non-Debian based OS
# How to run?
1) 127.0.0.1:5000/ - main page
2) http://127.0.0.1:5000/readme - detailed instruction on how to use - link shoudl be on main page

# Notes
1) Why hachoir used instead of PIL:
2) Bug on Python 3.6 and PIL with reading EXIF data: https://github.com/python-pillow/Pillow/issues/2944
3) Another similar report - not reading EXIF data in all files: https://github.com/python-pillow/Pillow/issues/518
4) Camera Make and Camera Model being displayed only if available in EXIF data otherwise "Not Available" text being displayed
5) Photo Created or Photo Digitized Date being displayed only if available in EXIF data otherwise "Not Available" text being displayed
6) Consider reading detailed instruction available by the link on the main page after you will run the project
