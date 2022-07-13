# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 20:14:34 2021

@author: kamil
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import sys
from pymongo import MongoClient
import pymongo

client = MongoClient("localhost",27017)
db = client["SteamDB"]
col = db["games"]
limit=x=col.find().sort("_id",pymongo.DESCENDING).limit(1)
cols = ["id","Title","Release date","Developer","Publisher","Genre","Tags","Price","Reviews number","Reviews positive","Languages","Description","Minimum requirements","Recommended requirements","DLC"]  # wpisać nazy kolumn
df = pd.DataFrame(None, columns=cols)
for gid in range(0,limit[0]["_id"]+1):
    print(gid)
    try:
        page_html=col.find_one({"_id":gid})["html"]
        soup = BeautifulSoup(page_html, 'html.parser')
        text=soup.find("div",{"class":"details_block"}).text
        prev=""
        genre=""
        for line in text.splitlines():
            if "Title:" in line:
                title=line.replace("Title: ","")
            if "Genre:" in line:
                genre=line.replace("Genre: ","")
            if "Developer:" in prev:
                dev=line
            if "Publisher:" in prev:
                pub=line
            if "Release Date:" in line and "Early" not in line:
                date=line.replace("Release Date: ","")    
            prev=line
        try:
            tags=soup.find("div",{"class":"glance_tags popular_tags"}).text
            tags=tags.replace("+","")
            tags=tags.replace("\t","")
            tags=tags.replace("\n","")
            tags=tags.replace("\r",",")
        except Exception as e:
            #print(e)
            tags=""
        try:
            price=soup.find("div",{"class":"game_purchase_price price"}).text
            price=price.replace("\t","")
            price=price.replace("\r","")
            price=price.replace("\n","")
        except Exception as e:
            #print(e)
            price=""
        try:    
            revn=soup.find("label",{"for":"purchase_type_steam"}).find("span",{"class":"user_reviews_count"}).text
        except Exception as e:
            #print(e)
            revn=""
        try:    
            revp=soup.find("span",{"class":"responsive_reviewdesc_short"}).text
            revp=revp[revp.find("(")+1:revp.find("%")+1]
        except Exception as e:
            #print(e)
            revp=""
        try:
            lang=soup.find("table",{"class":"game_language_options"}).text
            lang=lang.replace("✔","")
            lang=lang.replace("\t","")
            lang=lang.replace("\n","")
            lang=lang.replace("\r",",")
            lang=lang.replace("Interface","")
            lang=lang.replace("Full Audio","")
            lang=lang.replace("Subtitles,","")
        except Exception as e:
            #print(e)
            lang=""
        con=" "
        if soup.find("div",{"id":"game_area_purchase"}).find("h1").text == "Downloadable Content":
            con="DLC"
        else:
            try:
                con=len(soup.find_all("div",{"class":"game_area_dlc_name"}))
            except Exception as e:
                print(e)  
        try:    
            desc=soup.find("div",{"class":"game_description_snippet"}).text
            desc=desc.replace("\t","")
            desc=desc.replace("\n","")
            desc=desc.replace("\r",",")
        except Exception as e:
            #print(e)
            desc=""
        try:    
            sysm=soup.find("div",{"class":"game_area_sys_req_leftCol"}).text
            sysm=sysm.replace("\n","")
        except Exception as e:
            #print(e)
            sysm=""
        try:    
            sysr=soup.find("div",{"class":"game_area_sys_req_rightCol"}).text
            sysr=sysr.replace("\n","")
        except Exception as e:
            #print(e)
            sysr=""
        row = {"id":int(gid),"Title":title,"Release date":date,"Developer":dev,"Publisher":pub,"Genre":genre,"Tags":tags,"Price":price,"Reviews number":revn,"Reviews positive":revp,"Languages":lang,"Description":desc,"Minimum requirements":sysm,"Recommended requirements":sysr,"DLC":con}
        df=df.append([row])
    except Exception as e:
        pass
df.to_csv('./steam_data.csv', index=False)
    
