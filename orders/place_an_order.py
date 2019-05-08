import time
def get_qty(pid,sid):
    global connection, cursor
    cursor.execute('SELECT qty FROM carries WHERE sid=? and pid=?;', (sid,pid))
    qty=cursor.fetchone()
    if qty is None:
        qty=0
    else:
        qty=qty[0]
    return qty
def insert_values(oid, sid, pid,qty,price):
    global connection, cursor
    if check_availiability(qty, pid, sid):
        cursor.execute("INSERT INTO olines values(?,?,?,?,?)", (oid, sid, pid, qty, price))
        connection.commit()
        num_in_stores = get_qty(pid, sid)
        cursor.execute('UPDATE carries SET qty=? where sid=? and pid=?', (num_in_stores - int(qty), sid, pid))
        connection.commit()
    else:
        cursor.execute("select name from stores where sid=?",(sid,))
        s_name=cursor.fetchone()[0]
        cursor.execute("select name from products where pid=?",(pid,))
        p_name=cursor.fetchone()[0]
        str1=input('The store quantity for %s in %s is less than the quantity in the basket \nenter 1 if you want to change the quantity,enter 2 if you want to delete this product:\n'%(p_name,s_name))
        if str1=='1':
            qty = input('Please Enter the quantity:\n')
            insert_values(oid, sid, pid, qty, price)
        if str1=='2':
            pass
def check_availiability(num,pid,sid):
    global connection, cursor
    qty=get_qty(pid,sid)
    if int(num)<=int(qty):
        return True
    else:
        return False
def place_an_order(oid):
    global connection, cursor,basket
    for every_item in basket:
        qty=every_item[0]
        pid=every_item[1]
        sid=every_item[2]
        price=every_item[3]
        insert_values(oid, sid, pid,qty,price)
def create_an_order(c,co,cid,bas):
    global connection, cursor,basket
    basket=bas
    connection=co
    cursor=c
    cursor.execute("select address from customers where cid=?",(cid,))
    address=cursor.fetchone()[0]
    odate=time.strftime("%Y-%m-%d")
    cursor.execute('SELECT MAX(oid) from orders')
    max_oid=cursor.fetchone()
    if max_oid is None:
        oid=1
    else:
        oid=max_oid[0]+1
    place_an_order(oid)
    cursor.execute("select * from olines where oid=?",(oid,))
    a=cursor.fetchone()
    if a is not None:
        cursor.execute('INSERT INTO orders VALUES(?,?,?,?)',(oid,cid,odate,address))
        connection.commit()
    else:
        oid-=1
def list_orders(c,co,cid): #we have to identify the # of rows which should be displayed
    global connection, cursor
    connection=co
    cursor=c
    cursor.execute('select oid from orders where cid=?',(cid,))
    oids=cursor.fetchall()
    if oids is None:
        print("You have no orders")
    query_1='''
        select orders.oid,orders.odate,count(*),SUM(qty*uprice)
        from orders,olines
        where orders.cid=? and orders.oid=olines.oid
        group by orders.oid
        order by orders.oid desc
        ;
        '''
    cursor.execute(query_1,(cid,))
    alist=cursor.fetchall()
    display_information(alist)
def display_information(alist):
    global connection, cursor
    if len(alist)==0:
        return
    if len(alist)<=5:
        print(alist)
    else:
        print(alist[:5])
    option = input('Please enter 0 to see 5 more orders\nOr enter the # of orders to track details of that order:\nEnter q to exit\n')
    if option =='0':
        while len(alist)>5:
            alist=alist[5:]
            display_information(alist)
        option =input('enter the # of orders to track details of that order:\nEnter q to exit\n')
    if option =='q':
        return
    else:
        oid=int(option)
        query_2='''
        select trackingno, pickUpTime, dropOffTime,address
        from deliveries ,orders
        where orders.oid=deliveries.oid and orders.oid=?
        ;
        '''
        cursor.execute(query_2,(oid,))
        alist=cursor.fetchall()
        if len(alist)==0:
            print('The delivery have not been set yet\n')
        else:
            if alist[0] is None:
                print('The trackingno is null')
            else:
                print('The trackingno is ',alist[0][0])
            if  alist[0][1] is None:
                print('The pick-up time is null')
            else:
                print('The pick-up time is ', alist[0][1])
            if  alist[0][2] is None:
                print('The drop off time is null')
            else:
                print('The drop-off time is ', alist[0][2])
            print('address: ', alist[0][3])
        query_3='''select olines.sid,stores.name,olines.pid,products.name,olines.qty,products.unit,olines.uprice
        from olines,products,stores
        where olines.oid=? and olines.sid=stores.sid and olines.pid=products.pid
        ;'''
        cursor.execute(query_3, (oid,))
        all_items=cursor.fetchall()
        for item in all_items:
            print(item)
        return


