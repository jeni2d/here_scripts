# This script was created when I had to upload a bunch of videos from dashcam to Mapillary but Mapillary uploader was in redesigning stage 
# and didn't support video uploading, only photos with gps tags. 
# This script extracts gps tags from the video, then extract frames by gps tags, and then add gps metadata to that frames
# to use this script you have to download exiftool and ffmpeg
# !this script designed for BlackVue dashcam!

import os
import subprocess
import io
import time
from GPSPhoto import gpsphoto

t1 = time.time()

folder_num = '1' # I create subfolder for storage imageries

os.chdir('') #put path to videos here

def extract_geo(filename):
    #extracting gps data with timestamp in video
    sub = subprocess.Popen(['exiftool.exe', '-ee', '-n', '-p', '$sampletime,$gpslatitude,$gpslongitude,$gpsaltitude,$gpsdatetime', os.path.join(os.getcwd(), filename)],stdout=subprocess.PIPE)
    frames_temp = []
    frames_gps = []
    for line in io.TextIOWrapper(sub.stdout, encoding="utf-8"):
        frames_temp.append(line.strip())
    
    #reducing duplicate marks
    for i in range(len(frames_temp)):
        frames_temp[i] = frames_temp[i].split(',')
        if float(frames_temp[i][0]) > float(frames_temp[i-1][0]) or i == 0:
            frames_gps.append(frames_temp[i])
        else:
            break
            
    #framing video by seconds from the beginning of video and saving imageries
    if frames_gps:
        for i in frames_gps:
            subprocess.run(['ffmpeg.exe', '-ss', i[0], '-i', os.path.join(os.getcwd(), filename), '-vframes', '1', os.path.join(os.getcwd(), folder_num, str(time.time())[:12].replace('.','')+'_'+filename[:-4]+'.jpg')])
    
        return frames_gps


def add_metadata(meta_data, name):
    f = meta_data
    photos = [i for i in os.listdir(folder_num) if name[:18] in i]
    for index, j in enumerate(photos):
        photo = gpsphoto.GPSPhoto(os.path.join(os.getcwd(), folder_num, j))
        info = gpsphoto.GPSInfo((float(meta_data[index][1]), float(meta_data[index][2])), alt=int(float(meta_data[index][3])), timeStamp=meta_data[index][4].split('.')[0])
        photo.modGPSData(info, os.path.join(os.getcwd(), folder_num, j))

        
for i in os.listdir():
    if i.endswith('mp4'):
        meta_data = extract_geo(i)
        if meta_data:
            add_metadata(meta_data, i)


print((time.time()-t1)/60)	    
