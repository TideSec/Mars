#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19/2/12 下午4:58
# @Author  : 重剑无锋
# @Site    : www.tidesec.com
# @Email   : 6295259@qq.com

import hashlib,json,time,requests,os
import random,ssl,socket,urllib
import subprocess
import threading,datetime,hackhttp,Queue
import xml.etree.cElementTree as ET
import sys,pymongo,re,urlparse
from bs4 import BeautifulSoup as BS
from qqwry import QQwry
import nmap


debug_mod = 0   #debug模式，0为关闭，1为开启

try:
    import requests
except:
    print 'pip install requests[security]'
    os._exit(0)

try:
    import lxml
except:
    print 'pip install lxml'
    os._exit(0)

try:
    import qqwry
except:
    print 'pip install qqwry-py2'
    os._exit(0)

try:
    import dns.resolver
except:
    print 'pip install dnspython'
    os._exit(0)

# Check py version
pyversion = sys.version.split()[0]
if pyversion >= "3" or pyversion < "2.7":
    exit('Need python version 2.6.x or 2.7.x')

reload(sys)
sys.setdefaultencoding('utf-8')

lock = threading.Lock()


global pwd,path

# Ignore warning
requests.packages.urllib3.disable_warnings()
# Ignore ssl warning info.
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context



header_task = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Cookie': 'thinkphp_show_page_trace=0|0; thinkphp_show_page_trace=0|0; think_var=zh-cn; PHPSESSID=gljsd5c3ei5n813roo4878q203',
               'X-Requested-With': 'XMLHttpRequest'
               }


MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'mars',
    'username': 'mars',
    'password': 'tidesec.com'
}

def requests_proxies():
    '''
    Proxies for every requests
    '''
    proxies = {
    'http':'',#127.0.0.1:1080 shadowsocks
    'https':''#127.0.0.1:8080 BurpSuite
    }
    return proxies
def requests_headers():
    '''
    Random UA  for every requests && Use cookie to scan
    '''
    user_agent = ['Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre',
    'Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60','Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5']
    UA = random.choice(user_agent)
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent':UA,'Upgrade-Insecure-Requests':'1','Connection':'keep-alive','Cache-Control':'max-age=0',
    'Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8',
    "Referer": "http://www.baidu.com/link?url=www.so.com&url=www.soso.com&&url=www.sogou.com",
    'Cookie':"PHPSESSID=gljsd5c3ei5n813roo4878q203"}
    return headers

def url_protocol(url):
    domain = re.findall(r'.*(?=://)', url)
    if domain:
        return domain[0]
    else:
        return url

def url_to_subdoamin(urlprotocol,url):
    url = url.replace(urlprotocol + '://', '')
    if re.findall(r'^www', url) == []:
        sameurl = 'www.' + url
        if sameurl.find('/') != -1:
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
        else:
            sameurl = sameurl + '/'
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    else:
        if url.find('/') != -1:
            sameurl = 'www.' + re.findall(r'(?<=www.).*?(?=/)', url)[0]
        else:
            sameurl = url + '/'
            sameurl = 'www.' + re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    # print('the domain is：' + sameurl)
    return sameurl

class linkQuence:
    def __init__(self):
        self.visited = []    #已访问过的url初始化列表
        self.unvisited = []  #未访问过的url初始化列表
        self.external_url=[] #外部链接

    def getVisitedUrl(self):  #获取已访问过的url
        return self.visited
    def getUnvisitedUrl(self):  #获取未访问过的url
        return self.unvisited
    def getExternal_link(self):
        return self.external_url   #获取外部链接地址
    def addVisitedUrl(self,url):  #添加已访问过的url
        return self.visited.append(url)
    def addUnvisitedUrl(self,url):   #添加未访问过的url
        if url != '' and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0,url)
    def addExternalUrl(self,url):   #添加外部链接列表
        if url!='' and url not in self.external_url:
            return self.external_url.insert(0,url)

    def removeVisited(self,url):
        return self.visited.remove(url)
    def popUnvisitedUrl(self):    #从未访问过的url中取出一个url
        try:                      #pop动作会报错终止操作，所以需要使用try进行异常处理
            return self.unvisited.pop()
        except:
            return None
    def unvisitedUrlEmpty(self):   #判断未访问过列表是不是为空
        return len(self.unvisited) == 0

class Spider():
    '''
    真正的爬取程序
    '''
    def __init__(self,url,domain_url,urlprotocol):
        self.linkQuence = linkQuence()   #引入linkQuence类
        self.linkQuence.addUnvisitedUrl(url)   #并将需要爬取的url添加进linkQuence对列中
        self.current_deepth = 1    #设置爬取的深度
        self.domain_url = domain_url
        self.urlprotocol = urlprotocol

    def getPageLinks(self,url):
        '''
            获取页面中的所有链接
        '''
        try:
            headers = requests_headers()
            content = requests.get(url, timeout=5, headers=headers, verify=False).text.encode('utf-8')
            links = []
            tags = ['a', 'A', 'link', 'script', 'area', 'iframe', 'form']  # img
            tos = ['href', 'src', 'action']
            if url[-1:] == '/':
                url = url[:-1]
            try:
                for tag in tags:
                    for to in tos:
                        link1 = re.findall(r'<%s.*?%s="(.*?)"' % (tag, to), str(content))
                        link2 = re.findall(r'<%s.*?%s=\'(.*?)\'' % (tag, to), str(content))
                        for i in link1:
                            links.append(i)
                        for i in link2:
                            if i not in links:
                                links.append(i)
            except Exception, e:
                print e
                print '[!] Get link error'
                pass
            return links
        except:
            return []
    def getPageLinks_bak(self,url):
        '''
        获取页面中的所有链接
        '''
        try:

            # pageSource=urllib2.urlopen(url).read()
            headers = requests_headers()
            time.sleep(0.5)
            pageSource = requests.get(url, timeout=5, headers=headers).text.encode('utf-8')
            pageLinks = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')', pageSource)
            # print pageLinks
        except:
            # print ('open url error')
            return []
        return pageLinks

    def processUrl(self,url):
        '''
        判断正确的链接及处理相对路径为正确的完整url
        :return:
        '''
        true_url = []
        in_link = []
        excludeext = ['Down','down','.zip', '.rar', '.pdf', '.doc', '.xls', '.jpg', '.mp3', '.mp4','.png', '.ico', '.gif','.svg', '.jpeg','.mpg', '.wmv', '.wma','mailto','javascript','data:image']
        for suburl in self.getPageLinks(url):
            exit_flag = 0
            for ext in excludeext:
                if ext in suburl:
                    # print "break:" + suburl
                    exit_flag = 1
                    break
            if exit_flag == 0:
                if re.findall(r'/', suburl):
                    if re.findall(r':', suburl):
                        true_url.append(suburl)
                    else:
                        true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)
                else:
                    true_url.append(self.urlprotocol + '://' + self.domain_url + '/' + suburl)

        # for suburl in true_url:
        #     print('from:' + url + ' get suburl：' + suburl)

        return true_url

    def sameTargetUrl(self,url):
        same_target_url = []
        for suburl in self.processUrl(url):
            if re.findall(self.domain_url,suburl):
                same_target_url.append(suburl)
            else:
                self.linkQuence.addExternalUrl(suburl)
        return same_target_url

    def unrepectUrl(self,url):
        '''
        删除重复url
        '''
        unrepect_url = []
        for suburl in self.sameTargetUrl(url):
            if suburl not in unrepect_url:
                unrepect_url.append(suburl)
        return unrepect_url

    def crawler(self,crawl_deepth=1):
        '''
        正式的爬取，并依据深度进行爬取层级控制
        '''
        self.current_deepth=0
        while self.current_deepth < crawl_deepth:
            if self.linkQuence.unvisitedUrlEmpty():break
            links=[]
            while not self.linkQuence.unvisitedUrlEmpty():
                visitedUrl = self.linkQuence.popUnvisitedUrl()
                if visitedUrl is None or visitedUrl == '':
                    continue
                # print("#"*30 + visitedUrl +" :begin"+"#"*30)
                for sublurl in self.unrepectUrl(visitedUrl):
                    links.append(sublurl)
                links = self.unrepectUrl(visitedUrl)
                self.linkQuence.addVisitedUrl(visitedUrl)
                # print("#"*30 + visitedUrl +" :end"+"#"*30 +'\n')
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            self.current_deepth += 1
        # print(self.linkQuence.visited)
        # print (self.linkQuence.unvisited)
        urllist=[]
        External_link = []
        # urllist.append("#" * 30 + ' VisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getVisitedUrl():
            urllist.append(suburl)
        urllist.append("#" * 30 + ' UnVisitedUrl ' + "#" * 30)
        for suburl in self.linkQuence.getUnvisitedUrl():
            urllist.append(suburl)
        # urllist.append("#" * 30 + ' External_link ' + "#" * 30)
        for sublurl in self.linkQuence.getExternal_link():
            urllist.append(sublurl)
            External_link.append(sublurl)
        # urllist.append("#" * 30 + ' Active_link ' + "#" * 30)

        return urllist,External_link
def writelog(log,urllist):
    filename=log
    outfile=open(filename,'w')
    for suburl in urllist:
        outfile.write(suburl+'\n')
    outfile.close()

