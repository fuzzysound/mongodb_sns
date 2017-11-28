# a module that updates tag_specific_power and stores it to db

from pymongo import MongoClient
import networkx as nx
from collect_tags import collect_tags

if __name__ == '__main__':

    # connect to mongoDB
    client = MongoClient()
    db = client.lab3

    # update tags collection
    collect_tags(db)

    # create a dictionary for storing tags and their graphs, which represents 'who likes whom'
    graphs_by_tags = {}

    # fill the graphs with all the posts
    posts = db.posts.find()
    for post in posts:
        uploader = post['id']
        likers = post['likes']
        tags = post['tags']
        for tag in tags:
            graphs_by_tags.setdefault(tag, nx.MultiDiGraph()) # create a new graph for the tag if not exists
            for liker in likers:
                graphs_by_tags[tag].add_edge(liker, uploader)

    # compute pagerank for all the graphs and store it to tags collection
    for tag, graph in graphs_by_tags.items():
        power_dict = nx.pagerank_scipy(graph)
        power_sum = sum(power_dict.values())
        for id, power in power_dict.items():
            db.tags.update({'tag': tag}, {'$push': {'tsp': {'id': id, 'power': power / power_sum}}})

