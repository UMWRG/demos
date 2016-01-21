International Gas Trade Model (GTM)
===================================

Files available with this model
-------------------------------
- [Template.xml] (https://github.com/UMWRG/demos/tree/master/templates/GasTradeModel/Template>) : template which defines nodes and links and their attributes.
- [network.csv] (https://github.com/UMWRG/demos/tree/master/data/GasTradeModel>) : CSV files to load in Hydra Modeller which contain the network and scenario data.
- [GasTradeModel.gms](https://github.com/UMWRG/demos/tree/master/data/GasTradeModel/MODEL>) : The current version of the GAS trade model GAMS code
- [openstreet.wms] (https://github.com/UMWRG/demos/tree/master/data/GasTradeModel/GIS>) : The file you can load as a background in Hydra Modeller.
- [GasTradeModel.gms](https://github.com/UMWRG/demos/tree/master/data/GasTradeModel/MODEL>)  : The current version of the GAS trade model GAMS code
- [input.txt](https://github.com/UMWRG/demos/tree/master/data/GasTradeModel/MODEL>)    : The input file for the model, containing the network information and data. This is the file Hydra creates using the GAMS App.

Purpose of Model
----------------
The Gas Trade Model (GTM) models interrelated gas markets. Prices may be free to move as to equilibrate supplies and demand. Disequilibria can be introduced with controls over prices and/or quantities traded.
GTM is a market equilibrium model that allows interdependence between gas prices and the quantities traded at a single point in time. Regionally disaggregated trade flows are projected between Canada, Mexico, and the United States. 
The model is intended to provide a background for realistic bargaining over international prices and risk sharing in an era when the U.S. market becomes deregulated, but Canada and Mexico maintain export controls and lower domestic prices than those in the United States. If present policies are continued, Mexico will export only minor amounts of gas. 
GTM computes for both 1990 and 2000 market-clearing prices and a possible pattern of trade flows between 10 supply regions (1 in Mexico, 2 in Canada, and 7 in the United States) and 14 demand regions (1 in Mexico, 3 in Canada, and 10 in the United States). 

The original GAMS code for this model is located [here] (https://www.gams.com/modlib/libhtml/gtm.htm)

Running the Model
-----------------
The GAMS code provided here is modified to work with the input file which is genrated from Hydra's GAMS App.

This model can be run directly with the input file provided (input.txt), similar to the orginal code.

To run this version with Hydra, user needs to:
- Install the template
- Import the newtork and scenario data using the csv files.
- Download and install GAMS App into Hydra Modeller
- Run the GAMS app using the provided GAMS model.

Using the network data and GIS (wms) file provided, Hydra Modeller allows you to visualize the model network on their actual location on a map. Hydra Modeller also allows you to explore and modify network data easily. Using the [GAMS App] (http://hydraappstore.com/details/?app=1088), you can run the model automatically and the results will be stored in Hydra Modeller so you can explore them. 
You can then create multiple scenarios and the run the model against each one. Then you can compare the results graphically.

You can find more details about using Hydra Modeller in this [tutorial] (https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf>). [3]

Model inputs:
-------------
- unit transport cost ($ per mcf)
- pipeline capacities
- demand data at alternative price levels 
- supply data at alternative price levels

Model Outputs
-------------
- shipment of natural gas (tcf) 
- regional supply (tcf) 
- regional demand 
- benefit consumers benefits minus cost

You can find model formulation and core detailed description of the network in [1, 2].

Version History
---------------

| Version | Date     | Comment                                       | Author                                   |
| ------- | -------- | --------------------------------------------- | ---------------------------------------- |
| 0.0.1   | Jan 2016 | Modify the orginal version to work with Hydra | K. Mohamed, the University of Manchester |

More Information
----------------

1. Manne, A S, and Beltramo, M A, GTM: An International Gas Trade Model, International Energy Program Report. Stanford University, 1984.
2. Mark A. Beltramo, Alan S. Manne and John P. Weyant, “A North American Gas Trade Model (GTM)”, The Energy Journal, Vol. 7, No. 3 (July 1986), pp. 15-32.
3. Stephen Knox, ''Getting started with Hydra Modeller'', https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf, Dec 2015.



