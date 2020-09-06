import fb


# CLASS DESCRIPTION
#########################################################################################################
class Detail:
    def __init__(self, name, id_num):
        self.name = name
        self.id_num = id_num

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id_num

    def to_dict(self):
        dct = {u'name': self.get_name(),
               u'id_num': self.get_id()}
        return dct

    def set_painted(self):
        self.painted = True

    def update_data(self, db, coll='today_details'):
        db.collection(coll).document(self.get_id()).set(self.to_dict())

    def delete_from_db(self, db, coll='today_details'):
        db.collection(coll).document(self.get_id()).delete()
#########################################################################################################

# FUNCTION DESCRIPTION
#########################################################################################################
pass
#########################################################################################################

# FIRESTORE CONNECTION
#########################################################################################################
db, app, cred = fb.firebase_connection()
#########################################################################################################

# EXAMPLE DETAILS (TODO: REAL PLAN)
#########################################################################################################
from random import randint
details = []
details.append(Detail('Кронштейн №1', 'МРУ1.03.410.01'))
details.append(Detail('Крышка', '101.00.57.580'))
details.append(Detail('Металлическая балка', '101.04.03.040'))
details.append(Detail('Кожух', 'ДСЕ300.56.60.420'))
details.append(Detail('Крышка №2', 'ДСЕ142.14.06.150'))
details.append(Detail('Крышка №3', 'ДСЕ181.70.02.200'))
for d in details:
    try:
        d.delete_from_db(db)
    except:
        pass
    finally:
        d.update_data(db, 'all_details')
#########################################################################################################

