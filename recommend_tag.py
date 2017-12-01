# a function that returns tag recommendation by finding similar tags in db

from difflib import get_close_matches

def recommend_tag(db, tags):

    tags_dict = {}
    for doc in db.tags.find():

        tags_dict[doc['tag']] = doc['count']

    tags_list = list(tags_dict.keys())

    recommendation_dict = {}

    for tag in tags:

        recommendations = get_close_matches(tag, tags_list)

        for recommendation in recommendations:
            if recommendation == tag:
                recommendations.remove(recommendation)

        for i in range(len(recommendations)):
            tag_a = recommendations[i]
            for j in range(i+1, len(recommendations)):
                tag_b = recommendations[j]
                if get_close_matches(tag_a, [tag_b]):
                    loser = max([tag_a, tag_b], key=lambda x: tags_dict[x])
                    recommendations.remove(loser)

        if recommendations:
            recommendation_dict[tag] = recommendations


    if recommendation_dict:
        print("""
Some of your tags are replaceable with more popular ones.
Using popular tags, you'll get more accurate exploration results.
Select one of those if you want to change your tag, or just type '!no'.""")
        changes_dict = {}
        for tag, recommendations in recommendation_dict.items():
            change = input('Your tag: {0}, Recommendations: {1} -> Change: '.format(tag, ', '.join(recommendations)))
            if change != '!no':
                changes_dict[tag] = change

        return changes_dict

    else:
        return