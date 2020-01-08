__author__ = 'user'

import json
import requests
from bs4 import BeautifulSoup
import psycopg2
import datetime

def find_all_by_list(obj,myList):
    if len(myList)==1:
        return obj.find_all(myList[0])
    else:
        return obj.find_all(myList[0],myList[1])

def get_dataList(obj,myList,result):
    if len(myList)==1:
        a = find_all_by_list(obj,myList[0])
        element = []
        for item in a:
            
            element.append(item)
        result += element
        return result
    else:
        a = find_all_by_list(obj, myList[0])
        for item in a:
            result = get_dataList(item,myList[1:],result)
    return result

def get_html_dataList(url,myList):
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    return get_dataList(w, myList, [])

# (Yahoo新聞)+(首頁)
def yahooNews_title():
    result = []
    url = "https://tw.news.yahoo.com/_td-news/api/resource/content;fetchNewAttribution=true;getDetailView=true;getFullLcp=false;imageResizer=null;relatedContent=%7B%22enabled%22%3Atrue%7D;site=news;uuids=%5B%2222e870d8-01ec-3696-9835-97380f9681a8%22%2C%22760b2785-659e-3745-b848-f7320fdaacdc%22%2C%228c4d8ba4-d0e8-328e-bcf6-877fa04ddf21%22%2C%22ba5caae3-e0ae-3d92-9066-8b823ef0ae5d%22%2C%22d50907f3-d918-3b45-bbe5-060fdae59f32%22%2C%2253728cbf-21d4-31de-b67e-b1724d0d657c%22%2C%22580cfb14-b733-3480-b9b4-fa50b7e5da3e%22%2C%229466f332-8049-3db9-a464-3a3b8a8f3edf%22%2C%22932048f4-6715-3f37-ac55-eaa5fe3b9ef6%22%2C%228e11a60d-9df7-3f08-936e-d27d0c7a3e6b%22%2C%2222ef336a-7ffe-3859-819c-173d73a1a2c1%22%2C%222acef27d-a39e-3ceb-a914-4c50f85c8900%22%2C%224530ee05-78bc-391c-9301-4dbbea58d9d5%22%2C%224153f39a-61d5-3731-b72d-0ebeddb52057%22%2C%229f278fb1-21c3-36a0-befe-b5bad643a9ab%22%2C%228d5ac7f2-55be-3d24-afef-c7615598c999%22%2C%2280ab1ba1-4bb4-31ed-95c6-90c8db836987%22%2C%22332d63ef-fb6d-3c7c-9e22-a8f369c8357d%22%2C%227b726647-689e-3481-9c8f-5082655ee71e%22%2C%222d68da43-f080-367d-bd4a-9f8c4dcbd159%22%5D?bkt=TW-Non-NCP-stream-applet-control&device=desktop&feature=videoDocking&intl=tw&lang=zh-Hant-TW&partner=none&prid=4j66bp9f02nns&region=TW&site=news&tz=Asia%2FTaipei&ver=2.3.1325&returnMeta=true"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "accept":"application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    )
    myJson = json.loads(r.text)
    for item in myJson["data"]["items"]:
        item2 = {}
        item2["title"] = item["title"]
        item2["url"] = item["url"]
        try:
            item2["image"] = item["bodyImages"][0]["size"]["original"]["url"]
        except:
            item2["image"] = "https://aberrance.in/wp-content/uploads/2018/10/http-error-404-not-found.png"
        result.append(item2)
    return result
    
# (Yahoo新聞)+(選舉)
def yahooNews_election():
    result = []
    url = "https://news.campaign.yahoo.com.tw/2020election/ajax_index.php"
    r = requests.post(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "accept":"application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        data={"uuid": "6aa9e8e0-017d-11e8-bfb2-adcdba4e7721"}
    )
    myJson = json.loads(r.text)
    for item in myJson["data"]["mainStream"]["stream"]:
        item2 = {}
        item2["title"] = item["content"]["title"]
        item2["url"] = item["content"]["canonicalUrl"]["url"]
        item2["image"] = item["content"]["thumbnail"]["originalUrl"]
        result.append(item2)
    return result

