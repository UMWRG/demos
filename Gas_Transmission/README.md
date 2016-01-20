Gas Transmission Problem - Belgium
==================================

Files available with this model
-------------------------------
- [Template.xml] (https://github.com/UMWRG/demos/tree/master/templates/Gas_Transmission/Template>) : template which defines nodes and links and their attributes.
- [Gas_Trans.xlsx] (https://github.com/UMWRG/demos/tree/master/data/Gas_Transmission>) : An excel file to load in Hydra Modeller which contain the network and scenario data.
- [openstreet.wms] (https://github.com/UMWRG/demos/tree/master/data/Gas_Transmission/GIS>) : The file you can load as a background in Hydra Modeller.
- gastrans.gms : The current version of the GAS transmission GAMS code
- input.txt    : The input file for the model, containing the network information and data. This is the file Hydra creates using the GAMS App.

Purpose of Model
----------------
The problem considered in this model is to minimize the total supply cost of a gas transmission company which must satisfy demand in different nodes at a minimal guaranteed pressure.

The problem of distributing gas through a network of pipelines is formulated as a cost minimization subject to nonlinear flow-pressure relations, material balances, and pressure bounds. The Belgian gas network is used as an example.

First, a straight-forward NLP formulation that can be solved by todays NLP solvers is modeled.  Afterwards, the 3-stage approach by Wolf & Smeers [1] is implemented.

The original GAMS code for this model is located [here] (https://www.gams.com/modlib/libhtml/gastrans.htm)


Running the Model
-----------------
The GAMS code provided here is modified to work with the input file which is genrated from Hydra's GAMS App.

This model can be run directly with the input file provided (input.txt), similar to the orginal code.

To run this version with Hydra, user needs to:
- Install the template
- Import the newtork and scenario data using the excel file.
- Download and install GAMS App into Hydra Modeller
- Run the GAMS app using the provided GAMS model.

Using the network data and GIS (wms) file provided, Hydra Modeller allows you to visualize the model network (cities and pipelines) on their actual location on a map. Hydra Modeller also allows you to explore and modify network data easily. Using the [GAMS App] (http://hydraappstore.com/details/?app=1088), you can run the model automatically and the results will be stored in Hydra Modeller so you can explore them. 
You can then create multiple scenarios and the run the model against each one. Then you can compare the results graphically.

You can find more details about using Hydra Modeller in this [tutorial] (https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf>). [1]

Model inputs:
-------------
- compressibility factor (-)
- density of gas relative to air (-)
- length (km)
- diameter (mm)
- cost ($ per MBTU)   
- pressure upper bound (bar)
- pressure lower bound (bar)
- supply upper bound (mill M3 per day)
- supply lower bound (mill M3 per day)
- absolute rugosity (mm)
- gas temperature (K)  

Model Outputs
-------------
- pipeline flow (1e6 SCM)
- supply - demand (1e6 SCM)
- squared pressure 
- supply cost ($)

You can find model formulation and core detailed description of the Belgium network in [1].

Version History
---------------

| Version | Date     | Comment                                       | Author                                   |
| ------- | -------- | --------------------------------------------- | ---------------------------------------- |
| 0.0.1   | Jan 2016 | Modify the orginal version to work with Hydra | K. Mohamed, the University of Manchester |

More Information
----------------

1. de Wolf, D, and Smeers, Y, The Gas Transmission Problem Solved by and Extension of the Simplex Algorithm. Management Science 46, 11 (2000), 1454-1465.
2. Stephen Knox, ''Getting started with Hydra Modeller'', https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf, Dec 2015.


