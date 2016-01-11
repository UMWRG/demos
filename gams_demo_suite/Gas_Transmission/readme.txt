Gas Transmission Problem – Belgium
==================================

Files available with this model
===============================
Template.xml – a template which defines nodes and links and their attributes.
Gas_Trans.xlsx – An excel file to load in Hydra Modeller which contain the network and scenario dara.
openstreet.wms – a file you can load as a background in Hydra Modeller.
gastrans.gms – the current version of the GAS transmission model

Purpose of model
================
The problem considered in this model is to minimize the total supply cost of a gas transmission company which must satisfy demand in di?erent nodes at a minimal guaranteed pressure.
The problem of distributing gas through a network of pipelines is formulated as a cost minimization subject to nonlinear flow-pressure relations, material balances, and pressure bounds. The Belgian gas network is used as an example.
First, a straight-forward NLP formulation that can be solved fine by todays NLP solvers is modeled.  Afterwards, the 3-stage approach by Wolf & Smeers [1] is implemented.

The original GASM code for this model is located at:
https://www.gams.com/modlib/libhtml/gastrans.htm
The provided GAMS code is modified to work with the input file which is genrated from GAMS App. Also, it can run directley with the input file (input.txt)similar to the orginal code.

To run this version with Hydra, user needs to:
- Install template
- import the newtork and sceario data using the excel file.
- Download and install GAMS app
- Run the GAMS app using the provided GASM model.

Reader can find more details about the previous steps in getting start with Hydra tutorial[2].

Using this version with hydra modeller allow the user to visualize the model network (cities and pipelines) on their actual location on a dynamic map. In addition he/she can explore network data and modify them if needed. Using GAMSApp, the user will be able to run the model automatically and the results will be pushed to system database so the user can explore them. It is possible to have more than one model dataset (scenarios) and run the model for each of them and compare the results.

Model input
===========
compressibility factor (-)
density of gas relative to air (-)
length (km)
diameter (mm)
cost ($ per MBTU)   
pressure upper bound (bar)
pressure lower bound (bar)
supply upper bound (mill M3 per day)
supply lower bound (mill M3 per day)
absolute rugosity (mm)
gas temperature (K)  

Model output
============
Arc flow (1e6 SCM)
supply - demand (1e6 SCM)
squared pressure
supply cost ($)

Reader can find model formulation and core detailed description of the Belgium network on [1].

Version history
===============
- 0.0.1, Janu 2016, modify the orginla vresion to work with Hydra, K. Mohamed, the University of Manchester

More information
================
1.	de Wolf, D, and Smeers, Y, The Gas Transmission Problem Solved by and Extension of the Simplex Algorithm. Management Science 46, 11 (2000), 1454-1465.
2.	Stephen Knox, “Getting started with Hydra Modeller”, https://github.com/UMWRG/demos/blob/master/doc/GettingStartedWithHydraModeller.pdf, Dec 2015.


