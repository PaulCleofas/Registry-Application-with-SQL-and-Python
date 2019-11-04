import sqlite3
from random import randint
from datetime import date
import sys
from getpass import getpass


connection = None
cursor = None
usertype = "a"
userId = None


def connect(path):
    """
        Description:
            * A registry agent function used to record a new birth 
                registration into the database
        Arguments:
            None
        
        Returns:
            None
    """
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def agent_menu():
    """
        Description:
            * This function acts as a main menu of the command line interface
                which lets a registry agent user choose a transaction to accomplish
                and redirects the user to the interface of the chosen transaction
        Arguments:
            None
        
        Returns:
            None
    """
    print("\n*******************REGISTRY AGENT************************")
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

        func = redirect.get(option, lambda:print("CHOOSE A VALID NUMBER!"))
        func()
    except ValueError:
        print("CHOOSE A VALID NUMBER!")
        agent_menu()

    agent_menu()

    return


def enforcer_menu():
    """
        Description:
            * This function acts as a main menu of the command line interface
                which lets a traffic officer user choose a transaction to accomplish
                and redirects the user to the interface of the chosen transaction.
        Arguments:
            None
        
        Returns:
            None
    """
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

        func = redirect.get(option, lambda:print("CHOOSE A VALID NUMBER!"))
        func()
    except ValueError:
        print("CHOOSE A VALID NUMBER!")
        enforcer_menu()

    enforcer_menu()

    return


def login():
    """
        Description:
            * This function prompts the user to enter his/her credentials (userid and password)
            before giving access to the application. The credentials will then be compared against
            the database records to check if the entered information is valid.
        Arguments:
            None
        Returns:
            None
    """
    global connection, cursor, userId
    print("*************************ServiceCanada***********************************")
    # Prompt user to enter user id and password
    userId = input("Enter your user id: ")

    if (userId == "exit"):
        sys.exit()

    password = getpass("Enter your password: ")


    verify_user(userId,password)
    
    return

    
def verify_user(id, pwd):
    """
        Description:
            * This function verifies whether the entered account information of the user
                matches the records in the database. If it does, the user will be allowed to proceed
                the main menu; otherwise, the user will be asked again for his/her username and password
        Arguments:
            * id (str): this contains the user id entered by the user
            * pwd (str): this contains the password entered by the user
        Returns:
            None
    """
    global connection, cursor, usertype
    # Verify the user
    userQuery = "SELECT * FROM users WHERE uid = "+"'"+id+"' COLLATE NOCASE"+" AND pwd = '"+pwd+"';"

    try:
        cursor.execute(userQuery)
        info = [[str(item) for item in results] for results in cursor.fetchall()]
        

        if (len(info) == 0): # If the user entered nothing
            print("\nINVALID USER ID OR PASSWORD!")
            print("Type 'exit' as the user id to close the program.") 
            login()
        elif (len(info) == 1):
            # Otherwise, check the type of the user and redirect the user to the appropriate menu
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


def use_again(funcKeyword, function):
    """
        Description:
            * This function asks the user id they want to start another transaction
                with the same type as the previously finished/terminated transaction
        Arguments:
            *
    """
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
    """
        Description: 
            * Function used for inserting a person and verifying that all required fields are acquired
    """

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
    """
        Description:
        * This function prompts the user to input information for a person
           that does not exist in the current database
        * it will use an SQL query command and create the new person
    """

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


