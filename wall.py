import pymongo
from datetime import datetime

def wall(db,user):
    """
    Display your posts. Of course, get all posts would be fine.
    However, the function that supports displaying a few posts, e.g., five posts, looks much better than displaying all posts.
    Remind the lab4 that dealt'with cursor.
    """
    while True:
        try:
            id = user['id']
            cursor = db.posts.find({'id': id}).sort([('date', pymongo.DESCENDING)])
            post_exists = cursor.count()
            if post_exists:
                for doc in cursor:
                    show_post(doc)
                    while True:

                        while True:
                            demand = input('\nWhat do you want to do? [next/comment/delete]: ')
                            if demand.lower() in ['next', 'comment', 'delete']:
                                break
                            else:
                                print('\nInvalid input!')
                        if demand.lower() == 'next':
                            break
                        elif demand.lower() == 'comment':
                            write_comment(db, user, doc)
                            continue
                        else:
                            confirm = input('\nAre you serious? [y/any other key]: ')
                            if confirm.lower() == 'y':
                                db.posts.delete_one({'_id': doc['_id']})
                                break
                            else:
                                continue
                print('\nNo more post!')
                break

            else:
                print("\nYou've never uploaded any post!")
                break

        except KeyboardInterrupt:
            break

def show_post(doc):
    id = doc['id']
    date = doc['date']
    title = doc['title']
    content = doc['content']
    tags = doc['tags']
    likes = doc['likes']
    comments = doc['comments']
    print('\n\n\nID:', id)
    print('\nDate:', date)
    print('\nTitle:', title)
    print('\n' + content)
    print('\nTags: ' + ', '.join(tags))
    print('\n{0} people like this post.'.format(len(likes)))
    print('\n{0} comments'.format(len(comments)))
    if comments:
        print('\n{:^25}{:^20}{:^50}'.format('Date', 'ID', 'Comment'))
    for comment in comments:
        comment_date = comment['date']
        comment_id = comment['id']
        comment_content = comment['comment']
        print('{:^25}{:^20}{:^50}'.format(comment_date, comment_id, comment_content))

def write_comment(db, user, doc):
    _id = doc['_id']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = user['id']
    comment = input('\nInput your comment: ')
    while not comment.replace(' ', ''):
        print('\nThis is only a blank space!')
        comment = input('\nInput your comment: ')
    db.posts.update({'_id': _id}, {'$push': {
        'comments': {'date': date, 'id': id, 'comment': comment}
    }})
    print('\nYour comment has been successfully added!')