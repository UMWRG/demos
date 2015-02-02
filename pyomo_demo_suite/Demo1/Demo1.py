#  (c) Copyright 2015, University of Manchester
#
#  This file is part of the GAMS Plugin Demo Suite.
#
#  The GAMS Plugin Demo Suite is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  The GAMS Plugin Demo Suite is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with the GAMS Plugin Demo Suite.  If not, see <http://www.gnu.org/licenses/>.

# Demo1.py
#Version: no time-step
#Author: Majed Khadem

# Importing needed Packages
from pyomo.environ import *

from pyomo.opt import SolverFactory

# Declaring the model
model = AbstractModel()

# Declaring model indexes using sets
model.nodes = Set()
model.links = Set(within=model.nodes*model.nodes)
model.demand_nodes = Set()
model.nonstorage_nodes = Set()

# Declaring model parameters
model.consumption_coefficient = Param(model.nodes)
model.cost = Param(model.links)
model.inflow = Param(model.nodes)
model.flow_multiplier = Param(model.links)
model.lower_bound = Param(model.links)
model.upper_bound = Param(model.links)

# Defining the flow lower and upper bound
def capacity_constraint(model, node, node2):
    return (model.lower_bound[node,node2], model.upper_bound[node, node2])

# Declaring decision variable X
model.X = Var(model.links, domain=NonNegativeReals, bounds=capacity_constraint)

# Declaring the objective function Z
def objective_function(model):
    return summation(model.cost, model.X)

model.Z = Objective(rule=objective_function, sense=minimize)

# Declaring constraints

def flow_mass_balance(model, nonstorage_nodes):
    
    # inflow
    term1 = model.inflow[nonstorage_nodes]
    term2 = sum([model.X[node_in,nonstorage_nodes]*model.flow_multiplier[node_in,nonstorage_nodes]
                  for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])

    # outflow
    term3 = model.consumption_coefficient[nonstorage_nodes] \
        * sum([model.X[node_in, nonstorage_nodes]*model.flow_multiplier[node_in, nonstorage_nodes]
               for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])
    term4 = sum([model.X[nonstorage_nodes, node_out]
               for node_out in model.nodes if (nonstorage_nodes, node_out) in model.links])
    
    # inflow - outflow = 0:
    return (term1 + term2) - (term3 + term4) == 0
    
model.flow_mass_balance_constraint = Constraint(model.nonstorage_nodes, rule=flow_mass_balance)

if __name__ == '__main__':
    opt = SolverFactory("glpk")
    instance=model.create("Demo1.dat")
    res = opt.solve(instance)
    print res
#    instance.pprint()
