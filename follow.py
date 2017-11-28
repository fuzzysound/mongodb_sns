def followInterface(db, user):
    """
    - An interface for user to follow or unfollow other users
    - The user can input id of other user he/she wants to fol/unfol
    """
    while True:
        try:
            followings = user['followings']
            print('\nYou are currently following:', ', '.join(followings))
            demand = input("""
What do you want to do?

1. Follow
2. Unfollow

Tell me your demand: """)

            service_dict = {
                '1': follow,
                '2': unfollow
            }

            service_dict[demand](db, user, followings)

            id = user['id']
            user = db.userdb.find_one({'id':id})

        except KeyError:
            print('Invalid input!')

        except KeyboardInterrupt:
            break

def follow(db, user, followings):
    while True:
        try:
            '''
            1. 팔로우하고자 하는 유저가 존재하는지 확인, 없으면 경고 출력
    
            2. 팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 있으면 경고 출력
    
            3. 팔로잉 목록에 없으면,
                나의 팔로잉 목록에 팔로우할 유저id 추가 + 상대방의 팔로워 목록에 내 id 추가
            '''

            followid = input('\nInput ID you want to follow: ')
            followid_exists = db.userdb.find({'id':followid}).count()
            if not followid_exists:
                print('\nThat user does not exist in our world!')
                continue
            if followid == user['id']:
                print('\nYou cannot follow yourself!')
                continue
            if followid in followings:
                print('\nYou are already following that user!')
                continue
            userid = user['id']
            db.userdb.update({'id':userid}, {'$push':{'followings':followid}})
            db.userdb.update({'id':followid}, {'$push':{'followers':userid}})
            print('\nSuccessfully followed!')
            break

        except KeyboardInterrupt:
            break

def unfollow(db, user, followings):
    while True:
        try:
            '''
            1. 언팔로우하고자하는 유저가 존재하는지 확인, 없으면 경고 출력
    
            2. 언팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 없으면 경고 출력
    
            3. 팔로잉 목록에 있으면,
                나의 팔로잉 목록에서 언팔로우할 유저id 제거 + 상대방의 팔로워 목록에서 내 id 제거
            '''

            followid = input('\nInput ID you want to unfollow: ')
            followid_exists = db.userdb.find({'id':followid}).count()
            if not followid_exists:
                print('\nThat user does not exist in our world!')
                break
            if followid not in followings:
                print('\nYou are not following that user!')
                break
            userid = user['id']
            db.userdb.update({'id':userid}, {'$pull':{'followings':followid}})
            db.userdb.update({'id':followid}, {'$pull':{'followers': userid}})
            print('\nSuccessfully unfollowed!')
            break

        except KeyboardInterrupt:
            break
