import pymongo
from datetime import datetime, timedelta
from wall import show_post, write_comment

def explore(db, user):
    """
    Explore posts with tags in which the user is interested.
    The posts are shown ordered by tag-specific power of the post uploader.
    Posts of recent 7 days are displayed prior to others.
    """
    while True:
        try:
            first_flag = True
            target_tags = user['interest']
            users_tsp = {}
            for tag in target_tags:
                users_tsp.setdefault(tag, [])
                tag_doc = db.tags.find_one({'tag': tag})
                for doc in tag_doc['tsp']:
                    users_tsp[tag].append({'id': doc['id'], 'power': doc['power']})

            while True:

                docs_with_target_tags = {}

                if first_flag:
                    base_date = datetime.now()
                    storage = {}
                    cursors = {}
                    for tag in target_tags:
                        cursors[tag] = db.posts.find({'tags': tag}).sort([('date', pymongo.DESCENDING)])

                else:

                    base_date = base_date - timedelta(days=7)
                    for tag, doc in storage.copy().items():
                        docs_with_target_tags.setdefault(tag, [])
                        doc_date = datetime.strptime(doc['date'], '%Y-%m-%d %H:%M:%S')
                        if base_date - timedelta(days=7) <= doc_date < base_date:
                            docs_with_target_tags[tag].append(doc)
                            del storage[tag]

                for tag, cursor in cursors.items():
                    docs_with_target_tags.setdefault(tag, [])
                    for doc in cursor:
                        doc_date = datetime.strptime(doc['date'], '%Y-%m-%d %H:%M:%S')
                        if base_date - timedelta(days=7) <= doc_date < base_date:
                            docs_with_target_tags[tag].append(doc)
                        else:
                            storage[tag] = doc
                            break

                if docs_with_target_tags:
                    all_docs = {}
                    for tag, docs in docs_with_target_tags.items():
                        for doc in docs:
                            uploader_id = doc['id']
                            users_tsp_cursor = (doc for doc in users_tsp[tag] if doc['id'] == uploader_id)
                            temp_key = str(doc)
                            all_docs[temp_key] = (doc, max(all_docs.get(temp_key, 0), next(users_tsp_cursor)['power']))
                    if all_docs:
                        all_docs_sorted = sorted(list(zip(*all_docs.values()))[0], key=lambda x: all_docs[str(x)][1], reverse=True)
                    else:
                        all_docs_sorted = {}

                    for doc in all_docs_sorted:
                        if doc['id'] != user['id']:
                            show_post(doc)

                        while True:
                            if user['id'] in doc['likes']:
                                liked = True
                                demand = input('\nWhat do you want to do? [next/comment/undo like/skip7days]: ')
                            else:
                                liked = False
                                demand = input('\nWhat do you want to do? [next/comment/like/skip7days]: ')

                            if demand.lower() in ['next', 'comment', 'undo like', 'like', 'skip7days']:
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
                            db.posts.update({'_id': doc['_id']}, {'$pull': {'likes': user['id']}})
                            print('\nUndid like it!')
                            continue
                        elif demand.lower() == 'like':
                            db.posts.update({'_id': doc['_id']}, {'$push': {'likes': user['id']}})
                            print('\nLiked it!')
                            continue
                        else:
                            break

                    else:
                        print('\nShowing posts of next 7 days...')

                first_flag = False

                if not storage and not sum([cursor.alive for cursor in cursors.values()]):
                    print('\nNo more post!')
                    break

            break

        except KeyboardInterrupt:
            break



