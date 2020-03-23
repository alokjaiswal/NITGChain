import plyvel

DB_STATE = 0




NODE_PORT = 0
SEED_PORT = 0

def CHECK_DB():
    try:
        db = plyvel.DB('./')
        DB_STATE = 0
        return DB_STATE,db
    except:
        DB_STATE = 1
        return DB_STATE,None



NEW_CHAIN = 0