def subdomain_spider(target,main_domain,log,crawl_deepth=2):

    urlprotocol = url_protocol(target)
    domain_url = url_to_subdoamin(urlprotocol,target)
    print "domain_url:"+domain_url
    spider = Spider(target,domain_url,urlprotocol)
    urllist,External_link = spider.crawler(crawl_deepth)
    print "len(urllist):",len(urllist)
    # print External_link
    for external_url in External_link:   # 对外链爬取一次
        # print external_url
        urlprotocol_tmp = url_protocol(external_url)
        domain_url_tmp = url_to_subdoamin(urlprotocol_tmp,external_url)
        urllist.append(domain_url_tmp)
        # print "external_url_tmp:"+external_url
        external_url_spider = Spider(external_url,domain_url_tmp,urlprotocol_tmp)
        urllist_tmp,External_link_tmp = external_url_spider.crawler(crawl_deepth=1)
        if urllist_tmp:
            for url_tmp in urllist_tmp:
                urllist.append(url_tmp)
        # print "len(urllist):",len(urllist)

    domain_tmp = []
    server_tmp = []

    for x in urllist:
        x = x.strip()
        res = urlparse.urlparse(x)
        if x:
            sub_tmp = res.netloc
            url_tmp = res.scheme+"://"+res.netloc
            # print url_tmp

            if main_domain in sub_tmp:
                server_tmp.append(url_tmp)

                if ':' in sub_tmp:
                    domain_tmp.append(sub_tmp.split(':')[0])
                else:
                    domain_tmp.append(sub_tmp)

    quchong1 = set(list(domain_tmp))
    domain_tmp = []
    for xx in quchong1:
        domain_tmp.append(xx)

    quchong2 = set(list(server_tmp))
    server_tmp = []
    for xx in quchong2:
        server_tmp.append(xx)


    writelog(log, urllist)
    print '-' * 20 + main_domain + '-' * 20

    print '\n' + 'Result record in:' + log
    return domain_tmp,server_tmp


def getCoding(strInput):
    '''
    获取编码格式
    '''
    if isinstance(strInput, unicode):
        return "unicode"
    try:
        strInput.decode("utf8")
        return 'utf8'
    except:
        pass
    try:
        strInput.decode("gbk")
        return 'gbk'
    except:
        pass


def tran2UTF8(strInput):
    '''
    转化为utf8格式
    '''
    try:
        strCodingFmt = getCoding(strInput)
        if strCodingFmt == "utf8":
            return strInput
        elif strCodingFmt == "unicode":
            return strInput.encode("utf8")
        elif strCodingFmt == "gbk":
            return strInput.decode("gbk").encode("utf8")
    except:
        return strInput


def url2ip(url):
    '''
    Url to ip
    '''
    ip = ''
    try:
        url = url.strip()
        if not url.startswith("http"):
            url =add_protocal(url)
        handel_url = urlparse.urlparse(url).hostname
        ip = socket.gethostbyname(handel_url)
        # print ip
    except:
        print '[!] url2ip Can not get ip',url
        pass
    return ip

class Singleton(object):
    # 单例模式写法,参考：http://ghostfromheaven.iteye.com/blog/1562618
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

class MongoConn(Singleton):
    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.conn[MONGODB_CONFIG['db_name']]
            self.username=MONGODB_CONFIG['username']
            self.password=MONGODB_CONFIG['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password,mechanism="SCRAM-SHA-1")
                # self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
            else:
                self.connected = self.db
        except Exception:
            print 'Connect Statics Database Fail.'
            # sys.exit(1)

def check_connected(conn):
    #检查是否连接成功
    try:
        if not conn.connected:
            raise NameError, 'stat:connected Error'
    except Exception,e:
        now = time.strftime('%Y-%m-%d_%X', time.localtime(time.time()))
        info = '%s  Mongo Connect Error: %s' % (now, e)
        print info
        print "sleep 60s\n"
        time.sleep(60)
        print "Try to connect MongoDB:",MONGODB_CONFIG['host']
        my_conn = MongoConn()
        check_connected(my_conn)

def select_colum(table, value, colum):
    #查询指定列的所有值
    try:
        # my_conn = MongoConn()
        # check_connected(my_conn)
        return my_conn.db[table].find(value, {colum:1})
    except Exception:
        print 'stat:connected Error'

def insert_one(table, data):
    #更新插入，根据‘ip’删除其他记录，如果‘ip’的值不存在，则插入一条记录
    try:
        # my_conn = MongoConn()
        # check_connected(my_conn)
        query = {'ip': data.get('ip','')}
        if my_conn.db[table].find_one(query):
            my_conn.db[table].remove(query)
        my_conn.db[table].insert(data)
    except Exception,e:
        print "insert error:",e

def checkend(xmlfile):
    try:
        infile = open(xmlfile, 'r+')
        endxml = '''<runstats><finished time="1518405307" timestr="Sun Feb 11 22:15:07 2018" elapsed="396.80" summary="Nmap done at Sun Feb 11 22:15:07 2018; 256 IP addresses (136 hosts up) scanned in 396.80 seconds" exit="success"/><hosts up="136" down="120" total="256"/>
            </runstats>
            </nmaprun>'''
        x = infile.readlines()
        lens = len(x)
        if not x[lens - 3].startswith('<runstats>'):
            print xmlfile, " not endwith <runstats>"
            print '\n' * 3 + "Rstart python" + '\n' * 3
            restart_python = '. /root/tide/webscan/task.sh'
            os.system(restart_python)

            infile.write('\n')
            infile.write(endxml)
            infile.close()
            return "0"
        else:
            return "1"
    except:
        pass

def parse_xml(xmlfile):
    try:
        # outfile = open(ip_temp_db, 'a+')
        tree = ET.ElementTree(file=xmlfile)
        for elem in tree.iterfind('host'):
            if (elem[0].attrib['state']) == "up":
                is_up = "up"
            else:
                is_up = "down"
            ip = elem[1].attrib['addr']
            print ip
            scantime = elem.attrib['starttime']
            time_local = time.localtime(float(scantime))
            updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            if elem[3].tag == 'hostnames':
                port_num = 4
            else:
                port_num = 3

            port_info = []
            if len(elem) > 3:
                ports = elem[port_num]
                for x in ports.iterfind('port'):
                    port = x.attrib['portid']
                    protocol = x.attrib['protocol']
                    state = x[0].attrib['state']
                    service = ''
                    product = ''
                    product_ver = ''
                    extrainfo = ''
                    banner_brief = ''
                    banner_info = ''
                    site_info = ''
                    trap_flag = 1

                    if (state == 'open'):
                        url = ip + ":" + port
                        if (len(x) > 1):
                            if 'name' in x[1].keys():
                                service = x[1].attrib['name']

                            if 'product' in x[1].keys():
                                product = x[1].attrib['product']

                            if 'version' in x[1].keys():
                                product_ver = x[1].attrib['version']

                            if 'extrainfo' in x[1].keys():
                                extrainfo = x[1].attrib['extrainfo']

                            if 'ostype' in x[1].keys():
                                extrainfo = x[1].attrib['ostype']

                            if (len(x) > 2) and ('output' in x[2].keys()):
                                banner_brief = x[2].attrib['output']
                                banner_brief = banner_brief.decode('utf-8', 'ignore').encode('utf-8')
                            if (service == 'tcpwrapped'):
                                trap_flag = 0

                            # if ('http' in service):
                            #     site_info = get_header(url)
                            #     print "111"
                            #     if site_info:
                            #         banner_info = site_info

                        if trap_flag:
                            port_data = {'port': port, 'protocol': protocol, 'state': state,
                                         'service': service, 'product': product, 'banner_brief': banner_brief,
                                         'extrainfo': extrainfo, 'product_ver': product_ver, 'banner_info': banner_info}
                            port_info.append(port_data)

            os = elem[port_num+1]
            os_info = ''
            print "222"

            if len(os) > 0:
                for x in os.iterfind('osmatch'):
                    os_info = x.attrib['name']
                    break

            hostnames = elem[port_num-1]
            hostname_info = ''
            if len(hostnames) > 0:
                for x in hostnames.iterfind('hostname'):
                    hostname_info = x.attrib['name']
                    break

            ip_info = getipinfo(ip)
            print "333"

            ip_data = {'ip': ip, 'updatetime': updatetime, 'ip_info': ip_info, 'is_up': is_up,
                       'os': os_info,'hostname': hostname_info,
                       'port_info': port_info}

            print xmlfile, " current ip:", ip

            return ip_data

    except Exception, e:
        now = time.strftime('%Y-%m-%d_%X', time.localtime(time.time()))
        info = '\033[1;35m[!] %s\nParse_xml Error: %s \033[0m!' % (now, e)
        print info

def get_header(url):

    try:
        print "Get http header:",url
        url = add_protocal(url)
        hh = hackhttp.hackhttp()
        code, head, body, redirect, log = hh.http(url, headers=requests_headers())
        print "Get header ok:", url
        if log:
            return log['response'].decode('utf-8', 'ignore').encode('utf-8')
        else:
            return False
    except:
        return False


def getip_info_taobao(ip):
    try:
        url = "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip
        print url
        res = requests.get(url, headers=requests_headers(),timeout=10)
        res = json.loads(res.content)
        print res
        if res['code'] == 0:
            country = res['data']['country']
            region = res['data']['region']
            city = res['data']['city']
            isp = res['data']['isp']
        else:
            country = None
            region = None
            city = None
            isp = None
        if region or city:
            area = region+city
        else:
            area = country
        return area,isp
    except:
        return '',''

def getipgps(ip):
    try:
        url1 = 'http://ip-api.com/json/'+str(ip)
        print url1
        res1 = requests.get(url1, headers=requests_headers(),timeout=15,verify=False)
        info =eval(res1.content)
        gps = str(info['lat'])+','+str(info['lon'])

        if gps:
            # print gps[0]
            return gps
        else:
            url = 'http://www.gpsspg.com/ip/?q='+ip
            # http://ip-api.com/json/112.231.42.101
            print url
            res = requests.get(url, headers=requests_headers(),timeout=15)
            html = res.content
            soup = BS(html, 'lxml')
            td = soup.find_all('a')
            gps = td[7].text
            if gps.startswith('http'):
                return '0,0'
            else:
                return gps
    except:
        return ''


def getip_info_gpsspg(ip):
    try:
        url = 'http://www.gpsspg.com/ip/?q='+ip
        print url
        res = requests.get(url,timeout=30)
        html = res.content
        # print html
        soup = BS(html, 'lxml')
        td = soup.find_all('span')
        area = td[3].text
        country = None
        region = None
        city = None
        isp = None
        isp = area.split('--')[1].strip()
        country =  area.split('--')[0].split(' ')[0]
        region = area.split('--')[0].split(' ')[1]
        city = area.split('--')[0].split(' ')[2]
        if region or city:
            area=region+city
        else:
            area = country
        return area,isp
    except:
        return '',''


def getip_info_local(ip):
    try:
        q = QQwry()
        q.load_file('libs/qqwry.dat')
        result = q.lookup(ip)
        area = result[0]
        isp = result[1]
        return area,isp,True
    except:
        return '','',False

def getipinfo(ip):
    try:
        area, isp, flag = getip_info_local(ip)
        # print "getip_info_local_ok",time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        if not flag:
            area, isp, flag = getip_info_gpsspg(ip)
            print "getip_info_gpsspg_ok",time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
            if not flag:
                area, isp, flag = getip_info_taobao(ip)
                print "getip_info_taobao_ok",time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

        gps = getipgps(ip)
        # print "getipgps_Ok:",time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        ipinfo = [{'area': area, 'isp': isp, 'gps': gps}]
        return ipinfo
    except:
        pass
def md5hash(ip):
    md5 = hashlib.md5()
    md5.update(ip)
    return md5.hexdigest()


class Worker(threading.Thread):  # 处理工作请求
    def __init__(self, workQueue, resultQueue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue

    def run(self):
        while 1:
            try:
                callable, args, kwds = self.workQueue.get(False)  # get task
                res = callable(*args, **kwds)
                self.resultQueue.put(res)  # put result
            except Queue.Empty:
                break

class WorkManager:  # 线程池管理,创建
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()  # 请求队列
        self.resultQueue = Queue.Queue()  # 输出结果的队列
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue)  # 创建工作线程
            self.workers.append(worker)  # 加入到线程队列

    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()  # 从池中取出一个线程处理请求
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)  # 重新加入线程池中

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))  # 向工作队列中加入请求

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)


