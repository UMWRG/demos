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

# Importing needed Packages
from xml.dom import ValidationErr

from pyomo.environ import *

from pyomo.opt import SolverFactory
class PyMode():
    # Declaring the model
    def __init__(self):
        model = AbstractModel()
        # Declaring model indexes using sets
        model.nodes = Set()
        model.links = Set(within=model.nodes*model.nodes)
        model.river_section = Set(within=model.nodes*model.nodes) #==>links
        model.agricultural=Set()
        model.urban=Set()
        model.junction=Set()
        model.surface_reservoir=Set()
        #model.demand_nodes = Set() #==>urban and agricultural
        #model.nonstorage_nodes = Set() #=>junction, urban and agricultural
        model.time_step = Set()
        # Declaring model parameters
        model.inflow_surface_reservoir = Param(model.surface_reservoir, model.time_step)
        model.current_time_step = Set()
        model.consumption_coefficient_agricultural = Param(model.agricultural)
        model.consumption_coefficient_urban = Param(model.urban)
        model.initial_storage_surface_reservoir = Param(model.surface_reservoir, mutable=True)
        model.cost_river_section = Param(model.river_section, model.time_step)
        model.flow_multiplier_river_section = Param(model.river_section, model.time_step)
        model.min_flow_river_section = Param(model.river_section, model.time_step)
        model.max_flow_river_section = Param(model.river_section, model.time_step)
        model.storagelower_surface_reservoir= Param(model.surface_reservoir, model.time_step)
        model.storageupper_surface_reservoir = Param(model.surface_reservoir, model.time_step)
        model.Q = Var(model.river_section, domain=NonNegativeReals, bounds=flow_capacity_constraint) #* [ 1e6 m^3 mon^-1]
        model.Z = Objective(rule=objective_function, sense=minimize) #*[1e6 m^3 mon^-1]
    #Declaring delivery
        model.delivery=Var(model.nodes, domain=NonNegativeReals)  #*[1e6 m^3 mon^-1]
    # Declaring state variable S
        model.S = Var(model.surface_reservoir, domain=NonNegativeReals, bounds=storage_capacity_constraint) #*[1e6 m^3 mon^-1]
        model.mass_balance_const_agr = Constraint(model.agricultural, rule=mass_balance_agricultural)
        model.mass_balance_const_ur = Constraint(model.urban, rule=mass_balance_urban)
        model.mass_balance_const_jun = Constraint(model.junction, rule=mass_balance_junction)
        model.storage_mass_balance_const = Constraint(model.surface_reservoir, rule=storage_mass_balance)
        self.model=model

    def run(self, input_file):
        opt = SolverFactory("glpk")
        list=[]
        list_=[]
        instances=[]
        self.model.current_time_step.add(1)
        instance=self.model.create(input_file)
        for comp in instance.active_components():
            if(comp=="time_step"):
                parmobject = getattr(instance, comp)
                for vv in parmobject.value:
                    list_.append(vv)
        instance =self.model.create(input_file)
        storage={}
        demand_nodes=get_demand_nodes_list(instance)

        for vv in list_:
            ##################
            self.cu_timp=vv
            self.model.current_time_step.clear()
            self.model.preprocess()
            self.model.current_time_step.add(vv)
            self.model.preprocess()
            instance=self.model.create(input_file)

            if(len(storage)>0):
                set_initial_storage(instance, storage)
                self.model.preprocess()
                instance.preprocess()
            else:
                instance.preprocess()
            res=opt.solve(instance)
            instance.load(res)
            instance.preprocess()
            storage=get_storage(instance)
            set_delivery(instance, demand_nodes, vv)
            instances.append(instance)
            list.append(res)
            count=1
        for res in instances:
            print " ========= Time step:  %s =========="%count
            self.display_variables(res)
            count+=1
        return  list, instances

    def display_variables (self, instance):
        for var in instance.active_components(Var):
                s_var = getattr(instance, var)
                print "=================="
                print "Variable: %s"%s_var
                print "=================="
                for vv in s_var:
                    if(s_var[vv].value is None):
                        continue
                    if len(vv) ==2:
                        name="[" + ', '.join(map(str,vv)) + "]"
                    else:
                        name= ''.join(map(str,vv))
                    print name,": ",(s_var[vv].value)



# Defining the flow lower and upper bound
def flow_capacity_constraint(model, node, node2):
    return (model.min_flow_river_section[node, node2, model.current_time_step], model.max_flow_river_section[node, node2, model.current_time_step])

# Defining the storage lower and upper bound
def storage_capacity_constraint(model, storage_nodes):
    return (model.storagelower_surface_reservoir[storage_nodes, model.current_time_step], model.storageupper_surface_reservoir[storage_nodes, model.current_time_step])


def get_current_cost(model):
    current_cost= {}
    for link in model.river_section:
        current_cost[link]= model.cost_river_section[link, model.current_time_step]
    return current_cost

def objective_function(model):
    return summation(get_current_cost(model), model.Q)

##======================================== Declaring constraints
# Mass balance for non-storage nodes:

