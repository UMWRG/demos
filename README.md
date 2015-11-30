Demo Models in GAMS, Pyomo and WaterSys
=======================================

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

Model 2 (A cost minimisation model)
-----------------------------------

Model 3 (A water allocation model)
----------------------------------
Model in DEMO 1 and DEMO 2 do not allow for any scarcity, i.e. if the available level of supply is lower than the required level of demand (represented by lower bound of water delivered via links to each demand node), both models become infeasible and no solution can be reached. We therefore modify the previous model formulation to allow for water shortage so that infeasibilities are not generated. The available water, even when lower than the target demand, will be distributed to demand nodes with higher priority (cost) first and then to those with lower priority.
