from newsapi import NewsApiClient
import datetime as dt
import requests
import os
from decouple import config


def getNews():
    
    newsTitle = []
    newsDisp = []
    newsUrl = []

    newsapi = NewsApiClient(config('NEWS_API_KEY'))

    data = newsapi.get_top_headlines(language='en',page_size=10,country='in')

    articles = data['articles']

    newsDirectory = './tempContent/newsContent'
    if not os.path.exists(newsDirectory):
        os.makedirs(newsDirectory)

        
    imgDir = newsDirectory + '/images'
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)


    for x,y in enumerate(articles):

        currImgDir = imgDir + '/' + 'image' + str(x)
        if not os.path.exists(currImgDir):
            os.makedirs(currImgDir)
        imageFilePath = currImgDir + '/' + 'image.jpg'

        # Save Image
        image_url = y['urlToImage']
        img_data = requests.get(image_url).content
        with open(imageFilePath, 'wb') as handler:
            handler.write(img_data)
        

        newsDisp.append(y['description'])
        newsTitle.append(y['title'])
        newsUrl.append(y['url'])
        print(f'{x} --  {y["title"]}')

    
    return (newsTitle,newsDisp,newsUrl)



if __name__ == '__main__':
    getNews()