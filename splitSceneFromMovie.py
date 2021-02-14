import subprocess
import sys
import os
import re
from datetime import datetime

def loadData(file):
    f = open(file)
    data = f.read()
    f.close()
    return data

def getMovieEndTime(data):
    pattern = r'Duration: (\d{2}):(\d{2}):(\d{2})'
    match = re.search(pattern, data)
    hours, minutes, seconds = match[1], match[2], match[3]
    time = (int(hours) * 60 + int(minutes)) * 60 + int(seconds)
    return time

def getSceneChangeTime(data):
    pattern = r'pts_time:([0-9]+\.[0-9]+)'
    timeList = re.findall(pattern, data)
    timeList = [float(n) for n in timeList]
    return timeList

def getSceneChange(path):
    print(path)
    fileList = os.listdir(path)
    fileList = sorted(fileList)
    return fileList

def getSceneIndex(fileList):
    pattern = r'([0-9]+[0-9]*).jpg'
    indexList = []
    for i,j in enumerate(fileList):
        temp = re.findall(pattern, j)
        if(temp != None):
            indexList.append(temp[0])
    indexList = [int(k) for k in indexList]
    indexList.insert(0,0)#Added Start Index
    return indexList

def splitSceneFromMovie(sceneChangeIndex, movieSceneTime):
    text = ''
    for i, j in enumerate(sceneChangeIndex):
        delta = movieSceneTime[j + 1] - movieSceneTime[j]
        cmd = 'ffmpeg -ss %s ' % movieSceneTime[j] + \
            ' -i ' + sys.argv[1] + ' -t %g' % delta + ' movie/output%s.mp4' % j
        subprocess.call(cmd, shell=True)
        text += 'file output/output' + str(j) + '.mp4\n'
    return text

def writeFile(fileName, text):
    f = open(fileName, 'w')
    f.write(text)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid Number of argument¥nUsage: python cutSceneFromMovie.py Filename')
    else:
        if not os.path.exists('image'):
            subprocess.call(["mkdir", "image"])

        if not os.path.isfile('ffmpegOutput'):
            cmd = 'ffmpeg -i ' + sys.argv[1] + ' -vf '+ \
            '\"select=gt(scene\,0.3), scale=640:360,showinfo\" ' + '-vsync vfr image/%04d.jpg -f null - 2>ffmpegOutput'
            subprocess.call(cmd, shell=True)
            
        data = loadData('ffmpegOutput')
        sceneTime = getSceneChangeTime(data)
        sceneTime.insert(0, 0)#Added movieStartTime
        movieEndTime = getMovieEndTime(data)
        sceneTime.append(movieEndTime)

        sceneChangeFile = getSceneChange("./image")
        sceneIndex = getSceneIndex(sceneChangeFile)
        if not os.path.exists('./movie/output0.mp4'):
            if not os.path.exists('movie'):
                subprocess.call(["mkdir", "movie"])
            text = splitSceneFromMovie(sceneIndex, sceneTime)
        else:
            text = ''
            for i, j in enumerate(sceneIndex):
                text += 'file output/output' + str(i) + '.mp4\n'
        writeFile('sceneList.txt', text)
        subprocess.call(["cat", "sceneList.txt"])    