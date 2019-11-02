import sqlite3
import time
from random import randint
from datetime import date
import sys
# from marriage.registerMarriage import registerMarriage

connection = None
cursor = None
usertype = "a"
userId = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def agent_menu():
    print("\n*************************************************************")
    print("You are at the MAIN MENU.")
    print('''
        \t<1>  Register a birth
        \t<2>  Register a marriage
        \t<3>  Renew a vehicle registration
        \t<4>  Process a bill of sale
        \t<5>  Process a payment
        \t<6>  Get a driver abstract
        \t<7>  Log out of your account
        \t<8>  Exit Service Canada
    ''')
    try: # In case the user just pressed enter without writing anything
        option = int(input("Choose the number of your choice: "))

        # execute the option chosen using a dictionary
        redirect = {
            1: register_birth,
            2: register_marriage,
            3: renew_reg,
            4: process_bill,
            5: process_payment,
            6: get_abstract,
            7: login,
            8: sys.exit
        }

        func = redirect.get(option, lambda:"CHOOSE A VALID NUMBER!")
        print(func())
    except ValueError:
        print("CHOOSE A VALID NUMBER!")
        agent_menu()

    agent_menu()

    return

def enforcer_menu():
    print("\n*************************************************************")
    print("You are at the MAIN MENU.")
    print('''
        \t<1>  Issue a ticket
        \t<2>  Find a car owner
        \t<3>  Log out your account
        \t<4>  Exit Service Canada
    ''')

    try:
        option = int(input("Choose the number of your choice: "))

        # execute the option chosen using a dictionary
        redirect = {
            1: issue_ticket,
            2: find_owner,
            3: login,
            4: sys.exit
        }

        func = redirect.get(option, lambda:"CHOOSE A VALID NUMBER!")
        print(func())
    except ValueError:
        print("CHOOSE A VALID NUMBER!")
        enforcer_menu()

    enforcer_menu()

    return


def login():
    global userId
    print("*************************ServiceCanada********************************")
    userId = input("Enter your user id: ")

    if (userId == "exit"):
        sys.exit()

    password = input("Enter your password: ")


    verify_user(userId,password)
    
    return 0

    
def verify_user(id, pwd):
    global connection, cursor, usertype
    # Verify the user
    userQuery = "SELECT * FROM users WHERE uid = "+"'"+id+"'"+" AND pwd = '"+pwd+"';"

    try:
        cursor.execute(userQuery)
        info = [[str(item) for item in results] for results in cursor.fetchall()]
        

        if (len(info) == 0):
            print("\nINVALID USER ID OR PASSWORD!")
            print("Type 'exit' as the user id to close the program.")
            login()
        elif (len(info) == 1):
            if (info[0][2] == 'a'):
                usertype = 'a'
                print("\nWelcome back, "+info[0][3]+" "+info[0][4]+"!")
                agent_menu()
            elif (info[0][2] == 'o'):
                usertype = 'o'
                print("\nWelcome back, "+info[0][3]+" "+info[0][4]+"!")
                enforcer_menu()

    except sqlite3.OperationalError as error:
        print("\nINVALID USER ID OR PASSWORD!")
        print("Type 'exit' as the user id to close the program.")
        login()

    connection.commit()
    return


# Function that gives user options whether to be redirected to the recently used function
# or go back to the main menu
def use_again(funcKeyword, function):
    decision = input("Do you want to "+funcKeyword+" again?(y/n) ")

    try:
        if (decision.lower() == 'y'):
            function()
        else:
            print("You are being redirected to the MAIN MENU.") 
            if (usertype == 'a'):
                agent_menu()
            elif (usertype == 'o'):
                enforcer_menu()
    except:
        if (usertype == 'a'):
                agent_menu()
        elif (usertype == 'o'):
            enforcer_menu()
    
    return


