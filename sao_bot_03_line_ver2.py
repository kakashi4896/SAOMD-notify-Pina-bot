# https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/

# 需要安裝的
# pip3 install beautifulsoup4
# pip3 install line-bot-sdk

# crontab排程設定
# crontab -e
# 30 14 * * * /home/kakashi4896/pina.sh

# 查看crontab執行log
# sudo tail -f /var/mail/kakashi4896


#==============================================
import time
import datetime

# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
import requests

# import line bot 
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 下載網頁內容
# https://python-learnnotebook.blogspot.com/2019/12/beautifulsoup-object-of-type-response.html
r = (requests.get('https://api-defrag-ap.wrightflyer.net/webview/announcement?phone_type=2&lang=tc&fbclid=IwAR2x9O3yry0tPy95dCmt27WM2CO03GfH1UDDX_9a22v2lqOctfGqhvo5VWI')).content

# 以 Beautiful Soup 解析 HTML 程式碼
soup = BeautifulSoup(r, 'html.parser')

# 輸出排版後的 HTML 程式碼
#print(soup.prettify())

# 所有的超連結
dl_tags = soup.find_all("dl")

event_list=[]
for tag in dl_tags:
    # 公告內容
    h2=tag.find("h2")
    if h2!=None:
        h2=h2.string # 輸出超連結的文字
        
        xx=[] #[event name, event start, event end]
        if '故事解放活動' in h2: #event
            # 公告日期
            #dt=tag.find("dt")
            #print(dt.string)
            print(h2)
            xx.append(h2)
            
            # 活動期間
            h3=tag.find("h3")
            if (h3!=None) and (h3.string!=None):
                h3=h3.string
                print(h3)
                # 切出活動開始與截止日
                deadline_range=h3.split(' ~ ')
                event_start=deadline_range[0].split('(')[0]
                event_deadline=deadline_range[1].split('(')[0]
                xx.append(event_start)
                xx.append(event_deadline)
                
                event_list.append(xx)
                
            print("")
        
        elif '多人組隊活動' in h2: #event
            # 公告日期
            #dt=tag.find("dt")
            #print(dt.string)
            print(h2)
            xx.append(h2)
            
            # 活動期間
            h3=tag.find("h3")
            if (h3!=None) and (h3.string!=None):
                h3=h3.string
                print(h3)
                # 切出活動開始與截止日
                deadline_range=h3.split(' ~ ')
                event_start=deadline_range[0].split('(')[0]
                event_deadline=deadline_range[1].split('(')[0]
                xx.append(event_start)
                xx.append(event_deadline)
                
                event_list.append(xx)
                
            print("")
            
        elif '裝備交換活動' in h2: #event
            # 公告日期
            #dt=tag.find("dt")
            #print(dt.string)
            print(h2)
            xx.append(h2)
            
            # 活動期間
            h3=tag.find("h3")
            if (h3!=None) and (h3.string!=None):
                h3=h3.string
                print(h3)
                # 切出活動開始與截止日
                deadline_range=h3.split(' ~ ')
                event_start=deadline_range[0].split('(')[0]
                event_deadline=deadline_range[1].split('(')[0]
                xx.append(event_start)
                xx.append(event_deadline)
                
                event_list.append(xx)
                
            print("")
            
        elif '排名' in h2: #event
            # 公告日期
            #dt=tag.find("dt")
            #print(dt.string)
            print(h2)
            xx.append(h2)
            
            # 活動期間
            h3=tag.find("h3")
            if (h3!=None) and (h3.string!=None):
                h3=h3.string
                print(h3)
                # 切出活動開始與截止日
                deadline_range=h3.split(' ~ ')
                event_start=deadline_range[0].split('(')[0]
                event_deadline=deadline_range[1].split('(')[0]
                xx.append(event_start)
                xx.append(event_deadline)
                
                #event_list.append(xx)
                event_list.insert(0,xx)
                
            print("")
    
#print(len(dl_tags))
#print(event_list)

# 生成訊息內容(每日報告活動日程)
notify_list=""
for i in range(len(event_list)):
    notify_list=notify_list+"\n\n"+event_list[i][0]+"\n活動期間"+event_list[i][1]+"~"+event_list[i][2]

# 生成訊息內容(明天截止的活動)
notify_list_deadline=""
for i in range(len(event_list)):
    #活動截止日期
    dead_mon=int(event_list[i][2].split('/')[0])
    dead_day=int(event_list[i][2].split('/')[1])
    
    #明天
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1))
    tomorrow_ts = int(time.mktime(tomorrow.timetuple()))
    tomorrow_array = time.localtime(tomorrow_ts)
    tomorrow_mon= int(tomorrow_array.tm_mon)
    tomorrow_day= int(tomorrow_array.tm_mday)
    
    #判斷並生成訊息
    if (dead_mon==tomorrow_mon) and (dead_day==tomorrow_day):
        if notify_list_deadline=="":
            notify_list_deadline=notify_list_deadline+"\n【明天截止提醒】"
            
        notify_list_deadline=notify_list_deadline+"\n\n"+event_list[i][0]+"\n活動期間"+event_list[i][1]+"~"+event_list[i][2]

# 訊息合併
if notify_list_deadline!="":
    notify_list=notify_list_deadline+"\n\n【活動列表】"+notify_list
    
'''
# line bot msg
line_bot_api = LineBotApi('CPPrW02bu4Zd/1XBHX1XIZvGA4x/5YdUsdsh7ykw+/9RwhyqDAsyj+L38/EAD/DxNS7SbnlGd/YVHzME0kQyrbqcVJyzpDGMwN/pt9VtvFIKBqmcAYKPjTFPcg2LXacl79wseAkwK73UQ4avFY8e/gdB04t89/1O/w1cDnyilFU=') #YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('fc2bfae242d0209aefb2ee7b4ba5cad9') #YOUR_CHANNEL_SECRET

#line_bot_api.broadcast(TextSendMessage(text='test broadcast msg'))
line_bot_api.broadcast(TextSendMessage(text=str(event_list))
'''

# line notify msg
# self
headers = {
    "Authorization": "Bearer " + "<put_your_key>", # token
    "Content-Type": "application/x-www-form-urlencoded"
}

params = {"message": str(notify_list)}

r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)

time.sleep(1)

'''
# group
headers = {
    "Authorization": "Bearer " + "3sUDc9ZCg5WsaeEPFsl3EpLFODKPcslMCc2IaqmKiMi", # token
    "Content-Type": "application/x-www-form-urlencoded"
}
 
params = {"message": str(notify_list)}

r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
'''                      
#print(r.status_code)  #200


# 後續事項
# 與今天的日期做比較，找出需要提醒的項目(用int比較就沒有補0的問題了)
# 1. 今天開始的新活動
