# -*- coding: utf-8 -*-

"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

import speech_recognition as sr
from os import path
import time
import wave

from aip import AipSpeech

def listen_translate():
    while(True):
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone(sample_rate=8000) as source:
            print("Say something!")
    #         print(5),
    #         time.sleep(1)
    #         print(4),
    #         time.sleep(1)
    #         print(3),
    #         time.sleep(1)
    #         print(2),
    #         time.sleep(1)  
    #         print(1),     
    #         time.sleep(1)  
            audio = r.listen(source)#,timeout=5,phrase_time_limit=0.05
        
    #     r = sr.Recognizer()
    #     with sr.AudioFile('./english.wav') as source:
    #         audio = r.record(source)  # read the entire audio file
        
        # write audio to a WAV file    `````
        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
            
        # recognize speech using Sphinx
        try:
            print("Sphinx thinks you said :" + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
audiolist=[]  

def callback(recognizer,audio):
    audiolist.append(audio)
    
def translate(r,audio):    
    try:
        s=time.time()
        print(str(len(audiolist))+" Sphinx thinks you said :" + r.recognize_sphinx(audio))
        print time.time()-s
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
def listen_and_recognize():           
    r = sr.Recognizer()
    m = sr.Microphone(sample_rate=8000)
    r.listen_in_background(m,callback,phrase_time_limit=1)

    while(True):
        lastlen=0
        if len(audiolist)==0:        
            time.sleep(10)
            continue
        if lastlen==len(audiolist):
            time.sleep(10)
            continue
        output = wave.open('microphone-results.wav', 'wb')
        output.setnchannels(1)
        setparam=False
        para=None
        for audio in audiolist:
            with open("temps.wav", "wb") as f:
                f.write(audio.get_wav_data())       
            temps = wave.open('temps.wav', 'rb') 
            #print temps.getparams()
            if not setparam:
                para=temps.getparams()
                output.setparams(para)   
                setparam=True     
            output.writeframes(temps.readframes(temps.getnframes()))   
        
        output.close() 
#         output = wavefile.open('microphone-results.wav', 'rb')
#         outputaudio=sr.AudioData(output.readframes(output.getnframes()),para[2],para[1])
#         translate(r,outputaudio)
        #baidu('microphone-results.wav')
        lastlen=len(audiolist) 
        time.sleep(10)

def play_audio():
        
        r = sr.Recognizer()        

        with sr.AudioFile('./english.wav') as source:
            audio = r.record(source)  # read the entire audio file    
            print audio  
          
        # recognize speech using Sphinx
        try:
            print("Sphinx thinks you said :" + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            
def baidu(filePath,samplerate):
   
    APP_ID = '1234567'
    API_KEY = 'a8hBD6w0Dh1oXBSlAn5natYe'
    SECRET_KEY = '9b76b95ade9e7063088dfa52c208748e'
    
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    
    
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    #
    response=aipSpeech.asr(get_file_content(filePath), 'wav', samplerate, {
        'lan': 'en',
    })
    print response
#     # ��URL��ȡ�ļ�ʶ��
#     aipSpeech.asr('', 'wav', 44100, {
#         'url': 'http://121.40.195.233/res/16k_test.pcm',
#         'callback': 'http://xxx.com/receive',
#     })
    
#listen_and_recognize()
