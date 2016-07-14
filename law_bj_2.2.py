# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 10:50:42 2016

@author: xugang
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os


index_array = ["02","03","04","05","06","07","08","09","10","11"]

def isCompleted(flag,name):
    try:
        browser.switch_to_frame(name)
        flag = True
    except:
        flag = False
    return flag

def isLoaded(flag,indiv_name):
    try:
        if(browser.find_elements_by_class_name("tdRight")[0].text == indiv_name):        
            flag = True
    except:
        flag = False
    return flag
    
def waitForComplete(browser):
     
    js="return document.readyState"
    temp = browser.execute_script(js) 
    while(temp != "complete"):
        temp = browser.execute_script(js) 
        time.sleep(0.2)

def switchFrame(name,indiv_name="null"):
    
    flag = False
    flag = isCompleted(flag,name)
    count = 0
    while(not flag):
        time.sleep(0.2)
        count = count + 1
        flag = isCompleted(flag,name)  
        if(count > 20):
            break

    if(indiv_name!="null"):
        flag = False
        flag = isLoaded(flag,indiv_name)
        count = 0
        while(not flag):
            time.sleep(0.2)
            count = count + 1
            flag = isLoaded(flag,indiv_name)         
            if(count == 20):
               browser.refresh()
            if(count > 40):
                break
            
if __name__ == '__main__':
    
    url = "http://www.bjsf.gov.cn/publish/portal0/tab145/?type=1"
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

    os.environ["webdriver.chrome.driver"] = chromedriver
    
    print u"正在打开网页，请稍后.."
       
    foutput = file('log_bj', 'w')
    foutput_wrong = file('log_bj_wrong', 'w')
        
    browser = webdriver.Chrome(chromedriver)
    browser.get(url)
    
    flag = True   
    isFirstRound = True
    num = 0
    printTitle = True
    while(flag):
    #while(isFirstRound):
               
        waitForComplete(browser)
        
        handle_top = browser.current_window_handle
                    
        for index in index_array:
            
            num = num + 1
            
            wrong = False
            
            while(True):
                
                indiv_xpath = "//a[@id='ess_ctr740_LawOfficeSearchList_grdlist_ctl"+index+"_hyName']"
                switchFrame("main")
                
                try:
                    indiv = browser.find_element_by_xpath(indiv_xpath)    
                except:
                    flag = False
                    break
                
                indiv_name = indiv.text
                #print str(num) + "   " + indiv_name
                ActionChains(browser).click(indiv).perform() 
                
                #防止未打开就运行
                handles = browser.window_handles       
                while(len(handles)!=2):
                    print len(handles)
                    if(len(handles)>2):
                        for handle in handles: 
                            if handle != handle_top:  
                                browser.switch_to_window(handle) 
                                browser.close()
                    browser.switch_to_window(handle_top)
                    time.sleep(1)
                    switchFrame("main")
                    ActionChains(browser).click(indiv).perform()
                    handles = browser.window_handles
                    
                
                for handle in handles: 
                        
                    if handle != handle_top:       
                        browser.switch_to_window(handle)                
                        switchFrame("main",indiv_name)
                                        
                        keys = browser.find_elements_by_class_name("tdLeft") 
                        if(printTitle):
                            temp = ""
                            for key in keys:
                                temp = temp + key.text + ";"
                            foutput.write(temp)  
                            foutput.write("\n") 
                            printTitle = False
            
                        values = browser.find_elements_by_class_name("tdRight") 
                        temp = ""
                        name = ""
                        try:
                            name = values[0].text
                        except:
                            pass
                        if(name != indiv_name):
                            #记录错误日志
                            foutput_wrong.write(str(num) + "   " + indiv_name)
                            foutput_wrong.write("\n") 
                            print str(num) + "   " + indiv_name + "wrong"
                            wrong = True
                        else:
                        
                            for value in values:
                                
                                #正则表达式去换行和;
                                string = value.text                           
                                string = re.sub(';', '。', string) 
                                string = re.sub('\n', '', string) 
                                temp = temp + string + ";"
                                
                                wrong = False
                                
                            foutput.write(temp)
                            foutput.write("\n") 
                            
                            print str(num) + "   " + name
                        
                        browser.close() 
                        #time.sleep(0.5)
                        browser.switch_to_window(handle_top)
                        
                        if(wrong):
                            break
                    
                #无措跳出，有错重复        
                if(not wrong):
                    break
        #换页
        #print browser.current_window_handle
        if(isFirstRound):
            switchFrame("main")     
            isFirstRound = False
        try:
            next_page = browser.find_element_by_xpath("//a[@id='ess_ctr740_LawOfficeSearchList_lbtnNextPage']")        
        except:
            switchFrame("main")
            next_page = browser.find_element_by_xpath("//a[@id='ess_ctr740_LawOfficeSearchList_lbtnNextPage']")        

        ActionChains(browser).click(next_page).perform() 
        #print browser.current_window_handle
        #ActionChains(browser).click(browser.find_element_by_xpath("//a[@id='ess_ctr740_LawOfficeSearchList_grdlist_ctl02_hyName']")).perform() 

    foutput.close()
    foutput_wrong.close()
    browser.quit()
    
        