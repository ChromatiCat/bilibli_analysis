# 根据av号下载弹幕
# https://api.bilibili.com/x/v1/dm/list.so

import os
import sys
import time
import requests
import re
from fake_useragent import UserAgent
from lxml import etree
from getuid import getuid_l

def download(url):
    headers = {"User-Agent": UserAgent(verify_ssl=False).random}
    xml_content = requests.get(url, headers).content
    html = etree.HTML(xml_content)
    p_list = html.xpath('//d//@p')
    u_hash_list = [item.split(',')[6] for item in p_list]
    # uid_list = getuid_l(u_hash_list)
    uid_list = u_hash_list
    text_list = html.xpath('//d//text()')

    list_len = len(p_list)
    infolist = []
    for i in range(list_len):
        infolist.append(uid_list[i]+","+text_list[i])

    return infolist

def get_cid(av):
    video_url = f'http://www.bilibili.com/video/av{av}/?tg'
    headers = {"User-Agent": UserAgent(verify_ssl=False).random}
    video_html = requests.get(video_url, headers).text
    pattern = r'cid=(.*?)&aid'
    obj = re.search(pattern, video_html)

    return obj.group(1)

def get_danmu(av):
    cid = get_cid(av)
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    infolist = download(url)
    return infolist
            
if __name__ == "__main__":
    av = sys.argv[1]
    out_path = f'./data/av{av}_dm.csv'
    if os.path.exists(out_path):
        os.remove(out_path)
    cid = get_cid(av)
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    infolist = download(url)
    for item in infolist:
        with open(out_path, 'a', encoding='utf-8') as sw:
            sw.write(item.join('\n\n'))
