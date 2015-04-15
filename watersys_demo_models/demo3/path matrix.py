def path_matrix(co):
    """A method for creating path matrix of a network given its connectivity matrix"""
    pm = {}
    d = {}
    nodes_list = []
    # Creating a list of all nodes using data in connectivity matrix
    for i in co.keys():
        nodes_list.append(i)
    print "List of nodes: %s" % nodes_list

    def get_connected_nodes_list(node):
        """Creating a list of immediately connected nodes downstream of the given node"""
        l = []
        dic = co["%s" % node]
        ind = [k for k, val in enumerate(dic.values()) if val == 1]
        for m in range(len(ind)):
            l.append(dic.keys()[ind[m]])
        return l
    # Creating a path list for each node
    for node in nodes_list:
        d = {}
        path_list = []
        l = []
        l = ["%s" % node, "%s" %node]
        path_list.append(l)
        counter = 0
        while len(path_list[counter]) > 1:
            lis = path_list[counter]
            for i in range(len(lis)):
                if i != 0 and lis[i] != []:
                    l1 = []
                    l1.append(lis[i])
                    l2 = get_connected_nodes_list(lis[i])
                    for j in l2:
                        l1.append(j)
                    path_list.append(l1)

            counter += 1
        print "Path list for node %s: %s" % (node, path_list)
        print "_______________________________________________"
        # creating path matrix for the given node using its path list
        for lis in path_list:
            if len(lis) > 1:
                for item in lis:
                    d[item] = 1
        # assigning PM(i,j) = 0 for nodes j which are not in the path list for node i
        for i in nodes_list:
            if i not in d.keys():
                d[i] = 0
        # Adding the row of path matrix for the node (in line 19) to the final network path matrix, pm
        pm[node] = d

    return pm

CO = {
"s1":{"s1":0, "s2":0, "s3":0, "j1":1, "j2":0, "j3":0, "d1":0, "d2":0, "end":0},
"s2":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":1, "j3":0, "d1":0, "d2":0, "end":0},
"s3":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":0, "j3":0, "d1":0, "d2":1, "end":0},
"j1":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":1, "j3":1, "d1":0, "d2":0, "end":0},
"j2":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":0, "j3":0, "d1":0, "d2":1, "end":0},
"j3":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":0, "j3":0, "d1":1, "d2":0, "end":0},
"d1":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":0, "j3":0, "d1":0, "d2":0, "end":1},
"d2":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":0, "j3":0, "d1":0, "d2":0, "end":1},
"end":{"s1":0, "s2":0, "s3":0, "j1":0, "j2":0, "j3":0, "d1":0, "d2":0, "end":0}
}

print path_matrix(CO)