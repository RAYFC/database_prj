from bsddb3 import db
def sort(words):
    queries=[]
    for word in words:
        if ':' in word:
            index=word.find(':')
            b=[]
            b.append(word[:index])
            b.append(word[index])
            b.append(word[index+1:])
            queries.append(b)
        elif '>' in word:
            index = word.find('>')
            b=[]
            b.append(word[:index])
            b.append(word[index])
            b.append(word[index+1:])
            queries.append(b)
        elif '<' in word:
            index = word.find('<')
            b=[]
            b.append(word[:index])
            b.append(word[index])
            b.append(word[index+1:])
            queries.append(b)
        else:
            b=[]
            b.append(word)
            queries.append(b)
    return queries
def process(q):
    results=process_one(q[0])
    if len(q)>1:
        for a in q[1:]:
            results=list(set(results)&set(process_one(a)))
    return results
def process_one(q):
    results=[]
    if q[0]=='year':
        database=db.DB()
        database.open('ye.idx',None,db.DB_BTREE,db.DB_RDONLY)
        curs = database.cursor()
        if q[1]==':':
            results=equal_situation(q,curs)
        elif q[1]=='>':
            results=greater_situation(q,curs)
        elif q[1]=='<':
            results = smaller_situation(q, curs)
        else:
            print("Invalid input")
    else:
        database=db.DB()
        database.open('te.idx',None,db.DB_BTREE,db.DB_RDONLY)
        curs = database.cursor()
        if len(q)>1:
            if q[1]==":":
                results=term_search(q,curs)
        else:
            results=terms_search(q,curs)
    database.close()
    return results
def terms_search(q,curs):
    key1 = 't-'+ q[0]
    key2 = 'o-'+ q[0]
    key3 = 'a-'+ q[0]
    keys=[key1,key2,key3]
    a=[]
    for key in keys:
        result = curs.set(key.encode("utf-8"))
        if (result != None):
            a.append(str(result[1].decode("utf-8")))
            dup = curs.next_dup()
            while (dup != None):
                a.append(str(dup[1].decode("utf-8")))
                dup = curs.next_dup()
    a=list(set(a))
    curs.close()
    return a
def term_search(q,curs):
    key=q[0][0]+'-'+q[2]
    a=[]
    result = curs.set(key.encode("utf-8"))
    if (result != None):
        a.append(str(result[1].decode("utf-8")))
        dup = curs.next_dup()
        while (dup != None):
            a.append(str(dup[1].decode("utf-8")))
            dup = curs.next_dup()
    else:
        print("No Entry Found.")
    curs.close()
    return a
def equal_situation(q,curs):
    year=q[2]
    a=[]
    result = curs.set(year.encode("utf-8"))
    if (result != None):
        a.append(str(result[1].decode("utf-8")))
        dup = curs.next_dup()
        while (dup != None):
            a.append(str(dup[1].decode("utf-8")))
            dup = curs.next_dup()
    else:
        print("No Entry Found.")
    curs.close()
    return a
def greater_situation(q,curs):
    year=int(q[2])+1
    year=str(year)
    a=[]
    result = curs.set_range(year.encode("utf-8"))
    if (result != None):
        while (result != None):
            a.append(str(result[1].decode("utf-8")))
            dup = curs.next_dup()
            while (dup != None):
                a.append(str(dup[1].decode("utf-8")))
                dup = curs.next_dup()
            result=curs.next()
    else:
        print("No Entry Found")
    curs.close()
    return a
def smaller_situation(q, curs):
    year=q[2]
    a=[]
    curs.set_range(year.encode("utf-8"))
    result = curs.prev()
    if (result != None):
        while (result != None):
            a.append(str(result[1].decode("utf-8")))
            dup = curs.prev_dup()
            while (dup != None):
                a.append(str(dup[1].decode("utf-8")))
                dup = curs.prev_dup()
            result=curs.prev()
    else:
        print("No Entry Found")
    curs.close()
    return a
def print_records(results):
    database=db.DB()
    database.open('re.idx', None, db.DB_HASH, db.DB_RDONLY)
    if results==[]:
        print("No Entry Found")
    for i in results:
        i=i.rstrip("\n")
        index=i.encode("utf-8")
        record=database[index]
        record=record.decode("utf-8")
        print(record+'\n')
def main():
    mode=1
    while True:
        words=input("Enter the query or q to quit:")
        words=words.lower()
        if words=='q':
            break
        else:
            words=words.split()
            if 'output=key' in words:
                mode=1
                words.remove('output=key')
            if 'output=full' in words:
                mode=2
                words.remove('output=full')
            if len(words)>0:
                queries =sort(words)
                results=process(queries)
                if mode==1:
                    for result in results:
                        print(result)
                else:
                    print_records(results)
if __name__ == '__main__':
    main()
