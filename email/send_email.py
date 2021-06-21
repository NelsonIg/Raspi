import smtplib, ssl
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr  = sys.argv[sys.argv.index('-a') + 1] # email address
        passwd = sys.argv[sys.argv.index('-p') + 1] # password
        msg = sys.argv[sys.argv.index('-m') + 1] # msg
        
    port = 465  # For SSL
    smtp_server = "smtp." + addr.split('@')[1]
    message = """\
Subject: Automated Email from Raspi

""" + msg
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(addr, passwd)
        server.sendmail(addr, addr, message)