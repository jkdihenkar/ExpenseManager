import datetime

class expense():
    def __init__(self):
        self.from_member = None
        self.to_member = None
        self.amount = 0
        self.comment = ''
        self.timestamp = datetime.datetime.now()

    def set_main_data(self, from_member, to_member, amount, comment='', timestamp=datetime.datetime.now()):
        self.from_member = from_member
        self.to_member = to_member
        self.amount = amount
        self.comment = comment
        self.timestamp = timestamp