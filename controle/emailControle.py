# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime, timezone, timedelta

# create message object instance 
msg = MIMEMultipart()
# setup the parameters of the message
password = "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"
msg['From'] = "grupopenelopechavosa@gmail.com"
msg['login'] = "apikey"
#create server
server = smtplib.SMTP('smtp.sendgrid.net: 587')

def envia_senha(nome, dest, senha):
    try:
        msg['Subject'] = "JLima Control - Nova senha"
        message = f"Olá {nome}!\n \
                    Aqui está sua nova senha: {senha}"

        msg['To'] = dest    
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['login'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return 200
    except:
        return 400

def avisa_trajes(locacao, cliente, lista):
    try:
        msg['Subject'] = "JLima Control - Avisos"
        message = f"Olá {cliente.nome}!\n"
        message = message + f"Os seguintes trajes estão disponíveis para retirar:\n"
        for item in lista:
            message = message + f"{item.traje.nome} de modelo {item.traje.modelo} com corte {item.traje.corte} ficou pronto em {item.data_entrega.astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M')}.\n"
        message = message + f"Atenciosamente."
        msg['To'] = cliente.email  
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))        
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['login'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return 200
    except:
        return 400