def val_input(prompt, isRequired):

    attrb = input(prompt)
    if (attrb == '' and isRequired == False):
        print("here")
        attrb = "NULL"
    elif (attrb == '' and isRequired == True):
        print("This detail is required.")
        option = input("Try again? (y/n)")
        if (option == 'y'):
            val_input(prompt, isRequired)
        elif (option == 'n'):
            if (usertype == 'a'):
                agent_menu()
            elif (usertype == 'o'):
                enforcer_menu()


    option = input("You entered "+attrb+". Try again? (y/n)")

    if (option == 'y'):
        val_input(prompt, isRequired)
    elif (option == 'n'):
        return attrb
    else:
        print("INVALID ENTRY! MARRIAGE NOT RECORDED!")
        if (usertype == 'a'):
                agent_menu()
        elif (usertype == 'o'):
            enforcer_menu()

    return attrb

        
def insert_person():
    global connection, cursor

    # isRequired = False
    fname = val_input("Enter first name: ", True)
    lname = val_input("Enter last name: ", True)
    bdate = val_input("Enter birthdate (YYYY-MM-DD): ", False)
    bplace = val_input("Enter birth place: ", False)
    address = val_input("Enter person's address: ", False)
    phone = val_input("Enter phone number (XXX-XXX-XXXX): ", False)

    print('''
                INSERT INTO persons VALUES ('''+fname+", "+lname+", "+bdate+''', 
                '''+bplace+", "+address+", "+phone+");")
    try:
        cursor.execute("INSERT INTO persons VALUES ('"+fname+"', '"+lname+"', '"+bdate+"', '"+bplace+"', '"+address+"', '"+phone+"');")
    except:
        print("The person you are to register is already in the database.")
        if (usertype == 'a'):
                agent_menu()
        elif (usertype == 'o'):
            enforcer_menu()

    connection.commit()
    return [fname, lname]


# def register_birth():
#     global connection, cursor

#     regnoQuery = "SELECT regno FROM births;"
#     cursor.execute(regnoQuery)
#     regnums = [[str(item) for item in results] for results in cursor.fetchall()]
#     connection.commit()
 
#     # Check if regno already exists
#     while True:
#         regno = [str(randint(100,9999))]
#         if regno not in regnums:
#             break
    
#     personQuery = "SELECT fname, lname FROM persons;"
#     cursor.execute(personQuery)
#     persons = [[str(item) for item in results] for results in cursor.fetchall()]
#     connection.commit()

#     print("**************BIRTH REGISTRATION****************")

#     print("*****Child's information*******")
#     fname = input("Enter first name: ")
#     lname = input("Enter last name: ")
#     gender = input("Enter gender:(M/F) ")
#     bdate = input("Enter birthdate: ")
#     bplace = input("Enter birth place: ")

#     print("****Mother's information*****")

