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
model.agricultural=Set() #deman  && non_storage_nodes
model.urban=Set()  #deman && non_storage_nodes
model.discharge=Set() #deman && non_storage_nodes
model.desalination=Set() #storage_nodes
model.groundwater=Set()  #storage_nodes
model.hydropower=Set()   #non_storage_nodes
model.water_treatment=Set()  #non_storage_nodes
model.treatment_hydro_nodes = Set()   #non_storage_nodes
model.junction=Set() #non_storage_nodes
model.surface_reservoir=Set() #storage_nodes
model.river_section=Set(within=model.nodes*model.nodes)

# Declaring model parameters
model.inflow_desalination = Param(model.desalination, model.time_step, default=0)
model.inflow_surface_reservoir=Param(model.surface_reservoir, model.time_step, default=0)

model.current_time_step = Set()
model.initial_storage_desalination = Param(model.desalination, mutable=True)
model.initial_storage_groundwater = Param(model.groundwater, mutable=True)
model.initial_storage_surface_reservoir = Param(model.surface_reservoir, mutable=True)

model.priority_discharge = Param(model.discharge, model.time_step, default=0)
model.priority_urban = Param(model.urban, model.time_step, default=0)
model.priority_agricultural = Param(model.agricultural, model.time_step, default=0)

model.flow_multiplier_river_section = Param(model.river_section, model.time_step)

model.min_flow_river_section = Param(model.river_section, model.time_step)
model.max_flow_river_section = Param(model.river_section, model.time_step)

model.min_storage_desalination = Param(model.desalination, model.time_step)
model.min_storage_groundwater = Param(model.groundwater, model.time_step)
model.min_storage_surface_reservoir = Param(model.surface_reservoir, model.time_step)

model.max_storage_desalination = Param(model.desalination, model.time_step)
model.max_storage_groundwater = Param(model.groundwater, model.time_step)
model.max_storage_surface_reservoir = Param(model.surface_reservoir, model.time_step)
model.max_storage_treatment_hydro_nodes = Param(model.treatment_hydro_nodes, model.time_step)

model.demand_urban = Param(model.urban, model.time_step, default=0)
model.demand_agricultural = Param(model.agricultural, model.time_step, default=0)
model.demand_discharge = Param(model.discharge, model.time_step, default=0)

model.percent_loss_hydropower = Param(model.hydropower)
model.percent_loss_water_treatment = Param(model.water_treatment)

model.net_head_hydropower = Param(model.hydropower)
model.unit_price_hydropower = Param()

##======================================== Declaring Variables (X and S)

# Defining the flow lower and upper bound
def flow_capacity_constraint(model, node, node2):
    return (model.min_flow_river_section[node, node2, model.current_time_step], model.max_flow_river_section[node, node2, model.current_time_step])

# Defining the storage lower and upper bound
def  storage_capacity_constraint(model, storage_nodes):
    if(storage_nodes in model.surface_reservoir):
        return (model.min_storage_surface_reservoir[storage_nodes, model.current_time_step], model.max_storage_surface_reservoir[storage_nodes, model.current_time_step])
    elif(storage_nodes in model.groundwater):
        return (model.min_storage_groundwater[storage_nodes, model.current_time_step], model.max_storage_groundwater[storage_nodes, model.current_time_step])
    elif(storage_nodes in model.desalination):
        return (model.min_storage_desalination[storage_nodes, model.current_time_step], model.max_storage_desalination[storage_nodes, model.current_time_step])


# Declaring decision variable X
model.Flow = Var(model.river_section, domain=NonNegativeReals, bounds=flow_capacity_constraint) #*1e6 m^3 mon^-1

# Declaring state variable S

model.Storage = Var(model.storage_nodes, bounds=storage_capacity_constraint) #1e6 m^3

def percent_demand_met_bound(model):
    return 0, 1#, model.alpha, 1

model.percent_demand_met = Var(model.demand_nodes, bounds=percent_demand_met_bound) #*%

# Declaring variable alpha
demand_satisfaction_ratio_bound = Constraint(rule=percent_demand_met_bound)

# Defining post process variables

model.released_water = Var(model.nodes)
model.received_water = Var(model.nodes)
model.demand_met = Var(model.demand_nodes)
model.revenue = Var(model.hydropower)


