# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

def get_wave_statistic(waveData,threshhold=0.2):
    splitlist=[]
    
    zerolen=0
    nonezerolen=0
    
    if waveData[0]==0:
        pre=-1
    else:
        pre=0  
   
    for v in waveData:    
        if (abs(v)<=threshhold and abs(pre) <= threshhold) or (abs(v)>threshhold and abs(pre) >threshhold) :
            if abs(v)<=threshhold:
                zerolen+=1
                nonezerolen=0
            else:
                nonezerolen+=1
                zerolen=0
            
        elif (abs(v)<=threshhold and abs(pre) > threshhold) or (abs(v)>threshhold and abs(pre) <= threshhold):
            if abs(v)>threshhold:
                if len(splitlist)!=0:
                    zerolen+=1
                    nonezerolen=0
                splitlist.append([False,zerolen,0,0,0])
            else:
                if len(splitlist)!=0:                
                    nonezerolen+=1
                    zerolen=0
                splitlist.append([True,nonezerolen,0,0,0])
        pre=v
    
    print 'zerolen',zerolen,'nonezerolen',nonezerolen
    
    if zerolen:
        splitlist.append([False,zerolen,0,0,0])
    if nonezerolen:
        splitlist.append([True,nonezerolen,0,0,0])
    return splitlist

#statistic collum : flase/true continueframenum id accumulatetime middletimestamp
#assign id
#get accumulatetime,middletimestamp
def calculate_other_statistic_info(wavestatistic):
    id=1
    sum=0    
    for record in wavestatistic:
        t=(sum+record[1]/2.0)*1/8000
        sum+=record[1]
        record[2]=id
        record[3]=sum   
        record[4]=t  
        id+=1
        txt='%s %s %s %s %s\n'%(record[2],record[0],record[1],record[3],record[4])
        #print txt
        