# a function that collects all the tags and their frequencies

def collect_tags(db):

    # create a dictionary for storing tags
    tags_dict = {}

    # collect tags in user profiles
    for user in db.userdb.find():
        interests = user['interest']
        for interest in interests:
            tags_dict[interest] = tags_dict.get(interest, 0) + 1

    # collect tags in posts
    for post in db.posts.find():
        tags = post['tags']
        for tag in tags:
            tags_dict[tag] = tags_dict.get(tag, 0) + 1

    # reset tags collection
    db.tags.drop()

    # insert tags and their freqs into tags collection
    for tag, count in tags_dict.items():
        db.tags.insert_one({'tag': tag, 'count': count, 'tsp': []})

