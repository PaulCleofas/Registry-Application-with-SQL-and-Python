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
    cursor.execute('''select regno from registrations;''')
    print(regno)

    ## based on lab example
    regList = [[str(item) for item in results] for results in  cursor.fetchall()]
    print(regList)
    if regno in regList:
        
        expiryQuery = "select expiry from registrations where regno = "+regno[0]+";"
        cursor.execute(expiryQuery)
        exp = [[str(item) for item in results] for results in  cursor.fetchall()]

        print(regno)
        print(exp[0][0][0:4])

        today = date.today()
        expiryDate = date(int(exp[0][0][0:4]),int(exp[0][0][5:7]),int(exp[0][0][8:10]))
        todayStr = today.strftime("%Y-%m-%d")

        if (expiryDate <= today):
            exp = todayStr
            print("this is today's string")
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

def main():
    global connection, cursor

    path = "./registry.db"
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

    register_marriage()
    renew_reg()
    
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