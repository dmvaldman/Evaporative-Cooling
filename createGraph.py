from operator import itemgetter, attrgetter
import networkx as nx
import matplotlib.pyplot as plt
import pydot

filepath = 'dataset/reddit_votes.csv'   #location of reddit data dump
nRows = 10000                           #first rows of dataset to process
nSkip = 100                             #skip every nSkip row of dataset

#create subset of dataset and load it into 'data'
data = []

counter = 1
for line in open(filepath, 'r'):
    if counter % nSkip == 0:
        data.append(line.strip().split(','))
    if counter > nSkip*nRows:
        break
    counter += 1

#get all unique users
users_all = list(set([row[0] for row in data]))


#create edges
data_sorted_by_link = sorted(data, key=itemgetter(1))

#create dictionary of link : [users who upvoted the link]
link_dict = {}
linkID_old = ''
for row in data_sorted_by_link:
    #initialize new entry in dictionary
    if row[1] != linkID_old:                    #if new link
        linkID = row[1]                         #get link name
        link_dict[linkID] = [row[0]]            #create entry of dictionary
        linkID_old = linkID
    else:                                       #if old link
        link_dict[linkID_old].append(row[0])    #append new user to list


#create graph structure of nodes (connected users) and edges (shared liked articles)
edges = []
nodes = []
for link in link_dict:
    shared_users = link_dict[link]
    #check if link has more than one user who upvoted it
    if len(shared_users) > 1:
        nodes.append(shared_users)
        edges.append([(user1, user2) for user1 in shared_users for user2 in shared_users if shared_users.index(user1) > shared_users.index(user2)])

#flatten the connected user list
nodes = list(set(sum(nodes,[])))

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(sum(edges, []))

#drawing the graph
#nx.draw_graphviz(G)
#nx.write_dot(G,'reddit.dot')
