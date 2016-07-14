# -*- coding: utf-8 -*-

"""
Created on Tue Jul 12 10:50:42 2016

@author: xugang
"""

import re
import urllib,urllib2
import sys
from bs4 import BeautifulSoup
            
if __name__ == '__main__':

    stdout_old = sys.stdout  
    sys.stdout = open('log_tj','w')    
    
    page = 1
    while(page<=33):
        #print page
        url = "http://lg.tjsf.gov.cn/tianjinlawyermanager/justice/search/result.jsp"
        params = {
            "currentPage":page, 
        }    
        postData = urllib.urlencode(params)
        req=urllib2.Request(url, postData)
        resp = urllib2.urlopen(req).read().decode('gbk')
        #print resp
        
        soup = BeautifulSoup(resp)
        list_page = soup.find_all('a',target="_blank")        
    
        for indiv in  list_page:
            #正则找code
            officecode = re.search("[0-9]+", str(indiv)).group()
      
            url = "http://lg.tjsf.gov.cn/tianjinlawyermanager/justice/search/showoffice.jsp?officecode="+str(officecode)
            req=urllib2.Request(url)
            resp = urllib2.urlopen(req).read().strip().decode('gbk')
            
            soup = BeautifulSoup(resp)
            
            infos = soup.find_all('table',align="center")[3].find_all('td')
            
            temp = ""
            index = 0
            for info in infos:
                index = index + 1 
                if(index%2 == 0):
                   # print info.get_text().strip()
                    temp = temp + info.get_text().strip().encode('utf-8') + ";"
            print temp
            
        page = page + 1
    

    sys.stdout.close()
    sys.stdout = stdout_old
    