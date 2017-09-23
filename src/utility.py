# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

def write_txt_to_file(path,txt):
    with open(path,'ab+') as f:
        f.write(txt)

def seconds_to_timestamp_str(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    timestamp= ("%02d:%02d:%06.3f" % (h, m, s))
    return timestamp

def seconds_to_timestamp_ass(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    timestamp= ("%01d:%02d:%05.2f" % (h, m, s))
    return timestamp
#print seconds_to_timestamp_ass(1.737625)