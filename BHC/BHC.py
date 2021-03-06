import numpy as np
import itertools as it
from scipy.special import gamma
from scipy.special import multigammaln

def BHC(data, log_likelihood, alpha):
    """
    Bayesian hierarchical clustering algorithm, direct implementation from paper.
    
    Parameters
    ----------
    data : 2D numpy array
        Data with rows as observations and columns as variables.
    log_likelihood : function
        Function that returns the log marginal likelihood of data in BHC model.
    alpha : float
        Concentration parameter in model.
        
    Returns
    -------
    T_record : list(list(int))
        Cluster structure in each iteration.
    rk_record : list(float)
        Merge probability (rk) in each iteration.
    """
    
    n = data.shape[0]
    p = data.shape[1]
    c = n
    D = dict((index, Node(obs.reshape(-1, p), alpha)) for index, obs in enumerate(data))
    T = list(range(n))
    T_record = list(T)
    rk_record = [1]
    
    while c > 1:
        max_rk = float('-Inf')
        node_merge = None
        left_merge = -1
        right_merge = -1
        
        for i, j in it.combinations(D.keys(), 2):
            Di = D[i]
            Dj = D[j]
            Dk = Node.merge_node(Di, Dj)
            
            likelihood_i = np.exp(log_likelihood(Di.data))
            likelihood_j = np.exp(log_likelihood(Dj.data))
            likelihood_k = np.exp(log_likelihood(Dk.data))
            
            pi_k = Dk.pi_k

            rk = (pi_k * likelihood_k) / (pi_k * likelihood_k + (1 - pi_k) * likelihood_i * likelihood_j)

            if rk > max_rk:
                max_rk = rk
                node_merge = Dk
                left_merge = i
                right_merge = j
        
        #delete merged nodes and store new node
        del D[right_merge]
        D[left_merge] = node_merge

        #store the current tree structure and value of rk
        for item_index, node_index in enumerate(T):
            if node_index == right_merge:
                T[item_index] = left_merge
        T_record.append(list(T))
        rk_record.append(max_rk)
        
        c -= 1
        
    return T_record, rk_record
        

class Node(object):
    """
    Node class used in Bayesian hierarchical clustering algorithm. Main purpose is to store values of dk and pi_k for each node.
    
    Attributes
    ----------
    data : 2D numpy array
        Data with rows as observations and columns as variables.
    dk : float
        Some kind of number for computing probabilities
    pi_k : float
        For to compute merge probability
        
    Methods
    -------
    __init__(self, data, likelihood, alpha = 1)
        Instantiation operation.
    merge_node(cls, node1, node2, alpha = 1)
        Method that merges two Nodes into one new Node and return the new Node.
    """
    
    def __init__(self, data, alpha = 1, dk = 1, pi_k = 1):
        """
        Instantiation operation.
        
        Parameters
        ----------
        data : 2D numpy array
            Data with rows as observations and columns as variables.
        likelihood : function
            Function that returns the likelihood of data, sampling distribution in BHC model.
        alpha : float
            Concentration parameter in model.
        log_dk : float
            Cached probability variable. Do not define if the node is a leaf.
        log_pi : float
            Cached probability variable. Do not define if the node is a leaf.
        """
        
        #initialized according to paper
        self.data = data
        self.dk = dk
        self.pi_k = pi_k

    @classmethod
    def merge_node(cls, node1, node2, alpha = 1):
        """
        Merge two Nodes into one new Node and return the new Node.
        
        Parameters
        ----------
        node1 : Node
            First Node.
        node2 : Node
            Second Node.
        """

        data = np.vstack((node1.data, node2.data))

        nk = data.shape[0]
        dk = alpha * gamma(nk) + node1.dk * node2.dk
        pi_k = alpha * gamma(nk) / dk

        return cls(data, alpha, dk, pi_k)