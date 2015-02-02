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

from pyomo.environ import *

from pyomo.opt import SolverFactory

# Declaring the model
model = AbstractModel()
# Declaring model indexes using sets
model.nodes = Set()
model.links = Set(within=model.nodes*model.nodes)
model.demand_nodes = Set()
model.non_storage_nodes = Set()
model.storage_nodes = Set()
model.time_step = Set()

# Declaring model parameters
model.inflow = Param(model.nodes, model.time_step, default=0)
model.current_time_step = Set()
model.initial_storage = Param(model.storage_nodes, mutable=True)
model.cost = Param(model.demand_nodes, model.time_step, default=0)
model.flow_multiplier = Param(model.links, model.time_step)
model.min_flow = Param(model.links, model.time_step)
model.max_flow = Param(model.links, model.time_step)
model.min_storage = Param(model.storage_nodes, model.time_step)
model.max_storage = Param(model.storage_nodes, model.time_step)
model.demand = Param(model.demand_nodes, model.time_step, default=0)

##======================================== Declaring Variables (X and S)

# Defining the flow lower and upper bound
def flow_capacity_constraint(model, node, node2):
    return (model.min_flow[node, node2, model.current_time_step], model.max_flow[node, node2, model.current_time_step])

# Defining the storage lower and upper bound
def  storage_capacity_constraint(model, storage_nodes):
    return (model.min_storage[storage_nodes, model.current_time_step], model.max_storage[storage_nodes, model.current_time_step])

# Declaring decision variable X
# Declaring decision variable X
model.Q = Var(model.links, domain=NonNegativeReals, bounds=flow_capacity_constraint) #*1e6 m^3 mon^-1

# Declaring state variable S
model.S = Var(model.storage_nodes, bounds=storage_capacity_constraint) #1e6 m^3

def alpha_bound(model):
    return 0, 1#, model.alpha, 1

model.alpha = Var(model.demand_nodes, bounds=alpha_bound) #*%

# Declaring variable alpha
demand_satisfaction_ratio_bound = Constraint(rule=alpha_bound)

"""
def demand_satisfaction_ratio(model, demand_nodes):
            alpha = (sum([model.X[node_in, demand_nodes]*model.flow_multiplier[node_in, demand_nodes]
                          for node_in in model.nodes if (node_in, demand_nodes) in model.links]) - sum([model.X[demand_nodes, node_out]
                          for node_out in model.nodes if (demand_nodes, node_out) in model.links]))/model.targert_demand[demand_nodes]
            return (0, alpha, 1)
"""

def get_current_cost(model):
    current_cost = {}
    for node in model.demand_nodes:
        #print link
        current_cost[node] = model.cost[node, model.current_time_step]
    return current_cost  # model.cost [model.current_time_step]

def objective_function(model):
    return summation(get_current_cost(model), model.alpha)

model.Z = Objective(rule=objective_function, sense=maximize) #*Z_Unit

##======================================== Declaring constraints
# Mass balance for non-storage nodes:

def mass_balance(model, nonstorage_nodes):
    # inflow
    term1 = model.inflow[nonstorage_nodes, model.current_time_step]
    term2 = sum([model.Q[node_in, nonstorage_nodes]*model.flow_multiplier[node_in, nonstorage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])
    # outflow
    if nonstorage_nodes in model.demand_nodes:
        term3 = model.alpha[nonstorage_nodes] * model.demand[nonstorage_nodes, model.current_time_step]
    else:
        term3 = 0

    term4 = sum([model.Q[nonstorage_nodes, node_out]
                  for node_out in model.nodes if (nonstorage_nodes, node_out) in model.links])

    # inflow - outflow = 0:
    return (term1 + term2) - (term3 + term4) == 0

model.mass_balance_const = Constraint(model.non_storage_nodes, rule=mass_balance)

# Mass balance for storage nodes:
def storage_mass_balance(model, storage_nodes):
    # inflow
    term1 = model.inflow[storage_nodes, model.current_time_step]
    term2 = sum([model.Q[node_in, storage_nodes]*model.flow_multiplier[node_in, storage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, storage_nodes) in model.links])

    # outflow
    term3 = sum([model.Q[storage_nodes, node_out]
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
                    s_var[vv] = storage[vv]

def run_model(datafile):
    print "==== Running the model ===="
    opt = SolverFactory("glpk")
    list=[]
    list_=[]
    model.current_time_step.add(1)
    instance=model.create(datafile)
    #"""
    ## determine the time steps
    for comp in instance.active_components():
        if(comp=="time_step"):
            parmobject = getattr(instance, comp)
            for vv in parmobject.value:
                list_.append(vv)
    storage = {}
    insts=[]
    for vv in list_:
        ##################
        model.current_time_step.clear()
        model.preprocess()
        model.current_time_step.add(vv)
        model.preprocess()
        print "Running for time step: ", vv
        instance=model.create(datafile)
        ##update intial storage value from previous storage
        if len(storage) > 0:
            set_initial_storage(instance, storage)
            model.preprocess()
            instance.preprocess()
    #"""
        res=opt.solve(instance)
        instance.load(res)
        insts.append(instance)
        storage=get_storage(instance)
        list.append(res)
    #print "This is the list:", list
        ####################
    count=1
    for res in list:
        print " ========= Time step:  %s =========="%count
        print res
        count+=1
    count=1
    for inst in insts:
        print " ========= Time step:  %s =========="%count
        display_variables(inst)
        count+=1
    return list, insts

def display_variables (instance):
    for var in instance.active_components(Var):
            s_var = getattr(instance, var)
            print "=================="
            print "Variable: %s"%s_var
            print "=================="
            for vv in s_var:
                if len(vv) ==2:
                    name="[" + ', '.join(map(str,vv)) + "]"
                else:
                    name= ''.join(map(str,vv))
                print name,": ",(s_var[vv].value)

##========================
# running the model in a loop for each time step
if __name__ == '__main__':
    run_model("Demo3.dat")
    #run_model("input.dat")
