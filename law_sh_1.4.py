"""
Created on Tue Jul 12 10:50:42 2016

@author: xugang
"""

import json
import urllib,urllib2
import sys

#area_code = ['310230']
area_code = ['310230','310113','310114','310118','310112','310115','310117','310120','310116','310110','310108','310107','310109','310106','310105','310101','310104']
            
if __name__ == '__main__':
      
    total_info = []

    stdout_old = sys.stdout  
    sys.stdout = open('log_sh','w')
                
    for area in area_code:
        
        page = 1
        row = 10
        
        url = "http://xyxx.justice.gov.cn/xyxx/map/action/get_lawoffice_by_area.jsp?area_code="+area
        params = {
            "page":page,
            "rows":row,
        }    
        postData = urllib.urlencode(params)
        req=urllib2.Request(url, postData)
        resp = urllib2.urlopen(req).read().decode('gbk')
        result = json.loads(resp.strip())
        
        total = result['total']
        count = 0
        while(total >= (page-1)*row):
            
            page_indiv = result['rows']
            for indiv in page_indiv:
                count = count + 1
                indiv_id = str(indiv['id'])    
                url_indiv = "http://xyxx.justice.gov.cn/xyxx/target/lawoffice/action/find.jsp?&id="+indiv_id
                
                req=urllib2.Request(url_indiv)  
                resp_indiv = urllib2.urlopen(req).read().strip().decode('gbk').encode('utf-8')
                print resp_indiv              
                
                total_info.append(resp_indiv)
                
            page = page + 1
            
            params = {
                "page":page,
                "rows":row,
            }          
            postData = urllib.urlencode(params)
            req=urllib2.Request(url, postData)
            resp = urllib2.urlopen(req).read().decode('gbk')
            result = json.loads(resp.strip())                          
    
    sys.stdout.close()
    sys.stdout = stdout_old
        
        
        
        
        