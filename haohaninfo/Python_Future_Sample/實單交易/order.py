# -*- coding: UTF-8 -*-
#載入相關套件
import subprocess,time,haohaninfo

#下單子程式放置位置
ExecPath="C:/OrderCmd/GOrder/"

#送出交易委託
def Order(BrokerID,Product,BS,Price,Qty,OrderMethod,OrderType):
    OrderNo=subprocess.check_output([ExecPath+"Order.exe",BrokerID,Product,BS,Price,Qty,OrderMethod,OrderType,'0']).decode('cp950').strip('\r\n')
    return OrderNo

#取得下單帳務
def MatchAccount(BrokerID,OrderNo):
    OrderInfo=subprocess.check_output([ExecPath+"MatchAccount.exe",BrokerID,OrderNo]).decode('cp950').split('\r\n')
    if OrderInfo[0]=='over':
        return False
    else:
        OrderInfo = [ i.split(',') for i in OrderInfo ]
        return OrderInfo

#下單並取得帳務回傳
def OrderAndMatchAccount(BrokerID,Product,BS,Price,Qty,OrderMethod,OrderType):
    OrderNo=Order(BrokerID,Product,BS,Price,Qty,OrderMethod,OrderType)
    if OrderNo != '委託失敗':
        while 1:
            OrderInfo=MatchAccount(BrokerID,OrderNo)
            if OrderInfo != False:
                return OrderInfo
            else:
                print('尚未成交')
            time.sleep(2)
    else:
        print('下單失敗')
        return False

#下單並取得帳務回傳(package)
def OrderAndMatchAccountByhaohaninfo(BrokerID,Product,BS,Price,Qty,OrderMethod,OrderType):
    Go = haohaninfo.GOrder.GOCommand()
    OrderNo=Go.Order(BrokerID,Product,BS,Price,Qty,OrderMethod,OrderType)
    if OrderNo != '委託失敗':
        while 1:
            OrderInfo=Go.MatchAccount(BrokerID,OrderNo)
            if len(OrderInfo) != 0:
                return OrderInfo
            else:
                print('尚未成交')
            time.sleep(2)
    else:
        print('下單失敗')
        return False

#取消委託
def CancelOrder(BrokerID,OrderNo):
    CancelInfo=subprocess.check_output([ExecPath+"Order.exe",BrokerID,'Delete',OrderNo]).decode('cp950').split('\n')
    if CancelInfo[0] == '1':
        return True
    else:
        return False

#取得總帳務            
def GetAllAccount(BrokerID):
    AccInfo=subprocess.check_output([ExecPath+"GetAccount.exe",BrokerID,'All']).decode('cp950').split('\r\n')
    return AccInfo
                
#取得未平倉資訊
def GetStock(BrokerID):
    StockInfo=subprocess.check_output([ExecPath+"GetInStock.exe",BrokerID]).decode('cp950').split('\r\n')
    return StockInfo


#委託到期刪單
def LMT2DEL(BrokerID,Product,BS,Price,Qty,Sec):
    OrderNo=Order(BrokerID,Product,BS,Price,Qty,'ROD','LMT')
    StartTime=time.time()
    if OrderNo != '委託失敗':
        while time.time()-StartTime<Sec:
            time.sleep(2)
            OrderInfo=MatchAccount(BrokerID,OrderNo)
            if OrderInfo != False:
                return OrderInfo   
            else:
                print('尚未成交')
        CancelOrder(BrokerID,OrderNo)     
        return False
    else:
        print('下單失敗')
        return False        

#委託到期刪單(package)
def LMT2DELByhaohaninfo(BrokerID,Product,BS,Price,Qty,Sec):
    Go = haohaninfo.GOrder.GOCommand()
    OrderNo=Go.Order(BrokerID,Product,BS,Price,Qty,'ROD','LMT')
    StartTime=time.time()
    if OrderNo != '委託失敗':
        while time.time()-StartTime<Sec:
            time.sleep(2)
            OrderInfo=Go.MatchAccount(BrokerID,OrderNo)
            if len(OrderInfo) != 0:
                return OrderInfo
            else:
                print('尚未成交')
        Go.Delete(BrokerID,OrderNo)
        return False
    else:
        print('下單失敗')
        return False


#委託到期轉市價單
def LMT2MKT(BrokerID,Product,BS,Price,Qty,Sec):
    OrderNo=Order(BrokerID,Product,BS,Price,Qty,'ROD','LMT')
    StartTime=time.time()
    if OrderNo != '委託失敗':
        while time.time()-StartTime<Sec:
            time.sleep(2)
            OrderInfo=MatchAccount(BrokerID,OrderNo)
            if OrderInfo != False:
                return OrderInfo   
            else:
                print('尚未成交')
        CancelOrder(BrokerID,OrderNo)        
        OrderInfo = OrderAndMatchAccount(BrokerID,Product,BS,Price,Qty,'IOC','MKT')
        return OrderInfo
    else:
        print('下單失敗')
        return False        
        
#委託到期轉市價單(package)
def LMT2MKTByhaohaninfo(BrokerID,Product,BS,Price,Qty,Sec):
    Go = haohaninfo.GOrder.GOCommand()
    OrderNo=Go.Order(BrokerID,Product,BS,Price,Qty,'ROD','LMT')
    StartTime=time.time()
    if OrderNo != '委託失敗':
        while time.time()-StartTime<Sec:
            time.sleep(2)
            OrderInfo=Go.MatchAccount(BrokerID,OrderNo)
            if len(OrderInfo) != 0:
                return OrderInfo
            else:
                print('尚未成交')
        Go.Delete(BrokerID,OrderNo)
        OrderInfo = OrderAndMatchAccountByhaohaninfo(BrokerID,Product,BS,Price,Qty,'IOC','MKT')    
        return OrderInfo
    else:
        print('下單失敗')
        return False

            