def baidu_site(key_domain):
    '''
    Get baidu site:target.com result
    '''
    headers = requests_headers()
    baidu_domains,check = [],[]
    get_subdomain = 0
    baidu_url = 'https://www.baidu.com/s?ie=UTF-8&wd=site:{}'.format(key_domain)
    print baidu_url
    try:
        r = requests.get(url=baidu_url,headers=headers,timeout=30,verify=False).content
        if 'location.replace(location.href.replace' in r:
            return baidu_domains,False
        if 'class=\"nors\"' not in r:# Check first
            for page in xrange(0,70):# max page_number
                # print "baidu_domains",baidu_domains
                pn = page * 10
                newurl = 'https://www.baidu.com/s?ie=UTF-8&wd=site:{}&pn={}&oq=site:{}'.format(key_domain,pn,key_domain)
                # print newurl
                if 'location.replace(location.href.replace' in r:
                    return baidu_domains,False
                keys = requests.get(url=newurl,headers=headers,timeout=30,verify=False).content
                flags = re.findall(r'style=\"text-decoration:none;\">(.*?)%s.*?<\/a><div class=\"c-tools\"'%key_domain,keys)
                # print "flags",flags
                check_flag = re.findall(r'class="n">(.{9})&gt;',keys)
                # print "check_flag",check_flag,len(check_flag)
                for flag in flags:
                    domain_handle = flag.replace('https://','').replace('http://','')
                    # print "domain_handle",domain_handle
                    if domain_handle not in check and domain_handle != '':
                        check.append(domain_handle)
                        domain_flag = domain_handle + key_domain
                        print '[+] Get baidu site:'+key_domain+' > ' + domain_flag
                        baidu_domains.append(domain_flag)
                        get_subdomain = 1
                if len(check_flag) == 0:
                    return baidu_domains,True

            if not get_subdomain:
                return baidu_domains,False
            else:
                return baidu_domains,True
        else:
            print '[!] baidu site:domain no result'
            return baidu_domains,True
    except Exception,e:
        print "\033[1;35m[!] baidu_site error \033[0m!",e
        return baidu_domains,False

def fanjiexi(main_domain):
    fanjiexi_flag = 0
    fanjiexi_length = 0
    fanjiexi_url1 = "http://6295259."+main_domain
    fanjiexi_url2 = "http://17178930."+main_domain
    try:
        res1 = requests.get(url=fanjiexi_url1, headers=requests_headers(), timeout=10, verify=False)
        fanjiexi_flag = 1
        fanjiexi_length = len(res1.content)
        return fanjiexi_flag,fanjiexi_length
    except:
        return fanjiexi_flag,fanjiexi_length

def task_subdomain(main_domain,task_sub_domain):
    logpath = set_dirs(main_domain)
    target = main_domain
    try:
        if not main_domain.startswith("http"):
            target = "http://www." + main_domain
        res = requests.get(url=target, headers=requests_headers(), timeout=10, verify=False)
    except:
        target = "http://" + main_domain
    print "target:",target

    sub_domains = []
    server_tmp = []
    domain_all=[]
    for task_sub_url in task_sub_domain:
        urlprotocol = url_protocol(task_sub_url)
        task_sub_domain_tmp = url_to_subdoamin(urlprotocol,task_sub_url)
        domain_all.append(task_sub_domain_tmp)

    fanjiexi_flag,fanjiexi_length = fanjiexi(main_domain)
    try:
        host = main_domain
        global pwd
        os.chdir(pwd)
        domain_tmp = []
        server_tmp = []
        domain_tmp,server_tmp = subdomain_spider(target,main_domain,logpath + 'domain/' + main_domain + '-spiderdomain.txt',crawl_deepth=1)
        print domain_tmp
        # print server_tmp
        for domain_tmp_1 in domain_tmp:
            domain_all.append(domain_tmp_1)

        print "-------------baidu_domain_start-------------"

        baidu_domains,erro_flag = baidu_site(host)
        if not erro_flag:
            baidu_domains,erro_flag = baidu_site(host)
            if not erro_flag:
                baidu_domains,erro_flag = baidu_site(host)

        baidudomain = open(logpath + 'domain/' + main_domain + '-baidudomain.txt', 'a+')
        for baidu_domain in baidu_domains:
            baidudomain.write(baidu_domain + '\n')
        baidudomain.close()
        print "+++++++++++++baidu_domain_ok+++++++++++++"

        print "-------------Sublist3r_start-------------"
        os.chdir(path + '/Sublist3r/')
        Sublist3r = 'python ' + path + 'Sublist3r/sublist3r.py -d ' + host + ' -o ' + logpath + 'domain/' + main_domain + '-wydomain.txt'
        print Sublist3r
        os.system(Sublist3r)
        print "+++++++++++++Sublist3r_ok+++++++++++++"

        if not fanjiexi_flag:
            print "-------------subdomain_start-------------"
            os.chdir(path + '/subDomainsBrute/')
            subdomain = 'python ' + path + 'subDomainsBrute/subDomainsBrute.py  ' + host + ' --out ' + logpath + 'domain/' + main_domain + '-subdomain.txt'
            print subdomain
            os.system(subdomain) # 为加快速度，停止subdomain的枚举
            print "+++++++++++++subdomain_ok+++++++++++++"
        else:
            print "Fanjiexi:",main_domain

        print "-------------read_all_subdomain-------------"


        if os.path.exists(logpath + 'domain/' + main_domain + '-wydomain.txt'):
            wydomain_text = open(logpath + 'domain/' + main_domain + '-wydomain.txt', 'r').read().split('\n')
            if len(wydomain_text) < 500:
                for wydomain in wydomain_text:
                    wydomain = wydomain.strip()
                    if wydomain:
                        domain_all.append(wydomain)


        if os.path.exists(logpath + 'domain/' + main_domain + '-subdomain.txt'):
            subdomain_text = open(logpath + 'domain/' + main_domain + '-subdomain.txt', 'r')
            sub_domain_num = []
            for x in subdomain_text.readlines():
                x = x.strip('\n').strip('\r')
                sub_domain_num.append(x)

            if len(sub_domain_num) < 2000:
                for x in sub_domain_num:
                    x = x.strip('\n').strip('\r')
                    domain_all.append(x)

        try:
            if os.path.exists(logpath + 'domain/' + main_domain + '-baidudomain.txt'):
                baidudomain = open(logpath + 'domain/' + main_domain + '-baidudomain.txt', 'r')
                for baidu_domain in baidudomain.readlines():
                    baidu_domain = baidu_domain.strip('\n').strip('\r')
                    domain_all.append(baidu_domain)
        except:
            pass

        for baidu_tmp in baidu_domains:
            domain_all.append(baidu_tmp)

        sub_domains = list(set(domain_all))
        domain_num = len(sub_domains)
        print logpath + main_domain + '-domain.txt'
        alldomain = open(logpath + main_domain + '-domain.txt', 'w')

        for sub_domain in sub_domains:
            sub_domain = sub_domain.strip()
            if sub_domain:
                alldomain.write(sub_domain + '\n')
                # domains = x + '\n' + domains
        alldomain.close()

        print "+++++++++++++read_all_subdomain+++++++++++++"

        sub_domains_qc = set(list(sub_domains))
        sub_domains = []

        for x in sub_domains_qc:
            x = x.strip()
            if x:
                sub_domains.append(x)
        return sub_domains,logpath,server_tmp

    except Exception,e:
        print "\033[1;35m[!]get_sub_domain error,\033[0m!",e
        return sub_domains,logpath,server_tmp

