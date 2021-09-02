from cv2 import cv2
import numpy as np
import os
from os.path import isfile, join
from moviepy.editor import *
from moviepy.video.tools.credits import credits1
import moviepy.audio.fx.all as afx
from moviepy.audio.fx.volumex import volumex



def editVideo(pathOut,itr,mDespList):
    editedVideoDir = './tempContent/editedVideo'
    clip  = VideoFileClip(pathOut).margin(20).add_mask()

    newsDescription = mDespList[itr]

    print(len(newsDescription))
    clipDur = (len(newsDescription)/55)*11
    clip.set_duration(clipDur)

    title = TextClip(newsDescription,fontsize=60,color='white')
    w,h = clip.size
    txt_col = title.on_color(size=(clip.w + title.w,title.h+10),
                  color=(0,0,0), pos=(6,'center'), col_opacity=0.6)

    txt_col = txt_col.set_position(lambda t: (-t*180 + 400,0.90*h) ).set_duration(clipDur)
    #print(len(newsDescription))

    ## Audio
    audioClip = AudioFileClip("newsmusic.mp3")

    clip = clip.set_audio(audioClip).set_duration(clip.duration).volumex(0.7).audio_fadein(4.0).audio_fadeout(6.0)

    video = CompositeVideoClip([clip,txt_col.set_start(1)],size = clip.size)


    video.write_videofile(editedVideoDir+'/edited'+str(itr)+'.mp4',threads=20,fps=50) #fps





def convertToVideo(pathIn, pathOut,itr,mDespList , fps, time):
    # converts images to video
    try:
        frame_array = []
        files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
        # print(files)
        for i in range(len(files)):
            try:
                filename = pathIn+files[i]
                #print('.............'+filename)
                img=cv2.imread(filename)
                img = cv2.resize(img,(1920,1080)) #make it not stretch
                height, width, layers = img.shape
                size = (width,height)
                newsDescription = mDespList[itr]

                clipDur = int((len(newsDescription)/55)*11)
                
                for k in range (clipDur):
                    frame_array.append(img)
            
            except Exception as e:
                print(str(e))
    
        out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        for i in range(len(frame_array)):
            out.write(frame_array[i])
        out.release()

        editVideo(pathOut,itr,mDespList)
    except Exception as e:
        print(str(e))












if __name__ == "__main__":
    convertToVideo(pathIn = './tempContent/newsContent/images/',pathOut = './tempContent/video.mp4',itr=0,mDespList = [],fps = 1,time = 20)