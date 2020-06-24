import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def send_mail(owner_name, owner_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain'))                                     # Create a text/plain message

        me = 'dishashinde17@gmail.com'                                          # me == the sender's email address
        pw = 'Leeminho@1310'
        you = owner_email

        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you

        s = smtplib.SMTP('smtp.gmail.com', 587)                                 # Send the message via our own SMTP server, but don't include the envelope header.
        s.starttls()
        s.login(me, pw)                                                         #smtp.login('fu@gmail.com', 'fu')
        s.sendmail(me, [you], msg.as_string())                                  #s.sendmail(me, 'dishashinde17@gmail.com', msg.as_string())
        s.quit()
        
    except:
        pass


'''
user='AC'
address='Plot no. : 624, Sector no. : 20, Akurdi Railway Station, Akurdi, Pune, Maharashtra, India - 411019'
property_name='prop11'
owner_name='Sehal'
adhar_number=12341234
email_id='snehalpadekar0@gmail.com'
body = 'Registration Process done by ' + user + '\n\n\nProperty Details: \n' + '      Property Name: ' + property_name + '\n      Address: ' + address + '\n\n\nOwner Details: \n' + '      Owner Name: ' + owner_name + '\n      Adhar Number: ' + str(adhar_number) + '\n      Email Id: ' + email_id
send_mail(owner_name, 'snehalpadekar0@gmail.com', 'Trial', body)
'''