# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""
import os
from aip import AipSpeech
from utility import write_txt_to_file

APP_ID = '1234567'
API_KEY = 'natYea8hBD6w0Dh1oXBSlAn5'
SECRET_KEY = '8e9b76b95ade9e7063088dfa52c20874'
    
def baidu(filePath,samplerate,language):
    global APP_ID,API_KEY,SECRET_KEY
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
        
    response=aipSpeech.asr(get_file_content(filePath), 'wav', samplerate, {
        'lan': language,
    })
    return response
        
def speech_recognizai_baidu(filepath,samplerate,language='zh'):
    return baidu2(filepath,samplerate,language)
    
def baidu2(filestream,samplerate,language):
    global APP_ID,API_KEY,SECRET_KEY
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        
    response=aipSpeech.asr(filestream, 'wav', samplerate, {
        'lan': language,
    })
    return response