#
def get_url_title(url):
    try:
        url = url.strip()
        header = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                   "Accept-Encoding": "gzip",
                   "Accept-Language": "zh-CN,zh;q=0.8",
                   "Referer": "http://www.baidu.com/link?url=www.so.com&url=www.soso.com&&url=www.sogou.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                   }

        # html = urllib.urlopen(url).read()
        html = requests.get(url, timeout=3, verify=False,headers=header).content
        if re.search('gb2312', html):
            html = html.decode('gbk', 'replace').encode('utf-8')
        # print html
        soup = BS(html, "lxml")
        # print soup
        title = soup.title.text
        # print html
        return tran2UTF8(title)
    except:
        return ''

def get_whatweb(domain,target,log):
    try:
        os.chdir(pwd)

        whatweb_text = ''

        # print "-------------whatweb_start-------------"
        whatweb = path + 'WhatWeb/whatweb --log-json=' + log + " " + target
        print whatweb
        os.system(whatweb)
        # print "+++++++++++++whatweb_ok+++++++++++++"

        whatweb_text = open(log, 'r').read()
        temp = eval(whatweb_text)
        extrabanner = ''
        banner_tmp = ''
        banner =''
        IP_tmp,http_status_tmp,Title_tmp,HTTPServer_tmp,xpb_tmp = '','','','',''

        if len(temp)>1:
            for num in range(0,len(temp)-1,1):
                test = temp[num]
                banner = ''
                # print "num:",num
                if test.has_key('http_status'):
                    http_status = str(test['http_status'])
                    # print "http_status",http_status
                    if num == 0:
                        http_status_tmp = http_status
                    else:
                        extrabanner = extrabanner+', http_status:'+http_status

                if test.has_key('plugins'):
                    plugins = test['plugins']

                    if plugins.has_key('Title'):
                        if plugins['Title'].has_key('string'):
                            Title = plugins['Title']['string'][0]
                            # print "Title",Title
                            if num == 0:
                                Title_tmp = Title
                            else:
                                extrabanner = extrabanner+', Title:'+Title

                    if plugins.has_key('IP'):
                        if plugins['IP'].has_key('string'):
                            IP = plugins['IP']['string'][0]
                            # print "IP",IP
                            if num == 0:
                                IP_tmp = IP
                            else:
                                extrabanner = extrabanner+', IP:'+IP

                    if plugins.has_key('HTTPServer'):
                        if plugins['HTTPServer'].has_key('string'):
                            HTTPServer = plugins['HTTPServer']['string'][0]
                            # print "HTTPServer",HTTPServer
                            if num == 0:
                                HTTPServer_tmp = HTTPServer
                            else:
                                extrabanner = extrabanner+', HTTPServer:'+HTTPServer

                    if plugins.has_key('X-Powered-By'):
                        if plugins['X-Powered-By'].has_key('string'):
                            xpb = plugins['X-Powered-By']['string'][0]
                            # print "X-Powered-By",xpb
                            if num == 0:
                                xpb_tmp = xpb
                            else:
                                extrabanner = extrabanner+', xpb:'+xpb

                    if plugins.has_key('MetaGenerator'):
                        if plugins['MetaGenerator'].has_key('string'):
                            MetaGenerator = plugins['MetaGenerator']['string'][0]
                            if MetaGenerator:
                                banner = banner+','+MetaGenerator
                            # print "MetaGenerator",MetaGenerator

                    if plugins.has_key('Apache'):
                        if plugins['Apache'].has_key('string'):
                            Apache = plugins['Apache']['string'][0]
                            if Apache:
                                banner = banner+', Apache:'+Apache
                            # print "Apache",Apache
                        if plugins['Apache'].has_key('version'):
                            Apache = plugins['Apache']['version'][0]
                            if Apache:
                                banner = banner+', Apache:'+Apache
                            # print "Apache",Apache

                    if plugins.has_key('nginx'):
                        if plugins['nginx'].has_key('string'):
                            nginx = plugins['nginx']['string'][0]
                            if nginx:
                                banner = banner+', nginx:'+nginx
                            # print "nginx",nginx
                        if plugins['nginx'].has_key('version'):
                            nginx = plugins['nginx']['version'][0]
                            if nginx:
                                banner = banner+', nginx:'+nginx
                            # print "nginx",nginx

                    if plugins.has_key('PHP'):
                        if plugins['PHP'].has_key('string'):
                            PHP = plugins['PHP']['string'][0]
                            # print "PHP",PHP
                            if PHP:
                                banner = banner+', PHP:'+PHP
                        if plugins['PHP'].has_key('version'):
                            PHP = plugins['PHP']['version'][0]
                            # print "PHP",PHP
                            if PHP:
                                banner = banner+', PHP:'+PHP

                    if plugins.has_key('JQuery'):
                        if plugins['JQuery'].has_key('string'):
                            JQuery = plugins['JQuery']['string'][0]
                            # print "JQuery",JQuery
                            if JQuery:
                                banner = banner+', JQuery:'+JQuery
                        if plugins['JQuery'].has_key('version'):
                            JQuery = plugins['JQuery']['version'][0]
                            # print "JQuery",JQuery
                            if JQuery:
                                banner = banner+', JQuery:'+JQuery
                    if plugins.has_key('Meta-Author'):
                        if plugins['Meta-Author'].has_key('string'):
                            Author = plugins['Meta-Author']['string'][0]
                            if Author:
                                banner = banner+', Author:'+Author
                            # print "Author",Author

                    if plugins.has_key('Email'):
                        if plugins['Email'].has_key('string'):
                            Email = plugins['Email']['string'][0]
                            if Email:
                                banner = banner+','+Email
                            # print "Email",Email

                    if plugins.has_key('HTML5'):
                        if plugins['HTML5'].has_key('string'):
                            HTML5 = plugins['HTML5']['string'][0]
                            if HTML5:
                                banner = banner+', HTML5:'+HTML5
                        else:
                            banner = banner+', HTML5'
                            # print "HTML5",HTML5


                if banner.startswith(','):
                    banner = banner[1:]

                if num == 0:
                    banner_tmp = banner

                if num !=0:
                    if banner:
                        extrabanner = extrabanner+','+banner+'***'
                    else:
                        extrabanner = extrabanner+'***'

            if extrabanner:
                if extrabanner[-3:] == '***':
                    extrabanner = extrabanner[:-3]
                if extrabanner.startswith(','):
                    extrabanner = extrabanner[1:]

                extrabanner = extrabanner.replace('***,','***')
                # print "extrabanner:",extrabanner
            banner_tmp = banner_tmp.decode('utf-8')
            extrabanner = extrabanner.decode('utf-8')
            Title_tmp = Title_tmp.decode('utf-8')

            if re.search(u"[\x80-\xff]",Title_tmp):
                Title_tmp = re.sub(u"[\x80-\xff]", '',Title_tmp)

            if re.search(u"[\x80-\xff]",banner_tmp):
                banner_tmp = re.sub(u"[\x80-\xff]", '',banner_tmp)

            if re.search(u"[\x80-\xff]",extrabanner):
                extrabanner = re.sub(u"[\x80-\xff]", '',extrabanner)

            return IP_tmp,http_status_tmp,Title_tmp,HTTPServer_tmp,xpb_tmp,banner_tmp,extrabanner
        else:
            return '','','','','','',''
    except Exception,e:
        print "\033[1;35m[!] get_whatweb error \033[0m!",e
        return '','','','','','',''


def get_waf(domain,target,logpath):
    os.chdir(pwd)
    try:
        print "-------------waf_start-------------"
        waf = 'wafw00f ' + target + ' >> ' + logpath + domain + '-waf.txt'
        print waf
        os.system(waf)
        print "+++++++++++++waf_ok+++++++++++++"
        # --------------waf-------------
        waf_text = open(logpath + domain + '-waf.txt', 'r').read()
        # print waf_text
        pattern1 = re.compile('is behind a (.*)')
        waf1 = re.findall(pattern1, waf_text)
        waf = 'UnDetect'
        if waf1:
            waf = waf1[0]

        pattern2 = re.compile('.*?seems to be behind a WAF.*?')
        waf2 = re.findall(pattern2, waf_text)
        if waf2:
            waf = 'Unknown_Waf'

        pattern3 = re.compile('.*?No WAF detected by.*?')
        waf3 = re.findall(pattern3, waf_text)
        if waf3:
            waf = 'NoWaf'
            # print waf
        return waf
    except Exception,e:
        print "\033[1;35m[!] Waf detect error \033[0m!",e
        return ""

def connect_port(ip, port):
    global open_port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            print '[+] ', port, 'open'
            open_port.append(port)
    except:
        pass

def scan_ip(ip,i):
    all_thread = []
    for p in range(i,i+scan_thread):
        if p==53:continue
        t = threading.Thread(target=connect_port, args=(ip, p))
        all_thread.append(t)
        t.start()
    for t in all_thread:
        t.join()

def ipaddrs(ip):
    ipaddl=ip.split('.')
    ipaddrs=[]
    for i in range(1,255):
        ipaddrs.append(ipaddl[0]+'.'+ipaddl[1]+'.'+ipaddl[2]+'.'+str(i))
    return ipaddrs


