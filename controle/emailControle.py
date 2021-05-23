# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import cast

# create message object instance 
msg = MIMEMultipart()
# setup the parameters of the message
password = "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"
msg['From'] = "grupopenelopechavosa@gmail.com"
msg['login'] = "apikey"

def envia_senha(nome, dest, senha):
    try:
        msg['Subject'] = "Nova senha, JLControl"
        message = f"Olá {nome},\
                    aqui está sua nova senha: {senha}"

        msg['To'] = dest    

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #create server
    
        server = smtplib.SMTP('smtp.sendgrid.net: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['login'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()
        return 200
    except:
        return 400
    