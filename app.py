# coding: utf-8
'''

整體功能描述
Application 主架構

'''

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json
import os

# 載入爬蟲
import NewsSpider
import random

# 載入資料庫
#import CreateSqlite
from CreatePostgresql import Create_PG_SQL

# Heroku專案名稱
pg = Create_PG_SQL()

# 載入基礎設定檔
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding='utf8'))
server_url=secretFileContentJson.get("server_url")
user_ID = secretFileContentJson.get("self_user_id")
#print(secretFileContentJson)

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/data" , static_folder = "./data/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 引用套件
from linebot.models import (
    ImagemapSendMessage,
    TextSendMessage,
    ImageSendMessage,
    LocationSendMessage,
    VideoSendMessage,
    TextMessage,
    FollowEvent,
    MessageEvent,
    PostbackEvent,
    QuickReply, 
    QuickReplyButton,
    PostbackAction,
    FlexSendMessage,
    BubbleContainer,
    FlexSendMessage,
    CarouselContainer,
    MessageAction
)

from linebot.models.template import (
    ButtonsTemplate,CarouselTemplate,ConfirmTemplate,ImageCarouselTemplate
)

from linebot.models.template import *

from urllib.parse import parse_qs 

# 關注事件處理
@handler.add(FollowEvent)
def process_follow_event(event):
    # display_name = 使用者名稱
    # picture_url  = 使用者頭像
    # user_id      = 使用者id
    # select_news  = 使用者選擇的新聞台
    user_profile = vars(line_bot_api.get_profile(event.source.user_id))
    display_name = user_profile["display_name"]
    picture_url = user_profile["picture_url"]
    if user_profile["status_message"]==None:
        status_message = ""
    else:
        status_message = user_profile["status_message"]
    user_id = user_profile["user_id"]
    select_news = "TVBS新聞"
    
    # 記錄資料庫(如果user_id不存在,則新增該使用者資料,否則更新使用者資料)
    user_is_not_exist = len(pg.select_table("select user_id from user_info where user_id='"+user_id+"'"))==0
    if user_is_not_exist:
        pg.insert_data([select_news,display_name,picture_url,status_message,user_id])
    else:
        sql_cmd = "UPDATE user_info set display_name='"+display_name+"'," \
                  "picture_url='"+picture_url+"'," \
                  "status_message=='"+status_message+"' where user_id='"+user_id+"'"
        sql_cmd2 = "select select_news from user_info where user_id='"+user_id+"'"
        select_news = pg.select_table(sql_cmd2)[0][0]

    # 切換新聞台
    linkRichMenuId = open("data/"+select_news+'/rich_menu_id', 'r').read()
    line_bot_api.link_rich_menu_to_user(event.source.user_id,linkRichMenuId)

# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def process_text_message(event):
    # 讀取本地檔案，並轉譯成消息
    result_message_array =[]
    if event.message.text=="#切換新聞台":
        # 切換新聞台
        quickReplyList = QuickReply(items = create_QuickReplyButton(['TVBS新聞', 'Yahoo新聞', '蘋果日報']))
        quickReplyTextSendMessage = TextSendMessage(text='請選擇新聞台', quick_reply=quickReplyList)
        # 發送
        line_bot_api.reply_message(
            event.reply_token,
            quickReplyTextSendMessage
        )
        
    elif event.message.text=="#新聞頭條":
        user_profile = vars(line_bot_api.get_profile(event.source.user_id))
        user_id = user_profile["user_id"]
        select_news = pg.select_table("select select_news from user_info where user_id='"+user_id+"';")[0][0]
        flexCarouselContainerJsonDict = create_news_message(select_news,"首頁")
        if flexCarouselContainerJsonDict!="":
            carouselContent = CarouselContainer.new_from_json_dict(json.loads(flexCarouselContainerJsonDict))
            flexCarouselSendMeesage =  FlexSendMessage(alt_text="新聞頭條", contents=carouselContent)
            # 發送
            line_bot_api.reply_message(
                event.reply_token,
                flexCarouselSendMeesage
            )
    elif event.message.text=="#新聞類別":
        user_profile = vars(line_bot_api.get_profile(event.source.user_id))
        user_id = user_profile["user_id"]
        select_news = pg.select_table("select select_news from user_info where user_id='"+user_id+"';")[0][0]
        if select_news=="TVBS新聞":
            # 切換類別
            quickReplyList = QuickReply(items = create_QuickReplyButton(['焦點','地方社會','娛樂']))
            quickReplyTextSendMessage = TextSendMessage(text='請選擇類別', quick_reply=quickReplyList)
            # 發送
            line_bot_api.reply_message(
                event.reply_token,
                quickReplyTextSendMessage
            )
        elif select_news=="Yahoo新聞":
            # 切換類別
            quickReplyList = QuickReply(items = create_QuickReplyButton(['選舉','財金','娛樂','運動']))
            quickReplyTextSendMessage = TextSendMessage(text='請選擇類別', quick_reply=quickReplyList)
            # 發送
            line_bot_api.reply_message(
                event.reply_token,
                quickReplyTextSendMessage
            )
        elif select_news=="蘋果日報":
            # 切換類別
            quickReplyList = QuickReply(items = create_QuickReplyButton(['焦點','政治','娛樂','生活']))
            quickReplyTextSendMessage = TextSendMessage(text='請選擇類別', quick_reply=quickReplyList)
            # 發送
            line_bot_api.reply_message(
                event.reply_token,
                quickReplyTextSendMessage
            )
    elif event.message.text=="#隨機新聞":
        user_profile = vars(line_bot_api.get_profile(event.source.user_id))
        user_id = user_profile["user_id"]
        select_news = pg.select_table("select select_news from user_info where user_id='"+user_id+"';")[0][0]
        if select_news=="TVBS新聞":
            class_array = ['首頁','焦點','地方社會','娛樂']
            select_class = class_array[random.randint(0, len(class_array)-1)]
            flexCarouselContainerJsonDict = create_news_message(select_news,select_class)
            if flexCarouselContainerJsonDict!="":
                carouselContent = CarouselContainer.new_from_json_dict(json.loads(flexCarouselContainerJsonDict))
                flexCarouselSendMeesage =  FlexSendMessage(alt_text="隨機新聞", contents=carouselContent)
                # 發送
                line_bot_api.reply_message(
                    event.reply_token,
                    flexCarouselSendMeesage
                )
        elif select_news=="Yahoo新聞":
            class_array = ['首頁','選舉','財金','娛樂','運動']
            select_class = class_array[random.randint(0, len(class_array)-1)]
            flexCarouselContainerJsonDict = create_news_message(select_news,select_class)
            if flexCarouselContainerJsonDict!="":
                carouselContent = CarouselContainer.new_from_json_dict(json.loads(flexCarouselContainerJsonDict))
                flexCarouselSendMeesage =  FlexSendMessage(alt_text="Yahoo新聞", contents=carouselContent)
                # 發送
                line_bot_api.reply_message(
                    event.reply_token,
                    flexCarouselSendMeesage
                )
        elif select_news=="蘋果日報":
            class_array = ['首頁','焦點','政治','娛樂','生活']
            select_class = class_array[random.randint(0, len(class_array)-1)]
            flexCarouselContainerJsonDict = create_news_message(select_news,select_class)
            if flexCarouselContainerJsonDict!="":
                carouselContent = CarouselContainer.new_from_json_dict(json.loads(flexCarouselContainerJsonDict))
                flexCarouselSendMeesage =  FlexSendMessage(alt_text="蘋果日報", contents=carouselContent)
                # 發送
                line_bot_api.reply_message(
                    event.reply_token,
                    flexCarouselSendMeesage
                )
        
    elif "#" in event.message.text:
        user_profile = vars(line_bot_api.get_profile(event.source.user_id))
        user_id = user_profile["user_id"]
        select_news = pg.select_table("select select_news from user_info where user_id='"+user_id+"';")[0][0]
        select_class = event.message.text.replace("#","")
        flexCarouselContainerJsonDict = create_news_message(select_news,select_class)
        if flexCarouselContainerJsonDict!="":
            carouselContent = CarouselContainer.new_from_json_dict(json.loads(flexCarouselContainerJsonDict))
            flexCarouselSendMeesage =  FlexSendMessage(alt_text="#", contents=carouselContent)
            # 發送
            line_bot_api.reply_message(
                event.reply_token,
                flexCarouselSendMeesage
            )

@handler.add(PostbackEvent)
def process_postback_event(event):
    query_string_dict = parse_qs(event.postback.data)
    user_profile = vars(line_bot_api.get_profile(event.source.user_id))
    user_id = user_profile["user_id"]
    if "menu" in query_string_dict.keys():
        pg.update_data(user_id,query_string_dict["menu"][0])
        linkRichMenuId = open("data/"+query_string_dict.get('menu')[0]+'/rich_menu_id', 'r').read()
        # link_rich_menu_to_user : 更換選單指令
        line_bot_api.link_rich_menu_to_user(event.source.user_id,linkRichMenuId)

        # 新聞頭條
        flexCarouselContainerJsonDict = create_news_message(query_string_dict.get('menu')[0],"首頁")
        if flexCarouselContainerJsonDict!="":
            carouselContent = CarouselContainer.new_from_json_dict(json.loads(flexCarouselContainerJsonDict))
            flexCarouselSendMeesage =  FlexSendMessage(alt_text="新聞頭條", contents=carouselContent)
            # 發送
            line_bot_api.reply_message(
                event.reply_token,
                flexCarouselSendMeesage
            )

def create_news_element(img_url,title_text,web_url):
    result = """{
                "type": "bubble",
                "hero": {
                  "type": "image",
                  "url": "%s",
                  "size": "full",
                  "aspectRatio": "20:13",
                  "aspectMode": "cover",
                  "action": {
                    "type": "uri",
                    "label": "Action",
                    "uri": "%s"
                  }
                },
                "footer": {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "uri",
                        "label": "%s",
                        "uri": "%s"
                      }
                    }
                  ]
                }
              }""" % (img_url,web_url,title_text,web_url)
    return result

def create_news_message(select_news,select_class):
    if select_news=="TVBS新聞":
        if select_class=="首頁":
            news_dict = NewsSpider.tvbsNews_title()
        elif select_class=="焦點":
            news_dict = NewsSpider.tvbsNews_politics()
        elif select_class=="地方社會":
            news_dict = NewsSpider.tvbsNews_local()
        elif select_class=="娛樂":
            news_dict = NewsSpider.tvbsNews_entertainment()
        else:
            return ""
    elif select_news=="Yahoo新聞":
        if select_class=="首頁":
            news_dict = NewsSpider.yahooNews_title()
        elif select_class=="選舉":
            news_dict = NewsSpider.yahooNews_election()
        elif select_class=="財金":
            news_dict = NewsSpider.yahooNews_money()
        elif select_class=="娛樂":
            news_dict = NewsSpider.yahooNews_entertainment()
        elif select_class=="運動":
            news_dict = NewsSpider.yahooNews_sports()
        else:
            return ""
    elif select_news=="蘋果日報":
        if select_class=="首頁":
            news_dict = NewsSpider.appledailyNews_title()
        elif select_class=="焦點":
            news_dict = NewsSpider.appledailyNews_recommend()
        elif select_class=="政治":
            news_dict = NewsSpider.appledailyNews_politics()
        elif select_class=="娛樂":
            news_dict = NewsSpider.appledailyNews_entertainment()
        elif select_class=="生活":
            news_dict = NewsSpider.appledailyNews_life()
        else:
            return ""
    else:
        return ""
    result = ""
    for i in range(min(len(news_dict),5)):
        result += create_news_element(news_dict[i]["image"],news_dict[i]["title"],news_dict[i]["url"])+","
    result2 = """{"type": "carousel","contents": [%s]}""" % result.strip(",")
    return result2

def create_QuickReplyButton(news_array):
    result = []
    if ('TVBS新聞' in news_array) and ('Yahoo新聞' in news_array) and ('蘋果日報' in news_array):
        for item in news_array:
            result.append(QuickReplyButton(action=PostbackAction(label=item,display_text='#'+item,data="menu="+item)))
        return result
    else:
        for item in news_array:
            result.append(QuickReplyButton(action=MessageAction(label=item, text='#'+item)))
        return result
    
if __name__ == "__main__":
    # 本地執行
    #app.run(host='0.0.0.0')
    
    # 雲端執行
    app.run(host='0.0.0.0',port=os.environ['PORT'])