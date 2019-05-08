##########################################################################################################
# main.py - program that implements other project programs to create the delivery system

# CMPUT 291
# Mini Project 01
# Due: November 06, 2017
# Team 97
##########################################################################################################

import os
import sqlite3
import getpass
import sys
import re
from place_an_order import *
from agent import *
from searchProducts import *


connection = None
cursor =None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def logout():
    print("\nLogged Out Of System\n")
    sys.exit()


def clearScreen():
    os.system("clear")
def c_login():
    global connection, cursor
    cid=input("Please enter your username:\n ")
    cursor.execute("select pwd from customers where cid = ?",(cid,))
    pwd=cursor.fetchone()
    if pwd is None:
        input("You have not registered yet , please sign up")
        return c_sign_up()
    else:
        password=getpass.getpass("Please enter your password:")
        if re.match("^[A-Za-z0-9_]*$",password):
            if password==pwd[0]:
                print("Log in successfully")
                return cid
            else:
                print(password)
                print("Login information is not correct, please re-login")
                c_login()
        else:
            print("Invalid password")
            c_login()
def c_sign_up():
    global connection, cursor
    cid=input("username:")
    cursor.execute("select cid from customers where cid = ?", (cid,))
    check=cursor.fetchone()
    if check is None:
        pwd=input("Password:")
        name=input("name:")
        address=input("address:")
        cursor.execute("insert into customers values (?,?,?,?)",(cid,name,address,pwd))
        connection.commit()
        return cid
    else:
        print("The username exists,please sign in")
        c_login()
def a_login():
    global connection, cursor
    aid=input("Please enter your agent_id:\n ")
    cursor.execute("select pwd from agents where aid =?",(aid,))
    pwd = cursor.fetchone()
    if pwd is None:
        input("No such an agent")
        a_login()
    else:
        password=getpass.getpass("Please enter your password:")
        if re.match("^[A-Za-z0-9_]*$",password):
            if password==pwd[0]:
                print("Log in successfully")
            else:
                print(password)
                print("Login information is not correct, please re-login")
                a_login()
        else:
            print("Invalid password")
            a_login()

