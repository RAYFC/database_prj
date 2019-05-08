import sqlite3

def search_for_products(c,co,basket):
    global connection, cursor
    cursor=c
    connection=co
    keywords=input("Please enter the key word,please seperate keywords by comma ',':")
    items=keywords.split(',')
    display_info1(items)
    pid=input("Enter the pid of the products you want to add into basket,enter q if you want to quit: ")
    if pid=='q':
        return []
    else:
        s_name=input("Enter the store name:")
        cursor.execute("select sid from stores where name like ?",('%'+s_name+'%',))
        sid=cursor.fetchone()[0]
        cursor.execute("select uprice from carries where pid = ? and sid=?", (pid,sid))
        uprice=cursor.fetchone()[0]
        option=input("The quantity has been set to 1,if you want to change it,please enter 1. Return by entering other keys:")
        if option=='1':
            qty=input("Enter the quantity:")
            qty=int(qty)
            insertion=(qty,pid,sid,uprice)
            basket.append(insertion)
            return basket
        else:
            insertion = (1, pid, sid, uprice)
            basket.append(insertion)
            return basket
def display_info1(items):
    global connection, cursor, basket
    alist=[]
    sql1 = '''
        	SELECT products.pid, products.name, products.unit, count(sid),min(uprice)
        	FROM products, carries
        	WHERE products.pid = carries.pid and products.name like ?
        	GROUP BY products.pid
        	ORDER BY products.name desc;
        	'''
    sql2 = '''
            SELECT count(carries.sid),min(carries.uprice)
            From carries,products
            Where products.name like ? and products.pid = carries.pid and carries.qty>0
       	     GROUP BY products.pid
        	 ORDER BY products.name desc;'''
    for keyword in items:
        cursor.execute(sql1,('%'+keyword+'%',))
        a=cursor.fetchall()
        for i in range(len(a)):
            cursor.execute(sql2, ('%' + keyword + '%',))
            b=cursor.fetchall()
            cursor.execute("select count(*) from products,olines,orders where products.pid = ? and products.pid=olines.pid and olines.oid=orders.oid and date(orders.odate, '+7 day') >= date('now');"
            ,(a[i][0],))
            c=cursor.fetchall()
            if c is None:
                c=(0,)
            insertion=(a[i][0],a[i][1],a[i][2],a[i][3],a[i][4],b[i][0], b[i][1],c[0])
            alist.append(insertion)
    display_info2(alist)
def display_info2(alist):
    length=len(alist)
    if length<=5:
        for item in alist:
            print("products id:%s  products name:%s unit:%s the number of stores that carry it:%d"%(item[0],item[1],item[2],item[3]))
            print("the minimum price among the stores that carry it:%.2f the number of stores that have it in stock:%d the minimum price among the stores that have the product in stock:%.2f"%(item[4],item[5],item[6]))
            print(" the number of orders within the past 7 days: ", item[7][0])
            print("\n\n")
    else:
        for item in alist[:5]:
            print("products id:%s  products name:%s unit:%s the number of stores that carry it:%d"%(item[0],item[1],item[2],item[3]))
            print("the minimum price among the stores that carry it:%.2f the number of stores that have it in stock:%d the minimum price among the stores that have the product in stock:%.2f"%(item[4],item[5],item[6]))
            print(" the number of orders within the past 7 days: ", item[7][0])
            print("\n\n")
    option=input("Please enter 0 to see 5 more\nOr enter the pid of the product to see the details\nEnter q to main menu:")
    if option=='0':
        if length<=5:
            print("no more items")
            return
        else:
            alist=alist[5:]
            display_info2(alist)
    if option=='q':
        return
    if option !='0':
        pid=option
        sql3 = '''
        	SELECT carries.pid, stores.name, carries.uprice, carries.qty
        	FROM  carries, stores
        	WHERE stores.sid = carries.sid  and carries.pid=? 
        	order by carries.qty desc;
        	'''
        cursor.execute(sql3, (pid,))
        all_items = cursor.fetchall()
        for item in all_items:
            print(item)
        cursor.execute(
            "select count(*) from products,olines,orders where products.pid= ? and products.pid=olines.pid and olines.oid=orders.oid and date(orders.odate, '+7 day') <= date('now');"
            , (pid,))
        a = cursor.fetchone()
        if a is None:
            a = (0,)
        print(" the number of orders within the past 7 days:", a[0])
        return