A Transportation Problem 
========================

Files available with this model
-------------------------------
- [Template.xml] (https://github.com/UMWRG/demos/tree/master/templates/Transportation/Template>) : template which defines nodes and links and their attributes.
- [Transportation.xlsx] (https://github.com/UMWRG/demos/tree/master/data/Transportation>) : An excel file to load in Hydra Modeller which contain the network and scenario data.
- [openstreet.wms] (https://github.com/UMWRG/demos/tree/master/data/Transportation/GIS>) : The file you can load as a background in Hydra Modeller.
- Transportation.gms : The current version of the GAS transmission GAMS code
- input.txt    : The input file for the model, containing the network information and data. This is the file Hydra creates using the GAMS App.

Purpose of Model
----------------
This problem finds a least cost shipping schedule that meets
requirements at markets and supplies at factories.
There are six cities with demand constraints and three factories with maximum supply constraints. The cost of the transportation is to be minimized given supply and demand constraints.

The original model is located [here] (https://optimization.mccormick.northwestern.edu/index.php/Network_flow_problem)

Running the Model
-----------------
The GAMS code provided here is modified to work with the input file which is genrated from Hydra's GAMS App.

This model can be run directly with the input file provided (input.txt), similar to the orginal code.

To run this version with Hydra, user needs to:
- Install the template
- Import the newtork and scenario data using the excel file.
- Download and install GAMS App into Hydra Modeller
- Run the GAMS app using the provided GAMS model.

Using the network data and GIS (wms) file provided, Hydra Modeller allows you to visualize the model network (cities and factories) on their on a map. Hydra Modeller also allows you to explore and modify network data easily. Using the [GAMS App] (http://hydraappstore.com/details/?app=1088), you can run the model automatically and the results will be stored in Hydra Modeller so you can explore them. 
You can then create multiple scenarios and the run the model against each one. Then you can compare the results graphically.

You can find more details about using Hydra Modeller in this [tutorial] (https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf>). [1]

Model inputs:
-------------
- transportation cost 
- demand at markets
- capacity of factories

Model Outputs
-------------
- shipment quantities 
- total transportation costs

You can find model formulation and core detailed description of the Belgium network in [1].

Version History
---------------

| Version | Date     | Comment                                       | Author                                   |
| ------- | -------- | --------------------------------------------- | ---------------------------------------- |
| 0.0.1   | Jan 2016 | Modify the orginal version to work with Hydra | K. Mohamed, the University of Manchester |

More Information
----------------

1. R.J. Vanderbei, Linear Programming: Foundations and Extensions. Springer, 2008.  
2. Stephen Knox, ''Getting started with Hydra Modeller'', https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf, Dec 2015.


