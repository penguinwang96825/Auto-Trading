# 載入必要模組
import pandas as pd
import mplfinance as mpf
import numpy as np
from talib.abstract import SMA,RSI,BBANDS

# 將K線轉為DataFrame
def KbarToDf(KBar):
    # 將K線 Dictionary 轉換成 Dataframe
    Kbar_df=pd.DataFrame(KBar)
    # 將 Dataframe 欄位名稱轉換
    Kbar_df.columns = [ i[0].upper()+i[1:] for i in Kbar_df.columns ]
    # 將 Time 欄位設為索引
    Kbar_df.set_index( "Time" , inplace=True)
    # 回傳
    return Kbar_df

# 繪製K線圖
def ChartKBar(KBar,addp=[],volume_enable=True):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 開始繪圖
    mpf.plot(Kbar_df,volume=volume_enable,addplot=addp,type='candle',style='charles')

# 繪製K線圖以及下單紀錄
def ChartOrder(KBar,TR,addp=[],volume_enable=True):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 買方下單點位紀錄
    BTR = [ i for i in TR if i[0]=='Buy' or i[0]=='B' ]
    BuyOrderPoint = [] 
    BuyCoverPoint = []
    for date,value in Kbar_df['Close'].iteritems():
        # 買方進場
        if date in [ i[2] for i in BTR ]:
            BuyOrderPoint.append( Kbar_df['Low'][date] * 0.999 )
        else:
            BuyOrderPoint.append(np.nan)
        # 買方出場
        if date in [ i[4] for i in BTR ]:
            BuyCoverPoint.append( Kbar_df['High'][date] * 1.001 )
        else:
            BuyCoverPoint.append(np.nan)
    # 將下單點位加入副圖物件
    if [ i for i in BuyOrderPoint if not np.isnan(i) ] !=[]:
        addp.append(mpf.make_addplot(BuyOrderPoint,scatter=True,markersize=200,marker='^',color='red'))
        addp.append(mpf.make_addplot(BuyCoverPoint,scatter=True,markersize=200,marker='v',color='blue'))
    # 賣方下單點位紀錄
    STR = [ i for i in TR if i[0]=='Sell' or i[0]=='S' ]
    SellOrderPoint = [] 
    SellCoverPoint = []
    for date,value in Kbar_df['Close'].iteritems():
        # 賣方進場
        if date in [ i[2] for i in STR ]:
            SellOrderPoint.append( Kbar_df['High'][date] * 1.001 )
        else:
            SellOrderPoint.append(np.nan)
        # 賣方出場
        if date in [ i[4] for i in STR ]:
            SellCoverPoint.append( Kbar_df['Low'][date] * 0.999 )
        else:
            SellCoverPoint.append(np.nan)
    # 將下單點位加入副圖物件
    if [ i for i in SellOrderPoint if not np.isnan(i) ] !=[]:
        addp.append(mpf.make_addplot(SellOrderPoint,scatter=True,markersize=200,marker='v',color='green'))
        addp.append(mpf.make_addplot(SellCoverPoint,scatter=True,markersize=200,marker='^',color='blue'))
    # 開始繪圖
    ChartKBar(KBar,addp,volume_enable)


# 繪製K線圖以及MA
def ChartKBar_MA(KBar,longPeriod=20,shortPeriod=5):
    # 計算移動平均線(長短線)
    KBar['MA_long']=SMA(KBar,timeperiod=longPeriod)
    KBar['MA_short']=SMA(KBar,timeperiod=shortPeriod)
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 將副圖繪製出來
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['MA_long'],color='red'))
    addp.append(mpf.make_addplot(Kbar_df['MA_short'],color='yellow'))
    # 開始繪圖
    ChartKBar(KBar,addp,True)

# 繪製K線圖加上MA以及下單紀錄
def ChartOrder_MA(KBar,TR):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 定義指標副圖
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['MA_long'],color='red'))
    addp.append(mpf.make_addplot(Kbar_df['MA_short'],color='yellow'))
    # 繪製指標、下單圖
    ChartOrder(KBar,TR,addp)
    
# 繪製K線圖以及RSI
def ChartKBar_RSI_1(KBar,longPeriod=27,shortPeriod=9):
    # 計算RSI(長短線) 以及中介線 50
    KBar['RSI_long']=RSI(KBar,timeperiod=longPeriod)
    KBar['RSI_short']=RSI(KBar,timeperiod=shortPeriod)
    KBar['Middle']=np.array([50]*len(KBar['time']))
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 將副圖繪製出來
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['RSI_long'],panel='lower',color='red',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['RSI_short'],panel='lower',color='green',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['Middle'],panel='lower',color='black',secondary_y=False))
    # 開始繪圖
    ChartKBar(KBar,addp,False)

# 繪製K線圖加上RSI以及下單紀錄
def ChartOrder_RSI_1(KBar,TR):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 將副圖繪製出來
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['RSI_long'],panel='lower',color='red',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['RSI_short'],panel='lower',color='green',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['Middle'],panel='lower',color='black',secondary_y=False))
    # 開始繪圖
    ChartOrder(KBar,TR,addp,False)
    
# 繪製K線圖以及RSI
def ChartKBar_RSI_2(KBar,RSIPeriod,upper,lower):
    # 計算RSI 以及 買超賣超線 
    KBar['RSI']=RSI(KBar,timeperiod=RSIPeriod)
    KBar['Ceil']=np.array([upper]*len(KBar['time']))
    KBar['Floor']=np.array([lower]*len(KBar['time']))
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 將副圖繪製出來
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['RSI'],panel='lower',color='black',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['Ceil'],panel='lower',color='red',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['Floor'],panel='lower',color='red',secondary_y=False))
    # 開始繪圖
    ChartKBar(KBar,addp,False)
    
# 繪製K線圖加上RSI以及下單紀錄
def ChartOrder_RSI_2(KBar,TR):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 將副圖繪製出來
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['RSI'],panel='lower',color='black',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['Ceil'],panel='lower',color='red',secondary_y=False))
    addp.append(mpf.make_addplot(Kbar_df['Floor'],panel='lower',color='red',secondary_y=False))
    # 開始繪圖
    ChartOrder(KBar,TR,addp,False)

    
# 繪製K線圖以及布林通到
def ChartKBar_BBANDS(KBar,BBANDSPeriod):
    # 計算布琳通道
    KBar['Upper'],KBar['Middle'],KBar['Lower']=BBANDS(KBar,timeperiod=BBANDSPeriod)
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 將副圖繪製出來
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['Upper'],color='yellow'))
    addp.append(mpf.make_addplot(Kbar_df['Middle'],color='grey'))
    addp.append(mpf.make_addplot(Kbar_df['Lower'],color='yellow'))
    # 開始繪圖
    ChartKBar(KBar,addp,True)
    
# 繪製K線圖加上BBANDS以及下單紀錄
def ChartOrder_BBANDS(KBar,TR):
    # 將K線轉為DataFrame
    Kbar_df=KbarToDf(KBar)
    # 將副圖繪製出來
    addp=[]
    addp.append(mpf.make_addplot(Kbar_df['Upper'],color='yellow'))
    addp.append(mpf.make_addplot(Kbar_df['Middle'],color='grey'))
    addp.append(mpf.make_addplot(Kbar_df['Lower'],color='yellow'))
    # 開始繪圖
    ChartOrder(KBar,TR,addp,True)
