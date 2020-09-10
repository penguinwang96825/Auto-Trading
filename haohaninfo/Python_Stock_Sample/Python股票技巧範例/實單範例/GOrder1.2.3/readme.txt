GOrder_v1.2.3

指令：
輸入 Order.exe Capital/Yuanta查看說明

群益
下單: Order.exe #1 #2 #3 #4 #5 #6 #7
#1. Capital
#2. StockId(ex 2330)
#3. B: Buy, S: Sell
#4. Price
#5. Qty(張數)
#6. 0: 一般, 1: 零股, 2: 盤後
#7. 0: 現貨, 1: 融資, 2: 融券 3: 無券
取消: Order.exe Capital Delete 單號

元大
下單: Order.exe #1 #2 #3 #4 #5 #6 #7
#1. Yuanta
#2. StockId(ex 2330)
#3. B: Buy, S: Sell
#4. Price
#5. Qty(張數)
#6. 0: 一般, 1: 零股, 2: 盤後
#7. 0: 現貨, 1: 融資, 2: 融券 3: 借券
取消: Order.exe Yuanta Delete 單號

凱基證券
下單: Order.exe #1 #2 #3 #4 #5 #6 #7
#1. Kgi
#2. StockId(ex 2330)
#3. B: Buy, S: Sell
#4. Price
#5. Qty(張數)
#6. 0: 一般, 1: 零股, 2: 定價
#7. 0: 現貨, 1: 自資, 2: 自券, 3: 當沖融資, 4: 當沖融券, 5: 無券
取消: Order.exe Kgi Delete 單號

凱基期貨
下單: Order.exe #1 #2 #3 #4 #5 #6 #7
#1. Kgi_Future
#2. ProductId(ex TXFI8)
#3. B: Buy, S: Sell
#4. Price
#5. Qty(口數)
#6. ROD / IOC / FOK
#7. LMT / MKT
取消: Order.exe Kgi Delete 單號

虛擬期貨
下單: Order.exe #1 #2 #3 #4 #5 #6 #7
#1. Simulator
#2. ProductId(ex TXFI8)
#3. B: Buy, S: Sell
#4. Price
#5. Qty(口數)
#6. ROD / IOC / FOK
#7. LMT / MKT
取消: Order.exe Simulator Delete 單號
 
輸入 GetAccount.exe Capital/Yuanta/Kgi/Simulator/Kgi_Future 單號/All 查帳務
輸入 MatchAccount.exe Capital/Yuanta/Kgi/Simulator/Kgi_Future  單號/All 查成交單
輸入 GetInStock.exe Capital/Yuanta/Simulator/Kgi_Future 查庫存
(凱基: GetInStock.exe Kgi 股票代號)
輸入 MatchStock.exe Capital/Yuanta/Kgi/Simulator/Kgi_Future 查詢成交單