def up_host_scan(ipaddrs):
    try:
        ips_addr = str(ipaddrs)[3:-2].replace("', '"," ").replace("', u'"," ")
        # ips_addr = '127.0.0.1'
        # print ips_addr
        nm = nmap.PortScanner()
        print "Scanning up host ",ips_addr
        ping_scan_raw = nm.scan(hosts = ips_addr,arguments='-sn ')
        host_list_ip = []
        for result in ping_scan_raw['scan'].values():
            if result['status']['state'] == 'up':
                host_list_ip.append(result['addresses']['ipv4'])
        # return False
        print host_list_ip
        return sorted(host_list_ip)
    except Exception,e:
        print "up_host_scan Error:",time.strftime('%Y-%m-%d', time.localtime(time.time())),e
        return []

def scan_c_port(ip,scan_range,port_range):  # 扫描C段IP开放的端口，并返回C段开放的所有端口号（所有的累加后去重）
    try:
        global open_port
        if scan_range == 1:
            ipaddr = []
            ipaddr.append(ip)
        else:
            ipaddr = ipaddrs(ip)
            ip_up_addrs = up_host_scan(ipaddr)
            if ip_up_addrs:
                ipaddr = ip_up_addrs
        print "ipaddr length:",len(ipaddr)," ",ipaddr


        t1 = datetime.datetime.now()
        open_port = []

        for ip in ipaddr:

            if port_range == 1:   #port_range为1时扫描全端口
                print "scaning allport :", ip
                for i in range(1, 65535, scan_thread):
                # for i in port:
                    scan_ip(ip, i)
            else:
                print "scaning partport :", ip

                all_thread = []
                for p in port:
                    if p == 53: continue
                    t = threading.Thread(target=connect_port, args=(ip, p))
                    all_thread.append(t)
                    t.start()
                for t in all_thread:
                    t.join()

        port_items1 = set(list(open_port))
        port_items2 = []
        for x in port_items1:
            port_items2.append(x)
        port_items2.sort()
        open_port = port_items2
        target_port = str(open_port).replace(' ', '').replace('[', '').replace(']', '')
        print   ip, ':', target_port

        t2 = datetime.datetime.now()
        # print 'start_time', t1
        print '[ Scan ', ip, 'used', str((t2 - t1).seconds) + ' seconds ]'
        return target_port,ipaddr

    except:
        return "",""

def domain_nmap(xmlfile,domain,target,ip):
    if not ip:
        ip = url2ip(target)
    if ip:
        traget_open_port,ipaddr = scan_c_port(ip,1,2)  # ip地址，1=扫描单个地址 2=扫描c段，1=扫描所有端口 2=扫描部分端口
        if len(traget_open_port)>300:
            traget_open_port = '80,443,3306,22,3389'
        if traget_open_port:
            print "-------------nmap_start-------------"
            if debug_mod:
                nmap_cmd = "nmap -oX " + xmlfile + " " + domain + " -Pn --open -sS  -sV  -O --script=banner --host-timeout 30m  -p T:22,80,8080,3389"
            else:
                #nmap_cmd = "nmap -oX " + xmlfile + " " + target + " -Pn --open -sS  -sV  -O --script=banner  --host-timeout 30m  --version-all -p "+ traget_open_port ## 为加快速度，停止banner探测和version-all探测
				nmap_cmd = "nmap -oX " + xmlfile + " " + domain + " -Pn --open -sS  -sV  -O  --host-timeout 10m   -p "+ traget_open_port
                # nmap_cmd = "nmap -oX " + xmlfile + " " + sub_domain + " -Pn --open -sS  -sV -T4 -O --script=banner --min-parallelism 100  --host-timeout 20m  -p T:1,11,13,15,17,19,21,22,23,25,26,30,31,32,33,34,35,36,37,38,39,43,53,69,70,79,80,81,82,83,84,85,88,98,100,102,110,111,113,119,123,135,137,139,143,161,179,199,214,264,280,322,389,407,443,444,445,449,465,497,500,502,505,510,514,515,517,518,523,540,548,554,587,591,616,620,623,626,628,631,636,666,731,771,782,783,789,873,888,898,900,901,902,989,990,992,993,994,995,1000,1001,1010,1022,1023,1026,1040,1041,1042,1043,1080,1091,1098,1099,1200,1212,1214,1220,1234,1241,1248,1302,1311,1314,1344,1400,1419,1432,1434,1443,1467,1471,1501,1503,1505,1521,1604,1610,1611,1666,1687,1688,1720,1723,1830,1900,1901,1911,1947,1962,1967,2000,2001,2002,2010,2024,2030,2048,2051,2052,2055,2064,2080,2082,2083,2086,2087,2160,2181,2222,2252,2306,2323,2332,2375,2376,2396,2404,2406,2427,2443,2455,2480,2525,2600,2628,2715,2869,2967,3000,3002,3005,3052,3075,3128,3280,3306,3310,3333,3372,3388,3389,3443,3478,3531,3689,3774,3790,3872,3940,4000,4022,4040,4045,4155,4300,4369,4433,4443,4444,4567,4660,4711,4848,4911,5000,5001,5007,5009,5038,5050,5051,5060,5061,5222,5269,5280,5357,5400,5427,5432,5443,5550,5555,5560,5570,5598,5601,5632,5800,5801,5802,5803,5820,5900,5901,5902,5984,5985,5986,6000,6060,6061,6080,6103,6112,6346,6379,6432,6443,6544,6600,6666,6667,6668,6669,6670,6679,6697,6699,6779,6780,6782,6969,7000,7001,7002,7007,7070,7077,7100,7144,7145,7180,7187,7199,7200,7210,7272,7402,7443,7479,7547,7776,7777,7780,8000,8001,8002,8003,8004,8005,8006,8007,8008,8009,8010,8025,8030,8042,8060,8069,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8098,8112,8118,8129,8138,8181,8182,8194,8333,8351,8443,8480,8500,8529,8554,8649,8765,8834,8880,8881,8882,8883,8884,8885,8886,8887,8888,8890,8899,8983,9000,9001,9002,9003,9030,9050,9051,9080,9083,9090,9091,9100,9151,9191,9200,9292,9300,9333,9334,9443,9527,9595,9600,9801,9864,9870,9876,9943,9944,9981,9997,9999,10000,10001,10005,10030,10035,10080,10243,10443,11000,11211,11371,11965,12000,12203,12345,12999,13013,13666,13720,13722,14000,14443,14534,15000,15001,15002,16000,16010,16922,16923,16992,16993,17988,18080,18086,18264,19150,19888,19999,20000,20547,23023,25000,25010,25020,25565,26214,26470,27015,27017,27960,28006,28017,29999,30444,31337,31416,32400,32750,32751,32752,32753,32754,32755,32756,32757,32758,32759,32760,32761,32762,32763,32764,32765,32766,32767,32768,32769,32770,32771,32772,32773,32774,32775,32776,32777,32778,32779,32780,32781,32782,32783,32784,32785,32786,32787,32788,32789,32790,32791,32792,32793,32794,32795,32796,32797,32798,32799,32800,32801,32802,32803,32804,32805,32806,32807,32808,32809,32810,34012,34567,34599,37215,37777,38978,40000,40001,40193,44443,44818,47808,49152,49153,50000,50030,50060,50070,50075,50090,50095,50100,50111,50200,52869,53413,55555,56667,60010,60030,60443,61616,64210,64738,4786"
            print nmap_cmd
            lock.acquire()
            os.system(nmap_cmd)
            print "+++++++++++++nmap_ok+++++++++++++"

            checkend(xmlfile)
            nmap_info = parse_xml(xmlfile)
            lock.release()
            # nmap_info = 'test'
            return nmap_info
        else:
            return ""
    else:
        return ""

def port_scanner(host, target,ip_range,port_range):
    result = []
    ports = []
    try:
        scanner = nmap.PortScanner()
        if not host:
            host = url2ip(target)
        if host:
            traget_open_port,ipaddr = scan_c_port(host,ip_range,port_range)  # ip地址，1=扫描单个ip 2=扫描c段，1=全端口扫描 2=部分端口扫描
            updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if len(traget_open_port.split(','))>100:
                traget_open_port = '21,22,23,80,81,443,554,1080,1433,1900,3306,3389,7547,8080,8081,8082'
            if traget_open_port:
                arguments = "-sT -sV -sC -A -Pn -O --open -p " + traget_open_port
                print "Nmap Scaning: nmap ",arguments,' ',host
                # port processing
                scanner.scan(host, arguments=arguments)
                # port 'state' == 'open'
                print("Scanning: %s" % host)

                os =''
                for osmatch in scanner[host]['osmatch']:
                    os = osmatch['name']
                    break

                for port in scanner[host].all_tcp():
                    if scanner[host]['tcp'][port]['state'] == 'open':
                        if "script" in scanner[host]['tcp'][port].keys():
                            script = scanner[host]['tcp'][port]['script']
                            if script.has_key('http-robots.txt'):
                                script['http-robots_txt'] = script['http-robots.txt']
                                del script['http-robots.txt']
                        else:
                            script = ''
                        if len(scanner[host]['tcp'][port]['version']) > 0:
                            version = scanner[host]['tcp'][port]['version']
                        else:
                            version = 'Unknown'
                        if len(scanner[host]['tcp'][port]['product']) > 0:
                            product = scanner[host]['tcp'][port]['product']
                        else:
                            product = scanner[host]['tcp'][port]['name']
                        data = {
                            "product": product,
                            "version": version,
                            "name": scanner[host]['tcp'][port]['name'],
                            "script": script,
                            "extrainfo": scanner[host]['tcp'][port]['extrainfo'],
                            "cpe": scanner[host]['tcp'][port]['cpe'],
                            "host": host,
                            "port": port,
                            "updatetime":updatetime
                        }
                        ports.append(port)
                        result.append(data)
                return result,os,ports
    except Exception as msg:
        print(msg)
        pass
    return result,'',ports