def register_birth():
    global connection, cursor
    regnoQuery = "SELECT regno FROM births;"
    cursor.execute(regnoQuery)
    regnums = [[str(item) for item in results] for results in cursor.fetchall()]
    connection.commit()
 
    # Check if regno already exists
    while True:
        regno = [str(randint(100,9999))]
        if regno not in regnums:
            break


    personsQuery = "SELECT fname, lname FROM persons;"
    cursor.execute(personsQuery)
    persons = [[str(item) for item in results] for results in cursor.fetchall()]
    connection.commit()

    try:
        fname = input("First Name: ")
        lname = input("Last Name: ")
        print(fname + ", " + lname)

        childName = [fname, lname]


        if (childName in persons):
            print("Person already exists in database.\n")
            print("BIRTH NOT REGISTERED!")
            use_again("register a birth", register_birth)
            
        else:
            fname = "'" + fname + "'"
            lname = "'" + lname + "'"


        gender = input("Enter gender (M/F): ")
        print(type(gender))
        genderOptions = ['m','f']
        if gender.lower() not in genderOptions:
            print("INVALID GENDER!")
            use_again("register a birth", register_birth)
        
        bdate = "'"+input("Enter birthdate(YYYY-MM-DD): ")+"'"
        bplace = "'"+input("Enter birth place:")+"'"


        today = date.today()
        regdate = "'" + today.strftime("%Y-%m-%d") + "'"
        print(regdate)

        # regplace = "'" + input("Enter Birth Location: ") + "'"
        # print(regplace)

        # Get the city of the user and set it as the reg place
        userQuery = "SELECT city FROM users WHERE uid = '"+userId+"';"
        cursor.execute(userQuery)
        city = [[str(item) for item in results] for results in cursor.fetchall()]
        connection.commit()
        regplace = "'"+city[0][0]+"'"
        print("Regplace:"+regplace)

        print("*********Father's info*********")

        f_fname = input("Enter Father's First Name: ")
        f_lname = input("Enter Father's Last Name: ")
        f_name = [f_fname, f_lname]

        if (f_name not in persons):
            print("Father does not exists in database.")
            print("Registering Father:")
            insert_person()
        else:
            f_fname = "'" + f_fname + "'"
            f_lname = "'" + f_lname + "'"

        print("*********Mother's info**********")
        m_fname = input("Enter Mother's First Name: ")
        m_lname = input("Enter Mother's Last Name: ")
        m_name = [m_fname, m_lname]

        if (m_name not in persons):
            print("Mother does not exists in database.")
            print("Registering Mother:")
            insert_person()
        else:
            m_fname = "'" + m_fname + "'"
            m_lname = "'" + m_lname + "'" 

        
        motherQuery = "SELECT address, phone FROM persons WHERE fname = '"+m_name[0]+"' AND lname = '"+m_name[1]+"';"
        cursor.execute(motherQuery)
        motherInfo = [[str(item) for item in results] for results in cursor.fetchall()]
        connection.commit()

        childQuery = "INSERT INTO persons VALUES ('"+childName[0]+"', '"+childName[1]+"', "+bdate+", "+bplace+", '"+motherInfo[0][0]+"', '"+motherInfo[0][1]+"');"
        cursor.execute(childQuery)
        connection.commit()

        birthQuery = '''
            INSERT INTO births VALUES ('''+regno[0]+''', 
            "'''+childName[0]+'''", 
            "'''+childName[1]+'''", 
            '''+regdate+''', 
            '''+regplace+''', 
            "'''+gender.upper()+'''", 
            "'''+f_name[0]+'''", 
            "'''+f_name[1]+'''", 
            "'''+m_name[0]+'''", 
            "'''+m_name[1]+'''");
            '''
        cursor.execute(birthQuery)
        connection.commit()

        print("BIRTH RECORDED!")

    except sqlite3.OperationalError as error:
        print(error)

        
    use_again("Register a Birth", register_birth)

    connection.commit()

    return   
    

    


def register_marriage():
    global connection, cursor
    regnoQuery = "SELECT regno FROM marriages;"
    cursor.execute(regnoQuery)
    regnums = [[str(item) for item in results] for results in cursor.fetchall()]
    connection.commit()
 
    # Check if regno already exists
    while True:
        regno = [str(randint(100,9999))]
        if regno not in regnums:
            break
    
    personQuery = "SELECT fname, lname FROM persons;"
    cursor.execute(personQuery)
    persons = [[str(item) for item in results] for results in cursor.fetchall()]
    connection.commit()

    try: 
        print("***Partner 1***")
        
        p1_fname = input("First Name: ")
        p1_lname = input("Last Name: ")
        p1 = [p1_fname, p1_lname]

        if p1 not in persons:
            print("PERSON NOT EXISTING! Register below.")
            p1 = insert_person()

        print("***Partner 2***")
        p2_fname = input("First Name: ")
        p2_lname = input("Last Name: ")
        p2 = [p2_fname, p2_lname]


        if p2 not in persons:
            print("PERSON NOT EXISTING! Register below.")
            p2 = insert_person()

        today = date.today() # current date and time
        regdate = today.strftime("%Y-%m-%d")  # Converting date to string

        register = "INSERT INTO marriages VALUES ('"+regno[0]+"', '"+regdate+"', 'Manila', '"+p1[0]+"', '"+p1[1]+"', '"+p2[0]+"', '"+p2[1]+"');"

        cursor.execute(register)
        print("MARRIAGE RECORDED!")
        connection.commit()
    except:
        print("Invalid!")

    use_again("register a marriage", register_marriage)

    return


