import datetime
import sys
import json
import redis

sys.path.append("../")

import connection

class UtilsLib():

    def __init__(self):
        self.redisobj = redis.StrictRedis('localhost', port=7781)
        import random
        self.random = random
        self.random.seed(datetime.datetime.now().microsecond+3378)
        self.conn = connection.connection()

    def mail_sender(self, email, subject, mailtext):
        task = {}
        task['emailID'] = email
        task['subject'] = subject
        task['mailtext'] = mailtext
        self.redisobj.lpush('L:mailinglist',json.dumps(task))

    def send_otp_code(self, email, otp):
        self.mail_sender(
            email,
            "OTP for Expense Manager",
            '  Your OTP for Reset Password is {}'.format(otp)
        )

    def generate_otp_for_email(self, email):
        if self.redisobj.exists('k:'+email+':otp') and self.redisobj.ttl('k:'+email+':otp')>0:
            otpcode = str(self.redisobj.get('k:'+email+':otp').decode("utf-8"))
            self.send_otp_code(email, otpcode)
        else:
            otpcode = self.random.randint(1000000, 9999999)
            self.redisobj.set('k:'+email+':otp', otpcode)
            self.redisobj.expire('k:'+email+':otp', 300)
            self.send_otp_code(email, otpcode)

    def validate_otp(self, email, qotp):
        actual_otp = self.redisobj.get('k:'+email+':otp').decode('utf-8')
        if qotp == actual_otp:
            return True
        else:
            return False

    def hash_of_hashpass(self, email):
        import hashlib
        q = self.conn.q.get_password_for_email.format(email=email)
        res = self.conn.exec_query(q)
        pass_hash = res.fetchall()[0][0]
        hash_of_hash = hashlib.sha256(pass_hash.encode('utf-8')).hexdigest()
        return hash_of_hash

    def set_session(self, email,ip):
        # if not self.redisobj.exists('active_sessions:'+email) or self.redisobj.ttl('active_sessions:'+email)<1:
        self.redisobj.set('active_sessions:'+email, 'active_from_'+ip)
        security_keyname = 'security_verify:'+email
        self.redisobj.set(security_keyname,self.hash_of_hashpass(email))
        self.redisobj.expire('active_sessions:'+email, 60*15)
        self.redisobj.expire(security_keyname, 60 * 15)

    def check_and_update_exist_session(self, email):
        if email and self.redisobj.exists('active_sessions:'+email) and self.redisobj.ttl('active_sessions:'+email)>0:
            security_keyname = 'security_verify:' + email
            self.redisobj.expire('active_sessions:' + email, 60 * 15)
            self.redisobj.expire(security_keyname, 60 * 15)
            return True
        else:
            return False

    def clear_all_sessions(self, email):
        self.redisobj.delete('active_sessions:' + email)
        self.redisobj.delete('security_verify:' + email)
