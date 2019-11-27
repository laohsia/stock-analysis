import pandas as pd
import requests
from bs4 import BeautifulSoup


stocknumber = input("請輸入股票代號: ")
url = 'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=' + stocknumber
url2 = 'https://goodinfo.tw/StockInfo/ShowBuySaleChart.asp?STOCK_ID=' + stocknumber + '&CHT_CAT=DATE'
url3 = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=' + stocknumber
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
r = requests.get(url, headers = headers)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.find('div', {"id" : "divDetail"}).find('table', {"class": "solid_1_padding_4_0_tbl"})
dfs = pd.read_html(str(rows))


def stockprice():
    data = soup.find("table", {"class": "solid_1_padding_3_2_tbl"})
    dfs1 = pd.read_html(str(data))
    price = dfs1[0].iloc[2][0]#抓取股價
    print("股價: ", price)

def profit():
    num = 0
    money = []
    for i in (0,1,2,3,4):
        if dfs[0].iloc[i][7] == 0:
            print("股利發放中斷")
            break
        else:
            money.append(float(dfs[0].iloc[i][7]))#抓取發放股利
            num += 1
    print("連續",num,"年發放股利")
    print("平均股利: " ,format(sum(money)/len(money), ".2f"))
    profits = sum(money)/len(money)
    

def dividend():
    dividend = []
    for i in (0,1,2,3,4):
        data = float(dfs[0].iloc[i][20])
        dividend.append(data)#抓取殖利率
    print("過去五年平均殖利率: " ,format(sum(dividend)/len(dividend), ".2f"))

def how_many_stock():
    cash = input("請輸入預算金額: ")
    data = soup.find("table", {"class": "solid_1_padding_3_2_tbl"})
    dfs1 = pd.read_html(str(data))
    price = dfs1[0].iloc[2][0]
    quantity = format(int(cash)/float(price), ".2f")
    print("共可買", quantity, "股") #預算金額可買股數

    money = [] #重新抓取平均股利
    for i in (0,1,2,3,4):
        money.append(float(dfs[0].iloc[i][7]))
    profits = sum(money)/len(money)

    plus = profits *float(quantity) #以平均股利計算一年後股息
    print("預估一年後可領股息: ", plus, "元")

def foreign():
    r = requests.get(url2, headers = headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find('table', {'class': 'solid_1_padding_4_2_tbl' , 'style' : 'font-size:11pt;line-height:18px;'})
    dfs1 = pd.read_html(str(data))
    foreign = dfs1[0].iloc[1][4]
    if foreign.count("+") :
        print("外資五日內買超 ", foreign.split("(")[0] , "張")
    elif foreign.count("-"):
        print("外資五日內賣超 ", foreign.split("(")[0] , "張")

    data1 = soup.find('div', {'id':'divBuySaleDetail'}).find('table', {'class': 'solid_1_padding_4_1_tbl' , 'style' : 'font-size:10pt;line-height:17px;'})
    dfs2 = pd.read_html(str(data1))
    buysale = []
    for i in range(59):
        buysale.append(float(dfs2[0].iloc[i][9]))
    print("60日外資平均占比(%): ", format(sum(buysale)/len(buysale), ".2f"))

def ROE():
    r = requests.get(url3, headers = headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find('div', {'id':'divFinDetail'}).find('table', {'class':'solid_1_padding_4_0_tbl'})
    dfs = pd.read_html(str(rows))
    print("去年ROE表現(%): ",dfs[0].iloc[1][16])
    
def main():
    how_many_stock()
    stockprice()
    profit()
    dividend()
    ROE()
    foreign()


main()    

