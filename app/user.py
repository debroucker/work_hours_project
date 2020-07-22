#email imports
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def sendMailForgetPassWord(toaddr, password) :
    """
    send an email. (used to send an email for forgot password).
    :param: toaddr: email destination.
    :param password: the password to send.
    """
    fromaddr = "YOUR_GMAIL_EMAIL_TO_SEND"
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    # storing the senders email address 
    msg['From'] = fromaddr 
    # storing the receivers email address 
    msg['To'] = toaddr 
    # storing the subject 
    msg['Subject'] = "Mot de passe oublié"
    # string to store the body of the mail 
    body = "Votre mot de passe : " + password + "\nMail automatique." 
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(fromaddr, "YOUR_PASSWORD") 
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    # terminating the session 
    s.quit() 