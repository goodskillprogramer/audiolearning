# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 05:26:49 2017
@author: alex
@contact wj3235@126.com
"""

def get_wave_statistic(waveData,framerate,threshhold=0.2):
    splitlist=[]
    
    zerolen=0
    nonezerolen=0
    
    if waveData[0]==0:
        pre=-1
    else:
        pre=0  
   
    for v in waveData:    
        #如果当前点和上一个点都大于0.2或者都小于0.2
        #都小于的话空长度加1,zerolen
        #都大于的话有生长度加1,nonezerolen
        if (abs(v)<=threshhold and abs(pre) <= threshhold) or (abs(v)>threshhold and abs(pre) >threshhold) :
            if abs(v)<=threshhold:
                zerolen+=1
                nonezerolen=0
            else:
                nonezerolen+=1
                zerolen=0
        #有声音无声音状态转换   
        elif (abs(v)<=threshhold and abs(pre) > threshhold) or (abs(v)>threshhold and abs(pre) <= threshhold):
            #由无声转入有声状态
            #无声长度+1,记录无声长度,False
            if abs(v)>threshhold:
                if len(splitlist)!=0:
                    zerolen+=1
                    nonezerolen=0
                if zerolen>framerate*17-1:
                    while zerolen>framerate*17-1:
                        splitlist.append([False,framerate*17-1,0,0,0])
                        zerolen-=framerate*17-1
                splitlist.append([False,zerolen,0,0,0])
            #由有声转入无声状态
            #有声长度+1,记录无声长度,True
            else:
                if len(splitlist)!=0:                
                    nonezerolen+=1
                    zerolen=0
                splitlist.append([True,nonezerolen,0,0,0])
        pre=v
    
    #print 'zerolen',zerolen,'nonezerolen',nonezerolen
    
    #循环完之后,添加最后一段有/无声段
    if zerolen:
        splitlist.append([False,zerolen,0,0,0])
    if nonezerolen:
        splitlist.append([True,nonezerolen,0,0,0])
    return splitlist

#statistic collum : flase/true continueframenum id accumulatetime middletimestamp
#assign id
#get accumulatetime,middletimestamp
def calculate_other_statistic_info(wavestatistic,framerate):
    id=1
    sum=0    
    for record in wavestatistic:
        t=(sum+record[1]/2.0)*1/framerate#8000应为频率值,算出到目前时长总长,单位为s
        sum+=record[1]
        record[2]=id #序列
        record[3]=sum #字节长度累积,等于时长累计*8000*(双字节Int16)
        record[4]=t  
        id+=1
        #txt='%s %s %s %s %s\n'%(record[2],record[0],record[1],record[3],record[4])
        if(record[1]>2*17*framerate):
            #print (record[1])
            break;
    #print (wavestatistic[:10])
        