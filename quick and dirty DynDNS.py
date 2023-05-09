"""
Quick and dirty DynDNS client in python.
Published  on May 9, 2023 (queries: mrjoemaina01 at gmail dot com)
I needed a client for my dyndns account to run on Linux. I could of course use something like ddclient which I’m sure would work great, but the API is so simple it seems like a waste to use a 4500+ line perl script to do it. Instead I just wrote up a quick and dirty Python + Requests script which works great. I thought I’d share it.
 
The error messaging isn’t very pythonic, and there’s no logging which would be nice, but I popped it in my /etc/cron.hourly folder and it works great.
"""
#!/usr/bin/python
import requests
import json
 
user = "your user name here"
password = "your api code here (or password)"
checkip = "http://thisisnt.com/api/getRemoteIp.php"
dynupdate = "https://members.dyndns.com/nic/update"
 
 
 
print("starting. Get current IP...")
ipraw = requests.get(checkip)
if ipraw.status_code is not 200:
  raise "Cannot get IP address"
  exit
  
ip = ipraw.json()['REMOTE_ADDR']
print("Remote IP: " + ip)
print("updating...")
 
# update dyndns
headers = {'user-agent': 'mPythonClient/0.0.3'}
dyn = requests.get(dynupdate, \
              headers=headers, \
              auth=(user, password), \
              params={'hostname': '<domain name to update>', \
                       'myip': ip, \
                       'wildcard': 'NOCHG', \
                       'mx': '<mx host for domain>', \
                       })
 
if dyn.status_code is not 200:
  print("Update failed. HTTP Code: " + str(dyn.status_code))
if "good" in dyn.text:
  print("update successful..")
else:
  print("Update unsuccessful: " + dyn.text.strip())