def register_birth():
    """
        Description:
            * This function creates a new birth registrations. If the user inputted fname and lname
              already exist, than the function will return an "Already exists prompt" and will ask
              the user if they want to try again. If not, it will continue with the process.
            * This function will also insert a new persons if the father or mother do not exist in the
              database. It will call insert_person() and continue
        
        Returns:
            * none
    """
    print("*************REGISTER A BIRTH**************")
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
    lowPersons = [[str(item).lower() for item in results] for results in persons]
    connection.commit()

    try:
        # Ask child's name
        fname = input("First Name: ")
        lname = input("Last Name: ")
        print(fname + ", " + lname)

        childName = [fname, lname]
        lowChild = [fname.lower(), lname.lower()]


        if (lowChild in lowPersons):
            print("Person already exists in database.\n")
            print("BIRTH NOT REGISTERED!")
            use_again("register a birth", register_birth)
            
        else:
            for i in range(len(persons)):
                if (lowChild[0] == lowPersons[i][0] and lowChild[1] == lowPersons[i][1]):
                    childName[0] = persons[i][0]
                    childName[1] = persons[i][1]


        gender = input("Enter gender (M/F): ")
        print(type(gender))
        genderOptions = ['m','f']
        if gender.lower() not in genderOptions:
            print("INVALID GENDER!")
            use_again("register a birth", register_birth)
        
        bdate = "'"+input("Enter birthdate(YYYY-MM-DD): ")+"'"
        bplace = "'"+input("Enter birth place:")+"'"


        today = date.today()
        regdate = today.strftime("%Y-%m-%d")
        print(regdate)

        # regplace = "'" + input("Enter Birth Location: ") + "'"
        # print(regplace)

        # Get the city of the user and set it as the reg place
        userQuery = "SELECT city FROM users WHERE uid = '"+userId+"';"
        cursor.execute(userQuery)
        city = [[str(item) for item in results] for results in cursor.fetchall()]
        connection.commit()
        regplace = city[0][0]

        print("*********Father's info*********")

        f_fname = input("Enter Father's First Name: ")
        f_lname = input("Enter Father's Last Name: ")
        f_name = [f_fname, f_lname]

        lowFather = [f_fname.lower(), f_lname.lower()]

        if (lowFather not in lowPersons):
            print("Father does not exists in database.")
            print("Registering Father:")
            insert_person()
        else:
            for i in range(len(persons)):
                if (lowFather[0] == lowPersons[i][0] and lowFather[1] == lowPersons[i][1]):
                    f_name[0] = persons[i][0]
                    f_name[1] = persons[i][1]

        print("*********Mother's info**********")
        m_fname = input("Enter Mother's First Name: ")
        m_lname = input("Enter Mother's Last Name: ")
        m_name = [m_fname, m_lname]

        lowMother = [m_fname.lower(), m_lname.lower()]

        if (lowMother not in lowPersons):
            print("Mother does not exists in database.")
            print("Registering Mother:")
            insert_person()
        else:
            for i in range(len(persons)):
                if (lowMother[0] == lowPersons[i][0] and lowMother[1] == lowPersons[i][1]):
                    m_name[0] = persons[i][0]
                    m_name[1] = persons[i][1]

        # Check if mother and father are the same person  
        if (m_name != f_name):
            motherQuery = "SELECT address, phone FROM persons WHERE fname = '"+m_name[0]+"' COLLATE NOCASE AND lname = '"+m_name[1]+"' COLLATE NOCASE;"
            cursor.execute(motherQuery)
            motherInfo = [[str(item) for item in results] for results in cursor.fetchall()]


            childQuery = "INSERT INTO persons VALUES ('"+childName[0]+"', '"+childName[1]+"', "+bdate+", "+bplace+", '"+motherInfo[0][0]+"', '"+motherInfo[0][1]+"');"
            cursor.execute(childQuery)


            birthQuery = '''
                INSERT INTO births VALUES ('''+regno[0]+''', 
                "'''+childName[0]+'''", 
                "'''+childName[1]+'''", 
                "'''+regdate+'''", 
                "'''+regplace+'''", 
                "'''+gender.upper()+'''", 
                "'''+f_name[0]+'''", 
                "'''+f_name[1]+'''", 
                "'''+m_name[0]+'''", 
                "'''+m_name[1]+'''");
                '''
            
            cursor.execute(birthQuery)
            connection.commit()

            print("BIRTH RECORDED!")

        else:
            print("Mother and father cannot be the same person!")
            print("BIRTH NOT RECORDED!")

    except sqlite3.OperationalError as error:
        print(error)

        
    use_again("register a birth", register_birth)


    return   
    


