# 根据av号下载分页的评论
# http://api.bilibili.com/x/reply

import csv
import sys
import os
import time
import requests
from fake_useragent import UserAgent

def download(url,av):
    headers = {"User-Agent": UserAgent(verify_ssl=False).random}
    json_content = requests.get(url, headers).json()

    total = json_content["data"]["page"]["count"]
    page_num = total // 20 + 1
    infolist = []
    for i in range(1,page_num):
        url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&"\
            f"pn={i}&type=1&oid={av}&sort=1&nohot=1"
        
        json_content = requests.get(url, headers).json()
        
        for item in json_content["data"]["replies"]:
            info = {
                'author':item["member"]["mid"],
                'message':item["content"]["message"]
            }
            infolist.append(info)
    
    return infolist

def get_pinglun(av):
    url = f"http://api.bilibili.com/x/reply?"\
        f"type=1&oid={av}&pn=1&nohot=1&sort=0"

    infolist = download(url,av)

    return infolist

if __name__ == "__main__":
    av = sys.argv[1]
    out_path = f'./data/av{av}.csv'
    if os.path.exists(out_path):
        os.remove(out_path)

    url = f"http://api.bilibili.com/x/reply?"\
        f"type=1&oid={av}&pn=1&nohot=1&sort=0"

    infolist = download(url,av)

    with open(out_path, 'a', encoding='utf-8') as sw:
        fieldnames = ['author', 'message']
        writer = csv.DictWriter(sw, fieldnames=fieldnames)
        writer.writerows(infolist)
