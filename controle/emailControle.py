# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime, timezone, timedelta
from controle.models import LogEmail

# create message object instance 


def envia_senha(nome, dest, senha):
    msg = MIMEMultipart()
    msg['Subject'] = "JLima Control - Nova senha"
    message = f"Olá {nome}!\n Aqui está sua nova senha: {senha}"
    msg['To'] = dest
    # add in the message body
    return envia(msg, message)


def avisa_trajes(locacao, cliente, lista):
    msg = MIMEMultipart()
    msg['Subject'] = "JLima Control - Avisos"
    message = f"Olá {cliente.nome}!\n"
    message = message + f"Os seguintes trajes estão disponíveis para retirar:\n"
    for item in lista:
        message = message + f"{item.traje.nome} de modelo {item.traje.modelo} com corte {item.traje.corte} ficou pronto em {item.data_entrega.astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M')}.\n"
    message = message + f"Atenciosamente."
    msg['To'] = cliente.email  
    return envia(msg, message)


def envia(msg, corpo):
    try:
        # setup the parameters of the message
        password = "0npwbKjXkyr2Wz8J"
        msg['From'] = "grupopenelopechavosa@gmail.com"
        msg['login'] = "grupopenelopechavosa@gmail.com"
        # add in the message body
        msg.attach(MIMEText(corpo, 'plain'))      
        server = smtplib.SMTP('smtp-relay.sendinblue.com: 587')  
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['login'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        cria_log(msg['Subject'], msg['To'], corpo)
        server.quit()
        return 200
    except:
        return 400


def cria_log(titulo, dest, mensagem):
    email = LogEmail.objects.create(titulo=titulo, destinatario=dest, mensagem=mensagem)
    email.save()