def register_marriage():
    """
        Description:
            * This function is for creating a new registration for a marriage. It will prompt
              the user to enter two persons who want to have their registered and insert their marriage
              into the marriage records.

        Arguments:
            None
        Returns:
            None
    """
    global connection, cursor, userId
    print("****************Marriage Registration****************")
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
    lowPersons = [[str(item).lower() for item in results] for results in persons]
    connection.commit()

    try: 
        print("***Partner 1***")
        
        p1_fname = input("First Name: ")
        p1_lname = input("Last Name: ")
        p1 = [p1_fname, p1_lname]
        lowP1 = [p1_fname.lower(), p1_lname.lower()]

        print(lowPersons)
        print(persons)

        if lowP1 not in lowPersons:
            print("PERSON NOT EXISTING! Register below.")
            insert_person()
        else:
            for i in range(len(persons)):
                if (lowP1[0] == lowPersons[i][0] and lowP1[1]==lowPersons[i][1]):
                    p1[0] = persons[i][0]
                    p1[1] = persons[i][1]
            

        print("***Partner 2***")
        p2_fname = input("First Name: ")
        p2_lname = input("Last Name: ")
        p2 = [p2_fname, p2_lname]
        lowP2 = [p2_fname.lower(), p2_lname.lower()]

        if lowP2 not in lowPersons:
            print("PERSON NOT EXISTING! Register below.")
            insert_person()
        else:
            for i in range(len(persons)):
                if (lowP2[0] == lowPersons[i][0] and lowP2[1]==lowPersons[i][1]):
                    p2[0] = persons[i][0]
                    p2[1] = persons[i][1]

        # Check if husband and wife are the same person
        if (p1 != p2):

            today = date.today() # current date and time
            regdate = today.strftime("%Y-%m-%d")  # Converting date to string

            # Get the city of the user and set it as the reg place
            userQuery = "SELECT city FROM users WHERE uid = '"+userId+"';"
            cursor.execute(userQuery)
            city = [[str(item) for item in results] for results in cursor.fetchall()]
            connection.commit()
            regplace = city[0][0]
            print("Regplace:"+regplace)
            print("regno:"+regno[0])
            print("regdate: "+regdate)
            print("p1[0]: "+ p1[0])
            print("p1[1]: "+ p1[1])
            print("p2[0]: "+ p2[0])
            print("p2[1]: "+ p2[1])

            register = "INSERT INTO marriages VALUES ('"+regno[0]+"', '"+regdate+"', '"+regplace+"', '"+p1[0]+"', '"+p1[1]+"', '"+p2[0]+"', '"+p2[1]+"');"

            cursor.execute(register)
            print("MARRIAGE RECORDED!")
            connection.commit()
        else:
            print("Mother and father cannot be the same person!")
            print("BIRTH NOT RECORDED!")

    except sqlite3.OperationalError as error:
        print(error)

    use_again("register a marriage", register_marriage)

    return


