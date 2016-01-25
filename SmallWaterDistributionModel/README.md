water distribution systems model 
================================

Files available with this model
-------------------------------
- [Template.xml] (https://github.com/UMWRG/demos/tree/master/SmallWaterDistributionModel/template/SmallWaterDistributionModel/Template>) : template which defines nodes and links and their attributes.
- [Water.xlsx] (https://github.com/UMWRG/demos/tree/master/SmallWaterDistributionModel/data/>) : An excel file to load in Hydra Modeller which contain the network and scenario data.
- [water.gms](https://github.com/UMWRG/demos/tree/master/SmallWaterDistributionModel/model>) : The current version of the water GAMS code
- [input.txt]https://github.com/UMWRG/demos/tree/master/SmallWaterDistributionModel/model>)     : The input file for the model, containing the network information and data. This is the file Hydra creates using the GAMS App.

Purpose of Model
----------------
This example illustrates the use of nonlinear programming in the design of water distribution systems. The model captures the main features of an actual application for a city in Indonesia.
The original GAMS code for this model is located [here] (https://www.gams.com/modlib/libhtml/water.htm)


Running the Model
-----------------
The GAMS code provided here is modified to work with the input file which is genrated from Hydra's GAMS App.

This model can be run directly with the input file provided file(input.txt).

To run this version with Hydra, user needs to:
- Install the template
- Import the newtork and scenario data using the excel file.
- Download and install GAMS App into Hydra Modeller
- Run the GAMS app using the provided GAMS model.

Hydra Modeller also allows you to explore and modify network data easily. Using the [GAMS App] (http://hydraappstore.com/details/?app=1088), you can run the model automatically and the results will be stored in Hydra Modeller so you can explore them. 
You can then create multiple scenarios and the run the model against each one. Then you can compare the results graphically.

Model inputs:
-------------
- supply (m**3/sec)
- height over base (m)			
- demand (m**3/sec)
- pcost (rp/m**4)
- power on diameter in pressure loss equation 
- power on flow in pressure loss equation 
- minimum diameter of pipe (m)
- maximum diameter of pipe (m)
- constant in the pressure loss equation
- scale factor in the investment cost equation
- power on diameter in the cost equation
- interest rate 
- average diameter (geometric mean)
- ratio of demand to supply

Model Outputs
-------------
- flow on each arc - signed (m**3 per sec) 
- pipe diameter for each arc (m) 
- pressure at each node (m) 
- supply at reservoir nodes (m**3 per sec) 
- annual recurrent pump costs (mill rp) 
- investment costs for pipes (mill rp) 
- annual recurrent water costs (mill rp) 
- total discounted costs (mill rp)


Version History
---------------

| Version | Date     | Comment                                       | Author                                   |
| ------- | -------- | --------------------------------------------- | ---------------------------------------- |
| 0.0.1   | Jan 2016 | Modify the orginal version to work with Hydra | K. Mohamed, the University of Manchester |

More Information
----------------
1. Brooke, A, Drud, A S, and Meeraus, A, Modeling Systems and Nonlinear Programming in a Research Environment. In Ragavan, R, and Rohde, S M, Eds, Computers in Engineering, Vol. III. ACME, 1985. Drud, A S, and Rosenborg, 
2. A, Dimensioning Water Distribution Networks. Masters thesis, Institute of Mathematical Statistics and Operations Research, Technical University of Denmark, 1973. (in Danish)
3. [Details about using Hydra Modeller tutorial] (https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf>).  


