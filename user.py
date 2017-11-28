# user.py

import hashlib
import re
import getpass
from post import *
from follow import *
from explore import *
from wall import *
from newsfeed import *
from recommend_tag import recommend_tag

def signup(db):
    '''
    1. Get his/her information.
    2. Check if his/her password equals confirm password.
    3. Check if the userid already exists.
    4. Make the user document.
    5. Insert the document into users collection.
    '''
    while True:
        try:
            id_input_message = 'What will be your ID? '
            name_input_message = 'What is your name? '
            pw_input_message = 'Make up your own password. Must be more than 7 string and include both' \
                               'alphabet and numbers. '
            pw_confirm_input_message = "Type it one more for confirmation: "
            interest_input_message = "Tell me any area you are interested in, with comma-separated form: "
            profile_input_message = """
Write your profile below, in any form.

***COMMANDS***
!rm: Remove a line
!rw: Remove all and rewrite
!up: Finish writing profile
"""

            # Get id input, check if it has any non-alphanumeric, and check if it already exists in db.
            while True:
                id = input(id_input_message)
                if re.search('\W', id): # if ID contains any non-alphanumeric character
                    print('The ID must not contain any non-alphanumeric character!')
                elif db.userdb.find({'id':id}).count(): # if ID already exists in DB
                    print('This ID already exists! Try another.')
                else:
                    break

            # Get name input
            name = input(name_input_message)

            # Get password input, check if it is in proper form, and make password confirmation
            # The password is going through a hash function.
            while True:
                password = getpass.getpass(pw_input_message)
                if len(password) < 8: # if the password has length less than 8
                    print('Password too short!')
                elif not re.search('[a-zA-Z]', password) or not re.search('[0-9]', password):
                    # if the password contains only either alphabet or numbers
                    print('The password must include both alphabet and numbers!')
                else:
                    break
            while True:
                pw_confirm = getpass.getpass(pw_confirm_input_message)
                if password != pw_confirm:
                    print('It does not match!')
                else:
                    break
            pw_hash = hashlib.sha224(password.encode())

            # Get profile
            profile = ''
            print(profile_input_message)
            while True:
                line = input()
                if line == '!rm':
                    try:
                        content = content[:-(last_line_len+1)]
                    except NameError:
                        print('No line to remove!')
                elif line == '!rw':
                    profile = ''
                elif line == '!up':
                    break
                else:
                    profile += '\n' + line
                    last_line_len = len(line)

            # Get interested area with comma-seperated form
            interest = input(interest_input_message)
            interest_list = list(map(lambda string: string.strip(), interest.split(',')))
            changes_dict = recommend_tag(db, interest_list)
            if changes_dict:
                for old_tag, new_tag in changes_dict.items():
                    interest_list = [new_tag if tag == old_tag else tag for tag in interest_list]


            # Insert into db
            db.userdb.insert_one({'id': id, 'name': name, 'password': pw_hash.hexdigest(),
                                  'profile': profile, 'interest': interest_list, 'followers': [],
                                  'followings': []})
            print('Successfully signed up.')
            break

        except KeyboardInterrupt:
            break

def signin(db):
    '''
    1. Get his/her information.
    2. Find him/her in users collection.
    3. If exists, print welcome message and call userpage()
    '''
    while True:
        try:
            print('\nLogin')
            id_input_message = 'ID: '
            pw_input_message = 'Password: '
            while True:
                id = input(id_input_message)
                password = getpass.getpass(pw_input_message)
                pw_hash = hashlib.sha224(password.encode())
                user = db.userdb.find_one({'$and': [{'id': id}, {'password': pw_hash.hexdigest()}]})
                if not user:
                    print("You've just given me wrong ID or password!")
                else:
                    break
            print('Hi again')
            userpage(db, user)

        except KeyboardInterrupt:
            break

def mystatus(db, user):
    '''
    print user profile, # followers, and # followings
    '''
    profile = user['profile']
    interest = user['interest']
    followers = user['followers']
    followings = user['followings']

    print("""
Profile{0}

Interested area: {1}

Followers: {2}

Followings: {3}
    """.format(profile, ', '.join(interest), len(followers), len(followings)))



def userpage(db, user):
    '''
    user page
    '''

    while True:
        try:
            demand = input("""
What do you want to see?

1. Your Status
2. Upload / Delete Post
3. Explore
4. Newsfeed
5. Wall
6. Follow / Unfollow

Tell me your demand: """)

            service_dict = {
                '1': mystatus,
                '2': postInterface,
                '3': explore,
                '4': newsfeed,
                '5': wall,
                '6': followInterface

            }

            service_dict[demand](db, user)
            user = db.userdb.find_one({'id': user['id']})
        except KeyError:
            print('Invalid input!')

        except KeyboardInterrupt:
            break