def get_current_priority(model):
    current_priority = {}
    for node in model.agricultural:
         current_priority[node] = model.priority_agricultural[node, model.current_time_step]
    for node in model.urban:
         current_priority[node] = model.priority_urban[node, model.current_time_step]
    for node in model.discharge:
         current_priority[node] = model.priority_discharge[node, model.current_time_step]
    return current_priority  # model.cost [model.current_time_step]

def objective_function(model):
    return summation(get_current_priority(model), model.percent_demand_met)

model.Objective_function = Objective(rule=objective_function, sense=maximize) #*Z_Unit

##======================================== Declaring constraints
# Mass balance for non-storage nodes:

def mass_balance(model, nonstorage_nodes):
    # inflow
    if nonstorage_nodes in model.desalination:
        term1 = model.inflow_desalination[nonstorage_nodes, model.current_time_step]
    elif nonstorage_nodes in model.surface_reservoir:
        term1 = model.inflow_surface_reservoir[nonstorage_nodes, model.current_time_step]
    else:
        term1 = 0

    term2 = sum([model.Flow[node_in, nonstorage_nodes]*model.flow_multiplier_river_section[node_in, nonstorage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])

    if nonstorage_nodes in model.hydropower:
        term22 = model.percent_loss_hydropower[nonstorage_nodes]
    elif nonstorage_nodes in model.water_treatment:
        term22 = model.percent_loss_water_treatment[nonstorage_nodes]
    else:
        term22 = 0

    # outflow

    if nonstorage_nodes in model.demand_nodes:
        if(nonstorage_nodes in model.urban):
              term3=model.percent_demand_met[nonstorage_nodes] * model.demand_urban[nonstorage_nodes, model.current_time_step]
        elif (nonstorage_nodes in model.agricultural):
              term3=model.percent_demand_met[nonstorage_nodes] * model.demand_agricultural[nonstorage_nodes, model.current_time_step]
        elif (nonstorage_nodes in model.discharge):
              term3=model.percent_demand_met[nonstorage_nodes] * model.demand_discharge[nonstorage_nodes, model.current_time_step]
    else:
        term3 = 0

    term4 = sum([model.Flow[nonstorage_nodes, node_out]
                  for node_out in model.nodes if (nonstorage_nodes, node_out) in model.links])

    # inflow - outflow = 0:
    return (term1 + (1-term22) * term2) - (term3 + term4) == 0


model.mass_balance_const = Constraint(model.non_storage_nodes, rule=mass_balance)

# Mass balance for storage nodes:
def storage_mass_balance(model, storage_nodes):
    # inflow
    if(storage_nodes in model.surface_reservoir):
        term1= model.inflow_surface_reservoir[storage_nodes, model.current_time_step]
        term4 = model.initial_storage_surface_reservoir[storage_nodes]
    elif (storage_nodes in model.desalination):
        term1= model.inflow_desalination[storage_nodes, model.current_time_step]
        term4 = model.initial_storage_desalination[storage_nodes]
    elif (storage_nodes in model.groundwater):
        term1=0
        term4=model.initial_storage_groundwater[storage_nodes]

    term2 = sum([model.Flow[node_in, storage_nodes]*model.flow_multiplier_river_section[node_in, storage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, storage_nodes) in model.river_section])

    if storage_nodes in model.hydropower:
        term22 = model.percent_loss_hydropower[storage_nodes]
    elif storage_nodes in model.water_treatment:
        term22 = model.percent_loss_water_treatment[storage_nodes]
    else:
        term22 = 0

    # outflow
    term3 = sum([model.Flow[storage_nodes, node_out]
                  for node_out in model.nodes if (storage_nodes, node_out) in model.river_section])

    # storage
    term5 = model.Storage[storage_nodes]
    # inflow - outflow = 0:
    return (term1 + (1-term22) * term2 + term4) - (term3 + term5) == 0

model.storage_mass_balance_const = Constraint(model.storage_nodes, rule=storage_mass_balance)


def hydro_treatment_capacity(model, treatment_hydro_nodes):
    return 0 <= sum([model.Flow[node_in, treatment_hydro_nodes]*model.flow_multiplier_river_section[node_in, treatment_hydro_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, treatment_hydro_nodes) in model.links]) <= model.max_storage_treatment_hydro_nodes[treatment_hydro_nodes, model.current_time_step]

model.hydro_treatment_capacity_constraint = Constraint(model.treatment_hydro_nodes, rule=hydro_treatment_capacity)


def released(instance):
    for i in instance.nodes:
        instance.released_water[i]=sum([instance.Flow[i, node_out].value for node_out in instance.nodes if (i, node_out) in instance.links])


def received(instance):
    for i in instance.nodes:
        instance.received_water[i].value=sum([instance.flow_multiplier_river_section[node_in, i, instance.current_time_step]*instance.Flow[node_in, i].value for node_in in instance.nodes if (node_in, i) in instance.links])


def demand_met(instance):
    for i in instance.demand_nodes:
        instance.demand_met[i].value= instance.received_water[i].value - instance.released_water[i].value


def revenue(instance):
    for i in instance.hydropower:
        instance.revenue[i].value=(1-instance.percent_loss_hydropower[i])*instance.received_water[i].value*9.81*24*0.3858*instance.net_head_hydropower[i]*instance.unit_price_hydropower


def get_storage(instance):
    storage_levels={}
    for i in instance.storage_nodes:
        storage_levels[i]=instance.Storage[i].value
    return storage_levels


def set_initial_storage(instance, storage_levels):
    for i in instance.storage_nodes:
        if i in instance.surface_reservoir:
            instance.initial_storage_surface_reservoir[i].value =storage_levels[i]
        elif i in instance.groundwater:
            instance.initial_storage_groundwater[i].value =storage_levels[i]
        elif i in instance.desalination:
            instance.initial_storage_desalination[i].value =storage_levels[i]


def set_post_process_variables(instance):
    released(instance)
    received(instance)
    demand_met(instance)
    revenue(instance)
"""
model.initial_storage_desalination = Param(model.desalination, mutable=True)
model.initial_storage_groundwater = Param(model.groundwater, mutable=True)
model.initial_storage_surface_reservoir = Param(model.surface_reservoir, mutable=True)


def set_initial_storage(instance, storage_levels):
    for var in instance.component_objects(Param):
            if(str(var)=="initial_storage_surface_reservoir" or str(var)=="initial_storage_desalination" or str(var)=="initial_storage_groundwater"):
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = storage_levels[vv]


def set_post_process_variables(instance):
    for var in instance.component_objects(Var):
            if str(var) == "Released_Water":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = released(instance, vv)
            if str(var) == "Received_Water":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = received(instance, vv)
            if str(var) == "Demand_Met":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = demand_met(instance, vv)
            if str(var) == "Revenue":
                s_var = getattr(instance, str(var))
                for vv in s_var:
                    s_var[vv] = revenue(instance, vv)
"""
def run_model(datafile):
    print "==== Running the model ===="
    opt = SolverFactory("cplex")
    list=[]
    list_=[]
    model.current_time_step.add(1)
    instance=model.create_instance(datafile)
    ## determine the time steps
    for comp in instance.component_objects():
        if str(comp)=="time_step":
            parmobject = getattr(instance, str(comp))
            for vv in parmobject.value:
                list_.append(vv)
    storage = {}
    insts=[]
    for vv in list_:
        model.current_time_step.clear()
        model.current_time_step.add(vv)
        print "Running for time step: ", vv
        instance=model.create_instance(datafile)
        ##update intial storage value from previous storage
        if len(storage) > 0:
            set_initial_storage(instance, storage)
            instance.preprocess()

        res=opt.solve(instance)
        instance.solutions.load_from(res)
        insts.append(instance)
        storage=get_storage(instance)
        list.append(res)
        print "-------------------------"
    count=1
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
            if type(vv) is str:
                name = ''.join(map(str,vv))
                print name ,": ",(s_var[vv].value)
            elif len(vv) == 2:
                name = "[" + ', '.join(map(str,vv)) + "]"
                print name ,": ",(s_var[vv].value)

##========================
# running the model in a loop for each time step
if __name__ == '__main__':
    run_model("WaterAllocationDemo (shortage).dat")

