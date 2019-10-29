import sqlite3
import time
from random import randint
from datetime import date
# from marriage.registerMarriage import registerMarriage

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def register_marriage():
    global connection, cursor
    regno = randint(100000,999999)

    print("***Partner 1***")
     
    p1_fname = "'"+input("First Name: ")+"'"
    p1_lname = "'"+input("Last Name: ")+"'"

    print("***Partner 2***")
    p2_fname = "'"+input("First Name: ")+"'"
    p2_lname = "'"+input("Last Name: ")+"'"

    today = date.today() # current date and time
    regdate = "'"+today.strftime("%Y-%m-%d")+"'"  # Converting date to string

    register = "INSERT INTO marriages(regno,regdate,regplace,p1_fname,p1_lname,p2_fname,p2_lname) VALUES"+"("+str(regno)+", "+regdate+", "+"'Manila', "+p1_fname+", "+p1_lname+", "+p2_fname+", "+p2_lname+")"

    cursor.execute(register)
    connection.commit()

    return


def renew_reg():
    regno = [input("Enter the registration number: ")]
    cursor.execute("SELECT regno FROM registrations;")
    print(regno)

    ## based on lab example
    regList = [[str(item) for item in results] for results in  cursor.fetchall()]
    print(regList)
    if regno in regList:
        
        expiryQuery = "SELECT expiry FROM registrations WHERE regno = "+regno[0]+";"
        cursor.execute(expiryQuery)
        exp = [[str(item) for item in results] for results in  cursor.fetchall()]

        print(regno)
        print(exp[0][0][0:4])

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
        print("Expiry date is renewed to" + exp)
        connection.commit()

    else:
        print("The registration number does not exists.")

    return

def process_payment():
    print("***********TICKET PAYMENT****************")
    # Get today's date
    today = date.today()
    todayStr = today.strftime("%Y-%m-%d")
    # Get all ticket numbers and amount
    ticketQuery = "SELECT tno FROM tickets;"
    cursor.execute(ticketQuery)
    tickets =  [[str(item) for item in results] for results in cursor.fetchall()]
    print(tickets)

    # Get the ticket number from the user
    ticketNum = [input("Please enter a valid ticket number: ")]
    print("You are recording a payment for ticket number:"+ticketNum[0])

    # Verify that the ticket number entered is valid
    if ticketNum in tickets:
        cursor.execute("SELECT fine FROM tickets WHERE tno ="+ticketNum[0]+";")
        fine =  [[str(item) for item in results] for results in cursor.fetchall()]

        # Get the total amount already paid by the violator
        cursor.execute("SELECT SUM(amount) FROM payments WHERE tno ="+ticketNum[0]+" GROUP by tno;")
        paidAmount =  [[str(item) for item in results] for results in cursor.fetchall()]

        pendingAmount = int(fine[0][0]) - int(paidAmount[0][0])
        print("The pending amount is "+str(pendingAmount))

        payingAmount = int(input("Please enter the amount paid today: "))
        # TO DO: Check if the input is just a newline character 

        # try:
        if (payingAmount > pendingAmount):
            print("The amount paid exceeds the pending amount.")
        elif (payingAmount < pendingAmount):
            totalPaid = payingAmount + int(paidAmount[0][0])
            recordPayment = "INSERT INTO payments(tno, pdate, amount) VALUES ("+ticketNum[0]+","+"'"+todayStr+"'"+","+str(payingAmount)+");"
            cursor.execute(recordPayment) # Only one payment could be accepted for a ticket in a day
        print("Payment Recorded!")
        print("The pending amount is "+str(int(fine[0][0])-totalPaid))
        # except:
        #     print("Invalid")

    
    connection.commit()

# Check if the value is either yes or no, otherwise it will ask the user the second time
# and go back to the main menu the third time
# This function is made for the function find_owner
def yes_or_no(keyword, doesKnow):
    value = ""
    if (doesKnow.lower() == 'y'):
        value = input("Please enter the car "+keyword+": ")
    elif (doesKnow.lower() == 'n'):
        value = "none"
    else:
        print("Invalid entry!")
        option = input("Try again?(y/n) ")
        if (option.lower() == 'y'):
            print("\n****************************")
            doesKnow = input("Do you know the car "+keyword+"?(y/n) ")
            value = yes_or_no(keyword, doesKnow)
        elif (option.lower() == 'n'):
            print("You are being redirected to the main menu.")
        else:
            print("Invalid entry!")
            print("You are being redirected to the main menu.")
    return value


def find_owner():
    print("***********CAR OWNER SEARCH************")
    whereClause = "v.vin = r.vin"

    # Get the car make
    knowMake = input("Do you know the car make?(y/n) ")
    
    make = yes_or_no("make", knowMake)

    if (make != "none"): # Check if the user knows the make
        whereClause += " AND v.make = '"+make+"'"

    # Get the car model
    print("\n****************************")
    knowModel = input("Do you know the car model?(y/n) ")
    
    model = yes_or_no("model", knowModel)

    if (model != "none"): # Check if the user knows the model
        whereClause += " AND v.model = '"+model+"'"

    # Get the car year
    print("\n****************************")
    knowYear = input("Do you know the car year?(y/n) ")
    
    year = yes_or_no("year", knowYear)

    if (year != "none"): # Check if the user knows the model
        whereClause += " AND v.year = '"+year+"'"

    # Get the car color
    print("\n****************************")
    knowColor = input("Do you know the car color?(y/n) ")
    
    color = yes_or_no("color", knowColor)

    if (color != "none"): # Check if the user knows the color of the car
        whereClause += " AND v.color = '"+color+"'"

    # Get the car plate number
    print("\n****************************")
    knowPlate = input("Do you know the plate number?(y/n) ")
    
    plate = yes_or_no("plate", knowPlate)

    if (plate != "none"): # Check if the user knows the color of the car
        whereClause += "AND r.plate = '"+ plate+"'"

    print(whereClause)

    # Construct the query
    # TO DO: Figure out how to get the LATEST registration record
    # TODO: Implements string matching
    ownerQuery = '''

            SELECT v.make, v.model, v.year, v.color, r.plate,
                r.regdate, r.expiry, r.fname||" "||r.lname
            FROM vehicles v, registrations r
            WHERE '''+whereClause+''';

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
        for i in range(len(matched)):
            print("<"+str(i+1)+">")
            print("\tMake: "+matched[i][0])
            print("\tModel: "+matched[i][1])
            print("\tYear: "+matched[i][2])
            print("\tColor: "+matched[i][3])
            print("\tPlate Number: "+matched[i][4])

            if (len(matched) <= 4):
                print("\tLatest registration date: "+matched[i][5])
                print("\tExpiry date: "+matched[i][6])
                print("\tOwner: "+matched[i][7])

        if (len(matched) > 4):
            num = int(input("Enter the result number to see more details: "))
            print("<"+str(num)+">")
            print("\tMake: "+matched[num][0])
            print("\tModel: "+matched[num][1])
            print("\tYear: "+matched[num][2])
            print("\tColor: "+matched[num][3])
            print("\tPlate Number: "+matched[num][4])
            print("\tLatest registration date: "+matched[num][5])
            print("\tExpiry date: "+matched[num][6])
            print("\tOwner: "+matched[num][7])
        #TODO: Go back to all the results

        print("****************************")

    except:
        print("No results to show.")

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

    # register_marriage()
    # renew_reg()
    #process_payment()
    find_owner()
    # bool exists = false;
    # for student in studentList:
    #     if ()

	# for course in courseList:
	#     enroll(student[0], course[0])
    # connection.commit()
    connection.close()
    # return


if __name__ == "__main__":
    main()