def bugscan_cms(url,log):
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Referer": "http://whatweb.bugscaner.com/look/",
               }
    """
    try:
        res = requests.get('http://whatweb.bugscaner.com/look/',timeout=60, verify=False)
        if res.status_code==200:
            hashes = re.findall(r'value="(.*?)" name="hash" id="hash"',res.content)[0]
    except Exception as e:
        print str(e)
        return False
    """
    data = "url=%s&hash=0eca8914342fc63f5a2ef5246b7a3b14_7289fd8cf7f420f594ac165e475f1479" % (url)
    try:
        respone = requests.post("http://whatweb.bugscaner.com/what/", data=data, headers=headers,timeout=60,
                                verify=False)
        if int(respone.status_code) == 200:
            pattern1 = re.compile('.*?CMS": (.*?),')

            cms = re.findall(pattern1, respone.content)

            result = json.loads(respone.content)
            if len(result["CMS"]) > 0:
                # out.write(result["cms"].strip())
                return result["CMS"]
            else:
                return ''

    except Exception as e:
        print "bugscan_cms:",str(e)
        # out.write('Unknown')
        return ''



def check_info_changed(old_data,webinfo):
    try:

        info_changed = 0
        ip_changed=[]
        title_changed=[]
        if old_data.has_key('scan_times'):
            webinfo['scan_times'] = old_data['scan_times']+1
        else:
            webinfo['scan_times'] = 1

        if old_data:
            # print "old_data",old_data
            if old_data['ip'] != webinfo['ip']:
                if old_data.has_key('ip_changed'):
                    ip_changed = old_data['ip_changed']
                ip_changed.append(str(old_data['ip']) +'||'+str(old_data['title']) +'||'+str(old_data['ports'])+'||'+str(old_data['updatetime']))
                webinfo['ip_changed']=ip_changed

            if old_data['title'] != webinfo['title']:
                if old_data.has_key('title_changed'):
                    title_changed = old_data['title_changed']
                title_changed.append(str(old_data['ip']) +'||'+str(old_data['title']) +'||'+str(old_data['ports'])+'||'+str(old_data['updatetime']))
                webinfo['title_changed']=title_changed

            if webinfo['ports'] != old_data['ports']:  # 如果本次扫描的端口和上次不同，则创建新的port_info，从新数据到旧数据依次为port_info、port_info_2、port_info_3
                if  old_data.has_key('port_info_2'):
                    webinfo['port_info_3'] = old_data['port_info_2']
                    webinfo['ports_3'] = old_data['ports_2']
                    webinfo['port_info_2'] = old_data['port_info']
                    webinfo['ports_2'] = old_data['ports']
                else:
                    webinfo['port_info_2'] = old_data['port_info']
                    webinfo['ports_2'] = old_data['ports']

            for port_tmp in webinfo['ports']:
                if port_tmp not in old_data['ports']:
                    info_changed = 1
                    print "waring:",port_tmp
                    break
            if title_changed or ip_changed:
                info_changed = 1

        if info_changed:
            webinfo['info_changed'] = '1'

        return webinfo
    except Exception,e:
        print "\033[1;35m[!] check_info_changed error :\033[0m!",e
        return webinfo

class TimeoutError(Exception):
    pass

def run_check_cdn(cmd, timeout=60):
    try:
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        t_beginning = time.time()
        seconds_passed = 0
        while True:
            if p.poll() is not None:
                break
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                p.terminate()
                raise TimeoutError(cmd, timeout)
            time.sleep(0.1)
        return p.stdout.read()
    except:
        pass

