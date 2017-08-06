# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

import wave
from pydub import AudioSegment

def load_wave(wavepath):     

    f = wave.open(wavepath,'rb')
    params = f.getparams()
    print(params)
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)#读取音频，字符串格式
    print(nframes,len(strData))
    f.close()
    return nchannels, sampwidth, framerate, nframes,strData
    #wav_data1 = struct.unpack('%dh' % nframes, strData)

def audio_to_export(sourcepath,wavepath,start,end):
    
    wav = AudioSegment.from_wav(sourcepath) 
    
    wav[start*1000:end*1000].export(wavepath, format="wav") # 切e
    

