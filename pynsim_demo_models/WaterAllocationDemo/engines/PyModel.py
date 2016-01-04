#    (c) Copyright 2014, University of Manchester
#
#    This file is part of Pynsim.
#
#    Pynsim is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pynsim is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pynsim.  If not, see <http://www.gnu.org/licenses/>.


from pyomo.environ import *
from pyomo.opt import SolverFactory


class OptimisationModel:
    # creating the optimisation model

    def __init__(self, network):

        self.nodes_names = []
        self.demand_nodes = []
        self.storage_nodes = []
        self.nonstorage_nodes = []
        self.node_initial_storage = {}
        self.links_comp = {}
        self.flow_multiplier = {}
        self.min_storage = {}
        self.max_storage = {}
        self.inflow = {}
        self.consumption_coefficient = {}
        self.upper_flow = {}
        self.lower_flow = {}
        self.flow_multiplier = {}
        self.cost = {}
        self.target_demand = {}

        for node in network.nodes:
            self.nodes_names.append(node.name)
            self.inflow[node.name] = node.inflow

            if node.type == 'agricultural' or node.type == 'urban':
                self.demand_nodes.append(node.name)
                self.target_demand[node.name] = node.target_demand
                self.cost[node.name] = node.cost
                self.inflow[node.name] = node.inflow

            if node.type == 'surface reservoir' or node.type == 'aquifer storage':
                self.storage_nodes.append(node.name)
                self.node_initial_storage[node.name] = node.initial_storage
                self.min_storage[node.name] = node.min_storage
                self.max_storage[node.name] = node.max_storage
                self.inflow[node.name] = node.inflow

            if node.type != 'surface reservoir' and node.type != 'aquifer storage':
                self.nonstorage_nodes.append(node.name)

        for link in network.links:
            self.links_comp[(link.start_node.name, link.end_node.name)] = link
            self.flow_multiplier[(link.start_node.name, link.end_node.name)] = link.flow_multiplier
            self.upper_flow[(link.start_node.name, link.end_node.name)] = link.upper_flow
            self.lower_flow[(link.start_node.name, link.end_node.name)] = link.lower_flow

    def run(self):
        # Creating the model
        model = AbstractModel()

        # Declaring model indexes using sets
        model.nodes = Set(initialize=self.nodes_names)
        model.links = Set(within=model.nodes*model.nodes, initialize=self.links_comp.keys())
        model.demand_nodes = Set(initialize=self.demand_nodes)
        model.nonstorage_nodes = Set(initialize=self.nonstorage_nodes)
        model.storage_nodes = Set(initialize=self.storage_nodes)

        # Declaring model parameters
        model.initial_storage = Param(model.storage_nodes, mutable=True, initialize=self.node_initial_storage)
        model.inflow = Param(model.nodes, initialize=self.inflow)
        model.cost = Param(model.demand_nodes, initialize=self.cost)
        model.target_demand = Param(model.demand_nodes, initialize=self.target_demand)
        model.flow_multiplier = Param(model.links, initialize=self.flow_multiplier)
        model.flow_lower_bound = Param(model.links, initialize=self.lower_flow)
        model.flow_upper_bound = Param(model.links, initialize=self.upper_flow)
        model.storage_lower_bound = Param(model.storage_nodes, initialize=self.min_storage)
        model.storage_upper_bound = Param(model.storage_nodes, initialize=self.max_storage)

        # ======================================== Declaring Variables (X and S)

        # Defining the flow lower and upper bound
        def flow_capacity_constraint(model, node, node2):
            return (model.flow_lower_bound[node, node2], model.flow_upper_bound[node, node2])

        # Defining the storage lower and upper bound
        def storage_capacity_constraint(model, storage_nodes):
            return (model.storage_lower_bound[storage_nodes], model.storage_upper_bound[storage_nodes])

        # Declaring decision variable X
        model.X = Var(model.links, domain=NonNegativeReals, bounds=flow_capacity_constraint, initialize=0)

        # Declaring state variable S
        model.S = Var(model.storage_nodes, domain=NonNegativeReals, bounds=storage_capacity_constraint)

        # Defining demand satisfaction ratio (alpha)
        def demand_satisfaction_ratio(model, demand_nodes):
            return (sum([model.X[node_in, demand_nodes]*model.flow_multiplier[node_in, demand_nodes]
                         for node_in in model.nodes if (node_in, demand_nodes) in model.links]) - sum([model.X[demand_nodes, node_out]
                         for node_out in model.nodes if (demand_nodes, node_out) in model.links]))/model.target_demand[demand_nodes]

        model.alpha = Var(model.demand_nodes, domain=NonNegativeReals, bounds=(0, 1), initialize=demand_satisfaction_ratio)

        # ======================================== Declaring the objective function (Z)

        def objective_function(model):
            return summation(model.cost, model.alpha)

        model.Z = Objective(rule=objective_function, sense=maximize)

        # ======================================== Declaring constraints
        # Mass balance for non-storage nodes:
        def mass_balance(model, nonstorage_nodes):

            # inflows
            term1 = model.inflow[nonstorage_nodes]
            term2 = sum([model.X[node_in, nonstorage_nodes]*model.flow_multiplier[node_in, nonstorage_nodes]
                          for node_in in model.nodes if (node_in, nonstorage_nodes) in model.links])

            # outflows
            if nonstorage_nodes in model.demand_nodes:
                term3 = model.alpha[nonstorage_nodes]*model.target_demand[nonstorage_nodes]
            else:
                term3 = 0
            term4 = sum([model.X[nonstorage_nodes, node_out]
                          for node_out in model.nodes if (nonstorage_nodes, node_out) in model.links])

            # inflows - outflows = 0:
            return (term1 + term2) - (term3 + term4) == 0

        model.mass_balance_const = Constraint(model.nonstorage_nodes, rule=mass_balance)

        # Mass balance for storage nodes:
        def storage_mass_balance(model, storage_nodes):
            # inflows
            term1 = model.inflow[storage_nodes]
            term2 = sum([model.X[node_in, storage_nodes]*model.flow_multiplier[node_in, storage_nodes]
                          for node_in in model.nodes if (node_in, storage_nodes) in model.links])

            # outflows
            term3 = sum([model.X[storage_nodes, node_out]
                          for node_out in model.nodes if (storage_nodes, node_out) in model.links])

            # storage
            term4 = model.initial_storage[storage_nodes]

            term5 = model.S[storage_nodes]

            # inflows - outflows = 0:
            return (term1 + term2 + term4) - (term3 + term5) == 0

        model.storage_mass_balance_const = Constraint(model.storage_nodes, rule=storage_mass_balance)

        # ======================== running the model in a loop for each time step

        opt = SolverFactory("glpk")
        instance = model.create()
        result = opt.solve(instance)
        instance.load(result)
        return instance
