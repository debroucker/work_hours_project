import datetime
from datetime import datetime
import time
import genLib as gl
import sys
import mailHour as mh
#email imports
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def watchEveryHour(userFile, fileToSend, workerFile, hourFile, cssFile, fileNameWorker) :
    """
    watch every hour if we are into 00:00 and 01:00 at the 1 of the month.
    If it is, send an email with all work hours of all workers.
    :param userFile: path of the userFile (includes password, and email).
    :param fileToSend: the path of the file to send. This is the file with all work hours of all workers.
    :param workerFile: the path to the file with work hours.
    :param hourFile: the path to the html file, to write on it.
    :param cssFile: the path to the css file, to write it in the html file. (when the html file is sended by email, we don't need to send the css file).
    :param fileNameWorker: the path to the file includes all names and firstname worker. Used to empty workerFile, and write on it the name and forstname's workers.
    """
    while True :
        now = datetime.now()
        date = now.strftime("%d;%H")
        splitDate = date.split(";")
        day = int(splitDate[0])
        hour = int(splitDate[1])
        if day == 1 and hour <= 1 :
            mh.hoursDataBase(workerFile, hourFile, cssFile, False)
            mail = gl.getLinesOfFile(userFile)[1]
            if sendMail(mail, fileToSend) :
                mh.emptyHour(hourFile, fileNameWorker)
        time.sleep(3600)

def sendMail(toaddr, fileToSend) :
    """
    send an email with attachment.
    :param: toaddr: email destination.
    :param fileToSend: path to the html file.
    :rtype: bool
    :return: true if mail is sending, false otherwise.
    """
    try :
        fromaddr = "YOUR_GMAIL_EMAIL_TO_SEND"
        # instance of MIMEMultipart 
        msg = MIMEMultipart() 
        # storing the senders email address 
        msg['From'] = fromaddr 
        # storing the receivers email address 
        msg['To'] = toaddr 
        # storing the subject 
        msg['Subject'] = "horaire du mois de " + gl.getMonth()
        # string to store the body of the mail 
        body = "Mail automatique."
        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 
        # open the file to be sent 
        filename1 = "sendHour.html"
        attachment1 = open(fileToSend, "rb")
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        # To change the payload into encoded form 
        p.set_payload((attachment1).read()) 
        # encode into base64 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment1; filename= %s" % filename1) 
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 
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
        return True
    except :
        return False

def main() :
    """
    main of the script. Get all paths, and lunch the function that watch every hours.
    """
    fileToSend = "./html/sendHour.html"
    userFile = "./user/user.csv"
    cssFile = "./html/style.css"
    workerFile = "./dataBase/workerHour.csv"
    hourFile = "./html/sendHour.html"
    fileNameWorker = "./dataBase/workerName.csv"
    if sys.platform != 'linux' :
        fileToSend = "." + fileToSend 
        userFile = "." + userFile
        cssFile = "." + cssFile
        workerFile = "." + workerFile
        hourFile = "." + hourFile
        fileNameWorker = "." + fileNameWorker
    watchEveryHour(userFile, fileToSend, workerFile, hourFile, cssFile, fileNameWorker)

main()