# (Yahoo新聞)+(財金)
def yahooNews_money():
    result = []
    url = "https://tw.news.yahoo.com/_td-news/api/resource/content;fetchNewAttribution=true;getDetailView=true;getFullLcp=false;imageResizer=null;relatedContent=%7B%22enabled%22%3Atrue%7D;site=news;uuids=%5B%22205fbbc6-0d6b-3b71-b559-d5bcf39df7a2%22%2C%22737e2313-e1a5-3c48-abd1-b3b42269d5dc%22%2C%22e7769c2f-6272-3e49-8837-69521a175fcd%22%2C%22851ad841-09eb-32c3-aa5c-bdcf8ce73476%22%2C%22d88b783d-2d2d-381b-ac8d-3441da96e4f7%22%2C%22b4b705f1-5991-3b39-8203-daf920c2337f%22%2C%222251fd94-ef98-3eb0-95eb-a97a283cb59b%22%2C%225950c873-c8ca-3222-8fb8-f1f97cc082df%22%2C%22afa81ee7-6bb4-30e2-86d7-ad4afad46433%22%2C%22f485e87f-327c-3ae5-bc01-ce574feb503f%22%2C%2265fa091b-6089-3263-8db4-ee0fc10e166a%22%2C%22a3a4f3d3-1425-3bd5-9ef1-ee6d031fb599%22%2C%22ccd87825-4a12-361e-8074-3a980c57f4bf%22%5D?bkt=TW-Non-NCP-stream-applet-control&device=desktop&feature=videoDocking&intl=tw&lang=zh-Hant-TW&partner=none&prid=449nfj5f02p9h&region=TW&site=news&tz=Asia%2FTaipei&ver=2.3.1325&returnMeta=true"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "accept":"application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    )
    myJson = json.loads(r.text)
    for item in myJson["data"]["items"]:
        item2 = {}
        item2["title"] = item["title"]
        item2["url"] = item["url"]
        try:
            item2["image"] = item["bodyImages"][0]["size"]["original"]["url"]
        except:
            item2["image"] = "https://aberrance.in/wp-content/uploads/2018/10/http-error-404-not-found.png"
        result.append(item2)
    return result

# (Yahoo新聞)+(娛樂)
def yahooNews_entertainment():
    result = []
    url = "https://tw.news.yahoo.com/_td-news/api/resource/content;fetchNewAttribution=true;getDetailView=true;getFullLcp=false;imageResizer=null;relatedContent=%7B%22enabled%22%3Atrue%7D;site=news;uuids=%5B%22dca43819-6594-3ebb-bc64-5a3fe1fc2566%22%2C%2220375e6e-e544-3474-b460-d956dbb7e93e%22%2C%224c250227-b660-3628-b076-9052b58cf7f9%22%2C%225a2194a8-c079-3735-bf90-0ee2bbbc93b2%22%2C%228d6956ba-6e5a-3533-8706-c13973bcc6bb%22%2C%22468fa73c-ad66-3b90-b668-5f824ff50206%22%2C%22cbd8a452-e54e-376f-bc9b-596abe723370%22%2C%22f30667eb-9e41-3cce-aa3f-06d775a2bea1%22%2C%229a6c1373-b900-35b1-aabf-fdeb3a0446cf%22%2C%22964b967b-54aa-3cf3-99e9-33856d7eb38f%22%2C%22b538b5a7-db57-3c34-85f8-f5a28b2a5a6f%22%2C%220c64c6e0-4f4d-3bc6-9189-0a7064f1e3ce%22%2C%22d99bd532-e76c-32e1-8c5b-4dd3fcf54f0e%22%5D?bkt=TW-Non-NCP-stream-applet-control&device=desktop&feature=videoDocking&intl=tw&lang=zh-Hant-TW&partner=none&prid=6pnqcklf02pit&region=TW&site=news&tz=Asia%2FTaipei&ver=2.3.1325&returnMeta=true"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "accept":"application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    )
    myJson = json.loads(r.text)
    for item in myJson["data"]["items"]:
        item2 = {}
        item2["title"] = item["title"]
        item2["url"] = item["url"]
        try:
            item2["image"] = item["bodyImages"][0]["size"]["original"]["url"]
        except:
            item2["image"] = "https://aberrance.in/wp-content/uploads/2018/10/http-error-404-not-found.png"
        result.append(item2)
    return result

