# Requirements:
# births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
# regdate will be the current date when command is inputted
# regno is a random number of 6 digits (UNIQUE)

from random import randint
from datetime import date


def random_regno(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def register_birth():
    global connection, cursor

    len_no = 6

    print('Registering a birth:\n')

    fname = input('Enter first name: ')
    lname = input('Enter last name: ')

    regdate = date.today()
    regno = random_regno(len_no)

    print(regno)

    return


def main():
    user_input = input('Enter number: ')
    user_input = int(user_input)

    print(random_regno(user_input))
    return


main()