def get_domain_info(sub_domain,sub_target,logpath,task):
    try:

        open(logpath + sub_domain + '-waf.txt', 'w').close()
        open(logpath + sub_domain + '-whatweb.txt', 'w').close()
        open(logpath +sub_domain + '-cdncheck.txt','w').close()
        outlog = open(logpath + sub_domain + '-domaininfo.txt', 'w')
        xmlfile = logpath +sub_domain + '-nmap.xml'
        cmslog = logpath +sub_domain + '-whatcms.xml'
        cdnlog = logpath +sub_domain + '-cdncheck.txt'
        open(xmlfile, 'w').close()
        ip=''
        nmap_info=''
        ports = ''
        os_tmp =''

        ip, state, title, httpserver, xpb,banner,extrabanner = get_whatweb(sub_domain, sub_target, logpath + sub_domain + '-whatweb.txt')

        # print "-------------check_cdn_start-------------"
        # cdn_check = 'python '+ pwd + '/check_cdn.py ' + sub_domain + " " + sub_target + " "+cdnlog
        run_check_cdn(cmd='python '+ pwd + '/check_cdn.py ' + sub_domain + " " + sub_target + " "+cdnlog, timeout=30)

        # print "+++++++++++++check_cdn_ok+++++++++++++"

        cdn_check_txt = open(cdnlog, 'r').read()
        if cdn_check_txt:
            cdn = cdn_check_txt.split('|')[0]
            cdn_cname = cdn_check_txt.split('|')[1]
        else:
            cdn =''
            cdn_cname =''
        print "cdn,cname",cdn,cdn_cname

        if not title:
            title = get_url_title(sub_target)

        if re.search(u"[\x80-\xff]", title):
            title = re.sub(u"[\x80-\xff]", '',title)

        if not ip:
            ip = url2ip(sub_target)

        waf = get_waf(sub_domain, sub_target,logpath)
        site_info = get_header(sub_target)
        cms = ''
        # if site_info:
        #     cms = bugscan_cms(sub_target,cmslog)

        hash = md5hash(sub_domain)
        if not site_info:
            site_info = ""

        if ip:
            ip_info = getipinfo(ip) #
        else:
            ip_info=''

        # nmap_info = domain_nmap(xmlfile,sub_domain,sub_target,ip)
        print "ip",ip

        port_range = 2
        if task.has_key('domain_fast_port_scan'):
            if task['domain_fast_port_scan'] == 'Disable':
                port_range = 1

        if ip:
            exist_ip_data = my_conn.db[mongo_server_db].find_one({'asset_task_id':str(task['_id']),'ip':ip},sort=[('updatetime',-1)])
            if exist_ip_data:
                now = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
                jiange = datetime.datetime.strptime(now,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(exist_ip_data['updatetime'],'%Y-%m-%d %H:%M:%S')
                print "jiange.days",jiange.days
                if jiange.days == 0:
                    nmap_info = exist_ip_data['port_info']
                    os_tmp = exist_ip_data['os']
                    ports = exist_ip_data['ports']
                else:
                    # if not cdn:
                    lock.acquire()
                    nmap_info,os_tmp,ports= port_scanner(ip,sub_target,1,port_range)  # 后面两个参数： 1=扫描单个ip 2=扫描c段，1=全端口扫描 2=部分端口扫描
                    lock.release()
                    print "nmap_info_ok"
            else:
                # if not cdn:
                lock.acquire()
                nmap_info,os_tmp,ports= port_scanner(ip,sub_target,1,port_range)  # 后面两个参数： 1=扫描单个ip 2=扫描c段，1=全端口扫描 2=部分端口扫描
                lock.release()
                print "nmap_info_ok"

        webinfo =''

        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        scan_times=1
        whatweb_info = {'asset_cus_id':task['asset_cus_id'],'asset_cus_name':task['asset_cus_name'],'asset_name':task['asset_name'],'asset_task_id':str(task['_id']),'scan_node':scan_node,
                        'target': sub_target, 'domain': sub_domain, 'state': state, 'title': title,'httpserver': httpserver,'cms':cms,'ip':ip,'ports':ports,'scan_times':scan_times,'cdn':cdn,'cdn_cname':cdn_cname,
                        'xpb': xpb,'banner':banner,'extrabanner':extrabanner,'waf': waf, 'site_info': site_info, 'hash': hash,'task_type':'web','port_info':nmap_info,'ip_info':ip_info,'os':os_tmp,'updatetime':str(updatetime)}
        webinfo = dict(whatweb_info.items())  # + nmap_info.items()

        if webinfo:
            outlog.write(str(webinfo).replace('http-robots.txt','http-rcheck_info_changedobots_txt'))
            query = {'hash': hash}
            old_data = my_conn.db[mongo_server_db].find_one(query)

            if old_data:
                webinfo_new = check_info_changed(old_data,webinfo)
                print "webinfo_new",webinfo_new
                print '*' * 50 + '\n' * 3 + "Updating data to mongodb :", sub_target + '\n' * 3 + '*' * 50

                my_conn.db[mongo_server_db].update({'hash':hash},{'$set':webinfo_new}, False, False)
            else:
                print "webinfo",webinfo
                print '*' * 50 + '\n' * 3 + "Inserting new data to mongodb :", sub_target + '\n' * 3 + '*' * 50
                my_conn.db[mongo_server_db].save(webinfo)

        else:
            print "Target can not connect :",sub_target

    except Exception,e:
        print "\033[1;35m[!] get_domain_info error :\033[0m!",e



def get_c_info(c_ip,target_ip,logpath,task):
    try:
        nmap_info=[]
        port_range = 2
        if task.has_key('c_fast_port_scan'):
            if task['c_fast_port_scan'] == 'Disable':
                port_range = 1

        nmap_info,os,ports = port_scanner(target_ip,target_ip,1,port_range)

        print "nmap_info:",nmap_info

        hash = md5hash(target_ip)
        ip_info = getipinfo(target_ip)

        http_flag = 0
        http_port = ''
        webinfo = {}
        scan_times= 1
        outlog = open(logpath + target_ip + '-domaininfo.txt', 'w')

        for port_tmp in nmap_info:
            if "http" in str(port_tmp['name']):
                http_flag = 1
                http_port = str(port_tmp['port'])
                break

        if http_flag and http_port:

            print "Find http service:",target_ip,http_port
            open(logpath + target_ip + '-waf.txt', 'w').close()
            open(logpath + target_ip + '-whatweb.txt', 'w').close()
            xmlfile = logpath +target_ip + '-nmap.xml'
            cmslog = logpath +target_ip + '-whatcms.xml'
            open(xmlfile, 'w').close()
            sub_target = add_protocal(target_ip+":"+http_port)
            print "sub_target",sub_target

            ip, state, title, httpserver, xpb,banner,extrabanner = get_whatweb(target_ip, sub_target, logpath + target_ip + '-whatweb.txt')

            if not title:
                title = get_url_title(sub_target)
            ip=target_ip

            waf = get_waf(target_ip, sub_target,logpath)
            # waf = ""
            site_info = get_header(sub_target)
            cms = ''
            # if site_info:
            #     cms = bugscan_cms(sub_target,cmslog)

            if not site_info:
                site_info = ""

            updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            whatweb_info = {'asset_cus_id':task['asset_cus_id'],'asset_cus_name':task['asset_cus_name'],'asset_name':task['asset_name'],'asset_task_id':str(task['_id']),'scan_node':scan_node,'scan_times':scan_times,
                            'target': sub_target, 'domain': sub_target, 'state': state, 'title': title,'httpserver': httpserver,'cms':cms,'ip':ip,'ports':ports,'banner':banner,'extrabanner':extrabanner,
                            'xpb': xpb, 'waf': waf, 'site_info': site_info, 'hash': hash,'task_type':'host','port_info':nmap_info,'ip_info':ip_info,'os':os,'updatetime':str(updatetime)}
            webinfo = dict(whatweb_info.items())  # + nmap_info.items()

        else:
            updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            whatweb_info = {'asset_cus_id':task['asset_cus_id'],'asset_cus_name':task['asset_cus_name'],'asset_name':task['asset_name'],'asset_task_id':str(task['_id']),'scan_node':scan_node,'scan_times':scan_times,
                            'ip':target_ip,'domain':target_ip, 'hash': hash,'task_type':'host','port_info':nmap_info,'ip_info':ip_info,'os':os,'updatetime':str(updatetime),'ports':ports}
            webinfo = dict(whatweb_info.items())

        print "webinfo",webinfo
        if webinfo:
            outlog.write(str(webinfo))
            query = {'hash': hash}
            old_data = my_conn.db[mongo_server_db].find_one(query)
            if old_data:
                webinfo_new = check_info_changed(old_data,webinfo)

                print '*' * 50 + '\n' * 3 + "Updating data to mongodb :", target_ip + '\n' * 3 + '*' * 50

                my_conn.db[mongo_server_db].update({'hash':hash},{'$set':webinfo_new}, False, False)
            else:
                print '*' * 50 + '\n' * 3 + "Inserting new data to mongodb :", target_ip + '\n' * 3 + '*' * 50
                my_conn.db[mongo_server_db].save(webinfo)

        else:
            print "Target can not connect :",target_ip

    except Exception,e:
        print "\033[1;35m[!] get_c_info error :\033[0m!",e


def get_host_info():
    try:
        hostname = socket.gethostname()
    except:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
        hostname = ip
        s.close()
    return hostname

def get_nmap_target(target):
    url = target
    if url[0:4] == 'http':
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
    else:
        host = url
    if ':' in host:
        host = host.split(':')[0]
    if '/' in host:
        host = host.split('/')[0]
    return host

def get_domain(target):
    try:
        url = target
        if url[0:4] == 'http':
            proto, rest = urllib.splittype(url)
            host, rest = urllib.splithost(rest)
            if host[0:3] == 'www':
                host = host[4:]
        elif url[0:3] == 'www':
            host = url[4:]
        else:
            host = url
        if ':' in host:
            host = host.split(':')[0]
        if '/' in host:
            host = host.split('/')[0]

        return host
    except:
        return target

def get_main_domain(domain):
    double_exts = ['.com.cn','.edu.cn','.gov.cn','.org.cn','.net.cn']

    main_domain = domain

    for ext in double_exts:
        if ext in domain:
            if len(domain.split('.')) > 3:
                # print "yuanshi",domain
                domain_split = domain.split('.')
                domain_new = "%s.%s.%s" % (domain_split[-3], domain_split[-2], domain_split[-1])
                # print "exact",domain
                main_domain = domain_new
            else:
                main_domain = domain

            break
        else:
            if len(domain.split('.')) > 2:
                domain_split = domain.split('.')
                domain_new = "%s.%s" % (domain_split[-2], domain_split[-1])
                main_domain = domain_new
            else:
                main_domain = domain
    return main_domain


def ip_regex(raw):
    try:
        re_ips = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',str(raw))
        if re_ips:
            return True
        else:
            return False
    except Exception,e:
        print e
        return False

def set_dirs(domain):
    global pwd, path
    path = pwd + '/libs/'
    daytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    logpath = pwd + '/log/' + daytime + '/' + domain + '/'

    try:
        if not os.path.exists(logpath):
            os.makedirs(logpath, 0755)
        if not os.path.exists(pwd + '/log/loginfo/'):
            os.makedirs(pwd + '/log/loginfo/', 0755)
        if not os.path.exists(logpath + 'temp/'):
            os.makedirs(logpath + 'temp/', 0755)
        if not os.path.exists(logpath + 'domain/'):
            os.makedirs(logpath + 'domain/', 0755)
        return logpath
    except Exception,e:
        print "\033[1;35m[!] Set Dirs Error \033[0m!",e
        return logpath


def add_protocal(sub_target):
    sub_target_tmp = sub_target
    try:
        if not sub_target.startswith("http"):
            sub_target_tmp = "http://" + sub_target
        res = requests.get(url=sub_target_tmp,  timeout=10, verify=False)
        return sub_target_tmp
    except:
        try:
            if not sub_target.startswith("http"):
                sub_target_tmp = "https://" + sub_target
            res = requests.get(url=sub_target_tmp,  timeout=10, verify=False)
            return sub_target_tmp
        except:
            return "http://" + sub_target


def insert_new_c_asset_task(task):  #要避免重复添加
    try:
        ip_datas = my_conn.db[mongo_server_db].find({'asset_task_id':str(task['_id'])})
        # my_conn.db[mongo_server_db].find({'asset_task_id':task['asset_cus_id']})
        existe_task_datas = my_conn.db[mongo_asset_db].find({'asset_cus_id':str(task['asset_cus_id'])})
        existe_task = []
        for task_tmp in existe_task_datas:
            existe_task.append(task_tmp['asset_name'])

        ip_tmp2 = []
        for ip_datas_tmp in ip_datas:
            ip_tmp1 = ip_datas_tmp['ip']
            ip_tmp2.append(ip_tmp1)
        ip_tmp3 = set(list(ip_tmp2))

        ip_tmp4 = []
        for xx in ip_tmp3:
            ip_tmp4.append(xx)

        ip_dics = {}
        ip_tmp6=[]
        for ip_tmp5 in ip_tmp4:
            ip = ip_tmp5.strip()
            if ip:
                ip_split = ip.split('.')
                c_ip = "%s.%s.%s.1/24" % (ip_split[0], ip_split[1], ip_split[2])

                if ip_dics.has_key(c_ip):
                    ip_dics[c_ip] = ip_dics[c_ip]+1
                    if ip_dics[c_ip] > 2:  # 3个以上ip在同一个c段的时候添加该c段为新任务
                        ip_tmp6.append(c_ip)
                else:
                    ip_dics[c_ip] = 1
        ip_tmp7 = set(list(ip_tmp6))

        ip_tmp8 = []
        for ip_task in ip_tmp7:
            if ip_task not in existe_task:
            # ip_task = ip_task.split()
            # ip_tmp8.append(ip_task)
                asset_data = {
                    'asset_name': ip_task,
                    'asset_host': ip_task,
                    'asset_cus_id': task['asset_cus_id'],
                    'c_fast_port_scan': task['c_fast_port_scan'],
                    'asset_cus_name': task['asset_cus_name'],
                    'admin_name': task['admin_name'],
                    "asset_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'discover_option': task['discover_option'],
                    'task_state':'new',
                    'asset_scan_zhouqi':task['asset_scan_zhouqi'],
                }
                print "new_task_name",ip_task
                my_conn.db[mongo_asset_db].insert_one(asset_data)
            else:
                print "existed task ",ip_task

    except Exception,e:
        print "\033[1;35m[!] insert_new_c_asset_task error,\033[0m!",e


def domain_task(main_domain,task_sub_domain,task):
    try:
        wm_domain_task = WorkManager(10)

        if task.has_key('scan_times'):
            scan_times = task['scan_times']+1
        else:
            scan_times = 1

        if ip_regex(main_domain):
            ipaddl=main_domain.split('.')
            ipaddr_path=ipaddl[0]+'_'+ipaddl[1]+'_'+ipaddl[2]+'_1'
            logpath = set_dirs(ipaddr_path)
            ipaddr = ipaddrs(main_domain)

            # print ipaddr
            ip_up_addrs = up_host_scan(ipaddr)
            # ip_up_addrs= ['123.134.184.189']
            # print ip_up_addrs
            for ip in ip_up_addrs:
                print "get_c_info:",ip
                wm_domain_task.add_job(get_c_info,main_domain,ip,logpath,task)
                # get_c_info(main_domain,ip,logpath,task)
                # exit(0)
            wm_domain_task.start()
            wm_domain_task.wait_for_complete()
            # print "c_scan"
            updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            my_conn.db[mongo_asset_db].update({'_id':task['_id']},{"$set": {"task_state": "ok","updatetime":updatetime,"scan_times":scan_times}}, False, False)

        else:
            if main_domain == 'other_host':
                logpath = set_dirs(main_domain)
                for task_sub_url in task_sub_domain:
                    task_sub_url = task_sub_url.strip()
                    sub_domain = get_domain(task_sub_url)
                    sub_target = add_protocal(task_sub_url)
                    wm_domain_task.add_job(get_domain_info,sub_domain, sub_target, logpath,task)
                wm_domain_task.start()
                wm_domain_task.wait_for_complete()
            else:
                all_targets,logpath,server_tmp = task_subdomain(main_domain,task_sub_domain)

                print "all_targets:", all_targets
                logpath = set_dirs(main_domain)

                for sub_target in all_targets:
                    sub_domain = sub_target.strip()
                    sub_target = add_protocal(sub_domain)
                    print sub_target
                    wm_domain_task.add_job(get_domain_info,sub_domain, sub_target, logpath,task)
                    # get_domain_info(sub_domain, sub_target, logpath,task)
                wm_domain_task.start()
                wm_domain_task.wait_for_complete()

            updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            my_conn.db[mongo_asset_db].update({'_id':task['_id']},{"$set": {"task_state": "ok","updatetime":updatetime,"scan_times":scan_times}}, False, False)
            if task.has_key('c_scan'):
                if  task['c_scan'] == 'Enable':
                    insert_new_c_asset_task(task)

    except Exception,e:
        print "\033[1;35m[!] domain_task error,\033[0m!",e


def mongo_task_get(task_num):

    task_ing_num = my_conn.db[mongo_asset_db].find({'task_state':'ing','scan_node':scan_node}).count()
    print "task_ing_num",task_ing_num
    if task_ing_num > 0:
        task_datas=[]
        task_ing_datas = my_conn.db[mongo_asset_db].find({'task_state':'ing','scan_node':scan_node}).sort('asset_date',1).limit(task_ing_num)

        if task_ing_num < task_num:
            task_new_num = my_conn.db[mongo_asset_db].find({'task_state':'new','discover_option':'Enable'}).sort('asset_date',1).count()
            print "task_new_num",task_new_num
            if task_new_num > 0:
                task_new_datas = my_conn.db[mongo_asset_db].find({'task_state':'new','discover_option':'Enable'}).sort('asset_date',1).limit(task_num-task_ing_num)
                for task_tmp_2 in task_new_datas:
                    task_datas.append(task_tmp_2)
        for task_tmp_1 in task_ing_datas:
            task_datas.append(task_tmp_1)
        return task_datas
    else:
        task_new_num = my_conn.db[mongo_asset_db].find({'task_state':'new','discover_option':'Enable'}).sort('asset_date',1).count()
        print "task_new_num",task_new_num
        if task_new_num > 0:
            task_datas = my_conn.db[mongo_asset_db].find({'task_state':'new','discover_option':'Enable'}).sort('asset_date',1).limit(task_num)
            return task_datas
        else:
            task_datas = my_conn.db[mongo_asset_db].find({'task_state':'ok','discover_option':'Enable'}).sort('scan_times',1)

            now = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
            new_tasks = []

            for task in task_datas:
                jiange = datetime.datetime.strptime(now,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(task['updatetime'],'%Y-%m-%d %H:%M:%S')
                if int(task['asset_scan_zhouqi']) == 0:
                    continue
                elif jiange.days >= int(task['asset_scan_zhouqi']):
                    new_tasks.append(task)
                    break
            return new_tasks

run_month = time.strftime('%m', time.localtime(time.time()))
run_day = time.strftime('%d', time.localtime(time.time()))

port = [1,11,13,15,17,19,21,22,23,25,26,30,31,32,33,34,35,36,37,38,39,43,53,69,70,79,80,81,82,83,84,85,88,98,100,102,110,111,113,119,123,135,137,139,143,161,179,199,214,264,280,322,389,407,443,444,445,449,465,497,500,502,505,510,514,515,517,518,523,540,548,554,587,591,616,620,623,626,628,631,636,666,731,771,782,783,789,873,888,898,900,901,902,989,990,992,993,994,995,1000,1001,1010,1022,1023,1026,1040,1041,1042,1043,1080,1091,1098,1099,1200,1212,1214,1220,1234,1241,1248,1302,1311,1314,1344,1400,1419,1432,1434,1443,1467,1471,1501,1503,1505,1521,1604,1610,1611,1666,1687,1688,1720,1723,1830,1900,1901,1911,1947,1962,1967,2000,2001,2002,2010,2024,2030,2048,2051,2052,2055,2064,2080,2082,2083,2086,2087,2160,2181,2222,2252,2306,2323,2332,2375,2376,2396,2404,2406,2427,2443,2455,2480,2525,2600,2628,2715,2869,2967,3000,3002,3005,3052,3075,3128,3280,3306,3310,3333,3372,3388,3389,3443,3478,3531,3689,3774,3790,3872,3940,4000,4022,4040,4045,4155,4300,4369,4433,4443,4444,4567,4660,4711,4848,4911,5000,5001,5007,5009,5038,5050,5051,5060,5061,5222,5269,5280,5357,5400,5427,5432,5443,5550,5555,5560,5570,5598,5601,5632,5800,5801,5802,5803,5820,5900,5901,5902,5984,5985,5986,6000,6060,6061,6080,6103,6112,6346,6379,6432,6443,6544,6600,6666,6667,6668,6669,6670,6679,6697,6699,6779,6780,6782,6969,7000,7001,7002,7007,7070,7077,7100,7144,7145,7180,7187,7199,7200,7210,7272,7402,7443,7479,7547,7776,7777,7780,8000,8001,8002,8003,8004,8005,8006,8007,8008,8009,8010,8025,8030,8042,8060,8069,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8098,8112,8118,8129,8138,8181,8182,8194,8333,8351,8443,8480,8500,8529,8554,8649,8765,8834,8880,8881,8882,8883,8884,8885,8886,8887,8888,8890,8899,8983,9000,9001,9002,9003,9030,9050,9051,9080,9083,9090,9091,9100,9151,9191,9200,9292,9300,9333,9334,9443,9527,9595,9600,9801,9864,9870,9876,9943,9944,9981,9997,9999,10000,10001,10005,10030,10035,10080,10243,10443,11000,11211,11371,11965,12000,12203,12345,12999,13013,13666,13720,13722,14000,14443,14534,15000,15001,15002,16000,16010,16922,16923,16992,16993,17988,18080,18086,18264,19150,19888,19999,20000,20547,23023,25000,25010,25020,25565,26214,26470,27015,27017,27960,28006,28017,29999,30444,31337,31416,32400,32750,32751,32752,32753,32754,32755,32756,32757,32758,32759,32760,32761,32762,32763,32764,32765,32766,32767,32768,32769,32770,32771,32772,32773,32774,32775,32776,32777,32778,32779,32780,32781,32782,32783,32784,32785,32786,32787,32788,32789,32790,32791,32792,32793,32794,32795,32796,32797,32798,32799,32800,32801,32802,32803,32804,32805,32806,32807,32808,32809,32810,34012,34567,34599,37215,37777,38978,40000,40001,40193,44443,44818,47808,49152,49153,50000,50030,50060,50070,50075,50090,50095,50100,50111,50200,52869,5341,55555,56667,60010,60030,60443,61616,64210,64738,4768]

# port =[80,443,843,8080,18556,19359]

log = open('losg.txt','a+')
scan_node = get_host_info()
lock=threading.Lock()
# host_info = 'tide120'
print "scan_node:",scan_node

task_num = 5
scan_thread = 5000

mongo_asset_db = 'dev_asset'
mongo_server_db = 'dev_server'



pwd = os.getcwd()


if __name__ == "__main__":
    now = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    while True:
        try:
            my_conn = MongoConn()
            check_connected(my_conn)
            start = datetime.datetime.now()
            pwd = os.getcwd()

            now_day = time.strftime('%d', time.localtime(time.time()))

            targets=[]
            task_datas = mongo_task_get(task_num)
            domain_thread = []
            wm = WorkManager(5)
            # exit(0)

            if task_datas:
                for task in task_datas:
                    if task:
                        print task
                        if task['task_state'] == 'new':
                            my_conn.db[mongo_asset_db].update({'_id':task['_id']},{"$set": {"task_state": "ing",'scan_node':scan_node}}, False, False)

                        main_domain = task['asset_name']
                        task_sub_domain = task['asset_host']
                        print '\n' * 2 + "Start Scan Target:", tran2UTF8(main_domain), '\n'
                        wm.add_job(domain_task,main_domain,task_sub_domain,task)

                wm.start()
                wm.wait_for_complete()

            end = datetime.datetime.now()
            print "starttime:", start
            print "endtime:", end
            print "time_use:", (end - start).seconds
            time.sleep(300)
            # exit(0)
        except Exception, e:
            info = '\033[1;35m[!]%s\n Main_function Error: %s\033[0m!' % (now, e)
            print info


