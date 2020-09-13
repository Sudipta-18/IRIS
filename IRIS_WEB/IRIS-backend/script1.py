from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def anamoly_email_sender():
    anamoly_types = {'Abuse': ['iris.police100@gmail.com', 'Abuse Alert', 'A physical abuse has been detected, requesting you to investigate the incident'],
                    'Arrest': ['iris.police100@gmail.com', 'Arrest Alert', 'An arrest has been detected, requesting you to investigate the incident'],
                    'Arson': ['iris.fire101@gmail.com', 'Arson Alert', 'Malicious burning has been detected, requesting fire brigade to normalize the condition and inform the nearest police station to investigate the incident'],
                    'Assault': ['iris.police100@gmail.com', 'Assault Alert', 'An assault has been detected, requesting you to investigate the incident'],
                    'Burglary': ['iris.police100@gmail.com', 'Burglary Alert', 'A suspicious activity has been detected, requesting you to investigate the incident'],
                    'Explosion': ['iris.fire101@gmail.com', 'Explosion Alert', 'An explosion has been detected, requesting fire brigade to normalize the condition'],
                    'Fighting': ['iris.police100@gmail.com', 'Fighting Alert', 'A tussle has been detected, requesting you to investigate the incident'],
                    'RoadAccidents': ['iris.hospital102@gmail.com', 'Road Accident Alert', 'A road accident has been detected, requesting you to aid the accident victim'],
                    'Robbery': ['iris.police100@gmail.com', 'Robbery Alert', 'A theft activity has been detected, requesting you to investigate the incident'],
                    'Shooting': ['iris.police100@gmail.com', 'Shooting Alert', 'A firing activity has been detected, requesting you to investigate the incident'],
                    'Shoplifting': ['iris.police100@gmail.com', 'Shoplifting Alert', 'A folk crime has been detected, requesting you to investigate the incident'],
                    'Stealing': ['iris.police100@gmail.com', 'Stealing Alert', 'A folk crime has been detected, requesting you to investigate the incident'],
                    'Vandalism': ['iris.police100@gmail.com', 'Vandalism Alert', 'Destruction of property has been detected, requesting you to investigate the incident'],
                    'Normal': 0
                    }

    with open('public/text_files/text.txt', 'r') as anamoly_file:         # read file where the ML script saves our anamoly name.
        anamoly_type = anamoly_file.readline()
        reciepient = anamoly_types[anamoly_type][0]
        emailsubject = anamoly_types[anamoly_type][1]
        emailcontent = anamoly_types[anamoly_type][2]
    sendmail(reciepient, emailsubject, emailcontent)           # this operation takes about 5 secs 

def sendmail(reciever, emailsubject, body):
    msg = MIMEMultipart()
    msg['From'] = "pakhiyakomaro@gmail.com"
    msg['To'] = reciever
    msg['Subject'] = emailsubject
    msg.attach(MIMEText(body, 'html'))
    # print(msg)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(msg['From'], "share@1:)")
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


if __name__ == "__main__":
    print("inside python script") 
    try:
        anamoly_email_sender()   
    except Exception as e:
        print(f'Error: {e}')   
    print("Email was sent")
