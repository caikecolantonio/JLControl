# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import cast

# create message object instance 
msg = MIMEMultipart()
# setup the parameters of the message
password = "chavosa2020"
msg['From'] = "grupopenelopechavosa@gmail.com"

def envia_senha(nome, dest, senha):
    msg['Subject'] = "Nova senha, JLControl"
    message = f"Olá {nome},\
                aqui está sua nova senha: {senha}"

    msg['To'] = dest    

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #create server
    
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()
    return 200

    