def renew_reg():
    global connection, cursor
    regno = [input("Enter the registration number: ")]
    cursor.execute("SELECT regno FROM registrations;")
    print(regno)

    ## based on lab example
    regList = [[str(item) for item in results] for results in  cursor.fetchall()]
    # print(regList)
    if regno in regList:
        
        expiryQuery = "SELECT expiry FROM registrations WHERE regno = "+regno[0]+";"
        cursor.execute(expiryQuery)
        exp = [[str(item) for item in results] for results in  cursor.fetchall()]

        # print(regno)
        # print(exp[0][0][0:4])

        today = date.today()
        # Convert the fetched expiry date from string to Date
        expiryDate = date(int(exp[0][0][0:4]),int(exp[0][0][5:7]),int(exp[0][0][8:10]))
        todayStr = today.strftime("%Y-%m-%d")

        if (expiryDate <= today):
            exp = todayStr
            #print("this is today's string")
            print(exp)
        elif (expiryDate > today):
            exp = exp[0][0]
        
        renewDate= "UPDATE registrations SET expiry ="+"DATE("+"'"+exp+"'"+",'+1 year') WHERE regno = " +regno[0]+";"
        # renewDate= "UPDATE registrations SET expiry ="+"'2018-07-25' WHERE regno = " +regno[0]+";"

        cursor.execute(renewDate)
        print("Expiry date is renewed to " + exp)
        connection.commit()

    else:
        print("The registration number does not exists.")

    use_again('renew a car registration', renew_reg)    

    return

def process_bill():
    global connection, cursor
    print("****************PROCESS A BILL OF SALE********************")
    vin = input("Enter the Vehicle's vin: ")

    try:
        ownerQuery = '''
                SELECT r.fname, r.lname
                FROM registrations r
                WHERE r.vin = '''+vin+''' AND r.regdate IN 
                    (SELECT r2.regdate FROM registrations r2
                        ORDER BY r2.regdate DESC LIMIT 1);
                '''
        cursor.execute(ownerQuery)
        legitOwner = [[str(item) for item in results] for results in  cursor.fetchall()]
        legitOwner = legitOwner[0][0]+legitOwner[0][1]
        connection.commit()

    except:
        print("INVALID VIN! TRANSACTION CANNOT BE COMPLETED!")
        use_again("process a bill of sale", process_bill)

    # Get the current owner of the vehicle
    print("*************Vehicle's CURRENT Owner**************")
    currFname = input("Enter first name: ")
    currLname = input("Enter last name: ")
    curr = currFname+currLname

    # Verify the current owner
    if (curr.lower() != legitOwner.lower()):
        print("Your input DOES NOT match our records. TRANSACTION CANNOT BE COMPLETED!")
        use_again("process a bill of sale", process_bill)
    
    print("*************Vehicle's NEW Owner*****************")
    newFname = input("Enter first name: ")
    newLname = input("Enter last name: ")
    plateNum = input("Enter NEW plate number: ")

    regnoQuery = "SELECT regno FROM registrations;"
    cursor.execute(regnoQuery)
    regnums = [[str(item) for item in results] for results in cursor.fetchall()]
    connection.commit()
 
    # Check if regno already exists
    while True:
        regno = [str(randint(100,9999))]
        if regno not in regnums:
            break

    setNewOwner = '''
            INSERT INTO registrations VALUES ('''+regno[0]+''', date('now'), date('now','+1 year'), 
            "'''+plateNum+'''", '''+vin+''', 
            "'''+newFname+'''", "'''+newLname+'''");  
            '''

    try:
        cursor.execute(setNewOwner)
        connection.commit()
        print("BILL OF SALE PROCESSED!")

    except:
        print("BILL OF SALE NOT PROCESSED!")
        print("Make sure the new owner is listed in the database.")

    use_again("process a bill of sale", process_bill)

    return


