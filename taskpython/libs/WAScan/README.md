WAScan - Web Application Scanner
--

__WAScan__ ((__W__)eb (__A__)pplication (__Scan__)ner) is a Open Source web application security scanner. It is designed to find various vulnerabilities using "black-box" method, that means it won't study the source code of web applications but will work like a fuzzer, scanning the pages of the deployed web application, extracting links and forms and attacking the scripts, sending payloads and looking for error messages,..etc. WAScan is built on python2.7 and can run on any platform which has a Python environment.

![screen](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen.png)

Features
--

**Fingerprint**
- _Content Management System (CMS)_ -> __6__
- _Web Frameworks_ -> __22__
- _Cookies/Headers Security_
- _Languages_ -> __9__
- _Operating Systems (OS)_ -> __7__
- _Server_ -> __ALL__ 
- _Web App Firewall (WAF)_ -> __50+__

**Attacks**
- _Bash Commands Injection_
- _Blind SQL Injection_
- _Buffer Overflow_
- _Carriage Return Line Feed_
- _SQL Injection in Headers_
- _XSS in Headers_
- _HTML Injection_
- _LDAP Injection_
- _Local File Inclusion_
- _OS Commanding_
- _PHP Code Injection_
- _SQL Injection_
- _Server Side Injection_
- _XPath Injection_
- _Cross Site Scripting_
- _XML External Entity_

**Audit**
- _Apache Status Page_
- _Open Redirect_
- _PHPInfo_
- _Robots.txt_
- _XST_

**Bruteforce**
- _Admin Panel_
- _Common Backdoor_
- _Common Backup Dir_
- _Common Backup File_
- _Common Dir_
- _Common File_
- _Hidden Parameters_

**Disclosure**
- _Credit Cards_
- _Emails_
- _Private IP_
- _Errors_ -> (__fatal errors__,...)
- _SSN_

Installation
--
```
$ git clone https://github.com/m4ll0k/WAScan.git wascan
$ cd wascan 
$ pip install BeautifulSoup
$ python wascan.py
```

Usage
--
__Fingerprint:__
```
$ python wascan.py --url http://xxxxx.com/ --scan 0
```
![screen_2](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen_2.png)

__Attacks:__
```
$ python wascan.py --url http://xxxxx.com/index.php?id=1 --scan 1
```
![screen_3](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen_3.png)

__Audit:__
```
$ python wascan.py --url http://xxxxx.com/ --scan 2
```
![screen_4](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen_4.png)

__Bruteforce:__
```
$ python wascan.py --url http://xxxxx.com/ --scan 3
```
![screen_5](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen_5.png)

__Disclosure:__
```
$ python wascan.py --url http://xxxxx.com/ --scan 4
```
![screen_5](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen_6.png)

__Full Scan:__
```
$ python wascan.py --url http://xxxxx.com --scan 5 
```
![screen_5](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen_7.png)

__Bruteforce Hidden Parameters:__
```
$ python wascan.py --url http://xxxxx.com/test.php --brute
```
![screen_5](https://raw.githubusercontent.com/m4ll0k/WAScan/master/screen/screen_8.png)

Advanced Usage
--
```
$ python wascan.py --url http://xxxxx.com/test.php --scan 5 --auth "admin:1234"
$ python wascan.py --url http://xxxxx.com/test.php --scan 5 --data "id=1" --method POST
$ python wascan.py --url http://xxxxx.com/test.php --scan 5 --auth "admin:1234" --proxy xxx.xxx.xxx.xxx 
$ python wascan.py --url http://xxxxx.com/test.php --scan 5 --auth "admin:1234" --proxy xxx.xxx.xxx.xxx --proxy-auth "root:4321"
$ python wascan.py --url http://xxxxx.com/test.php --scan 5 --auth "admin:1234" --proxy xxx.xxx.xxx.xxx --proxy-auth "root:4321 --ragent -v
```
