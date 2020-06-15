# -*- coding: utf-8 -*-
import time
import networkx as nx
import numpy as np
#paper --> http://www.ru.is/~mmh/papers/WIS_WG.pdf

class WGHeuNode():

    def __init__(self, node_index, weighted_degree):
        self.node_index = node_index
        self.weighted_degree = weighted_degree
        self.is_available = True

    def __lt__(self, other):
         return self.weighted_degree < other.weighted_degree        
        

class WGHeu():

    def solve(
        self, graph, profits
    ):
        """[summary]
        
        Arguments:
            dict_data {[type]} -- [description]
        
        Keyword Arguments:
            time_limit {[type]} -- [description] (default: {None})
            gap {[type]} -- [description] (default: {None})
            verbose {bool} -- [description] (default: {False})
        
        Returns:
            [type] -- [description]
        """
        start = time.time()
        # add vertex weights
        for u in graph:
            graph.nodes[u]['weight'] = profits[u]

        #compute the adjacency matrix
        adj_0 = nx.adj_matrix(graph).todense()
        #pesi cambiati di segno
        a = -np.array([graph.nodes[u]['weight'] for u in graph.nodes])
        IS = -np.ones(adj_0.shape[0])
        while np.any(IS==-1):
            #fancy indexing https://www.python-course.eu/numpy_masking.php
            rem_vector = IS == -1
            adj = adj_0.copy()
            #reduce the adj matrix only to the remainings nodes
            adj = adj[rem_vector, :] 
            adj = adj[:, rem_vector]

            u = np.argmin(a[rem_vector].dot(adj!=0)/a[rem_vector]) #selects a minimum weighted degree vertex (see the paper for the def)
            n_IS = -np.ones(adj.shape[0])
            n_IS[u] = 1 #choose the node
            neighbors = np.argwhere(adj[u,:]!=0) #find neighbors and excludes them from the solution
            if neighbors.shape[0]:
                n_IS[neighbors] = 0
            IS[rem_vector] = n_IS #update the indipendent set
        end = time.time()
        of = np.array([graph.nodes[u]['weight'] for u in graph.nodes]).dot(IS)
        return of, IS.tolist(), end - start,

    def solveOptimized(
        self, graph, profits
    ):
        """[summary]
        
        Arguments:
            dict_data {[type]} -- [description]
        
        Keyword Arguments:
            time_limit {[type]} -- [description] (default: {None})
            gap {[type]} -- [description] (default: {None})
            verbose {bool} -- [description] (default: {False})
        
        Returns:
            [type] -- [description]
        """
        start = time.time()
        # add vertex weights
        for u in graph:
            graph.nodes[u]['weight'] = profits[u]

        #compute the adjacency matrix
        adj_0 = nx.adj_matrix(graph).todense()

        IS = -np.ones(adj_0.shape[0])

        #pesi cambiati di segno
        weights = np.array([graph.nodes[u]['weight'] for u in graph.nodes])
        weighted_degrees = weights.dot(adj_0!=0)/weights
        wgnodes = []
        for i in range(len(graph.nodes)):
            wgnodes.append(WGHeuNode(i, weighted_degrees[0,i]))
        wgnodes.sort()

        wgnode_index = 0

        while np.any(IS==-1):
            selected_node = wgnodes[wgnode_index]
            selected_node_index = selected_node.node_index      
            if IS[selected_node_index] != -1:
                wgnode_index = wgnode_index + 1
                continue                          
            IS[selected_node_index] = 1 #choose the node
            neighbors = np.argwhere(adj_0[selected_node_index,:]!=0) #find neighbors and excludes them from the solution
            if neighbors.shape[0]:
                IS[neighbors] = 0
            wgnode_index = wgnode_index + 1
        end = time.time()
        of = np.array([graph.nodes[u]['weight'] for u in graph.nodes]).dot(IS)
        return of, IS.tolist(), end - start,        