def get_abstract():
    global connection, cursor

    dfname = input("Please enter driver's first name: ")
    dlname = input("Please enter driver's last name: ")

    driverQuery = '''
            CREATE VIEW drivers(fname, lname, num_tickets, num_demeritnote, num_demeritpts)
            AS SELECT r.fname, r.lname, COUNT(t.tno), COUNT(DISTINCT d.ddate), SUM(d.points) 
                FROM (registrations r LEFT OUTER JOIN tickets t ON (r.regno = t.regno AND (t.vdate >= date('now', '-2 year' )))) 
                LEFT OUTER JOIN demeritNotices d ON (r.fname=d.fname AND r.lname=d.lname AND (d.ddate >= date('now', '-2 year'))) ''' +'''
                WHERE r.fname = "'''+dfname+'''" AND r.lname = "'''+dlname+'''"  
                GROUP BY r.fname, r.lname;
        '''

    # driverQuery = '''
    # CREATE VIEW drivers(fname, lname, num_tickets, num_demeritnote, num_demeritpts)
    # AS SELECT r.fname, r.lname, COUNT(t.tno), COUNT(d.points), SUM(d.points)
    #     FROM (registrations r LEFT OUTER JOIN tickets t ON (r.regno = t.regno AND (t.vdate >= date('now', '-2 year' ) OR t.vdate = NULL)))
    #             LEFT OUTER JOIN demeritNotices d ON (r.=fnamed.fname AND r.lname=d.lname AND (d.ddate >= date('now', '-2 year' ) OR d.ddate = NULL))
    #     GROUP BY r.fname, r.lname;
    # '''

    # SELECT p.fname, p.lname, COUNT(t.tno), COUNT(DISTINCT d.ddate), SUM(d.points) FROM persons p, (registrations r LEFT OUTER JOIN tickets t ON (r.fname = p.fname AND r.fname = p.lname AND r.regno = t.regno AND (t.vdate >= date('now', '-2 year' )))) LEFT OUTER JOIN demeritNotices d ON (r.fname=d.fname AND r.lname=d.lname AND (d.ddate >= date('now', '-2 year'))) GROUP BY p.fname, p.lname;
    # SELECT p.fname, p.lname, COUNT(t.tno), COUNT(DISTINCT d.ddate), SUM(d.points) FROM persons p1, (registrations r LEFT OUTER JOIN tickets t ON (r.regno = t.regno AND (t.vdate >= date('now', '-2 year' )))) q, (demeritNotices d LEFT JOIN persons p ON (p.fname=d.fname AND p.lname=d.lname AND (d.ddate >= date('now', '-2 year')))) s WHERE GROUP BY p.fname, p.lname;

    try:
        cursor.execute("DROP VIEW IF EXISTS drivers;")
        cursor.execute(driverQuery)
        connection.commit()
        cursor.execute("SELECT * FROM drivers;")

        abstract = [[str(item) for item in results] for results in cursor.fetchall()]
        connection.commit()

        print("Driver's Profile:")
        print("\tFirst name: "+abstract[0][0])
        print("\tLast name: "+abstract[0][1])
        print("\tNumber of tickets: "+abstract[0][2])
        print("\tNumber of demerit notices: "+abstract[0][3])
        print("\tNumber of demerit points: "+abstract[0][4])

        option = input("Enter 't' to see the list of tickets, 's' to search again, or any character to go back to the main menu: ")

        if (option == 't'):
            ticketQuery = '''
                    SELECT t.tno, t.fine, t.violation, t.vdate, t.regno, v.make, v.model 
                    FROM tickets t, registrations r, vehicles v 
                    WHERE t.regno = r.regno AND  r.vin = v.vin
                        AND t.vdate >= date('now', '-2 year') AND r.fname||r.lname ="'''+abstract[0][0]+abstract[0][1]+'''";
                    '''
            cursor.execute(ticketQuery)
            tickets = [[str(item) for item in results] for results in cursor.fetchall()]
            connection.commit()
            numTickets = len(tickets)
            
            for i in range(numTickets):
                print("*********************************")
                print("Ticket number: "+tickets[i][0])
                print("\tFine: $"+tickets[i][1])
                print("\tViolation: "+tickets[i][2])
                print("\tViolation date:"+tickets[i][3])
                print("\tRegistration number: "+tickets[i][4])
                print("\tCar make: "+tickets[i][5])
                print("\tCar model:"+tickets[i][6])

                if((i+1) % 5 == 0):
                    option = input("Enter 'm' to see more, 's' to search again, or any character to go back to the main menu: ")

                    if (option == 'm'):
                        continue
                    elif (option == 's'):
                        get_abstract()
                    else:
                        if (usertype == 'a'):
                            agent_menu()
                        elif (usertype == 'o'):
                            enforcer_menu()
        elif (option == 's'):
            get_abstract()
        else:
            if (usertype == 'a'):
                agent_menu()
            elif (usertype == 'o'):
                enforcer_menu()

        
    except sqlite3.OperationalError as error:
        print(error)

    use_again("get a driver's abstract", get_abstract)
    
    return        


