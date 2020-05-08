#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt

from re import search
from lib.utils.printer import *

def errors(content,url):
	patterns = ("<font face=\"Arial\" size=2>error \'800a0005\'</font>",
				"<h2> <i>Runtime Error</i> </h2></span>",
				"<p>Active Server Pages</font> <font face=\"Arial\" size=2>error \'ASP 0126\'</font>",
				"<b> Description: </b>An unhandled exception occurred during the execution of the",
				"<H1>Error page exception</H1>",
				"<h2> <i>Runtime Error</i> </h2></span>",
				"<h2> <i>Access is denied</i> </h2></span>",
				"<H3>Original Exception: </H3>",
				"Server object error",
				"invalid literal for int()",
				"exceptions.ValueError",
				"\[an error occurred while processing this directive\]",
				"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE>",
				"</HEAD><BODY><HR><H3>Error Occurred While Processing Request</H3><P>",
				"\[java.lang.",
				"class java.lang.",
				"java.lang.NullPointerException",
				"java.rmi.ServerException",
				"at java.lang.",
				"onclick=\"toggle(\'full exception chain stacktrace\')",
				"at org.apache.catalina",
				"at org.apache.coyote.",
				"at org.apache.tomcat.",
				"at org.apache.jasper.",
				"<html><head><title>Application Exception</title>",
				"<p>Microsoft VBScript runtime </font>",
				"<font face=\"Arial\" size=2>error '800a000d'</font>",
				"<TITLE>nwwcgi Error",
				"\] does not contain handler parameter named",
				"PythonHandler django.core.handlers.modpython",
				"t = loader.get_template(template_name) # You need to create a 404.html template.",
				"<h2>Traceback <span>(innermost last)</span></h2>",
				"<h1 class=\"error_title\">Ruby on Rails application could not be started</h1>",
				"<title>Error Occurred While Processing Request</title></head><body><p></p>",
				"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE></HEAD><BODY><HR><H3>",
				"<TR><TD><H4>Error Diagnostic Information</H4><P><P>",
				"<li>Search the <a href=\"http://www.macromedia.com/support/coldfusion/\"",
				"target=\"new\">Knowledge Base</a> to find a solution to your problem.</li>",
				"Server.Execute Error",
				"<h2 style=\"font:8pt/11pt verdana; color:000000\">HTTP 403.6 - Forbidden: IP address rejected<br>",
				"<TITLE>500 Internal Server Error</TITLE>",
				"<b>warning</b>[/]\w\/\w\/\S*",
				"<b>Fatal error</b>:",
				"<b>Warning</b>:",
				"open_basedir restriction in effect",
				"eval()'d code</b> on line <b>",
				"Fatal error</b>:  preg_replace",
				"thrown in <b>",
				"Stack trace:",
				"</b> on line <b>"
				)
	for pattern in patterns:
		if search(pattern,content):
			plus("Found: \"%s\" at %s"%(pattern,url))