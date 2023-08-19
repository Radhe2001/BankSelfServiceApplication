import mysql.connector
from datetime import datetime
import pytz

con = mysql.connector.connect(host="localhost",user="root",password="Shyam@2001",database="bankselfservice")
cur = con.cursor()

# register function definition
def register():
    name = input("Enter your name : ")
    avl_bal = int(input("Enter the initial amount you want to add : "))
    try:
        cur.execute("select account_number from static_value")
        result = cur.fetchone()
        list = (name,int(result[0]),avl_bal)
        query = "insert into account_details(name,account_number,available_balance) values(%s,%s,%s)"
        try:
            cur.execute(query,list)
            con.commit()          
            try:
                cur.execute("update static_value set account_number = account_number+1")
                con.commit()
            except:
                print("failed to update account number")              
        except:
            print("unable to insert the value")           
        print("Registered successfully")
        try:
            cur.execute("select * from account_details where account_number = %s"%result[0])
            res = cur.fetchone()
            print(res)
        except:
            print("Failed to fetch account details")       
    except:
        print("Failed to fetch the account number")



# function definition for login function
def login():
    name = input("Enter your name : ")
    ac_no = int(input("Enter account number : "))
    try:
        cur.execute("select * from account_details where account_number = %s"%ac_no)
        result = cur.fetchone()
        print(result)
        if name == result[0] and ac_no==int(result[1]):
            return int(result[1])
        else:
            print("invalid credentials")
            return 0
    except:
        print("invalid credentials")
        return 0
    
# defining debit function 
def debit(id):
    amount = int(input("Enter the amount : "))
    date = str(datetime.now(pytz.timezone('Asia/Kolkata')))
    tid = 0
    t_type = "DE"
    balance = 0
    try:
        cur.execute("select transaction_id from static_value")
        result = cur.fetchone()
        tid = result[0]
    except:
        print("Failed to fetch transaction id")
        
    try:
        cur.execute("select available_balance from account_details where account_number = %s"%id)
        result = cur.fetchone()
        balance = result[0]
    except:
        print("Failed to fetch availabe balance")
    if balance>=amount:
        balance = balance - amount
        query="insert into transaction values(%s,%s,%s,%s,%s,%s)"
        list = (id,amount,date,balance,tid,t_type)
        try:
            cur.execute(query,list)
            con.commit()
            print("Amount debited successfully")
            try:
                list = (balance,id)
                cur.execute("update account_details set available_balance = %s where account_number = %s"%list)
                con.commit()
            except:
                print("Failed to update the available balance")
                
            try:
                cur.execute("update static_value set transaction_id = transaction_id+1")
                con.commit()
            except:
                print("Failed to update the transaction id")
        except:
            print("Unable to perform the transaction")
    else:
        print("Available balance is not enough")
    

# defining credit function
def credit(id):
    amount = int(input("Enter the amount : "))
    date = str(datetime.now(pytz.timezone('Asia/Kolkata')))
    tid = 0
    t_type = "CR"
    balance = 0
    try:
        cur.execute("select transaction_id from static_value")
        result = cur.fetchone()
        tid = result[0]
    except:
        print("Failed to fetch transaction id")
        
    try:
        cur.execute("select available_balance from account_details where account_number = %s"%id)
        result = cur.fetchone()
        balance = result[0]
    except:
        print("Failed to fetch availabe balance")
        
        
    balance = balance + amount
    query="insert into transaction values(%s,%s,%s,%s,%s,%s)"
    list = (id,amount,date,balance,tid,t_type)
    try:
        cur.execute(query,list)
        con.commit()
        print("Amount credited successfully")
        try:
            list = (balance,id)
            cur.execute("update account_details set available_balance = %s where account_number = %s"%list)
            con.commit()
        except:
            print("Failed to update the available balance")
            
        try:
            cur.execute("update static_value set transaction_id = transaction_id+1")
            con.commit()
        except:
            print("Failed to update the transaction id")
    except:
        print("Unable to perform the transaction")
    

# defining printStatement function
def printStatement(id):
    try:
        cur.execute("select * from transaction where account_number = %s"%id)
        result = cur.fetchall()
        print("A/C No.    Amount            Date                      Avl. Bal    Transaction ID  Type")
        for i in result:
            print("%s   %s        %s   %s         %s         %s"%(i[0],i[1],i[2],i[3],i[4],i[5]))
    except:
        print("Failed to fetch the transaction details")


# defining checkBalance function
def checkBalance(id):
    try:
        cur.execute("select available_balance from account_details where account_number = %s"%id)
        result = cur.fetchone()
        print("Your available balance is : %s"%result[0])
    except:
        print("Failed to fetch the available balance details")
  

print("*--*--*--*--*--*--*--*--*--*--*  Mini Bank Self Services  *--*--*--*--*--*--*--*--*--*--*\n\n")

id = 0

while(True):
    print("Choose the option from below\n")
    print("\n1.   Register")
    print("2.   Login")
    print("3.   Exit\n")

    n = int(input("Enter your choosen option : "))
    if n==1 or n==2 or n==3 :
        
        if n==1 :
            register()
        elif n==2 :
            id = login()
            if id==0:
                print("Failed to login")
            else:
                while True:
                    print("Choose the option from below\n")
                    print("\n1.   Debit")
                    print("2.   Credit")
                    print("3.   Print statement")
                    print("4.   Check balance")
                    print("5.   Exit\n")
                    m = int(input("Enter your choosen option : "))
                    if m==1 or m==2 or m==3 or m==4 or m==5 :
                        if m==1 :
                            debit(id)
                        elif m==2:
                            credit(id)
                        elif m==3:
                            printStatement(id)
                        elif m==4:
                            checkBalance(id)
                        else:
                            break
                    else:
                        print("Please enter the valid input")
        else:
            break
    else:
        print("Please enter the correct option\n")

con.close()