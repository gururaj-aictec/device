class PersonTemp:
    def __init__(self, user_id=None, name=None, privilege=None, imagepath=None, password=None, card_num=None):
        self.user_id = user_id
        self.name = name if name is not None else None
        self.privilege = privilege
        self.imagepath = imagepath if imagepath is not None else None
        self.password = password if password is not None else None
        self.card_num = card_num if card_num is not None else None

    def __str__(self):
        return f"PersonTemp [userId={self.user_id}, name={self.name}, privilege={self.privilege}, imagePath={self.imagepath}, password={self.password}, cardNum={self.card_num}]"
