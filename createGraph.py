from operator import itemgetter, attrgetter
import networkx as nx
import matplotlib.pyplot as plt
import pydot

filepath = '/Users/dmvaldman/Documents/datasets/reddit_votes.csv'

file = open(filepath)

data = []

skip = 80

counter = 1
for line in file:
    if counter % skip == 0:
        data.append(line.strip().split(','))
    if counter > skip*10000:
        break
    counter = counter + 1

#get unique users
users = list(set([row[0] for row in data]))


#create edges
data_sorted_by_link = sorted(data, key=itemgetter(1))

link_dict = {}
linkID_old = ''
counter_redundancy = 0
for row in data_sorted_by_link:
    #initialize new entry in edge dictionary
    if row[1] != linkID_old:
        linkID = row[1]
        link_dict[linkID] = [row[0]]
        linkID_old = linkID
    else:
        link_dict[linkID_old].append(row[0])
        counter_redundancy = counter_redundancy + 1

edges = []
users_connected = []
for link in link_dict:
    shared_users = link_dict[link]
    if len(shared_users) > 1:
        users_connected.append(shared_users)
        edges.append([(user1, user2) for user1 in shared_users for user2 in shared_users if shared_users.index(user1) > shared_users.index(user2)])


users_connected_list = list(set(sum(users_connected,[])))


G = nx.Graph()
G.add_nodes_from(users_connected_list)
G.add_edges_from(sum(edges, []))

#nx.draw(G)
#plt.show()

nx.draw_graphviz(G)
nx.write_dot(G,'reddit.dot')
