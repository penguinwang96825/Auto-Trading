# -*- coding: UTF-8 -*-
#載入相關套件
import subprocess

#下單子程式放置位置
ExecPath="./bin/"

#市價單下單
def OrderMKT(Product,BS,Qty):
 OrderNo=subprocess.check_output([ExecPath+"order.exe",Product,BS,"0",Qty,"MKT","IOC","0"]).strip('\r\n')
 while True:
  ReturnInfo=subprocess.check_output([ExecPath+"GetAccount.exe",OrderNo]).strip('\r\n').split(',')
  if len(ReturnInfo)>1:
   return ReturnInfo

#限價單委託
def OrderLMT(Product,BS,Price,Qty):
 OrderNo=subprocess.check_output([ExecPath+"order.exe",Product,BS,Price,Qty,"LMT","ROD","0"]).strip('\r\n')
 return OrderNo

#查詢帳務明細
def QueryOrder(Keyno): 
 ReturnInfo=subprocess.check_output([ExecPath+"GetAccount.exe",Keyno]).strip('\r\n')
 return ReturnInfo.split(',')

#查詢總帳務明細
def QueryAllOrder(): 
 ReturnInfo=subprocess.check_output([ExecPath+"GetAccount.exe","ALL"]).strip('\r\n').split('\r\n')
 ReturnInfo= [ line.split(',') for line in ReturnInfo]
 return ReturnInfo

#查詢未平倉資訊
def QueryOnOpen(): 
 ReturnInfo=subprocess.check_output([ExecPath+"OnOpenInterest.exe"]).strip('\r\n')
 return ReturnInfo.split(',')

#查詢權益數資訊
def QueryRight(): 
 ReturnInfo=subprocess.check_output([ExecPath+"FutureRights.exe"]).strip('\r\n')
 return ReturnInfo.split(',')

#取消委託
def CancelOrder(Keyno):
 ReturnInfo=subprocess.check_output([ExecPath+"order.exe","Delete",Keyno])
 if "cancel send" in ReturnInfo:
  return True
 else:
  return False 

#限價轉刪單
def LMT2DEL(Product,BS,Price,Qty,Sec):
 OrderNo=OrderLMT(Product,BS,Price,Qty)
 StartTime=time.time()
 while time.time()-StartTime<Sec:
  ReturnInfo=QueryOrder(OrderNo)
  if len(ReturnInfo)!=1:
   return ReturnInfo
 CancelOrder(OrderNo)
 return False  

#限價轉市價
def LMT2MKT(Product,BS,Price,Qty,Sec):
 OrderNo=OrderLMT(Product,BS,Price,Qty)
 StartTime=time.time()
 while time.time()-StartTime<Sec:
  ReturnInfo=QueryOrder(OrderNo)
  if len(ReturnInfo)!=1:
   return ReturnInfo
 if CancelOrder(OrderNo):
  ReturnInfo=OrderMKT(Product,BS,Qty)
  return ReturnInfo
