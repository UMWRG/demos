Water infrastructure investment planning model 
==============================================

Files available with this model
-------------------------------
- [Template.xml] (https://github.com/UMWRG/demos/tree/master/templates/EBSD_model/template>) : template which defines nodes and links and their attributes.
- [EBSD_Tutorial_Data.xlsx] (https://github.com/UMWRG/demos/tree/master/data/EBSD_Tutorial>) : An excel file to load in Hydra Modeller which contain the network and scenario data.
- [openstreet.wms] (https://github.com/UMWRG/demos/tree/master/data/EBSD_Tutorial/GIS>) : The file you can load as a background in Hydra Modeller.
- EBSD_Tutorial.gms : The current version of the EBS tutorial GAMS code
- input.txt    : The input file for the model, containing the network information and data. This is the file Hydra creates using the GAMS App.

Purpose of Model
----------------
Economics of Balancing Supply and Demand (EBSD) planning framework used by the water industry since 2002 in England. The base model is formulated as a mixed integer linear programming optimisation model that selects the least cost annual schedule of supply and demand management options that meet forecasted demand over the planning horizon. 
This a simple tutorial model for EBSD where a hypothetical regional system composed by two water companies is considered. Water Company 1 has one demand node named ‘WRZ1’, node ‘WRZ2’ belongs to Company 2. Existing and optional future schemes are represented through nodes, interconnected via links to their respective demand nodes. Demand nodes‘WRZ2’ can also receive water from ‘WRZ1’ through an existing link or two optional ones. The demand required in nodes ‘WRZ1’ and ‘WRZ2’ are given. . The planning period 26 years, from year 2010 to year 2035.

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
-  interest rate
-  discount rate,
-  length of construction period for sources,
-  length of construction period for links,
-  final year of the planning horizon,
-  connectivity matrix (network topology)
-  sundiscapi, lundiscapi,j= undiscounted capital cost for optional sources and links respectively
- fixed operating costs for sources and links 
-  variable operating costs for sources and links 
- water demand at demand node

Model Outputs
-------------
- Annualised capital and operating cost of sources&links [-];
- Activation for optional source during period t [-]
- Activitation of link optilnal during period t [-];
- Flow from node i to j during year t [1e6 m^3 mon^-1]
- Supply from source i during year t [1e6 m^3];


Version History
---------------

| Version | Date     | Comment                                       | Author                                   |
| ------- | -------- | --------------------------------------------- | ---------------------------------------- |
| 0.0.1   | Jan 2016 | Modify the orginal version to work with Hydra | K. Mohamed, the University of Manchester |

More Information
----------------
1. [Model formulation and core detailed description of the model and network in this document] (https://github.com/UMWRG/demos/blob/master/gams_demo_suite/EBSD_Tutorial/EBSD_Tutorial.docx>)
2. [Details about using Hydra Modeller in this tutorial] (https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf>).  

