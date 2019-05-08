
import random
def  set_up_delivery(c,co):
    global connection, cursor
    cursor=c
    connection=co
    trackingNo = random.randint(0,1000000)
    print(trackingNo)
    cursor.execute("SELECT * FROM orders")
    print(cursor.fetchall())
    oid =input("select a oid from orders \n" )
    option=input("Press 1 to enter a pickuptime 2 to set it as default enter any other key to return")
    if option=='1':
        pickUpTime = input("Please enter the pickup time in format yyyy-mm-dd hh:mm:ss\nFor an instance 2017-11-11 11:11:11\n") #I am not sure how to add time here,
    if option=='2':
        pickUpTime = None
    else:
        return
    dropOffTime = None
    cursor.execute(" INSERT INTO deliveries VALUES (?,?,?,?)", (trackingNo, oid, pickUpTime, dropOffTime))
    connection.commit()
    return
def update_a_delivery(c,co):# this work
    global connection, cursor
    cursor=c
    connection=co
    cursor.execute("SELECT trackingNo FROM deliveries;")
    print("select tracking number \n")
    print(cursor.fetchall())
    trackNum = input("please enter tracking number \n")
    cursor.execute('SELECT * FROM deliveries WHERE trackingNo=?;',(trackNum,))
    print(cursor.fetchone())
    option=input("Enter 1 for updating pickup/drop off time\nEnter 2 for remove an order\nenter any other key to return:")
    if option=='1':
        Update_delivery_time(cursor,connection)
    if option=='2':
        Update_delivery_delet(c, co)

def Update_delivery_time(c,co):
    global cursor,connection
    cursor=c
    connection=co
    oid1=input('please enter oid \n')
    pickUpTime=input("please enter pickUpTime \n")
    dropOffTime=input("please enter dropOffTime\n")
    cursor.execute("UPDATE deliveries SET pickUpTime=?, dropOffTime=? WHERE oid = ?;",(pickUpTime, dropOffTime, oid1))
    connection.commit()
    return
def Update_delivery_delet(c,co): #this work
        global cursor, connection
        cursor = c
        connection = co
        print("please enter oid which you want delet")
        oid2=input('\n')
        cursor.execute("DELETE FROM deliveries WHERE oid=?;", oid2)
        connection.commit()
        return


def add_to_stock(c,co): # this work
    global connection, cursor
    cursor=c
    connection=co
    pid = input("enter a product id \n")
    sid = input("enter a store id \n")
    qty1 = input("Enter how many products should be add to a store \n")
    cursor.execute("select qty from carries where sid=? and pid=?",(sid,pid))
    a=cursor.fetchone()
    if a is None:
        a=(0,)
    qty2=a[0]
    option=input("Do you want to change the unit price? (y for yes and n for no)")
    if option=='y':
        uprice = input("Enter unit price of products \n")
        cursor.execute("update carries SET qty=?, uprice=? where sid=? and pid=?",(int(qty1)+qty2,uprice,sid,pid))
        connection.commit()
    if option=='n':
        cursor.execute("update carries SET qty=? where sid=? and pid=?", (int(qty1) + qty2, sid, pid))
        connection.commit()
    return