from database import db
# class Person:
#     def __init__(self, id=None, name=None, roll_id=None):
#         self.id = id
#         self.name = name if name is not None else None
#         self.roll_id = roll_id
#
#     def __str__(self):
#         return f"Person [id={self.id}, name={self.name}, rollId={self.roll_id}]"
#

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    roll_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"Person [id={self.id}, name={self.name}, rollId={self.roll_id}]"

    # 插入数据
    def insert_person(self,**person):
        person = Person(**person)
        db.session.add(person)
        db.session.commit()

    # 查询数据
    def select_all(self):
        return Person.query.all()

    def select_person_by_id(self,id):
        return Person.query.get(id)

    # 删除数据
    def delete_person_by_id(self,id):
        person = select_person_by_id(id)
        if person:
            db.session.delete(person)
            db.session.commit()


        # 更新数据
    def update_person_by_id(self,id, name=None, roll_id=None):
        person = select_person_by_id(id)
        if name is not None:
            person.name = name
        if roll_id is not None:
            person.roll_id = roll_id
        db.session.commit()
    def delete_by_primary_key(self,id):
        person = select_person_by_id(id)
        if person:
            db.session.delete(person)
            db.session.commit()
def insert_person(**person):
    person = Person(**person)
    db.session.add(person)
    db.session.commit()

def insert_person2(person):

    db.session.add(person)
    db.session.commit()

# 查询数据
def select_all():
    return db.session.query(Person).all()

def select_person_by_id(id):
    return  db.session.query(Person).get(id)
# 删除数据
def delete_person_by_id(id):
    person = select_person_by_id(id)
    db.session.delete(person)
    db.session.commit()


# 更新数据
def update_person_by_id(id, name=None, roll_id=None):
    person = select_person_by_id(id)
    if name is not None:
        person.name = name
    if roll_id is not None:
        person.roll_id = roll_id
    db.session.commit()
def update_by_primary_key(person):
    person = select_person_by_id(person.id)
    if person:
        person.name = person.name
        person.roll_id = person.roll_id
        db.session.commit()