# (Yahoo新聞)+(運動)
def yahooNews_sports():
    result = []
    url = "https://tw.news.yahoo.com/_td-news/api/resource/content;fetchNewAttribution=true;getDetailView=true;getFullLcp=false;imageResizer=null;relatedContent=%7B%22enabled%22%3Atrue%7D;site=news;uuids=%5B%222ab3ca9f-fd77-3e57-a2ec-af146229eea1%22%2C%22fb5a4558-d1aa-3dfd-bde2-cb8e047f8f9d%22%2C%226216a51c-70e6-3fd9-8465-2b452c58ddbb%22%2C%22b15d4372-ba54-3e45-bcfd-3bff20e23872%22%2C%22ab88f167-48c3-3029-abf0-996dc9abe03f%22%2C%22e8cbbb5e-8bc0-3cb8-9bb8-5a427f1d381e%22%2C%222d585149-6c99-342b-8e1b-ea4d8b9b1d96%22%2C%2245c76df1-2421-39b5-a468-b50ace286e3c%22%2C%22e2ed7775-11bd-3bfb-b791-72404174bafb%22%2C%22229f8361-01a6-3893-9ddd-607e3d697746%22%2C%2280590d54-f09f-3399-a0b2-aff5dd274996%22%2C%220d6b63e4-8094-3ae3-8c1a-fecfd4837257%22%2C%227800b3ef-8cee-3899-b924-835c091f6633%22%5D?bkt=TW-Non-NCP-stream-applet-control&device=desktop&feature=videoDocking&intl=tw&lang=zh-Hant-TW&partner=none&prid=e4h9np9f02qgc&region=TW&site=news&tz=Asia%2FTaipei&ver=2.3.1325&returnMeta=true"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "accept":"application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    )
    myJson = json.loads(r.text)
    for item in myJson["data"]["items"]:
        item2 = {}
        item2["title"] = item["title"]
        item2["url"] = item["url"]
        try:
            item2["image"] = item["bodyImages"][0]["size"]["original"]["url"]
        except:
            item2["image"] = "https://aberrance.in/wp-content/uploads/2018/10/http-error-404-not-found.png"
        result.append(item2)
    return result

