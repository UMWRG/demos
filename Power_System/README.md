A Power generation distribution and consumption Problem
=======================================================

Files available with this model
-------------------------------
- [Template.xml] (https://github.com/UMWRG/demos/tree/master/Power_Generation_Distribution_and_Consumption/template/Power_network/Template>) : template which defines nodes and links and their attributes.
- [power_network.xlsx] (https://github.com/UMWRG/demos/tree/master/Power_Generation_Distribution_and_Consumption/data>) : An excel file to load in Hydra Modeller which contain the network and scenario data.
- [openstreet.wms] (https://github.com/UMWRG/demos/tree/master/Power_Generation_Distribution_and_Consumption/GIS>) : The file you can load as a background in Hydra Modeller.
- [Power.gms](https://github.com/UMWRG/demos/tree/master/Power_Generation_Distribution_and_Consumption/model>) : The current version of the model GAMS code
- [input.txt](https://github.com/UMWRG/demos/tree/master/Power_Generation_Distribution_and_Consumption/model>): The input file for the model, containing the network information and data. This is the file Hydra creates using the GAMS App.

Purpose of Model
----------------
Electricity is mainly produced at generation facilities, shipped though the transmission and distribution grids to the consumers
Consider a power network comprised of two groups: the first group with power generation facilities and the second group for power consumption.  The power transmission lines can be used to transfer power to consumers. 
The essence of the problem becomes clear assuming that "a1" refers to the set UZB (Uzbekistan), and "a5" to another set KIR (Kyrgyzstan).  
The power transfer in all lines of the network and the power generation at Uzbekistan are to be determined. 
The original model is located in section 7.1 in this [document] (http://www.ce.utexas.edu/prof/mckinney/ce385d/papers/GAMS-Tutorial.pdf)

Running the Model
-----------------
The GAMS code provided here is modified to work with the input file which is genrated from Hydra's GAMS App.

This model can be run directly with the input file provided (input.txt), similar to the orginal code.

To run this version with Hydra, user needs to:
- Install the template
- Import the newtork and scenario data using the excel file.
- Download and install GAMS App into Hydra Modeller
- Run the GAMS app using the provided GAMS model.

Using the network data and GIS (wms) file provided, Hydra Modeller allows you to visualize the model network (genrators and consumers) on their on a map. Hydra Modeller also allows you to explore and modify network data easily. Using the [GAMS App] (http://hydraappstore.com/details/?app=1088), you can run the model automatically and the results will be stored in Hydra Modeller so you can explore them. 
You can then create multiple scenarios and the run the model against each one. Then you can compare the results graphically.

You can find more details about using Hydra Modeller in this [tutorial] (https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf>). [2]

Model inputs:
-------------
- Min genration at each producer node.
- Max genration at each producer node.
- Fixed power flow for fixed flow links.

Model Outputs
-------------
- power generation at power producer node.
- power consumption at consumer node.
- power flow from node i to node j.

Version History
---------------

| Version | Date     | Comment                                       | Author                                   |
| ------- | -------- | --------------------------------------------- | ---------------------------------------- |
| 0.0.1   | Jan 2016 | Modify the orginal version to work with Hydra | K. Mohamed, the University of Manchester |

More Information
----------------

1. http://www.ce.utexas.edu/prof/mckinney/ce385d/papers/GAMS-Tutorial.pdf, Sction 7.1.
2. Stephen Knox, ''Getting started with Hydra Modeller'', https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf, Dec 2015.


