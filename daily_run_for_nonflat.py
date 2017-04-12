#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'jie.su2@hpe.com'

import urllib, urllib2, re
import MySQLdb, datetime, sys
import time

url = "http://speedy.arubanetworks.com/cgi-bin/re/build_info_mysql.html"

version = sys.argv[1]
print version
branch = sys.argv[2]
print branch
values = {'codeline': branch, 'submit': 'search'}
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
time.sleep(2)
response = urllib2.urlopen(req)
time.sleep(5)
the_page = response.read()

m = re.search(r'http?://speedy\.arubanetworks\.com/cgi\-bin/re/comments\.html\?id=(\d+)', the_page, re.M | re.I)
build = m.group(1)
version_build = version + '_' + str(build)
dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
try:
    conn = MySQLdb.connect(host='10.65.10.26', user='root', passwd='123456', port=3306, db='autoSmoke', charset='latin1')
    cur = conn.cursor()
    iap_webui = "insert INTO queue (priority,userName,status,description,dbResults,tftpIP,creationDate,lastChangeDate,build,command,testbed,suite) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
          ('0', 'nightly', '2', 'Automatically queued from Nightly Build Server',\
           'Y', 'IP:10.1.1.41,ftp,anonymous,anonymous,',dt,dt,version_build, 'GA:1', 'TB:iap_webui', 'DD:S')
    iap_wired = "insert INTO queue (priority,userName,status,description,dbResults,tftpIP,creationDate,lastChangeDate,build,command,testbed,suite) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
          ('0', 'nightly', '2', 'Automatically queued from Nightly Build Server',\
           'Y', 'IP:10.1.1.41,ftp,anonymous,anonymous,',dt,dt,version_build, 'GA:1', 'TB:iap_wired', 'DD:S')
    iap_3g = "insert INTO queue (priority,userName,status,description,dbResults,tftpIP,creationDate,lastChangeDate,build,command,testbed,suite) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
          ('0', 'nightly', '2', 'Automatically queued from Nightly Build Server',\
           'Y', 'IP:10.1.1.41,ftp,anonymous,anonymous,',dt,dt,version_build, 'GA:1', 'TB:iap_3g', 'DD:S')
    iap_mixed_network = "insert INTO queue (priority,userName,status,description,dbResults,tftpIP,creationDate,lastChangeDate,build,command,testbed,suite) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
          ('0', 'nightly', '2', 'Automatically queued from Nightly Build Server',\
           'Y', 'IP:10.1.1.41,ftp,anonymous,anonymous,',dt,dt,version_build, 'GA:1', 'TB:iap_mixed_network', 'DD:S')
    iap_wifi_uplink = "insert INTO queue (priority,userName,status,description,dbResults,tftpIP,creationDate,lastChangeDate,build,command,testbed,suite) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
          ('0', 'nightly', '2', 'Automatically queued from Nightly Build Server',\
           'Y', 'IP:10.1.1.41,ftp,anonymous,anonymous,',dt,dt,version_build, 'GA:1', 'TB:iap_wifi_uplink', 'DD:S')
    cur.execute(iap_webui)
    cur.execute(iap_wired)
    cur.execute(iap_3g)
    cur.execute(iap_mixed_network)
    cur.execute(iap_wifi_uplink)
    cur.close()
    conn.commit()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
