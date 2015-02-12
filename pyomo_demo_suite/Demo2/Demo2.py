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

from pyomo.environ import *

from pyomo.opt import SolverFactory
class PyMode():
    # Declaring the model
    def __init__(self):
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
        model.consumption_coefficient = Param(model.nodes)
        model.initial_storage = Param(model.storage_nodes, mutable=True)
        model.cost = Param(model.links, model.time_step)
        model.flow_multiplier = Param(model.links, model.time_step)
        model.min_flow = Param(model.links, model.time_step)
        model.max_flow = Param(model.links, model.time_step)
        model.storagelower = Param(model.storage_nodes, model.time_step)
        model.storageupper = Param(model.storage_nodes, model.time_step)
        model.X = Var(model.links, domain=NonNegativeReals, bounds=flow_capacity_constraint) # [X units]
        model.Z = Objective(rule=objective_function, sense=minimize) #[Z units]

    # Declaring state variable S
        model.S = Var(model.storage_nodes, domain=NonNegativeReals, bounds=storage_capacity_constraint) #[S unit]
        model.mass_balance_const = Constraint(model.nonstorage_nodes, rule=mass_balance)
        model.storage_mass_balance_const = Constraint(model.storage_nodes, rule=storage_mass_balance)
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

        for vv in list_:
            ##################
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
            instances.append(instance)
            list.append(res)
        for res in list:
            print res
        return  list, instances

#print "Result: ", res
# Defining the flow lower and upper bound
def flow_capacity_constraint(model, node, node2):
    return (model.min_flow[node, node2, model.current_time_step], model.max_flow[node, node2, model.current_time_step])

# Defining the storage lower and upper bound
def storage_capacity_constraint(model, storage_nodes):
    return (model.storagelower[storage_nodes, model.current_time_step], model.storageupper[storage_nodes, model.current_time_step])


def get_current_cost(model):
    current_cost= {}
    for link in model.links:
        current_cost[link]= model.cost[link, model.current_time_step]
    return current_cost

def objective_function(model):
    return summation(get_current_cost(model), model.X)

##======================================== Declaring constraints
# Mass balance for non-storage nodes:

def mass_balance(model, nonstorage_nodes):
    # inflow
    term1 = model.inflow[nonstorage_nodes, model.current_time_step]
    term2 = sum([model.X[node_in, nonstorage_nodes]*model.flow_multiplier[node_in, nonstorage_nodes, model.current_time_step]
                  for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])
    # outflow
    term3 = model.consumption_coefficient[nonstorage_nodes] \
        * sum([model.X[node_in, nonstorage_nodes]*model.flow_multiplier[node_in, nonstorage_nodes, model.current_time_step]
               for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])
    term4 = sum([model.X[nonstorage_nodes, node_out]
                  for node_out in model.nodes if (nonstorage_nodes, node_out) in model.links])

    # inflow - outflow = 0:
    return (term1 + term2) - (term3 + term4) == 0



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
def run_model(datafile):
    pymodel=PyMode()
    return pymodel.run(datafile)
	
if __name__ == '__main__':     
    pymodel=PyMode()    
    pymodel.run("Demo2.dat")
    