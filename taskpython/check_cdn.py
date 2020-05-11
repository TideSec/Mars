#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/4/12 下午4:58
# @Author  : 重剑无锋
# @Site    : www.tidesec.com
# @Email   : 6295259@qq.com

import requests,urlparse,threading,os,sys,time,urllib2
import dns.resolver,random

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

class check_dns_resolve_num:
    def __init__(self,domain,dns_dict):
        self.domain = domain
        self.myResolver = dns.resolver.Resolver()
        self.dns_list = dns_dict
        self.good_dns_list,self.result_ip = set(),set()

    def test_dns_server(self,server):
        self.myResolver.lifetime = self.myResolver.timeout = 2.0
        try:
            self.myResolver.nameservers = [server]
            sys.stdout.write('[+] Check Dns Server %s \r' % server)
            sys.stdout.flush()
            answer = self.myResolver.query('google-public-dns-a.google.com')
            if answer[0].address == '8.8.8.8':
                self.good_dns_list.add(server)
        except:
            pass

    def load_dns_server(self):
        print '[+] Load Dns Servers ...',time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        threads = []
        for i in self.dns_list:
            threads.append(threading.Thread(target=self.test_dns_server,args=(i,)))
        for t in threads:
            t.start()
            while True:
                if len(threading.enumerate()) < len(self.dns_list) / 2:
                    break
                else:
                    time.sleep(1)
        print '\n[+] Release The Thread ...'
        for j in threads: j.join()
        print '[+] %d Dns Servers Available' % len(self.good_dns_list)

    def ip(self,dns_server):
        self.myResolver.nameservers = [dns_server]
        try:
            result = self.myResolver.query(self.domain)
            for i in result:
                self.result_ip.add(str(i.address))
        except:
            pass

    def run(self):
        self.load_dns_server()
        print '[+] Dns Servers Test Target Cdn ...'
        threads = []
        for i in self.good_dns_list:
            threads.append(threading.Thread(target=self.ip,args=(i,)))
        for t in threads:
            t.start()
            while True:
                if len(threading.enumerate()) < len(self.good_dns_list) / 2:
                    break
                else:
                    time.sleep(1)
        for j in threads: j.join()
        for i in self.result_ip: print i
        print time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

        if  len(self.result_ip) > 1:
            return True
        else:
            return False

