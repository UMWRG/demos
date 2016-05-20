Traffic Equilibrium Problem
===========================

Files available with this model
-------------------------------
- [Template.xml] (https://github.com/UMWRG/demos/tree/master/TrafficEquilibrium/template/TrafficEquilibriumModel/template>) : template which defines nodes and links and their attributes.
- [network.csv] (https://github.com/UMWRG/demos/tree/master/TrafficEquilibrium/data>) : CSV files to load in Hydra Modeller which contain the network and scenario data.
- [TrafficEquilibrium.gms](https://github.com/UMWRG/demos/tree/master/TrafficEquilibrium/model>) : The current version of the Traffic Equilibrium model GAMS code
- [input.txt](https://github.com/UMWRG/demos/tree/master/TrafficEquilibrium/model/input.txt>)    : The input file for the model, containing the network information and data. This is the file Hydra creates using the GAMS App.

Purpose of Model
----------------
In this model, a network that is given by a set of nodes N and a set of arcs A. it is assumed that the time cost of traveling along a given arc is a nonlinear (increasing) function of the total flow along that arc. There are two subsets of N that represent the set of origin nodes O and destination nodes D respectively. Associated with each origin-destination pair is a demand that represents the required flow from the origin node to the destination node.
The fundamental assumption of this model is that drivers are fully informed: a driver going from point A to point B follows the fastest available route, taking the decisions of other drivers as given.
A multicommodity formulation which  can provide a compact and efficient representation of the model, permitting direct solution with “off-the-shelf” algorithms, is demonstrated. It is found that in many cases the larger complementarity model provides a more efficient formulation than either the primal or dual nonlinear program.
Three different models are used to compute traffic equilibria. These are a mixed complementarity formulation and a primal and dual formulation using NLPs [1].
The original GAMS code for this model is located in this [paper] (http://ftp.cs.wisc.edu/math-prog/tech-reports/95-03.pdf
and [here](https://www.gams.com/modlib/libhtml/traffic.htm)

Running the Model
-----------------
The GAMS code provided here is modified to work with the input file which is genrated from Hydra's GAMS App.

This model can be run directly with the input file provided (input.txt), similar to the orginal code.

To run this version with Hydra, user needs to:
- Install the template
- Import the newtork and scenario data using the csv files.
- Download and install GAMS App into Hydra Modeller
- Run the GAMS app using the provided GAMS model.

Hydra Modeller also allows you to explore and modify network data easily. Using the [GAMS App] (http://hydraappstore.com/details/?app=1088), you can run the model automatically and the results will be stored in Hydra Modeller so you can explore them. 
You can then create multiple scenarios and the run the model against each one. Then you can compare the results graphically.

You can find more details about using Hydra Modeller in this [tutorial] (https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf>). [2]

Model inputs:
-------------
- arc cost data: a, b, and k
- trip matrix from i to j

Model Outputs
-------------
- t(i,j) time to get from node i to node 
- j v(i,j) time to traverse arc form i to j 
- y(i,j,k) flow to k along arc i-j 
- x(i,j) aggregate flow on arc i-j 

You can find model formulation and core detailed description of the network in [1].

Version History
---------------

| Version | Date     | Comment                                       | Author                                   |
| ------- | -------- | --------------------------------------------- | ---------------------------------------- |
| 0.0.1   | Jan 2016 | Modify the orginal version to work with Hydra | K. Mohamed, the University of Manchester |

More Information
----------------

1. Ferris, M C, Meeraus, A, and Rutherford, T F, Computing Wardropian Equilibria in a Complementarity Framework. Optimization Methods and Software 10 (1999), 669-685.
3. Stephen Knox, ''Getting started with Hydra Modeller'', https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf, Dec 2015.



