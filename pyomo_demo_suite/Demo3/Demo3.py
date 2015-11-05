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
model.treatment_hydro_nodes = Set()
model.hydro_nodes = Set()

# Declaring model parameters
model.inflow = Param(model.nodes, model.time_step, default=0)
model.current_time_step = Set()
model.initial_storage = Param(model.storage_nodes, mutable=True)
model.priority = Param(model.demand_nodes, model.time_step, default=0)
model.flow_multiplier = Param(model.links, model.time_step)
model.min_flow = Param(model.links, model.time_step)
model.max_flow = Param(model.links, model.time_step)
model.min_storage = Param(model.nodes, model.time_step)
model.max_storage = Param(model.nodes, model.time_step)
model.demand = Param(model.demand_nodes, model.time_step, default=0)
model.percent_loss = Param(model.treatment_hydro_nodes, model.time_step)
model.net_head = Param(model.hydro_nodes)
model.unit_price = Param(model.hydro_nodes)
##======================================== Declaring Variables (X and S)

# Defining the flow lower and upper bound
def flow_capacity_constraint(model, node, node2):
    return model.min_flow[node, node2, model.current_time_step], model.max_flow[node, node2, model.current_time_step]

# Defining the storage lower and upper bound
def storage_capacity_constraint(model, storage_nodes):
    return model.min_storage[storage_nodes, model.current_time_step], model.max_storage[storage_nodes, model.current_time_step]

# Declaring decision variable X

model.Flow = Var(model.links, domain=NonNegativeReals, bounds=flow_capacity_constraint) #*1e6 m^3 mon^-1

# Declaring state variable S
model.Storage = Var(model.storage_nodes, bounds=storage_capacity_constraint) #1e6 m^3

def percent_demand_met_bound(model):
    return 0, 1

model.percent_demand_met = Var(model.demand_nodes, bounds=percent_demand_met_bound) #*%

# Declaring variable alpha
demand_satisfaction_ratio_bound = Constraint(rule=percent_demand_met_bound)

# Defining post process variables
model.Released_Water = Var(model.nodes)
model.Received_Water = Var(model.nodes)
model.Demand_Met = Var(model.demand_nodes)
model.Revenue = Var(model.hydro_nodes)

def get_current_priority(model):
    current_priority = {}
    for node in model.demand_nodes:
        #print link
        current_priority[node] = model.priority[node, model.current_time_step]
    return current_priority  # model.priority [model.current_time_step]

def objective_function(model):
    return summation(get_current_priority(model), model.percent_demand_met)

model.Objective = Objective(rule=objective_function, sense=maximize)

##======================================== Declaring constraints
# Mass balance for non-storage nodes:

def mass_balance(model, non_storage_nodes):
    # inflow
    term1 = model.inflow[non_storage_nodes, model.current_time_step]
    term2 = sum([model.Flow[node_in, non_storage_nodes]*model.flow_multiplier[node_in, non_storage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, non_storage_nodes) in model.links])

    if non_storage_nodes in model.treatment_hydro_nodes:
        term22 = model.percent_loss[non_storage_nodes, model.current_time_step]
    else:
        term22 = 0

    # outflow

    if non_storage_nodes in model.demand_nodes:
        term3 = model.percent_demand_met[non_storage_nodes] * model.demand[non_storage_nodes, model.current_time_step]
    else:
        term3 = 0

    term4 = sum([model.Flow[non_storage_nodes, node_out]
                  for node_out in model.nodes if (non_storage_nodes, node_out) in model.links])

    # inflow - outflow = 0:
    return (term1 + (1-term22) * term2) - (term3 + term4) == 0

model.mass_balance_const = Constraint(model.non_storage_nodes, rule=mass_balance)

# Mass balance for storage nodes:
def storage_mass_balance(model, storage_nodes):
    # inflow
    term1 = model.inflow[storage_nodes, model.current_time_step]
    term2 = sum([model.Flow[node_in, storage_nodes]*model.flow_multiplier[node_in, storage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, storage_nodes) in model.links])
    if storage_nodes in model.treatment_hydro_nodes:
        term22 = model.percent_loss[storage_nodes, model.current_time_step]
    else:
        term22 = 0

    # outflow
    term3 = sum([model.Flow[storage_nodes, node_out]
                  for node_out in model.nodes if (storage_nodes, node_out) in model.links])

    # storage
    term4 = model.initial_storage[storage_nodes]
    term5 = model.Storage[storage_nodes]
    # inflow - outflow = 0:
    return (term1 + (1-term22) * term2 + term4) - (term3 + term5) == 0

