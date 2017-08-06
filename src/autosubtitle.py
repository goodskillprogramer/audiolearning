# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

import os
import shutil

import numpy as np
from scipy import signal
from pydub import AudioSegment
from audiohelper import load_wave
import matplotlib.pyplot as plt
from speechrecognize import speech_recognizai_baidu
from utility import write_txt_to_file
from utility import seconds_to_timestamp_str
from audiostatistic import get_wave_statistic
from audiostatistic import calculate_other_statistic_info

def plot_data(waveData,nframes,framerate):
    time = np.arange(0,nframes)*(1.0 / framerate)
    fig=plt.figure(figsize=(100,2)) 
    plt.plot(time,waveData)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Single channel wavedata")
    plt.grid('on')#标尺，on：有，off:无。
    fig.savefig('test2png.png', dpi=100)
    print len(waveData)
    print (waveData[0:1000])

def timevalidate(timetable,endtime,timerange):
    timetable+=[endtime]
    ordertime=sorted(timetable)
    for i in range(len(ordertime)-1):
        if ordertime[i+1]-ordertime[i]>timerange:
            print ordertime[i+1],ordertime[i]
            return False            
    return True    

def time_transform(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print ("%02d:%02d:%02d" % (h, m, s))
if __name__ =="__main__":
    wavepath=r'./dataset/ted80001.wav'
   
    laguage='zh'
    laguage='en'
    nchannels, sampwidth, framerate, nframes,strData=load_wave(wavepath)
    waveData = np.fromstring(strData,dtype=np.int16)   
    
    waveData=signal.medfilt(waveData)    
    waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
    if nchannels>1:
        waveData = np.reshape(waveData,[nframes,nchannels])
        waveData=waveData[:,0]

    #plot_data(waveData,nframes,framerate)
    wavestatistic=get_wave_statistic(waveData)
    print 'len(wavestatistic)',(len(wavestatistic))
    
    calculate_other_statistic_info(wavestatistic)
    
    sortedwavestatistic=sorted(wavestatistic,key=lambda x:(x[0],-x[1]))

    splittimestamp=[0]
    for split in sortedwavestatistic:
        splittimestamp+=[split[4]]
        if timevalidate(splittimestamp,nframes*1.0/8000,17):
            break
        splittimestamp.pop()

    splittimestamp=sorted(splittimestamp)
    print splittimestamp
    basename=os.path.basename(wavepath)
    filename=os.path.splitext(basename)[0]
    savefilefolder=os.path.join(r'./temp',filename)
    print 'save floder:',savefilefolder
    if os.path.exists(savefilefolder):
        shutil.rmtree(savefilefolder)      
   
    os.mkdir(savefilefolder)
    wav = AudioSegment.from_wav(wavepath) # 打开mp3文件
    srtid=1
    maxrecognize=50
    lentimestamp=len(splittimestamp)
    for i in range(len(splittimestamp)-1):
        if i>maxrecognize:
            print 'end recognize ',maxrecognize
            break
        starttime=splittimestamp[i]
        endtime=splittimestamp[i+1]
        if endtime>nframes*1.0 / framerate:
            print 'out of time',endtime,nframes*1.0 / framerate
            endtime=nframes*1.0 / framerate
        print starttime,endtime
        savefilename=str(i)+"_"+str(starttime)+"_"+str(endtime)
        savepath=os.path.join(savefilefolder,savefilename+'.wav')#overwrite
        print 'savepath',savepath
        try:
            print 'export timerage:',starttime,endtime,' completion ',i,lentimestamp,i*1.0/lentimestamp
            wav[starttime*1000:endtime*1000].export(savepath, format="wav") # 切e
        except Exception as e:
            print 'export exception',str(e)
            continue
        
        if framerate==8000 or framerate==16000:
            response=speech_recognizai_baidu(savepath,framerate,laguage)            
            savejsonpath=os.path.join(savefilefolder,savefilename+'.json') 
            #print str(response)
            if response['err_no']==0:      
                recognize_txt=(response['result'][0])
                for r in recognize_txt:
                    print r,
                print ''
                #write_txt_to_file(savejsonpath,recognize_txt.encode('utf-8'))
                startstr=seconds_to_timestamp_str(starttime)
                endstr=seconds_to_timestamp_str(endtime)
                srtpath=os.path.join(savefilefolder,filename+'.srt')
                asspath=os.path.join(savefilefolder,filename+'.ass ')
                if srtid<10:
                    recognize_txt=("%s     %s")%(u'subtitle(autocreated) wj3235@126.com =>',recognize_txt)                    
                    
                srttxt=('%s\n%s-->%s\n%s\n\n')%(srtid,startstr,endstr,recognize_txt)
                asstxt=('Dialogue:0,%s,%s,AGMStyle,NTP,0000,0000,0000,,%s\n')%(startstr,endstr,recognize_txt)
                write_txt_to_file(srtpath,srttxt.encode('utf-8'))
                #write_txt_to_file(asspath,asstxt.encode('utf-8'))
                
                srtid+=1
                print 'save ok'
                