def mass_balance_agricultural(model, agricultural_nodes):
    # inflow
    #nonstorage_nodes
    term2 = sum([model.Q[node_in, agricultural_nodes]*model.flow_multiplier_river_section[node_in, agricultural_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, agricultural_nodes) in model.river_section])
    # outflow
    term3 = sum([model.Q[agricultural_nodes, node_out]
                  for node_out in model.nodes if (agricultural_nodes, node_out) in model.river_section])
    term4 = model.consumption_coefficient_agricultural[agricultural_nodes] \
        * sum([model.Q[node_in, agricultural_nodes]*model.flow_multiplier_river_section[node_in, agricultural_nodes, model.current_time_step]
               for node_in in model.nodes if (node_in, agricultural_nodes) in model.river_section])
        # inflow - outflow = 0:
    return  term2 - (term3 + term4) == 0


def mass_balance_urban(model, urban_nodes):
    #nonstorage_nodes
    term1 = sum([model.Q[node_in, urban_nodes]*model.flow_multiplier_river_section[node_in, urban_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, urban_nodes) in model.river_section])
    term2 = model.consumption_coefficient_urban[urban_nodes] \
        * sum([model.Q[node_in, urban_nodes]*model.flow_multiplier_river_section[node_in, urban_nodes, model.current_time_step]
               for node_in in model.nodes if (node_in, urban_nodes) in model.river_section])
    term3 = sum([model.Q[urban_nodes, node_out]
                  for node_out in model.nodes if (urban_nodes, node_out) in model.river_section])
    # inflow - outflow = 0:
    return term1 - (term2 + term3) == 0

def mass_balance_junction(model, junction_nodes):
    # inflow
    term1 = sum([model.Q[node_in, junction_nodes]*model.flow_multiplier_river_section[node_in, junction_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, junction_nodes) in model.river_section])
    # outflow
    term2 = sum([model.Q[junction_nodes, node_out]
                  for node_out in model.nodes if (junction_nodes, node_out) in model.river_section])
    return (term1 -  term2) == 0


# Mass balance for storage nodes:
def storage_mass_balance(model, storage_nodes):
    # inflow
    term1 = model.inflow_surface_reservoir[storage_nodes, model.current_time_step]
    term2 = sum([model.Q[node_in, storage_nodes]*model.flow_multiplier_river_section[node_in, storage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, storage_nodes) in model.river_section])

    # outflow
    term3 = sum([model.Q[storage_nodes, node_out]
                  for node_out in model.nodes if (storage_nodes, node_out) in  model.river_section])

    # storage
    term4 = model.initial_storage_surface_reservoir[storage_nodes]
    term5 = model.S[storage_nodes]
    # inflow - outflow = 0:
    return (term1 + term2 + term4) - (term3 + term5) == 0


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
            if(var=="initial_storage_surface_reservoir"):
                s_var = getattr(instance, var)
                for vv in s_var:
                    s_var[vv]=storage[vv]

def get_demand_nodes_list(instance):
    list={}
    for comp in instance.active_components():
        if(comp=="agricultural"):
            parmobject = getattr(instance, comp)
            for vv in parmobject.value:
                for comp_2 in instance.active_components():
                    if(comp_2=="consumption_coefficient_agricultural"):
                        parmobject_2 = getattr(instance, comp_2)
                        for vv2 in parmobject_2:
                            list[vv]=parmobject_2[vv2]
        elif(comp=="urban"):
                parmobject = getattr(instance, comp)
                for vv in parmobject.value:
                    for comp_2 in instance.active_components():
                        if(comp_2=="consumption_coefficient_urban"):
                            parmobject_2 = getattr(instance, comp_2)
                            for vv2 in parmobject_2:
                                list[vv]=parmobject_2[vv2]
    return list

def set_delivery(instance, demand_nodes, cs):
    for var in instance.active_components(Var):
            if(var=="delivery"):
                s_var = getattr(instance, var)
                for vv in s_var:
                    #s_var[vv]=-2
                    if(vv in demand_nodes.keys()):
                        sum=0
                        q=0
                        flow_m=0
                        for var_2 in instance.active_components():
                            if(var_2=="Q"):
                                s_var_2 = getattr(instance, var_2)
                                for vv2 in s_var_2:
                                    if(vv == vv2[1]):
                                        q=s_var_2[vv2].value
                                        if(flow_m is not 0):
                                            sum=sum+q*flow_m
                                            q=0
                                            flow_m=0
                            if(var_2=="flow_multiplier_river_section"):
                                s_var_2 = getattr(instance, var_2)
                                for vv2 in s_var_2:
                                    if(vv == vv2[1] and cs== vv2[2]):
                                        flow_m=s_var_2[vv2]
                                        if(q is not 0):
                                            sum=sum+q*flow_m
                                            q=0
                                            flow_m=0
                                        #print flow_m, q

                        s_var[vv]=sum
                
def run_model(datafile):
    pymodel=PyMode()
    return pymodel.run(datafile)

if __name__ == '__main__':
    pymodel=PyMode()
    pymodel.run("CostMinimisation.dat")