def process_payment():
    global connection, cursor

    print("***********TICKET PAYMENT****************")
    # Get today's date
    today = date.today()
    todayStr = today.strftime("%Y-%m-%d")
    # Get all ticket numbers and amount
    ticketQuery = "SELECT tno FROM tickets;"
    cursor.execute(ticketQuery)
    tickets =  [[str(item) for item in results] for results in cursor.fetchall()]
    # print(tickets)

    # Get the ticket number from the user
    ticketNum = [input("Please enter a valid ticket number: ")]
    print("You are recording a payment for ticket number "+ticketNum[0]+".")

    # Verify that the ticket number entered is valid
    if ticketNum in tickets:
        cursor.execute("SELECT fine FROM tickets WHERE tno ="+ticketNum[0]+";")
        fine =  [[str(item) for item in results] for results in cursor.fetchall()]

        # Get the total amount already paid by the violator
        cursor.execute("SELECT SUM(amount) FROM payments WHERE tno ="+ticketNum[0]+" GROUP by tno;")
        paidAmount =  [[str(item) for item in results] for results in cursor.fetchall()]

        if (len(paidAmount) > 0): # Check if there was already a previous payment
            pendingAmount = int(fine[0][0]) - int(paidAmount[0][0])
            print("The pending amount is $"+str(pendingAmount))
        
        else:
            pendingAmount = int(fine[0][0])
            print("The pending amount is $"+str(pendingAmount))


        # TO DO: Check if the input is just a newline character or a negative number

        try:
            payingAmount = int(input("Please enter the amount paid today: $"))

            if (payingAmount > 0):
                if (payingAmount > pendingAmount):
                    print("The amount paid exceeds the pending amount.")
                elif (payingAmount < pendingAmount):
                    if (len(paidAmount) > 0):  # Check if there was already a previous payment
                        totalPaid = payingAmount + int(paidAmount[0][0])
                    else:
                        totalPaid = payingAmount
                    recordPayment = "INSERT INTO payments(tno, pdate, amount) VALUES ("+ticketNum[0]+","+"'"+todayStr+"'"+","+str(payingAmount)+");"
                    cursor.execute(recordPayment) # Only one payment could be accepted for a ticket in a day
                print("PAYMENT RECORDED!")
                print("The pending amount is $"+str(int(fine[0][0])-totalPaid))
            else:
                print("PAYMENT NOT RECORDED!Amount entered is not valid!")
        except:
            print("PAYMENT NOT RECORDED! Either a payment has already been made today for this ticket or the amount entered is not valid.")

    else:
        print("You entered an invalid ticket!")

    
    connection.commit()

    use_again("process a payment", process_payment)
    return





