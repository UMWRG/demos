#  (c) Copyright 2015, University of Manchester
#
#  This file is part of the Pyomo Plugin Demo Suite.
#
#  The Pyomo Plugin Demo Suite is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  The Pyomo Plugin Demo Suite is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with the Pyomo Plugin Demo Suite.  If not, see <http://www.gnu.org/licenses/>.


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
model.river_section= Set(within=model.nodes*model.nodes)
model.demand_nodes = Set()
model.nonstorage_nodes = Set()
model.junction=Set()
model.urban=Set()
model.agricultural=Set()
model.discharge=Set()

# Declaring model parameters
model.consumption_coefficient_agricultural = Param(model.agricultural)
model.consumption_coefficient_urban = Param(model.urban)

model.cost_river_section = Param(model.river_section)
model.inflow_junction = Param(model.junction)
model.flow_multiplier_river_section = Param(model.river_section)
model.min_flow_river_section = Param(model.river_section)
model.max_flow_river_section = Param(model.river_section)

# Defining the flow lower and upper bound
def capacity_constraint(model, node, node2):
    return (model.min_flow_river_section[node,node2], model.max_flow_river_section[node, node2])

# Declaring decision variable X
model.X = Var(model.river_section, domain=NonNegativeReals, bounds=capacity_constraint)

# Declaring the objective function Z
def objective_function(model):
    return summation(model.cost_river_section, model.X)

model.Z = Objective(rule=objective_function, sense=minimize)

# Declaring constraints

def flow_mass_balance(model, nonstorage_nodes):
    
    # inflow
    term1 = model.inflow_junction[nonstorage_nodes]
    term2 = sum([model.X[node_in,nonstorage_nodes]*model.flow_multiplier_river_section[node_in,nonstorage_nodes]
                  for node_in in model.nodes if (node_in, nonstorage_nodes) in model.river_section])

    # outflow
    term3 = model.consumption_coefficient[nonstorage_nodes] \
        * sum([model.X[node_in, nonstorage_nodes]*model.flow_multiplier_river_section[node_in, nonstorage_nodes]
               for node_in in model.nodes if (node_in, nonstorage_nodes) in model.river_section])
    term4 = sum([model.X[nonstorage_nodes, node_out]
               for node_out in model.nodes if (nonstorage_nodes, node_out) in model.river_section])
    
    # inflow - outflow = 0:
    return (term1 + term2) - (term3 + term4) == 0
    
model.flow_mass_balance_constraint = Constraint(model.nonstorage_nodes, rule=flow_mass_balance)

def run_model (input_data_file):
    list=[]
    insts=[]
    opt = SolverFactory("glpk")
    instance=model.create(input_data_file)
    res = opt.solve(instance)
    instance.load(res)
    list.append(res)
    insts.append(instance)
    print res
    return list, insts

if __name__ == '__main__':
    run_model("Demo1.dat")

