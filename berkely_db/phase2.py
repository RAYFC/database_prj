from bsddb3 import db
import os
def main():
    os.system('sort -u years.txt -o years_output.txt')
    os.system('sort -u terms.txt -o terms_output.txt')
    os.system('sort -u recs.txt -o recs_output.txt')
    year = open('years_output.txt', 'r')
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open('ye.idx', None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()

    for line in year:
        y=line[:4]
        record=line[5:]
        database.put(y.encode("utf-8"),record)
    curs.close()
    database.close()
    #######################################################

    terms = open('terms_output.txt', 'r')
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
    cur = database.cursor()
    
    for line in terms:
        a=line.split(":")
        term=a[0]
        record=a[1]
        database.put(term.encode("utf-8"), record)
    database.close()
    cur.close()
#############################################################
    recs = open('recs_output.txt', 'r')
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open('re.idx', None, db.DB_HASH, db.DB_CREATE)
    cur = database.cursor()

    for line in recs:
        a = line.split(":")
        record=a[0]
        b=a[1]
        database .put(record.encode("utf-8"),b)
    os.system('db_dump -p ye.idx')
    os.system('db_dump -p te.idx')
    os.system('db_dump -p re.idx')
    database.close()
    cur.close()

main()
