
#    (c) Copyright 2014, University of Manchester
#
#    This file is part of WaterSys.
#
#    WaterSys is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WaterSys is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WaterSys.  If not, see <http://www.gnu.org/licenses/>.

from watersys import Network


class Demo3Network(Network):
    type = 'network'
    _properties = dict(
        predicted_rainfall={},
        rainfall=0,
    )

    def set_initial_storage(self, storage):
        for node in self.nodes:
            if node.type == 'surface reservoir' and node.type == 'aquifer storage':
                    node.initial_storage = storage[node.name]

    def path_matrix(self, co):
        """A method for creating path matrix of a network given its connectivity matrix"""
        self.pm = {}
        d = {}
        self.nodes_list = []
        self.co = co
        # Creating a list of all nodes using data in connectivity matrix
        for i in self.co.keys():
            self.nodes_list.append(i)

        def get_connected_nodes_list(node):
            """Creating a list of immediately connected nodes downstream of the given node"""
            l = []
            dic = co["%s" % node]
            ind = [k for k, val in enumerate(dic.values()) if val == 1]
            for m in range(len(ind)):
                l.append(dic.keys()[ind[m]])
            return l
        # Creating a path list for each node
        for node in self.nodes_list:
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
            # creating path matrix for the given node using its path list
            for lis in path_list:
                if len(lis) > 1:
                    for item in lis:
                        d[item] = 1
            # assigning PM(i,j) = 0 for nodes j which are not in the path list for node i
            for i in self.nodes_list:
                if i not in d.keys():
                    d[i] = 0
            # Adding the row of path matrix for the node (in line 19) to the final network path matrix, pm
            self.pm[node] = d
        return self.pm