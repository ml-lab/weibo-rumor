#!/usr/bin/env python
# coding=utf8

# __Author__: Yixuan Li (yl2363@cornell.edu), Zheng Yao (zy87@cornell.edu)


import json
import pickle
import string
from bs4 import BeautifulSoup
import weiboLogin
import urllib2
import re


""" Simulate a user login to Sina Weibo with cookie.
You can use this method to visit any page that requires login.

--------------------------------------------

1. Rumor meta data example:

  'K1CaM6g1l6Kol': ['结果公示',
  '/show?rid=K1CaM6g1l6Kol',
  'http://weibo.com/u/2805765994',
  'http://weibo.com/supperb',
  '31',
  '2015-02-16']

  format: 
  The meta data of each rumor is stored in a dictionary, where the key is the unique rumor ID. The first attribute in the value
  corresponds to the status of the reported rumor, either in evidence collection stage (举证阶段) or processed stage (结果公示). The second attribute is 
  the URL of rumor details. The third and fourth URLs are the homepages of the rumor reporter and rumor disseminator, respectively.
  The fifth attribute indicates the view times of this particular rumor. And the sixth attribute is the timestamp of this rumor report. 

----------------------------------------------

2. Individual rumor specifics example:

    'K1CaM7wpi7Koi': [2,1,2,'2015-03-15 22:01:59','2015-03-16 09:50', '2015-03-16 15:38']]

    format:
    'Rumor_ID':[number of reporters, whether succeed (1 indicates yes), number of evidence items, timestamp of the rumor being posted, timestamp of rumor being reported]

"""


def visit(url):
    try:
        req = urllib2.Request(url)
        text = urllib2.urlopen(req).read()
        return text

    except urllib2.URLError, e:
        print "Error: code = ",e
        time.sleep(300)
        logger.warn("Exception! Sleep 300s")
        logger.warn("Crawling top page url "+ url)
        logger.warn("Code = "+str(e.code))
        time.sleep(300)
    

def parse_rumor(page_content):
    
    #reguler expression to extract json data which contains html info
    patt_view = '<script>STK && STK.pageletM && STK.pageletM.view\((.*)\)</script>'
    patt = re.compile(patt_view, re.MULTILINE)
    weibo_scripts = patt.findall(page_content)
    soup_list = []
    for script in weibo_scripts:
        view_json = json.loads(script)
        if 'html' in view_json:
            html = view_json['html']
            soup = BeautifulSoup(html) # WOW...we got the soup
            soup_list.append(soup)
    return soup_list[4]



def sortInfo(soup):
    result = []
    raw_info = soup.find_all("tr")
    for one in raw_info[1:]:
        item = one.find_all("td")
        category = item[0].contents[0].encode("utf-8")
        url = one.find_all("div","m_table_tit")[0].contents[0].get("href")
        reporter = item[2].contents[0].get("href")
        poster = item[3].contents[0].get("href")
        viewtimes = item[4].contents[0].encode("utf-8")
        timestamp = item[5].contents[0].encode("utf-8")
        result.append({url[10:]:[category,url,reporter,poster,viewtimes,timestamp]})
    return result


def extract_cases(url):
    return sortInfo(parse_rumor(visit(url)))


def iterate_pages(start=1,end=100):
    rumor_page_info_collection = []
    top_page_url_base = u'http://service.account.weibo.com/index?type=5&status=0&page='
    each_page_base = u'http://service.account.weibo.com'
    urls = []
    #output_file = file("report_page_urls.txt", 'a')
    for page_number in range(start, end):
        top_page_url = top_page_url_base + str(page_number)
        rumor_page_info_collection = rumor_page_info_collection + extract_cases(top_page_url)

    pickle.dump(rumor_page_info_collection,open("rumor_page_info_collection.txt", "wb"))    


def parse_rumor_indiv(page_content):
    #reguler expression to extract json data which contains html info
    patt_view = '<script>STK && STK.pageletM && STK.pageletM.view\((.*)\)</script>'
    patt = re.compile(patt_view, re.MULTILINE)
    weibo_scripts = patt.findall(page_content)
    soup_list = []
    for script in weibo_scripts:
        view_json = json.loads(script)
        if 'html' in view_json:
            html = view_json['html']
            soup = BeautifulSoup(html) #WOW...we got the soup
            soup_list.append(soup)
    return soup_list[0]


#Extract the information in each page
def indivi_rumor_sort(soup):
    no_of_reports = int(returnNumber(soup.find_all("span","W_f12 W_textb")[0].contents[0].encode("utf-8"))) #Number of people who reported it
    win = len(soup.find_all("div","m_report_info")[0].find_all("div","resault win"))  #Whether the reporter has won, 1 stands for a win and 0 stands for a lose
    no_of_evidence = len(soup.find_all("div","con"))-1 #Number of evidence
    time_publish = returnDate(soup.find_all("p","publisher")[-1].contents[0].encode("utf-8")) #Timestamp for the original post
    time_report = []
    for timestamp in soup.find_all("p","publisher")[:-1]:
       time_report.append(returnDate(timestamp.contents[0].encode("utf-8"))) #Timestamps for reports
    return [no_of_reports, win, no_of_evidence, time_publish, time_report]


def allTogetherIndiv(url):
    return indivi_rumor_sort(parse_rumor_indiv(visit(url))) 



#Helper Method to return number from Chinese characters
def returnNumber(a):
    number = ""
    length = 0
    for b in a:
        length = len(number)
        if b.isdigit():
            number = number + b
        if ((length == len(number)) &(length != 0)):
            return number



#Helper Method to return date from Chinese characters
def returnDate(a):
    delEStr = string.digits + string.punctuation + " " #ASCII punctuation，"" and digits
    date = ""
    for c in a:
        if c in delEStr:
            date = date +c
    return date.rstrip().lstrip()

def iterate_rumors():
    # load the pickle of rumor meta data
    copy = pickle.load(open("rumor_page_info_collection.txt", "rb" ))
    newdict = {}
    for r in copy:
        print r
        newdict.update(r)

    indivi_rumor = {}
    for k in newdict.keys()[10:12]:
        indivi_rumor[k] = allTogetherIndiv("http://service.account.weibo.com/show?rid="+k)

    print indivi_rumor


#####################################################################################

if __name__ == '__main__':

    # simulate Sina Weibo user login using username and password
    username = '...your username...'
    pwd = '...your password...'
    
    cookie_file = 'weibo_login_cookies.dat'
    if weiboLogin.login(username, pwd, cookie_file):
        print 'Login WEIBO succeeded'

    # unit test for crawling rumor showcase pages
    # print extract_cases("http://service.account.weibo.com/index?type=5&status=0&page=101")

    # iterate over the rumor showcase pages
    iterate_pages(101,102)

    # iterate over individual rumors 
    iterate_rumors()

    









