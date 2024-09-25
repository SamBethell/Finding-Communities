import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random


class Queue:
    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop(0)

    def empty(self):
        return len(self.queue) == 0

class Dataset:
    def __init__(self, data):
        self.data = data

    def maxpooling(self, data): # data will be list of connected nodes
        max_x = 0
        max_y = 0
        for value in data:
            if value[0] > max_x:
                max_x = value[0]
        for value in data:
            if value[1] > max_y:
                max_y = value[1]
        if max_x > max_y:
            return max_x
        else:
            return max_y

    def find_adj_matrix(self, data): # data will be list of connected nodes
        lim = self.maxpooling(data)
        adj_matrix = array = np.zeros((lim+1, lim+1)) # plus 1 since lim is value of largest entry and range(0, lim) only goes to lim-1
        for item in data:
            adj_matrix[item[0], item[1]] = 1
            adj_matrix[item[1], item[0]] = 1
        return adj_matrix

    def clean(self):
        '''
        Self.data is a dataframe, then transformed to a list.
        For all other functions in Dataset class, cleaned data must be given.
        Returns random 100 entries of the data.
        '''
        connected_nodes = []
        for value in range(0, 100):
            lim = random.randint(0, 1000)
            connected_nodes.append([self.data.node1[lim], self.data.node2[lim]])
        return connected_nodes

class Node:
    '''
    Class for individual nodes in a graph.
    Connections will be given as [0, 1...] which is an entry
    of the adjacency matrix for the entire graph corresponding
    to this node.
    '''
    def __init__(self, value, connections=None):
        self.connections = connections
        self.value = value
    def get_neighbours(self):
        return np.where(np.array(self.connections) == 1)[0]



class Network:
    '''
    Adjacency matrix given from dataset.
    Each node will be class Node() and its connections
    will be given from the nth entry of self.adjacency matrix
    '''
    def __init__(self, nodes, adjacency_matrix): # node must be given as a list
        self.nodes = nodes # each node will be 'class Node()'
        self.adjacency_matrix = adjacency_matrix

    def sorting(self, lst):
        for i in lst:
            for j in lst:
                if lst[i] > lst[j]:
                    lst[i], lst[j] = lst[j], lst[i]
        return list

    def sorting_two_lists(self, list1, list2):
        '''
        Will sort list 1 in order of smallest to largest
        Will then sort list two according to the changes made
        in list one
        Returns lists
        '''
        sorted_list2 = []
        list1_copy = list1
        sorted_list1 = self.sorting(list1)
        for index_1 in range(0, len(list1)):
            for index_2 in range(0, len(list1)):
                if sorted_list1[index_1] == list1_copy[index_2]:
                    sorted_list2[index_2] == list2[index_1]

        return sorted_list1, sorted_list2

    def breath_first_search(self, node1, node2):
        search_queue = Queue()
        visited = []
        goal = node2
        start = node1
        search_queue.push(goal)
        visited.append(goal)
        while not search_queue.empty():
            node_to_check = search_queue.pop()
            if node_to_check == goal:
                break
            for neighbour_index in node_to_check.get_neighbours():
                neighbour = self.nodes[neighbour_index]
                if neighbour_index not in visited:
                    self.search_queue.push(neighbour)
                    visited.append(neighbour_index)
                    neighbour.parent = node_to_check
        route = 0
        if node_to_check == self.goal:
            self.start_node.parent = None
            while node_to_check.parent:  # to back propagate until node has no parent which represents start node
                node_to_check = node_to_check.parent
                route += 1
        return route

    def degree_centrality(self):
        centrality = []
        for node in self.nodes:
            degree = 0
            for value in node.connections:
                if value == 1:
                    degree += 1
            centrality.append(degree/99) # degree(v)/n-1 where n is 100

    def betweenness_centrality(self):
        totals = []
        for node1 in self.nodes:
            path_lengths = []
            for node2 in self.nodes:
                if node1 == node2:
                    continue
                else:
                    path_lengths.append(self.breath_first_search(node1, node2))
            path_lengths = self.sorting(path_lengths)
            smallest_value = path_lengths[0]
            total = 0
            for value in path_lengths:
                if value == smallest_value:
                    total += 1
            totals.append(total)
        return totals

    def closeness_centrality(self):
        sums = []
        shortest_paths = []
        for u in self.nodes:
            uv_path = []
            for v in self.nodes:
                if u == v:
                    continue
                else:
                    uv_path.append(self.breath_first_search(u, v))
                    shortest_paths.append([uv_path])
        for item in shortest_paths:
            sums.append(sum(item))
        return 1/(sum(sums))

    def display(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_axis_off()
        num_nodes = len(self.nodes)
        network_radius = num_nodes*10
        ax.set_xlim([-1.1 * network_radius, 1.1 * network_radius])
        ax.set_ylim([-1.1 * network_radius, 1.1 * network_radius])
        for i, node in enumerate(self.nodes):
            node_angle = i*2*np.pi / num_nodes
            node_x = network_radius * np.cos(node_angle)
            node_y = network_radius * np.sin(node_angle)
            circle = plt.Circle((node_x, node_y), num_nodes, color=cm.hot(node.value))
            ax.add_patch(circle)
            for neighbour_index in range(i+1, num_nodes):
                if node.connections[neighbour_index] == 1:
                    neighbour_angle = neighbour_index * 2 * np.pi / num_nodes
                    neighbour_x = network_radius * np.cos(neighbour_angle)
                    neighbour_y = network_radius * np.sin(neighbour_angle)
                    ax.plot((node_x, neighbour_x), (node_y, neighbour_y), color='black')
        plt.show()

    def creating_networks(self, file_path):
        df = pd.read_csv(file_path, sep=' ', names=['node1', 'node2'])
        data = Dataset(df)
        cleaned_data = data.clean()
        adj_matrix = data.find_adj_matrix(cleaned_data)

        self.nodes = []
        for i, value in enumerate(adj_matrix):
            self.nodes.append(Node(i, value))

        network = Network(self.nodes, adj_matrix)
        network.display()
def main():
    file_path = "C:/Users/samue/python/SocialNetworkAnalysis/facebook_combined.txt.gz"
    pass # TBD

if __name__ == "__main__":
    main()