# Checks if the value is either yes or no, otherwise it will ask the user the second time
# and go back to the main menu the third time
# This function is made for the function find_owner
def yes_or_no(keyword, doesKnow):
    value = ""
    if (doesKnow.lower() == 'y'):
        value = input("Please ENTER the car "+keyword+": ")
    elif (doesKnow.lower() == 'n'):
        value = "none"
    else:
        print("INVALID ENTRY!")
        option = input("Try again?(y/n) ")
        if (option.lower() == 'y'):
            print("\n****************************")
            doesKnow = input("Do you KNOW the car "+keyword+"?(y/n) ")
            value = yes_or_no(keyword, doesKnow)
        elif (option.lower() == 'n'):
            print("You are being redirected to the MAIN MENU.")
            if (usertype == 'a'):
                agent_menu()
            elif (usertype == 'o'):
                enforcer_menu()
        else:
            print("INVALID ENTRY!")
            print("You are being redirected to the MAIN MENU.")
            if (usertype == 'a'):
                agent_menu()
            elif (usertype == 'o'):
                enforcer_menu()
    return value



# For find_owner
def show_results(matched):
    for i in range(len(matched)):
        print("<"+str(i+1)+">")
        print("\tMake: "+matched[i][0])
        print("\tModel: "+matched[i][1])
        print("\tYear: "+matched[i][2])
        print("\tColor: "+matched[i][3])
        print("\tPlate Number: "+matched[i][4])

        if (len(matched) < 4):
            print("\tLatest registration date: "+matched[i][5])
            print("\tExpiry date: "+matched[i][6])
            print("\tOwner: "+matched[i][7])

    if (len(matched) >= 4):
        num = int(input("Enter the result number to see more details or press any key to start a new search: "))
        print("<"+str(num)+">")
        print("\tMake: "+matched[num][0])
        print("\tModel: "+matched[num][1])
        print("\tYear: "+matched[num][2])
        print("\tColor: "+matched[num][3])
        print("\tPlate Number: "+matched[num][4])
        print("\tLatest registration date: "+matched[num][5])
        print("\tExpiry date: "+matched[num][6])
        print("\tOwner: "+matched[num][7])

        option = input("Do you want to see all the results again?(y/n) ")
        if(option == 'y'):
            show_results(matched)
        else:
            return
            
        # else:
        #     print("No results to show.")

    return


def issue_ticket():

    print("****************************************************************")
    regno = [input("Enter the registration number: ")]
    cursor.execute("SELECT r.regno FROM registrations r;")
    regNums = [[str(item) for item in results] for results in cursor.fetchall()]

    # Check if regno is valid or not
    if regno not in regNums:
        print("INVALID REGISTRATION NUMBER!")
        use_again("issue a ticket", issue_ticket)
    
    
    try:

        regQuery = '''SELECT r.fname||" "||r.lname AS name, v.make, v.model, v.year, v.color
                FROM vehicles v, registrations r
                WHERE v.vin = r.vin AND r.regno = '''+regno[0]+''';
            '''
        cursor.execute(regQuery)
        regInfo = [[str(item) for item in results] for results in cursor.fetchall()]
        connection.commit()

        print("Registration number "+regno[0])
        print("\tRegistered owner: "+regInfo[0][0])
        print("\tVehicle make: "+regInfo[0][1])
        print("\tVehicle model: "+regInfo[0][2])
        print("\tVehicle year: "+regInfo[0][3])
        print("\tVehicle color: "+regInfo[0][4])
        print()

    except:
        print("SOMETHING WENT WRONG!")
        use_again("issue a ticket", issue_ticket)
    
    option = input("Do you want to ticket this registration?(y/n) ")

    if (option == 'y'):
        tnoQuery = "SELECT tno FROM tickets;"
        cursor.execute(tnoQuery)
        tnums = [[str(item) for item in results] for results in cursor.fetchall()]
        connection.commit()
    
        # Check if regno already exists
        while True:
            tno = [str(randint(100,9999))]
            if tno not in tnums:
                break
        
        # Get violation date
        vdate = input("Enter violation date (YYYY-MM-DD): ")

        # Set violation date to today's date
        if (vdate == ''):
            today = date.today() # current date and time
            vdate = today.strftime("%Y-%m-%d")  # Converting date to string


        # Get description
        text = "'"+input("Describe the violation: ")+"'"

        # Get fine amount
        fine = input("Enter fine amount: $")

        issueQuery = "INSERT INTO tickets VALUES ("+tno[0]+", "+regno[0]+", "+fine+", "+text+", '"+vdate+"');"

        try:
            cursor.execute(issueQuery)
            connection.commit()
            print("TICKET ISSUED!")
        except:
            print("TICKET NOT ISSUED!")

    elif (option == 'n'):
        use_again("issue a ticket", issue_ticket)

    else:
        print("INVALID ENTRY!")

    use_again("issue a ticket", issue_ticket)

    return



