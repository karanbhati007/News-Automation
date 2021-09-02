from flask import Flask,request,send_file
import os
import json
from os.path import isfile, join
app = Flask(__name__)

base_url = 'http://ec2-52-87-180-130.compute-1.amazonaws.com/'

def getImageList():

    imageList = []
    for i in range(10):
        imageList.append(base_url+'image/'+ str(i))
    
    return imageList


@app.route('/')
def getNewsData():

    newsContent = {}

    with open('newsData.txt', 'r') as filehandle:
        newsContent = json.load(filehandle)

    #print(newsContent)
    newsContent['images'] = getImageList()

    return newsContent


@app.route('/image/<im>')
def return_image(im):
    imagesDir = './tempContent/newsContent/images/'
    try:
        return send_file(imagesDir+'image'+str(im)+'/image.jpg',attachment_filename = 'image.jpg')
    except Exception as e:
 	    return str(e)




if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)
    