def renew_reg():
    """
        Description:
            * This function is used to renew an existing vehicle registration's expiry date one year after
                today.
        Arguments:
            None
        Returns:
            None
    """
    global connection, cursor
    print("*************RENEW VEHICLE REGISTRATION*************")
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
    """
        Description:
            * This function is used to transfer ownership of the vehicle from current
                owner to the new owner given that the user inputs the correct owner and vin

        Arguments:
            None
        Returns:
            None
    """

    global connection, cursor
    print("****************PROCESS A BILL OF SALE********************")
    vin = input("Enter the vehicle's vin: ")

    try:
        ownerQuery = '''
                SELECT r.fname, r.lname
                FROM registrations r
                WHERE r.vin = '''+vin+''' AND r.regdate IN 
                    (SELECT r2.regdate FROM registrations r2
                        GROUP BY r2.vin ORDER BY r2.regdate DESC)
                ;
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
    """
        Description:
            * This function shows user the information about a driver they are looking for,
                showing the name, number of tickets, number of demerit notices, and number of demerit points.
            * This will also give user an option to see all tickets under the driver's name

        Arguments:
            None
        Returns:
            None
    """
    global connection, cursor
    print("***********GET DRIVER'S ABSTRACT*************")
    dfname = input("Please enter driver's first name: ")
    dlname = input("Please enter driver's last name: ")

    driverQuery = '''
            CREATE VIEW drivers(fname, lname, num_tickets, num_demeritnote, num_demeritpts)
            AS SELECT r.fname, r.lname, COUNT(DISTINCT t.tno), COUNT(DISTINCT d.ddate), SUM(d.points) 
                FROM (registrations r LEFT OUTER JOIN tickets t ON (r.regno = t.regno AND (t.vdate >= date('now', '-2 year' )))) 
                LEFT OUTER JOIN demeritNotices d ON (r.fname=d.fname AND r.lname=d.lname AND (d.ddate >= date('now', '-2 year'))) ''' +'''
                WHERE r.fname = "'''+dfname+'''" COLLATE NOCASE AND r.lname = "'''+dlname+'''" COLLATE NOCASE  
                GROUP BY r.fname, r.lname ;
        '''


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

        if (option.lower() == 't'):
            ticketQuery = '''
                    SELECT t.tno, t.fine, t.violation, t.vdate, t.regno, v.make, v.model 
                    FROM tickets t, registrations r, vehicles v 
                    WHERE t.regno = r.regno AND  r.vin = v.vin
                        AND t.vdate >= date('now', '-2 year') AND r.fname||r.lname ="'''+abstract[0][0]+abstract[0][1]+'''"
                    ORDER BY t.vdate DESC;
                    '''
            cursor.execute(ticketQuery)
            tickets = [[str(item) for item in results] for results in cursor.fetchall()]
            connection.commit()
            numTickets = len(tickets)
            
            # Show 5 tickets at a time
            for i in range(numTickets):
                print("*********************************")
                print("Ticket number: "+tickets[i][0])
                print("\tFine: $"+tickets[i][1])
                print("\tViolation: "+tickets[i][2])
                print("\tViolation date:"+tickets[i][3])
                print("\tRegistration number: "+tickets[i][4])
                print("\tCar make: "+tickets[i][5])
                print("\tCar model: "+tickets[i][6])

                if((i+1) % 5 == 0):
                    option = input("Enter 'm' to see more, 's' to search again, or any character to go back to the main menu: ")

                    if (option.lower() == 'm'):
                        continue
                    elif (option.lower() == 's'):
                        get_abstract()
                    else:
                        if (usertype.lower() == 'a'):
                            agent_menu()
                        elif (usertype.lower() == 'o'):
                            enforcer_menu()
        elif (option.lower() == 's'):
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
    """
        Description:
            * This function enables user to accept payments for a specified ticket.
            * Payments can be made in multiple installments but only one payment a day per ticket

        Arguments:
            None
        Returns:
            None
    """
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


def issue_ticket():
    """
    Description:
        * This function enables traffic officer to issue a ticket to a registered vehicle.
        * Violation date and fine amount are inputted by the user, however, violation date is optional
            and will be set to today's date if not given
    Arguments:
        None
    Returns:
        None
    """

    print("*******************ISSUE A TICKET*****************************")
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

        # Set violation date to today's date uf nothing's entered
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

def yes_or_no(keyword, doesKnow):
    """ 
        Checks if the value is either yes or no, otherwise it will ask the user the second time
        and go back to the main menu the third time
        This function is made for the function find_owner
    """

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



# Show results for find_owner
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


def find_owner():
    """
    Description:
        * This function enables traffic officer to find a car owner by specifying any combinations of
            make, model, year, color, and plate number. 
    Arguments:
        None
    Returns:
        None
    """
    global connection, cursor
    print("***********CAR OWNER SEARCH************")
    whereClause = "v.vin = r.vin"

    # Get the car make
    knowMake = input("Do you KNOW the car make?(y/n) ")
    
    make = yes_or_no("make", knowMake)

    if (make != "none"): # Check if the user knows the make
        whereClause += " AND v.make = '"+make+"' COLLATE NOCASE"

    # Get the car model
    print("\n****************************")
    knowModel = input("Do you KNOW the car model?(y/n) ")
    
    model = yes_or_no("model", knowModel)

    if (model != "none"): # Check if the user knows the model
        whereClause += " AND v.model = '"+model+"' COLLATE NOCASE"

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
        whereClause += " AND v.color = '"+color+"' COLLATE NOCASE"

    # Get the car plate number
    print("\n****************************")
    knowPlate = input("Do you KNOW the plate number?(y/n) ")
    
    plate = yes_or_no("plate", knowPlate)

    if (plate != "none"): # Check if the user knows the color of the car
        whereClause += " AND r.plate = '"+ plate+"' COLLATE NOCASE"

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
    
    login()


if __name__ == "__main__":
    main()