model.storage_mass_balance_const = Constraint(model.storage_nodes, rule=storage_mass_balance)

# Storage capacity constraint for Hydro-power and Treatment nodes

def hydro_treatment_capacity(model, treatment_hydro_nodes):
    return 0 <= sum([model.Flow[node_in, treatment_hydro_nodes]*model.flow_multiplier[node_in, treatment_hydro_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, treatment_hydro_nodes) in model.links]) <= model.max_storage[treatment_hydro_nodes, model.current_time_step]

model.hydro_treatment_capacity_constraint = Constraint(model.treatment_hydro_nodes, rule=hydro_treatment_capacity)

def released(instance):
    released_water = {}
    for i in instance.nodes:
        released_water[i] = sum([instance.Flow[i, node_out].value for node_out in instance.nodes if (i, node_out) in instance.links])
    return released_water


def received(instance):
    received_water = {}
    for i in instance.nodes:
        received_water[i] = sum([instance.flow_multiplier[node_in, i, instance.current_time_step]*instance.Flow[node_in, i].value for node_in in instance.nodes if (node_in, i) in instance.links])
    return received_water


def demand_met(instance):
    dem_met = {}
    incoming = received(instance)
    outgoing = released(instance)
    model.dem_met = {}
    for i in instance.demand_nodes:
        dem_met[i] = incoming[i] - outgoing[i]
    return dem_met


def revenue(instance):
    rev = {}
    incoming = received(instance)
    for i in instance.hydro_nodes:
        rev[i] = (1-instance.percent_loss[i, instance.current_time_step])*incoming[i]*9.81*24*0.3858*instance.net_head[i]*instance.unit_price[i]
    return rev


def get_storage(instance):
    storage_levels={}
    for var in instance.component_objects(Var):
            if str(var)=="Storage":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    name = ''.join(map(str,vv))
                    storage_levels[name]=(s_var[vv].value)
    return storage_levels


def set_initial_storage(instance, storage_levels):
    for var in instance.component_objects(Param):
            if str(var) == "initial_storage":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = storage_levels[vv]


def set_post_process_variables(instance):
    for var in instance.component_objects(Var):
            if str(var) == "Released_Water":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = released(instance)[vv]
            if str(var) == "Received_Water":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = received(instance)[vv]
            if str(var) == "Demand_Met":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = demand_met(instance)[vv]
            if str(var) == "Revenue":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = revenue(instance)[vv]


def run_model(datafile):
    print "==== Running the model ===="
    opt = SolverFactory("cplex")
    list = []
    list_ = []
    model.current_time_step.add(1)
    instance = model.create_instance(datafile)

    ## determine the time steps
    for comp in instance.component_objects():
        if str(comp) == "time_step":
            parmobject = getattr(instance, str(comp))
            for vv in parmobject.value:
                list_.append(vv)
    storage = {}
    insts = []

    for vv in list_:
        model.current_time_step.clear()
        model.current_time_step.add(vv)
        print "Running for time step: ", vv

        instance = model.create_instance(datafile)
        # update initial storage value from previous storage
        if len(storage) > 0:
            set_initial_storage(instance, storage)
            instance.preprocess()

        res=opt.solve(instance)  
        instance.solutions.load_from(res)

        #instance.load(res)
        insts.append(instance)
        storage=get_storage(instance)
        list.append(res)
        print "-------------------------"


    count=1
    for inst in insts:
        print "******************This is inst: %s" % type(inst)
    for res in list:
        print " ========= Time step:  %s =========="%count
        print res
        count+=1
    count=1

    for inst in insts:
        print " ========= Time step:  %s =========="%count
        set_post_process_variables(inst)
        display_variables(inst)
        count+=1
    return list, insts


def display_variables(instance):
    for var in instance.component_objects(Var):
            s_var = getattr(instance, str(var))
            print "=================="
            print "Variable: %s"%s_var
            print "=================="
            for vv in s_var:
                if len(vv) == 2:
                    name = "[" + ', '.join(map(str,vv)) + "]"
                else:
                    name = ''.join(map(str,vv))
                print name ,": ",(s_var[vv].value)

##========================
# running the model in a loop for each time step
if __name__ == '__main__':
    run_model("Demo3 (shortage).dat")