# -*- coding: UTF-8 -*-

import numpy
import datetime
from os import listdir


def DayList(path='Stock_Tick'):
    data_list = listdir(path)
    day_list = [ i[:8] for i in data_list ]
    return day_list

def GetHistoryData(date,sid):
    HData = open('Stock_Tick/'+date+'_Stock.csv').readlines()
    MData = [ line.strip('\n').split(',') for line in HData ]
    MData_1 = [ line for line in MData if line[1] == sid ]
    return MData_1

    
def GetHistoryKBar(date,sid):
    Data = GetHistoryData(date,sid)
    #定義相關變數
    KBar = []
    InitTime = datetime.datetime.strptime(date+'090000000000',"%Y%m%d%H%M%S%f")
    Cycle = 60
    #開始進行K線計算
    for i in range(len(Data)):
        time=datetime.datetime.strptime(date+Data[i][0],"%Y%m%d%H%M%S%f")
        price=float(Data[i][2])
        qty=int(Data[i][3])
        if len(KBar)==0:
            KBar.append([InitTime,price,price,price,price,qty])
        else:
            if time < InitTime + datetime.timedelta(0,Cycle):
                if price > KBar[-1][2]:
                    KBar[-1][2] = price
                elif price < KBar[-1][3]:
                    KBar[-1][3] = price
                KBar[-1][4] = price
                KBar[-1][5] += qty
            else:
                InitTime += datetime.timedelta(0,Cycle)
                KBar.append([InitTime,price,price,price,price,qty])
    return KBar

def GetHistoryTAKBar(date,sid):
    KBar = GetHistoryKBar(date,sid)
    TAKBar={}
    TAKBar['time']=numpy.array([ line[0] for line in KBar ])
    TAKBar['open']=numpy.array([ line[1] for line in KBar ])
    TAKBar['high']=numpy.array([ line[2] for line in KBar ])
    TAKBar['low']=numpy.array([ line[3] for line in KBar ])
    TAKBar['close']=numpy.array([ line[4] for line in KBar ])
    TAKBar['volumn']=numpy.array([ line[5] for line in KBar ])
    return TAKBar