def find_owner():
    global connection, cursor
    print("***********CAR OWNER SEARCH************")
    whereClause = "v.vin = r.vin"

    # Get the car make
    knowMake = input("Do you KNOW the car make?(y/n) ")
    
    make = yes_or_no("make", knowMake)

    if (make != "none"): # Check if the user knows the make
        whereClause += " AND v.make = '"+make+"'"

    # Get the car model
    print("\n****************************")
    knowModel = input("Do you KNOW the car model?(y/n) ")
    
    model = yes_or_no("model", knowModel)

    if (model != "none"): # Check if the user knows the model
        whereClause += " AND v.model = '"+model+"'"

    # Get the car year
    print("\n****************************")
    knowYear = input("Do you KNOW the car year?(y/n) ")
    
    year = yes_or_no("year", knowYear)

    if (year != "none"): # Check if the user knows the model
        whereClause += " AND v.year = '"+year+"'"

    # Get the car color
    print("\n****************************")
    knowColor = input("Do you KNOW the car color?(y/n) ")
    
    color = yes_or_no("color", knowColor)

    if (color != "none"): # Check if the user knows the color of the car
        whereClause += " AND v.color = '"+color+"'"

    # Get the car plate number
    print("\n****************************")
    knowPlate = input("Do you KNOW the plate number?(y/n) ")
    
    plate = yes_or_no("plate", knowPlate)

    if (plate != "none"): # Check if the user knows the color of the car
        whereClause += " AND r.plate = '"+ plate+"'"

    # print(whereClause)

    # Construct the query
    # TO DO: Figure out how to get the LATEST registration record --> solve by grouping by vin
    # TODO: Implements string matching
    ownerQuery = '''

            SELECT v.make, v.model, v.year, v.color, r.plate,
                r.regdate, r.expiry, r.fname||" "||r.lname
            FROM vehicles v, registrations r
            WHERE '''+whereClause+''' AND r.regdate IN 
                (SELECT r2.regdate FROM registrations r2
                    WHERE r2.vin = v.vin
                    ORDER BY r2.regdate DESC LIMIT 1);
            '''
    try:
        cursor.execute(ownerQuery)
        matched = [[str(item) for item in results] for results in cursor.fetchall()]
        # print(matched)
        connection.commit()
    except sqlite3.OperationalError:
        print("Your search is invalid.")

    print("\n****************************************")

    try:
        show_results(matched)
        #TODO: Go back to all the results

        print("****************************")
        

    except:
        print("No results to show.")

    use_again('find a car owner', find_owner)

    return
        #SELECT v.make, v.model, v.color, r.plate, r.regno, r.expiry, r.fname||r.lname FROM vehicles v, registrations r GROUP BY v.vin


   
def main():
    global connection, cursor
    dbName = input("Please enter the database name (format: <dbname>.db):")
    path = "./"+dbName
    connect(path)
    # drop_tables()
    # define_tables()
    # insert_data()

    #### your part ####
    # register all students in all courses.
    # cursor.execute('''select student_id from student;''')
    # studentList = [[str(item) for item in results] for results in  cursor.fetchall()]
    # cursor.execute("""select course_id from course""")
    # studentList = [[str(item) for item in results] for results in  cursor.fetchall()]

    login()
    # register_marriage()
    # renew_reg()
    #process_payment()
    # find_owner()
    # bool exists = false;
    # for student in studentList:
    #     if ()

	# for course in courseList:
	#     enroll(student[0], course[0])
    # connection.commit()

    # return


if __name__ == "__main__":
    main()