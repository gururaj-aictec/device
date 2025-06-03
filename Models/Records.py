from database import db
from datetime import datetime
# class Records:
#     def __init__(self, id=None, enroll_id=None, records_time=None, mode=None,
#                  intout=None, event=None, device_serial_num=None, temperature=None, image=None):
#         self.id = id
#         self.enroll_id = enroll_id
#         self.records_time = records_time if records_time is not None else None
#         self.mode = mode
#         self.intout = intout
#         self.event = event
#         self.device_serial_num = device_serial_num if device_serial_num is not None else None
#         self.temperature = temperature
#         self.image = image if image is not None else None


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    enroll_id = db.Column(db.BigInteger)
    records_time = db.Column(db.DateTime)
    mode = db.Column(db.Integer)
    intOut = db.Column(db.Integer)
    event = db.Column(db.Integer)
    device_serial_num = db.Column(db.String)
    temperature = db.Column(db.Float)
    image = db.Column(db.String)

    def __str__(self):
        return f"Record [id={self.id}, enroll_id={self.enroll_id}, records_time={self.records_time}, mode={self.mode}, " \
               f"intOut={self.intOut}, event={self.event}, device_serial_num={self.device_serial_num}, " \
               f"temperature={self.temperature}, image={self.image}]"

    def to_dict(self):

        return {
            "id": self.id,
            "enroll_id": self.enroll_id,
            "records_time": str(self.records_time),
            "mode": self.mode,
            "intOut": self.intOut,
            "event": self.event,
            "device_serial_num": self.device_serial_num,
            "temperature": self.temperature,
            "image": self.image
        }



    def format_date(self,date_string):
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
        return date.strftime("%Y-%m-%d %H:%M:20")
def insert_record(record):
    db.session.add(record)
    db.session.commit()
def insert_record2(**record):
    record = Record(**record)
    db.session.add(record)
    db.session.commit()

def select_record_by_id(id):
    return  db.session.query(Record).get(id)


def delete_record_by_id(id):
    record = select_record_by_id(id)
    db.session.delete(record)
    db.session.commit()


def update_record_by_id(id, **kwargs):
    record = select_record_by_id(id)
    for key, value in kwargs.items():
        setattr(record, key, value)
    db.session.commit()

def select_all_records():
    return db.session.query(Record).all()

# def format_date(date_string):
#     date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
#     return date.strftime("%Y-%m-%d %H:%M:%S")
# if "__main__" == __name__:
