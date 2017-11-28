import pymongo
from wall import show_post, write_comment

def newsfeed(db,user):
    """
    It is similar to the function in wall.py
    Get posts of your followings.
    There can be a few options to sort the posts such as posting date or alphabetical order of following's name.
    """
    while True:
        try:
            followings = user['followings']
            if not followings:
                print('\nYou are not following anyone!')
                break
            cursor = db.posts.find({'id': {'$in': followings}}).sort([('date', pymongo.DESCENDING)])
            post_exists = cursor.count()
            if post_exists:
                for doc in cursor:
                    show_post(doc)
                    while True:
                        if user['id'] in doc['likes']:
                            liked = True
                            demand = input('\nWhat do you want to do? [next/comment/undo like]: ')
                        else:
                            liked = False
                            demand = input('\nWhat do you want to do? [next/comment/like]: ')

                        if demand.lower() in ['next', 'comment', 'undo like', 'like']:
                            if liked and demand.lower() == 'like':
                                print('\nInvalid input!')
                            elif not liked and demand.lower() == 'undo like':
                                print('\nInvalid input!')
                            else:
                                break
                        else:
                            print('\nInvalid input!')
                    if demand.lower() == 'next':
                        continue
                    elif demand.lower() == 'comment':
                        write_comment(db, user, doc)
                        continue
                    elif demand.lower() == 'undo like':
                        db.posts.update({'_id': doc['_id']}, {'$pull':{'likes': user['id']}})
                        print('\nUndid like it!')
                        continue
                    else:
                        db.posts.update({'_id': doc['_id']}, {'$push':{'likes': user['id']}})
                        print('\nLiked it!')
                        continue

                print('\nNo more post!')
                break
            else:
                print("\nYour followers've never uploaded even one post!")
                break

        except KeyboardInterrupt:
            break
