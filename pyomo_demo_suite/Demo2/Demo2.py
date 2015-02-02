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
model.storage_nodes = Set()
model.time_step = Set()

# Declaring model parameters
model.inflow = Param(model.nodes, model.time_step)
model.current_time_step = Set()
model.consumption_coefficient = Param(model.nodes, model.time_step)
model.initial_storage = Param(model.storage_nodes, mutable=True)
model.cost = Param(model.links, model.time_step)
model.flow_multiplier = Param(model.links, model.time_step)
model.flow_lower_bound = Param(model.links, model.time_step)
model.flow_upper_bound = Param(model.links, model.time_step)
model.storage_lower_bound = Param(model.storage_nodes, model.time_step)
model.storage_upper_bound = Param(model.storage_nodes, model.time_step)


##======================================== Declaring Variables (X and S)

# Defining the flow lower and upper bound
def flow_capacity_constraint(model, node, node2):
    return (model.flow_lower_bound[node, node2, model.current_time_step], model.flow_upper_bound[node, node2, model.current_time_step])

# Defining the storage lower and upper bound
def storage_capacity_constraint(model, storage_nodes):
    return (model.storage_lower_bound[storage_nodes, model.current_time_step], model.storage_upper_bound[storage_nodes, model.current_time_step])

# Declaring decision variable X
model.X = Var(model.links, domain=NonNegativeReals, bounds=flow_capacity_constraint)

# Declaring state variable S
model.S = Var(model.storage_nodes, domain=NonNegativeReals, bounds=storage_capacity_constraint)

def get_current_cost(model):
    current_cost= {}
    for link in model.links:
        print link
        current_cost[link]= model.cost[link, model.current_time_step]
    return current_cost#model.cost [model.current_time_step]

def objective_function(model):
    return summation(get_current_cost(model), model.X)

model.Z = Objective(rule=objective_function, sense=minimize)

##======================================== Declaring constraints
# Mass balance for non-storage nodes:

def mass_balance(model, nonstorage_nodes):
    # inflow
    term1 = model.inflow[nonstorage_nodes, model.current_time_step]
    term2 = sum([model.X[node_in, nonstorage_nodes]*model.flow_multiplier[node_in, nonstorage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])
    # outflow
    term3 = model.consumption_coefficient[nonstorage_nodes, model.current_time_step] \
        * sum([model.X[node_in, nonstorage_nodes]*model.flow_multiplier[node_in, nonstorage_nodes, model.current_time_step]
               for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])
    term4 = sum([model.X[nonstorage_nodes, node_out]
                  for node_out in model.nodes if (nonstorage_nodes, node_out) in model.links])

    # inflow - outflow = 0:
    return (term1 + term2) - (term3 + term4) == 0

model.mass_balance_const = Constraint(model.nonstorage_nodes, rule=mass_balance)

# Mass balance for storage nodes:
def storage_mass_balance(model, storage_nodes):
    # inflow
    term1 = model.inflow[storage_nodes, model.current_time_step]
    term2 = sum([model.X[node_in, storage_nodes]*model.flow_multiplier[node_in, storage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, storage_nodes) in model.links])

    # outflow
    term3 = sum([model.X[storage_nodes, node_out]
                  for node_out in model.nodes if (storage_nodes, node_out) in model.links])

    # storage
    term4 = model.initial_storage[storage_nodes]
    term5 = model.S[storage_nodes]
    # inflow - outflow = 0:
    return (term1 + term2 + term4) - (term3 + term5) == 0

model.storage_mass_balance_const = Constraint(model.storage_nodes, rule=storage_mass_balance)

def get_storage(instance):
    storage={}
    for var in instance.active_components(Var):
            if(var=="S"):
                s_var = getattr(instance, var)
                for vv in s_var:
                    name= ''.join(map(str,vv))
                    storage[name]=(s_var[vv].value)
    return storage

def set_initial_storage(instance, storage):
    for var in instance.active_components(Param):
            if(var=="initial_storage"):
                s_var = getattr(instance, var)
                for vv in s_var:
                    s_var[vv]=storage[vv]

##======================== running the model in a loop for each time step
if __name__ == '__main__':
    print "Test the result"
    opt = SolverFactory("glpk")
    list=[]
    list_=[]
    model.current_time_step.add(1)
    instance=model.create("Demo2.dat")
    ## determine the time steps
    for comp in instance.active_components():
        if(comp=="time_step"):
            parmobject = getattr(instance, comp)
            for vv in parmobject.value:
                list_.append(vv)
    #instance =model.create("Demo2.dat")
    storage={}
    for vv in list_:
        ##################
        model.current_time_step.clear()
        model.preprocess()
        model.current_time_step.add(vv)
        model.preprocess()
        instance=model.create("Demo2.dat")
        ##update intial storage value from previous storage
        if(len(storage)>0):
            set_initial_storage(instance, storage)
            model.preprocess()
            instance.preprocess()
        res=opt.solve(instance)
        instance.load(res)
        storage=get_storage(instance)
        list.append(res)
        ####################

    for res in list:
        print res
