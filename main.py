# main.py

from pymongo import MongoClient
import user

def mainpage(db):
    '''
    call signup() or signin()
    '''
    while True:
        try:
            demand = input("""
Mongstagram: A Social Network Service

Choose what you want to do:

1. Sign In
2. Sign Up

*Important*: Inside the program, you can back a level with Ctrl+C whenever you want to.
(quit program if it was mainpage)
""")

            service_dict = {
                '1': user.signin,
                '2': user.signup
            }
            try:
                service_dict[demand](db)
            except KeyError:
                print('Invalid input!')
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    '''
    call mainpage()
    '''

    client = MongoClient()
    db = client.lab3
    mainpage(db)

