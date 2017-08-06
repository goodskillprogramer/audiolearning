# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

def get_name(pinyin):
    try:
        youdao = Youdao(pinyin)     
        jsonresult=youdao.executor() 
        return  jsonresult['translation'][0]
    except Exception as e:
        return ' '

if __name__ =='__main__':
    pass