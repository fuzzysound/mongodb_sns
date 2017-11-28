from datetime import datetime
import pymongo
from recommend_tag import recommend_tag

def postInterface(db, user):
    """
    Implementing the interface to post your text.
    There are three or more items to choose functions such as inserting and deleting a text.
    """
    while True:
        try:
            demand = input("""
What do you want to do?

1. Upload a post
2. Delete a post

Tell me your demand: """)

            service_dict = {
                '1': insertPost,
                '2': deletePost
            }

            service_dict[demand](db, user)

        except KeyError:
            print('Invalid input!')

        except KeyboardInterrupt:
            break


def insertPost(db, user):
    """
    Insert user's text. You should create the post schema including,
    for example, posting date, posting id or name, and comments.
    
    You should consider how to delete the text.
    """
    while True:
        try:
            title = input('\nTitle: ')
            content = ''
            print("""
Write your post content below.

***COMMANDS***
!rm: Remove a line
!rw: Remove all and rewrite
!prv: Preview your post
!up: Upload the post
"""
                  )
            while True:
                line = input()
                if line == '!rm':
                    try:
                        content = content[:-(last_line_len+1)]
                    except NameError:
                        print('No line to remove!')
                elif line == '!rw':
                    content = ''
                elif line == '!prv':
                    print('\n' + title + '\n' + '\n' + content[1:] + '\n' + '\nResume your work: \n')
                elif line == '!up':
                    break
                else:
                    content += '\n' + line
                    last_line_len = len(line)
            tags = input('\nTag your post, in comma-separated form: ')
            tags_list = list(map(lambda string: string.strip(), tags.split(',')))
            changes_dict = recommend_tag(db, tags_list)
            if changes_dict:
                for old_tag, new_tag in changes_dict.items():
                    tags_list = [new_tag if tag == old_tag else tag for tag in tags_list]

            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id = user['id']
            name = user['name']
            db.posts.insert_one({'date': date, 'id': id, 'name': name, 'title': title,
                                 'content': content[1:], 'tags': tags_list, 'likes': [], 'comments': []})
            print('\nThe post has been successfully uploaded!')
            break

        except KeyboardInterrupt:
            break


def deletePost(db, user):
    """
    Delete user's text.
    With the post schema, you can remove posts by some conditions that you specify.
    """

    """
    Sometimes, users make a mistake to insert or delete their text.
    We recommend that you write the double-checking code to avoid the mistakes.
    """
    while True:
        try:
            id = user['id']
            cursor = db.posts.find({'id': id}).sort([('date', pymongo.DESCENDING)])
            if not cursor.count():
                print('\nYou have not uploaded any post!')
                break
            print('\nYour posts are below:\n')
            print('{:^15}{:^20}{:^30}{:^50}'.format('#', 'Date', 'Title', 'Content'))
            num = 1
            post_id_dict = {}
            for doc in cursor:
                _id = doc['_id']
                date = doc['date']
                title_compressed = doc['title'][:20] + '...' if len(doc['title']) > 15 else doc['title']
                content_compressed = doc['content'][:50] + '...' if len(doc['content']) > 20 else doc['content']
                post_id_dict[str(num)] = _id
                print('{:^15}{:^20}{:^30}{:^50}'.format(num, date, title_compressed,
                                                        content_compressed.replace('\n', ' / ')))
                num += 1
            while True:
                demand = input('\nInput # of the post you want to delete: ')
                if demand in post_id_dict.keys():
                    confirm = input('\nAre you serious? [y/any other key]: ')
                    if confirm.lower() == 'y':
                        db.posts.delete_one({'_id': post_id_dict[demand]})
                        print('\nThe post has been successfully deleted!')
                        demand = input('\nDelete more? [y/any other key]: ')
                        if demand.lower() == 'y':
                            continue
                        else:
                            break
                    else:
                        break
                else:
                    print('\nNo such post!')

        except KeyboardInterrupt:
            break


