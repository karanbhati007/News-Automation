from convertToVideo import convertToVideo
import os
from moviepy.editor import *
from os.path import isfile, join
from newsApi import getNews
from uploadYT import uploadYtvid
import schedule
import shutil
import time
import json
import nltk
from summarizeText import summarizeText

countNews = 19
DAILY_SCHEDULED_TIME = "03:00"

mainDir = './tempContent'
currImagesDir = './tempContent/newsContent/images'
videoDir = './tempContent/videos'
editedVideoDir = './tempContent/editedVideo'
newsTitle = []
nltk.download('punkt')



def composeVideo():
    allVideos = []
    numVideoDir = './num_video'
    introClip = VideoFileClip('./intro.mp4').resize((1920,1080))
    endClip = VideoFileClip('./end.mp4').resize((1920,1080))
    allVideos.append(introClip)

    for itr,fileName in enumerate(os.listdir(editedVideoDir)):
        #print(itr)
        filePath = os.path.join(editedVideoDir, fileName)
        if isfile(filePath) and fileName.endswith(".mp4"):
            s = 'no_' + str(itr) + '.mp4'
            introNumPath = os.path.join(numVideoDir,s)
            numIntroClip = VideoFileClip(introNumPath).resize((1920,1080))
            clip = VideoFileClip(filePath)
            allVideos.append(numIntroClip)
            allVideos.append(clip)

    
    allVideos.append(endClip)
    finalClip = concatenate_videoclips(allVideos, method="compose")
    finalClip.write_videofile('./tempContent/finalVideo.mp4', threads=20, remove_temp=True, codec="libx264", audio_codec="aac")


def deleteAllFiles():
    print("Removing temp files!")
    # Delete all files made:
    #   Folder videoDirectory
    shutil.rmtree(mainDir, ignore_errors=True)
    #   File outputFile
    # # try:
    # #     os.remove(outputFile
    # # except OSError as e:  ## if faile,d, report it back to the user ##
    # #     print ("Error: %s - %s." % (e.filename, e.strerror))
    print("Removed temp files!")


def uploadVideoOnYT():
    global countNews
    global newsTitle

    description  = "Today's Top 10 Trending News  :: \n\n\n"

    for itr,st in enumerate(newsTitle):
        description += str(itr+1) + '  --  ' + st + '\n'

    description+='\n\n\n\n\n\nBy KSB'
   
    title = 'Daily Top 10 Trending News #' + str(countNews)
    countNews = countNews + 1

    tags=['news','top daily news','daily news','automated','new','automated news','top 10 daily news']


    print("Uploading to Youtube...")
    uploadYtvid(VIDEO_FILE_NAME='./tempContent/finalVideo.mp4',
                title=title,
                description=description,tags=tags)
    print("Uploaded To Youtube!")


def attemptRoutine():
    try:
        routine()
    except OSError as err:
        print("Routine Failed on " + "OS error: {0}".format(err))
        time.sleep(60*60)
        routine()


def routine():
    print('Main Starts .............')

    global newsTitle

    if not os.path.exists(videoDir):
        os.makedirs(videoDir)


    if not os.path.exists(editedVideoDir):
        os.makedirs(editedVideoDir)


    newsTitle,newsDescp,newsUrl = getNews()

    summarizedNewsDescp = []

    for itr,url in enumerate(newsUrl):
        summarizedNewsDescp.append(summarizeText(url,newsDescp,itr))
    

    # Save to File
    newsData = {}
    newsData['title'] = newsTitle
    newsData['descp'] = summarizedNewsDescp #newsDescp
    newsData['newsUrl'] = newsUrl

    with open('newsData.txt', 'w') as filehandle:
        json.dump(newsData, filehandle)

   
    # Make Video
    for i in range(10):
        print(i)
        convertToVideo(pathIn = currImagesDir+'/image'+str(i)+'/',pathOut = './tempContent/videos/video'+str(i)+'.mp4',itr=i,mDespList = summarizedNewsDescp,fps = 1,time = 18)


    # Compose all video into one
    composeVideo()


    #Upload On YT
    uploadVideoOnYT()


    #deleteAllFiles()

    print('Main Ends ..............')





# Daily Routine
attemptRoutine()
#schedule.every().hour.do(attemptRoutine)
schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one min









