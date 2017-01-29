import redis
import smtplib
import json

class mailsender_service():

    def __init__(self):
        self.redisobj = redis.StrictRedis('localhost',7781)


    def mail_sender(self, sender, recievers, subject_content, mail_content):
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com:587')
            smtpObj.starttls()
            smtpObj.login(sender, 'jaykdihenkar#24101993')
            msg = "\r\n".join([
                "From: jkdihenkar@gmail.com",
                "To: "+recievers,
                "Subject: "+subject_content,
                "",
                mail_content
            ])
            smtpObj.sendmail(sender, recievers, msg)
            print("Successfully sent email")
        except:
            print("Error: unable to send email")
            raise

    def routine(self):
        item = self.redisobj.brpop('L:mailinglist')[1].decode("utf-8")
        print(item)
        mail = json.loads(item)
        self.mail_sender('jkdihenkar@gmail.com', mail['emailID'],mail['subject'],mail['mailtext'])

    def eventloop(self):
        while(True):
            self.routine()


if __name__=='__main__':
    ms = mailsender_service()
    ms.eventloop()
