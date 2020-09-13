from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def anamoly_email_sender():
    anamoly_types = {'Abuse': ['lwar780@gmail.com', 'python sent this to you', 'check if you have recieved it.'],
                    'Arrest': 0,
                    'Arson': 0,
                    'Assault': 0,
                    'Burglary': 0,
                    'Explosion': 0,
                    'Fighting': 0,
                    'RoadAccidents': 0,
                    'Robbery': 0,
                    'Shooting': 0,
                    'Shoplifting': 0,
                    'Stealing': 0,
                    'Vandalism': 0,
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