class CdnCheck(object):
    def __init__(self, url):
        super(CdnCheck, self).__init__()
        self.cdninfo()
        self.url = url
        self.cnames = []
        self.headers = []

    def get_cnames(self): # get all cname
        furl = urlparse.urlparse(self.url)
        url = furl.netloc

        rsv = dns.resolver.Resolver()
        # rsv.nameservers = ['8.8.8.8']
        try:
            answer = dns.resolver.query(url,'CNAME')
        except Exception as e:
            self.cnames = None
            # print "ERROR: %s" % e
        else:
            cname = [_.to_text() for _ in answer][0]
            self.cnames.append(cname)
            self.get_cname(cname)

    def get_cname(self,cname): # get cname
        try:
            answer = dns.resolver.query(cname,'CNAME')
            cname = [_.to_text() for _ in answer][0]
            self.cnames.append(cname)
            self.get_cname(cname)
        except dns.resolver.NoAnswer:
            pass

    def get_headers(self): # get header
        try:
            resp = urllib2.urlopen(self.url,timeout=10)
        except:
            try:
                resp = requests.get(self.url, headers=requests_headers(),timeout=10)
                self.headers = str(resp.headers)
            except:
                self.headers = None
            # print "ERROR: %s" % e
        else:
            headers = str(resp.headers).lower()
            self.headers = headers

    def matched(self, context, *args): # Matching string
        if not isinstance(context, basestring):
            context = str(context)

        func = lambda x, y: y in x
        for pattern in args:
            if func(context,pattern):
                return pattern
        return False

    def check(self):
        flag = None
        self.get_cnames()
        self.get_headers()
        # print self.headers

        if self.cnames:
            flag = self.matched(self.cnames,*self.cdn['cname'])
            if flag:
                return {'Status':True, 'CDN':self.cdn['cname'].get(flag),'CNAME':self.cnames}

        if not flag and self.headers:
            flag = self.matched(self.headers,*self.cdn['headers'])
            if flag:
                return {'Status':True, 'CDN':self.cdn['headers'].get(flag),'CNAME':self.cnames}

        return {'Status':False, 'CNAME':self.cnames}

    def cdninfo(self):
        self.cdn = {
            'headers': {
                'via':u'OtherCdn',
                'x-via':u'OtherCdn',
                'by-360wzb':u'360wzb',
                'by-anquanbao':u'anquanbao',
                'cc_cache':u'OtherCdn',
                'cdn cache server':u'cdn cache server',
                'cf-ray':u'cf-ray',
                'chinacache':u'chinacache',
                'verycdn':u'verycdn',
                'webcache':u'OtherCdn',
                'x-cacheable':u'OtherCdn',
                'x-fastly':u'x-fastly',
                'yunjiasu':u'yunjiasu',
                'wzws':u'360wzws',
                'cfduid':u'CloudFlare'
            },
            'cname': {
                'tbcache.com':u'taobao', # 应该是淘宝自己的。。。。
                'cloudfront.net':u'CloudFrontCdn',
                'amazonaws.com':u'Amazon CloudFrontCdn',
                'tcdn.qq.com':u'tcdn.qq.com', # 应该是腾讯的。。。
                'cdn.dnsv1.com':u'TencentCdn',
                'cdntip':u'TencentCdn',
                'yunjiasu':u'Baiduyun', # 百度云加速
                'kunlunar.com':u'ALiyun', # 阿里云
                'kunlunca.com':u'ALiyun', # 阿里云
                'aliyuncs.com':u'ALiyun', # 阿里云
                'aliyun-inc.com':u'ALiyun', # 阿里云
                'kxcdn.com':u'KeyCDN', # KeyCDN
                'lswcdn.net':u'Leaseweb', # Leaseweb
                'lxcdn.com':u'WangSuCdn', # 网宿科技
                'wscloudcdn':u'WangSuCdn', # 网宿科技
                'cdn20.com':u'WangSuCdn', # 网宿科技
                'lxdns.com':u'WangSuCdn', # 网宿科技
                'qiniudns.com':u'QiNiuCdn',
                '365cyd.cn':u'ChuangYuDun',
                'cdn':u'OtherCdn',
                '360safedns.com':u'360Cdn',
                'strikinglydns.com':u'CloudFire',
                # 其余的特征可以自己找一下
            }
        }

# pip install dnspython
def check_cname_cdn(url):
    # url = "http://www.sanshan.gov.cn"
    # url = sys.argv[1]
    cdn_check = CdnCheck(url)
    cdndict = cdn_check.check()
    print "cdndict:",cdndict
    cdn_cname = ''
    cdn =''
    if cdndict:
        if cdndict.has_key('Status'):
            if cdndict['Status']:
                if cdndict.has_key('CDN'):
                    cdn = cdndict['CDN']
                else:
                    cdn = 'UnKnownCdn'
                if cdndict.has_key('CNAME'):
                    if cdndict['CNAME']:
                        for x in cdndict['CNAME']:
                            cdn_cname = cdn_cname +'|'+x
                        if cdn_cname.startswith('|'):
                            cdn_cname = cdn_cname[1:]
                    else:
                        cdn_cname=''
    return cdn,cdn_cname

dns_list = ["8.8.8.8","8.8.4.4","208.67.222.222","208.67.220.220","208.67.222.123","208.67.220.123","216.146.35.35","216.146.36.36","8.26.56.26","8.20.247.20","156.154.70.1","156.154.71.1","199.85.126.10","199.85.127.10","114.114.114.114","114.114.115.115","223.5.5.5","223.6.6.6","180.76.76.76","1.1.1.1"]

if __name__ == "__main__":
    sub_domain = sys.argv[1]
    sub_target = sys.argv[2]
    outfile = open(sys.argv[3],'w')

    check_dns_resolve_cdn = check_dns_resolve_num(sub_domain,dns_list)
    dns_resolve_cdn = check_dns_resolve_cdn.run()
    cdn = ''
    cdn_cname = ''
    if dns_resolve_cdn:
        cdn = "UnKownCdn"
        cdn_tmp,cdn_cname_tmp = check_cname_cdn(sub_target)
        if cdn_tmp:
            cdn = cdn_tmp
        if cdn_cname_tmp:
            cdn_cname = cdn_cname_tmp
        outfile.write(cdn+'|'+cdn_cname)
    else:
        outfile.write('')
    outfile.close()
