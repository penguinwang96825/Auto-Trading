#取I020，依照逗點分隔，並將分隔符號去除
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#取得特定時間前的價格資料
p= [int(line[4]) for line in I020 if  int(line[0])<9000000]
#取得特定時間前的總量資料
q= [int(line[6]) for line in I020 if int(line[0])<9000000]

print p[-1],q[-1]