# (TVBS新聞)+(首頁)
def tvbsNews_title():
    url = "https://news.tvbs.com.tw/"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"class": "content_center_kv_total"})
    result = []
    def get_Image(a,result):
        for item in a:
            a2 = item.find_all("div", {"class": "img"})
            for item2 in a2:
                a3 = item2.find_all("img")
                for item3 in a3:
                    result.append({"image":item3["src"]})
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                result[index]["url"] = "https://news.tvbs.com.tw/"+item2["href"]
                index += 1
        return result

    def get_Title(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("div",{"class":"txtbox"})
            for item2 in a2:
                result[index]["title"] = item2.text.replace("\u3000"," ")
                index += 1
        return result

    get_Image(a,result)
    get_Title(a,result)
    get_Url(a,result)
    return result

# (TVBS新聞)+(焦點)
def tvbsNews_politics():
    url = "https://news.tvbs.com.tw/politics"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"class": "masterVision1_box_main"})
    result = []
    def get_Image(a,result):
        for item in a:
            a2 = item.find_all("div", {"class": "img"})
            for item2 in a2:
                a3 = item2.find_all("img")
                for item3 in a3:
                    result.append({"image":item3["src"]})
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                result[index]["url"] = "https://news.tvbs.com.tw/"+item2["href"]
                index += 1
        return result

    def get_Title(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                a3 = item2.find_all("h1")
                for item3 in a3:
                    result[index]["title"] = item3.text.replace("\u3000"," ")
                index += 1
        return result

    get_Image(a,result)
    get_Title(a,result)
    get_Url(a,result)
    return result

# (TVBS新聞)+(地方社會)
def tvbsNews_local():
    url = "https://news.tvbs.com.tw/local"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"class": "masterVision1_box_main"})
    result = []
    def get_Image(a,result):
        for item in a:
            a2 = item.find_all("div", {"class": "img"})
            for item2 in a2:
                a3 = item2.find_all("img")
                for item3 in a3:
                    result.append({"image":item3["src"]})
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                result[index]["url"] = "https://news.tvbs.com.tw/"+item2["href"]
                index += 1
        return result

    def get_Title(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                a3 = item2.find_all("h1")
                for item3 in a3:
                    result[index]["title"] = item3.text.replace("\u3000"," ")
                index += 1
        return result

    get_Image(a,result)
    get_Title(a,result)
    get_Url(a,result)
    return result

# (TVBS新聞)+(娛樂)
def tvbsNews_entertainment():
    url = "https://news.tvbs.com.tw/entertainment"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"id": "pc_star_kv_list"})
    result = []
    def get_Image(a,result):
        for item in a:
            a2 = item.find_all("div", {"class": "star_kv_list1_R"})
            for item2 in a2:
                a3 = item2.find_all("div",{"class":"img"})
                for item3 in a3:
                    a4 = item3.find_all("img")
                    for item4 in a4:
                        result.append({"image":item4["src"]})
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("div", {"class": "star_kv_list1_R"})
            for item2 in a2:
                a3 = item2.find_all("div",{"class":"img"})
                for item3 in a3:
                    a4 = item3.find_all("a")
                    for item4 in a4:
                        result[index]["url"] = "https://news.tvbs.com.tw"+item4["href"]
                        index += 1
        return result

    def get_Title(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("div", {"class": "star_kv_list1_R"})
            for item2 in a2:
                a3 = item2.find_all("div",{"class":"txt"})
                for item3 in a3:
                    result[index]["title"] = item3.text
                    index += 1
        return result

    get_Image(a,result)
    get_Title(a,result)
    get_Url(a,result)
    return result

# 蘋果日報+首頁
def appledailyNews_title():
    url = "https://tw.appledaily.com/index/videoajax/StartRow/0/201510271456"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"id": "ajaxlist"})
    result = []
    def get_Image(a,result):
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                a3 = item2.find_all("img")
                for item3 in a3:
                    result.append({"image":item3["src"]})
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                result[index]["url"] = item2["href"]
                index += 1
        return result

    def get_Title(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                a3 = item2.find_all("p")
                for item3 in a3:
                    result[index]["title"] = item3.text
                    index += 1
        return result

    get_Image(a,result)
    get_Url(a,result)
    get_Title(a,result)
    return result

# 蘋果日報+焦點
def appledailyNews_recommend():
    url = "https://tw.appledaily.com/recommend/realtime"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"id": "videobox"})
    result = []

    def get_Title(a,result):
        for item in a:
            a2 = item.find_all("div",{"id":"recommendlist2"})
            for item2 in a2:
                a3 = item2.find_all("li")
                for item3 in a3:
                    a4 = item3.find_all("p")
                    for item4 in a4:
                        a5 = item4.find_all("a")
                        for item5 in a5:
                            item6 = {}
                            item6["url"] = "https://tw.appledaily.com"+item5["href"]
                            item6["title"] = item5.text.encode(r.encoding).decode("utf8").replace(" ","").replace("\n","").replace("\u5803","").replace("\u3000","")
                            result.append(item6)
        return result

    def get_Image(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("div",{"id":"recommendlist2"})
            for item2 in a2:
                a3 = item2.find_all("li")
                for item3 in a3:
                    a4 = item3.find_all("div",{"id":"recommendpic2"})
                    for item4 in a4:
                        a5 = item4.find_all("img")
                        for item5 in a5:
                            if "playicon" in item5["src"]: continue
                            result[index]["image"] = item5["src"]
                            index += 1
        return result

    get_Title(a,result)
    get_Image(a,result)
    return result

# 蘋果日報+政治
def appledailyNews_politics():
    url = "https://tw.news.appledaily.com/politics/realtime"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"id": "rt3box"})
    result = []

    def get_Title(a,result):
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                a3 = item2.find_all("h2")
                for item3 in a3:
                    item4 = {}
                    item4["title"] = item3.text.encode(r.encoding).decode("utf8").replace(" ","").replace("\n","").replace("\u5803","").replace("\u3000","")
                    result.append(item4)
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("figure")
            for item2 in a2:
                a3 = item2.find_all("a")
                for item3 in a3:
                    result[index]["url"] = "https://tw.appledaily.com"+item3["href"]
                    index += 1
        return result

    def get_Image(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("figure")
            for item2 in a2:
                a3 = item2.find_all("a")
                for item3 in a3:
                    a4 = item2.find_all("img")
                    for item4 in a4:
                        if ("play_large" in item4["src"]) or ("playicon" in item4["src"]):continue
                        result[index]["image"] = item4["src"]
                        index += 1
        return result

    get_Title(a,result)
    get_Url(a,result)
    get_Image(a,result)
    return result

# 蘋果日報+娛樂
def appledailyNews_entertainment():
    url = "https://tw.entertainment.appledaily.com/realtime"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"id": "rt3box"})
    result = []

    def get_Title(a,result):
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                a3 = item2.find_all("h2")
                for item3 in a3:
                    item4 = {}
                    item4["title"] = item3.text.encode(r.encoding).decode("utf8").replace(" ","").replace("\n","").replace("\u5803","").replace("\u3000","")
                    result.append(item4)
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("figure")
            for item2 in a2:
                a3 = item2.find_all("a")
                for item3 in a3:
                    result[index]["url"] = "https://tw.appledaily.com"+item3["href"]
                    index += 1
        return result

    def get_Image(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("figure")
            for item2 in a2:
                a3 = item2.find_all("a")
                for item3 in a3:
                    a4 = item2.find_all("img")
                    for item4 in a4:
                        if ("play_large" in item4["src"]) or ("playicon" in item4["src"]):continue
                        result[index]["image"] = item4["src"]
                        index += 1
        return result

    get_Title(a,result)
    get_Url(a,result)
    get_Image(a,result)
    return result

# 蘋果日報+生活
def appledailyNews_life():
    url = "https://tw.news.appledaily.com/life/realtime"
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    w = BeautifulSoup(r.text, "html.parser")
    a = w.find_all("div", {"id": "rt3box"})
    result = []

    def get_Title(a,result):
        for item in a:
            a2 = item.find_all("a")
            for item2 in a2:
                a3 = item2.find_all("h2")
                for item3 in a3:
                    item4 = {}
                    item4["title"] = item3.text.encode(r.encoding).decode("utf8").replace(" ","").replace("\n","").replace("\u5803","").replace("\u3000","")
                    result.append(item4)
        return result

    def get_Url(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("figure")
            for item2 in a2:
                a3 = item2.find_all("a")
                for item3 in a3:
                    result[index]["url"] = "https://tw.appledaily.com"+item3["href"]
                    index += 1
        return result

    def get_Image(a,result):
        index = 0
        for item in a:
            a2 = item.find_all("figure")
            for item2 in a2:
                a3 = item2.find_all("a")
                for item3 in a3:
                    a4 = item2.find_all("img")
                    for item4 in a4:
                        if ("play_large" in item4["src"]) or ("playicon" in item4["src"]):continue
                        result[index]["image"] = item4["src"]
                        index += 1
        return result

    get_Title(a,result)
    get_Url(a,result)
    get_Image(a,result)
    return result

def database_insert():
    DATABASE_URL = "postgres://hlanvvnxzkvipq:066670d2118d48d1ce537bbe2eaf6d89f06c2cf99f92e30e3ae6bb55f709addf@ec2-174-129-32-240.compute-1.amazonaws.com:5432/dba4qpfa6mafgt"
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    def insert_news(conn,myData):
        sql_cmd = "INSERT INTO news_info (news_type,news_class,news_title,news_image,news_url,news_date) \
              VALUES ('"+myData[0]+"','"+myData[1]+"','"+myData[2]+"','"+myData[3]+"','"+myData[4]+"','"+myData[5]+"')"
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        conn.commit()
        cursor.close()
    yahoo_news = yahooNews_title()
    for news_dict in yahoo_news:
        insert_news(conn,
                    ["Yahoo新聞","首頁",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    yahoo_news2 = yahooNews_entertainment()
    for news_dict in yahoo_news2:
        insert_news(conn,
                    ["Yahoo新聞","娛樂",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    yahoo_news3 = yahooNews_money()
    for news_dict in yahoo_news3:
        insert_news(conn,
                    ["Yahoo新聞","財金",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    yahoo_news4 = yahooNews_sports()
    for news_dict in yahoo_news4:
        insert_news(conn,
                    ["Yahoo新聞","運動",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    tvbs_news = tvbsNews_title()
    for news_dict in tvbs_news:
        insert_news(conn,
                    ["TVBS新聞","首頁",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    tvbs_news2 = tvbsNews_politics()
    for news_dict in tvbs_news2:
        insert_news(conn,
                    ["TVBS新聞","焦點",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    tvbs_news3 = tvbsNews_entertainment()
    for news_dict in tvbs_news3:
        insert_news(conn,
                    ["TVBS新聞","娛樂",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    tvbs_news4 = tvbsNews_local()
    for news_dict in tvbs_news4:
        insert_news(conn,
                    ["TVBS新聞","地方社會",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    apple_news = appledailyNews_title()
    for news_dict in apple_news:
        insert_news(conn,
                    ["蘋果日報","首頁",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    apple_news2 = appledailyNews_entertainment()
    for news_dict in apple_news2:
        insert_news(conn,
                    ["蘋果日報","娛樂",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    apple_news3 = appledailyNews_life()
    for news_dict in apple_news3:
        insert_news(conn,
                    ["蘋果日報","生活",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    apple_news4 = appledailyNews_politics()
    for news_dict in apple_news4:
        insert_news(conn,
                    ["蘋果日報","焦點",
                     news_dict["title"],news_dict["image"],news_dict["url"],str(datetime.datetime.now())])
    conn.close()

if __name__=="__main__":
    # appledailyNews_point()
    # for item in yahooNews_sports():
    #     print(item)
    #     print("=================")
    pass