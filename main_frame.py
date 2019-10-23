import sqlite3
import time
import hashlib
import register_birth

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return


def insert_data():
    global connection, cursor

    insert_courses = '''
                        INSERT INTO course(course_id, title, seats_available) VALUES
                            (1, 'CMPUT 291', 200),
                            (2, 'CMPUT 391', 100),
                            (3, 'CMPUT 101', 300);
                     '''

    insert_students = '''
                        INSERT INTO student(student_id, name) VALUES
                                (1509106, 'Saeed'),
                                (1409106, 'Alex'),
                                (1609106, 'Mike');
                       '''

    cursor.execute(insert_courses)
    cursor.execute(insert_students)
    connection.commit()
    return


def enroll_assign_grades():
    global connection, cursor

    cursor.execute('SELECT * FROM course;')
    all_courses = cursor.fetchall()

    cursor.execute('SELECT * FROM student;')
    all_students = cursor.fetchall()

    grades = ['A', 'A', 'C', 'B', 'C', 'B', 'F', 'C', 'A']
    i = 0

    for every_course in all_courses:
        for every_student in all_students:
            enroll(every_student[0], every_course[0])

            data = (grades[i], every_student[0], every_course[0])
            cursor.execute('UPDATE enroll SET grade=? where student_id=? and course_id=?;', data)
            i += 1

    return


def enroll(student_id, course_id):
    global connection, cursor

    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    crs_id = (course_id,)
    cursor.execute('SELECT seats_available FROM course WHERE course_id=?;', crs_id)
    seats_available = cursor.fetchone()

    if seats_available > 0:
        data = (student_id, course_id, current_date)
        cursor.execute('INSERT INTO enroll (student_id, course_id, enroll_date) VALUES (?,?,?);', data)
        cursor.execute('UPDATE course SET seats_available = seats_available - 1 where course_id=?;', crs_id)

    connection.commit()
    return


def drop(student_id, course_id):
    global connection, cursor

    # YOUR PART
    # Drop the course for the student and update the seats_avialable column

    connection.commit()
    return


def GPA(grade):
    global connection, cursor

    # YOUR PART
    # Map the grade to a numerical value

    return 0


def main():
    global connection, cursor

    path = "./register.db"
    connect(path)
    connection.create_function('GPA', 1, GPA)

    insert_data()
    enroll_assign_grades()
    register_birth()

    # YOUR PART
    # Use the GPA function to get a sorted list of the student names with their average GPAs.

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
