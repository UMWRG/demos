Demo Models in GAMS, Pyomo and Pynsim
=====================================

Here you will find three models:

1. A trivial example of how to minimise cost for a network in a single time step.
2. A Cost Minimisation Demo (CMD) over multiple time steps
3. A Water Allocation Demo (WAD), which allocates water to the resources with the greatest need (priority).

Variations
----------
The WAD and CMD are written in [GAMS](http://www.gams.com), [Pyomo](http://www.pyomo.org) and [Pynsim](http://umwrg.github.io/pynsim).
The trivial example is written in GAMS & Pyomo only.

All models use a network structure of nodes & links, allowing them to be compatible
with [Hydra Platform](http://umwrg.github.io/HydraPlatform).

Each model comes with its own set of data, which is compatible with Hydra Platform.
Each model also comes with a [template](http://umwrg.github.io/HydraPlatform/tutorials/plug-in/templates.html?highlight=template), again for use with Hydra Platform. A template
defines the node & link types, including their attributes and the dimension and units
of each attribute.

Model 1 (A trivial example)
---------------------------
This simple water allocation model includes a single time step cost minimisation objective. Available water introduced as rainfall inflow at upstream of the water system is distributed according to the cost of water delivery in each link. Target demand values are set by the minimum flow capacity of links delivering water to demand nodes.

Model 2 (A cost minimisation model)
-----------------------------------
This is a more sophisticated form of the trivial example. This involves a storage node which can feature storing and releasing water. Six bi-monthly time steps are used to account for allocation planning over a year.

Model 3 (A water allocation model)
----------------------------------
Models 1&2 do not allow for any scarcity, i.e. if the available level of supply is lower than the required level of demand (represented by lower bound of water delivered via links to each demand node), both models become infeasible and no solution can be reached. Assigning cost to links to favour a delivery path is likely to make model behaviour unpredictable in case of large networks. This model is an evolution of Model 2 which allows for water shortage so that infeasibilities are not generated. priorities (costs) are assigned to demand nodes and the objective function maximises the level of demand satisfaction in all demand nodes. The available water, even when lower than the target demand, will be distributed to demand nodes with higher priority (cost) first and then to those with lower priority.

