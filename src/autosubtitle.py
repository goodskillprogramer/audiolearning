# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

import os
import shutil
import sys
import time

#NumPy系统是Python的一种开源的数值计算扩展。这种工具可用来存储和处理大型矩阵

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
    #print len(waveData)
    #print (waveData[0:1000])

def timevalidate(timetable,endtime,timerange):
    timetable+=[endtime]    
    for i in range(len(timetable)-1):
        if timetable[i+1]-timetable[i]>timerange:
            return False            
    return True    

#折半插入排序
def insertsort(timearr,item):
    if len(timearr)==1:
        timearr.append(item) if item>timearr[0] else timearr.insert(0,item)
    elif len(timearr)==2:
        if item>timearr[0]:
            timearr.append(item) if item>timearr[1] else timearr.insert(1,item)
        else:
            timearr.insert(0,item)
    else:
        if item<timearr[0]:
            timearr.insert(0,item)
        elif item>timearr[len(timearr)-1]:
            timearr.append(item)
        else:
            middle(timearr,0,len(timearr)-1,item)
#折半插入排序递归方法        
def middle(timearr,start,end,item):
    if end-start==1:        
        timearr.insert(end,item)
    else:        
        middle(timearr,start,(start+end)//2,item) if timearr[(start+end)//2]>item else middle(timearr,(start+end)//2,end,item)        

def time_transform(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print ("%02d:%02d:%02d" % (h, m, s))
if __name__ =="__main__":
    wavepath=r'./dataset/ted80001.wav'
   
    laguage='zh'
    laguage='en'
    nchannels, sampwidth, framerate, nframes,strData=load_wave(wavepath)
    
    # 使用字符串创建矩阵,简单的转换实现了ASCII码的转换,int16使得每2个字符(16位)转化成10进制的数组
    waveData = np.fromstring(strData,dtype=np.int16)       
        
    #中值滤波medfilt计算太慢,使用下面方法速度提升一倍
    #waveData=signal.medfilt(waveData)
    middata=[0]*len(waveData)
    if(len(waveData)>2):
        middata[0]=sorted([0,waveData[1],waveData[2]])[1]
        middata[len(waveData)-1]=sorted([0,waveData[len(waveData)-1],waveData[len(waveData)-2]])[1]
    for i in range(1,len(waveData)-1):
        
        middata[i]=(waveData[i] if waveData[i] > waveData[i+1] else\
        (waveData[i+1] if waveData[i-1] > waveData[i+1] else waveData[i-1]))\
        if waveData[i-1] > waveData[i] else\
        (waveData[i-1] if waveData[i-1] > waveData[i+1] else\
        (waveData[i+1] if waveData[i] > waveData[i+1] else waveData[i]));
    for j in range(len(waveData)):
        waveData[j]=middata[j]
        
    #wave幅值归一化 取数组中最大的值为分母,每个元素作为分母
    waveData = waveData*1.0/(max(abs(waveData)))
    if nchannels>1:
        waveData = np.reshape(waveData,[nframes,nchannels])
        waveData=waveData[:,0]

    #plot_data(waveData,nframes,framerate)#绘制音频波谱图片
    #统计有声音和没声音的分段每段时长
    wavestatistic=get_wave_statistic(waveData,framerate)
    #print 'len(wavestatistic)',(len(wavestatistic))
    
    calculate_other_statistic_info(wavestatistic,framerate)
    
    sortedwavestatistic=sorted(wavestatistic,key=lambda x:(x[0],-x[1]))

    splittimestamp=[0]
    for split in sortedwavestatistic:
        #splittimestamp+=[split[4]]
        
        #split[4]为音频时间点,表示到目前时长总长,单位为s
        #插入并折半排序        
        insertsort(splittimestamp,split[4])   
        
        #nframes字节总长度/采样率
        #print(nframes*1.0/8000); 输出329.537625等于5分29秒,如果相邻2段都小于17秒则结束
        if timevalidate(splittimestamp,nframes*1.0/framerate,17):
            break
        splittimestamp.pop()

    #splittimestamp=sorted(splittimestamp)
    #print splittimestamp
    basename=os.path.basename(wavepath)
    filename=os.path.splitext(basename)[0]
    savefilefolder=os.path.join(r'./temp',filename)
    #print 'save floder:',savefilefolder
    if os.path.exists(savefilefolder):
        shutil.rmtree(savefilefolder)      
   
    os.mkdir(savefilefolder)
    wav = AudioSegment.from_wav(wavepath) # 打开mp3文件
    srtid=1
    maxrecognize=50
    lentimestamp=len(splittimestamp)
    

    for i in range(len(splittimestamp)-1):
        #if i>maxrecognize:
            #print 'end recognize ',maxrecognize
            #break
        starttime=splittimestamp[i]
        endtime=splittimestamp[i+1]
        if endtime>nframes*1.0 / framerate:
            #print 'out of time',endtime,nframes*1.0 / framerate
            endtime=nframes*1.0 / framerate
        #print starttime,endtime
        savefilename=str(i)+"_"+str(starttime)+"_"+str(endtime)
        savepath=os.path.join(savefilefolder,savefilename+'.wav')#overwrite
        #print 'savepath',savepath
        #try:
            #print 'export timerage:',starttime,endtime,' completion ',i,lentimestamp,i*1.0/lentimestamp
            #wav[starttime*1000:endtime*1000].export(savepath, format="wav") # 切e
        #except Exception as e:
            #print 'export exception',str(e)
            #continue
        
        if framerate==8000 or framerate==16000:
            #调用百度api
            response=speech_recognizai_baidu(wav[starttime*1000:endtime*1000].raw_data,framerate,laguage)           
            savejsonpath=os.path.join(savefilefolder,savefilename+'.json') 
            #print str(response)
            #解析百度的回复{'corpus_no': '6462566101916659365', 'result': ['he,', 'e,', 'here,', 'each,', 'a,'],
            #'err_msg': 'success.', 'err_no': 0, 'sn': '949466616181504683425'}百度给出前5种可能的识别结果
            if response['err_no']==0:      
                recognize_txt=(response['result'][0])
                #for r in recognize_txt:
                    #print(r)
                #print ''
                #write_txt_to_file(savejsonpath,recognize_txt.encode('utf-8'))
                startstr=seconds_to_timestamp_str(starttime)
                endstr=seconds_to_timestamp_str(endtime)
                srtpath=os.path.join(savefilefolder,filename+'.srt')
                asspath=os.path.join(savefilefolder,filename+'.ass ')
                #if srtid<10:
                    #recognize_txt=("%s     %s")%(u'subtitle(autocreated) wj3235@126.com =>',recognize_txt)                    
                    
                srttxt=('%s\n%s --> %s\n%s\n')%(srtid,startstr,endstr,recognize_txt)
                #asstxt=('Dialogue:0,%s,%s,AGMStyle,NTP,0000,0000,0000,,%s\n')%(startstr,endstr,recognize_txt)
                write_txt_to_file(srtpath,srttxt.encode('utf-8'))
                #write_txt_to_file(asspath,asstxt.encode('utf-8'))
                
                srtid+=1
                #print 'save ok'
                