####### M  a  i  n ##########
def main():
    global connection, cursor

    path =sys.argv[1]
    connect(path)

    if connection == 0:
        print("Error connecting to database")
        return

    ##########################################################################################################
    #									LOGIN SCREEN
    ##########################################################################################################
    print("\n\n- - - - - - - - - - - - - - - -")
    print("- - - L O G I N  M E N U - - -")
    print("- - - - - - - - - - - - - - - -\n")
    print("Who are you?")
    print("1. Customer (c)")
    print("2. Agent (a)")

    print("\n* logout of system (ls)")

    while True:
        Uinput = input("\nEnter your selection: ").lower()
        if Uinput == 'ls':
            while True:
                Uinput = input("Logout? (yes/no): ").lower()
                if Uinput == 'y' or Uinput == 'yes':
                    print("*** Logged Out of System ***\n")
                    return
                elif Uinput == 'n' or Uinput == 'no':
                    break
                else:
                    print("Not a valid option; please enter yes(y) or no(n)")
                    continue
            continue

        elif Uinput == '1' or Uinput == 'c':
            cid = c_login()
            basket=[]
            ##########################################################################################################
            #									CUSTOMER MENU
            ##########################################################################################################
            while True:
                print("\n\n----------------------------")
                print("---Main Customer Menu---")
                print("----------------------------")
                print("Please select an option...")
                print("1. Search for Products (s)")
                print("2. Place an Order (p)")
                print("3. List Orders (l)\n")

                print("* quit(q) to quit")
                print("* cls(c) to clear screen")
                print("* menu(m) to display menu")
                Uinput = input("\nEnter your choice: ").lower()
                if Uinput == 'q' or Uinput == 'quit' or Uinput == "exit":
                    while True:
                        Uinput = input("Exit? (yes/no/quit): ").lower()
                        if Uinput == 'y' or Uinput == 'yes' or Uinput == 'q' or Uinput == 'quit':
                            print("Quit System\n")
                            return
                        elif Uinput == 'n' or Uinput == 'no':
                            break
                        else:
                            print("\nPlease enter yes (y) or no (n)\n")
                            continue
                    continue

                # (1) - search_for_products
                elif Uinput == '1' or Uinput == 's':
                    search_for_products(cursor,connection,basket)
                # (2) - place_an_order
                elif Uinput == '2' or Uinput == 'p':
                    create_an_order(cursor,connection,cid,basket)
                    basket=[]
                # (3) - list_orders
                elif Uinput == '3' or Uinput == 'l':
                    list_orders(cursor,connection,cid)

                elif Uinput == 'cls' or Uinput == 'c':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\n\n----------------------------")
                    print("---Main Customer Menu---")
                    print("----------------------------")
                    print("Please select an option...\n")
                    print("1. Search for Products (s)")
                    print("2. Place an Order (p)")
                    print("3. List Orders (l)\n")

                    print("* quit(q) to quit")
                    print("* cls(c) to clear screen")
                    print("* menu(m) to display menu")

                elif Uinput == 'menu' or Uinput == 'm':
                    print("\n\n----------------------------")
                    print("---Main Customer Menu---")
                    print("----------------------------")
                    print("Please select an option...\n")
                    print("1. Search for Products (s)")
                    print("2. Place an Order (p)")
                    print("3. List Orders (l)\n")

                    print("* quit(q) to quit")
                    print("* cls(c) to clear screen")
                    print("* menu(m) to display menu")
                else:
                    print("Sorry that's not an option - please choose from numbers 1-3")

                print(Uinput)

        elif Uinput == '2' or Uinput == 'a':
            a_login()
            ##########################################################################################################
            #											AGENT MENU
            ##########################################################################################################
            while True:
                print("\n\n-------------------------")
                print("---Main Agent Menu---")
                print("-------------------------")
                print("Please select an option...")
                print("1. Set up a delivery (s)")
                print("2. Update a delivery (u)")
                print("3. Add to Stock (a)\n")

                print("* quit(q) to quit")
                print("* cls(c) to clear screen")
                print("* menu(m) to display menu")
                Uinput = input("\nEnter your choice: ").lower()
                if Uinput == 'q' or Uinput == 'quit' or Uinput == "exit":
                    while True:
                        Uinput = input("Exit? (yes/no/quit): ").lower()
                        if Uinput == 'y' or Uinput == 'yes' or Uinput == 'q' or Uinput == 'quit':
                            print("Quit System\n")
                            return
                        elif Uinput == 'n' or Uinput == 'no':
                            break
                        else:
                            print("\nPlease enter yes (y) or no (n)\n")
                            continue
                    continue

                # (1) - set_up_delivery
                elif Uinput == '1' or Uinput == 's':
                    set_up_delivery(cursor, connection)
                # (2) - update_delivery
                elif Uinput == '2' or Uinput == 'p':
                    update_a_delivery(cursor, connection)
                # (3) - add_to_stock
                elif Uinput == '3' or Uinput == 'l':
                    add_to_stock(cursor, connection)

                elif Uinput == 'cls' or Uinput == 'c':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\n\n-------------------------")
                    print("---Main Agent Menu---")
                    print("-------------------------")
                    print("Please select an option...\n")
                    print("1. Search for Products (s)")
                    print("2. Place an Order (p)")
                    print("3. List Orders (l)\n")

                    print("* quit(q) to quit")
                    print("* cls(c) to clear screen")
                    print("* menu(m) to display menu")

                elif Uinput == 'menu' or Uinput == 'm':
                    print("\n\n-------------------------")
                    print("---Main Agent Menu---")
                    print("-------------------------")
                    print("Please select an option...\n")
                    print("1. Search for Products (s)")
                    print("2. Place an Order (p)")
                    print("3. List Orders (l)\n")

                    print("* quit(q) to quit")
                    print("* cls(c) to clear screen")
                    print("* menu(m) to display menu")
                else:
                    print("Sorry that's not an option - please choose from numbers 1-3")

                print(Uinput)

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
