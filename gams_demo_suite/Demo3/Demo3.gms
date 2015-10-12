**    (c) Copyright 2014, University of Manchester
**
**    This file is part of the GAMS Plugin Demo Suite.
**
**    The GAMS Plugin Demo Suite is free software: you can redistribute it and/or modify
**    it under the terms of the GNU General Public License as published by
**    the Free Software Foundation, either version 3 of the License, or
**    (at your option) any later version.
**
**    The GAMS Plugin Demo Suite is distributed in the hope that it will be useful,
**    but WITHOUT ANY WARRANTY; without even the implied warranty of
**    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**    GNU General Public License for more details.
**
**    You should have received a copy of the GNU General Public License
**    along with the GAMS Plugin Demo Suite.  If not, see <http://www.gnu.org/licenses/>.
**

$TITLE    Demo3.gms

* version: time-step by time-step

 option limrow=10000;
 option limcol=10000;

** ----------------------------------------------------------------------
**  Loading Data: sets, parameters and tables
** ----------------------------------------------------------------------

*$        include "shortage.txt";
$        include "non_shortage.txt";

** ----------------------------------------------------------------------
**  Model variables and equations
** ----------------------------------------------------------------------


* Optimisation model variables

VARIABLES
Objective_function objective function [-]
Obj(t) an interim variable for saving the value of the objective function at the end of each time step[-]
Q(i,j,t) flow in each link in each period [-]
S(i,t) storage volume in storage nodes [-]
receive(i) water delivered to every node i in each period [-]
release(i) water released from node i in each period [-]
delivery(i) water delivered to demand node i in each period [-]
alpha(i,t) an interim variable for saving the value of the satisfaction ratio at the end of each time-step [-]
Z objective function [-]
;

POSITIVE VARIABLES
Flow(i,j,t) flow in each link in each period [-]
Storage_level(i,t) storage volume in storage nodes [-]
percent_demand_met_ratio(i) target demand satisfaction ratio [-]
storage(storage_nodes,t) an interim variable for saving the value of the storage at the end of each time step
percent_demand_met(i,t) an interim variable for saving the value of the satisfaction ratio at the end of each time step [-]
received_water(i,t) a variable for saving the amount of water received by every node at the end of each time step[-]
released_water(i,t) a variable for saving the amount of water released by every node at the end of each time step[-]
demand_met(i,t) a variable for saving the amount of demand met in each node at the end of each time step [-]
Revenue(i,t) a variable for saving the value of revenue calculated for each hydropower node at the end of each time step [-];

percent_demand_met_ratio.up(demand_nodes)=1;


EQUATIONS
MassBalance_storage(storage_nodes)
MassBalance_nonstorage(non_storage_nodes)
MinFlow(i,j,t)
MaxFlow(i,j,t)
MaxStor(storage_nodes,t)
MinStor(storage_nodes,t)
MaxStorForTratment(treatment_hydro_nodes,t)
Objective
;

* introducing a dummy variable to empty (reset) the time-step in each loop

$onempty
set dv(t) / /;


* Objective function for time step by time step formulation

Objective ..
    Objective_function =E= sum(t$dv(t),SUM((demand_nodes), percent_demand_met_ratio(demand_nodes)
          * priority(demand_nodes, t)));

* Mass balance constraint for non-storage nodes:

MassBalance_nonstorage(non_storage_nodes)..

         SUM(t$dv(t),inflow(non_storage_nodes, t)
<<<<<<< HEAD
         +(1-percent_loss(non_storage_nodes,t))*SUM(j$links(j,non_storage_nodes), Flow(j,non_storage_nodes,t)
=======
         +(1-percent_efficiency(non_storage_nodes, t))*SUM(j$links(j,non_storage_nodes), Flow(j,non_storage_nodes,t)
>>>>>>> origin/master
         * flow_multiplier(j,non_storage_nodes, t))
         - SUM(j$links(non_storage_nodes,j), Flow(non_storage_nodes,j,t))
         - (percent_demand_met_ratio(non_storage_nodes)* demand(non_storage_nodes, t)))
         =E= 0;

* Mass balance constraint for storage nodes:

MassBalance_storage(storage_nodes)..

         SUM(t$dv(t),inflow(storage_nodes, t)
<<<<<<< HEAD
         + (1-percent_loss(storage_nodes,t))*SUM(j$links(j,storage_nodes), Flow(j,storage_nodes,t)
=======
         + (1-percent_efficiency(storage_nodes, t))*SUM(j$links(j,storage_nodes), Flow(j,storage_nodes,t)
>>>>>>> origin/master
         * flow_multiplier(j, storage_nodes, t))
         - SUM(j$links(storage_nodes,j), Flow(storage_nodes,j,t))
         - Storage_level(storage_nodes,t)
         + storage(storage_nodes,t-1)$(ord(t) GT 1)
         + initial_storage(storage_nodes)$(ord(t) EQ 1))
         =E= 0;

* Lower and upper bound of possible flow in links

MinFlow(i,j,t)$(links(i,j) and dv(t)) ..
    Flow(i,j,t) =G= min_flow(i,j, t);

MaxFlow(i,j,t)$(links(i,j)  and dv(t))..
    Flow(i,j,t) =L= max_flow(i,j, t);

* Lower and upper bound of Storage volume at storage nodes
MaxStor(storage_nodes,t)$dv(t)..
    Storage_level(storage_nodes,t) =L= max_storage(storage_nodes, t);

MinStor(storage_nodes,t)$dv(t)..
    Storage_level(storage_nodes,t)=G= min_storage(storage_nodes, t);

* Upper capacity limit at treatment and hydropower nodes
MaxStorForTratment(treatment_hydro_nodes,t)$dv(t)..
   SUM(j$links(j,treatment_hydro_nodes), Flow(j,treatment_hydro_nodes,t)* flow_multiplier(j,treatment_hydro_nodes,t))
   =L=
   max_storage(treatment_hydro_nodes,t);



** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------

alias(t, tsteps)
MODEL Demo3 /MassBalance_storage, MassBalance_nonstorage,MinFlow,MaxFlow,MinStor,MaxStor,MaxStorForTratment,Objective/;

loop (tsteps,
            dv(tsteps)=t(tsteps);
            SOLVE Demo3 USING LP MAXIMIZING Objective_function;
            storage.fx(storage_nodes,tsteps)=Storage_level.l(storage_nodes,tsteps) ;
            percent_demand_met.l(i,tsteps)=percent_demand_met_ratio.l(i);
            Obj.l(tsteps)=Objective_function.l;
            DISPLAY  Objective_function.l, Storage_level.l, Flow.l;
            dv(tsteps)=no;
      );


************************************* post-processing: ******************************

loop (tsteps,
            dv(tsteps)=t(tsteps);


*** Water tracking equations

* Equation to calculate the amount of water received by each node

    received_water.l(i,tsteps) =
         SUM(j$links(j,i), Flow.l(j,i,tsteps)* flow_multiplier(j,i,tsteps));

* Equation to calculate the amount of water released from each node

    released_water.l(i,tsteps) =
         SUM(j$links(i,j), Flow.l(i,j,tsteps));

* Equation to calculate the amount of demand met in each node

    Demand_met.l(i,tsteps)$(demand_nodes(i)) =
         received_water.l(i,tsteps)-released_water.l(i,tsteps);

*** Equation to calculate the hydropower revenue:

*         Revenue=power*unit price
*         Power=Flow*g*efficiency*Net head
*		  Assume flow is in cubic metres per day and Net head is in metres and unit price is in GBP
*		  Conversion factor of 0.0003858 is used to convert cubic metres per day to litres per second
*		  i.e. times by 1000 litres per m3 and divide by 
*		  (60{seconds/minute}*60{minutes/hour}*24{hours/day}*30{days/month})
*		  An additional multiplication by 24 used to convert kW to kWh

    Revenue.l(hydropower,tsteps)= (1-percent_loss(hydropower,tsteps))
         * SUM(j$links(hydropower,j), Flow.l(hydropower,j,tsteps))
         * 9.81
<<<<<<< HEAD
         * net_head
         * unit_price
		 * 0.3858
		 * 24;
=======
         * net_head(hydropower)
         * unit_price;
>>>>>>> origin/master

            dv(tsteps)=no;
      );

*Generating results output

execute_unload "Results.gdx" ,
    Flow,
    percent_demand_met,
    Obj,
    Demand_met,
    storage,
    received_water,
    released_water,
    Revenue;



