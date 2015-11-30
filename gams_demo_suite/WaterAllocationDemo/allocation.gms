**    (c) Copyright 2014, University of Manchester
**
**    Authors: Majed Khadem, Silvia Padula, Khaled Mohamed, Stephen Knox, Brett Korteling and Julien Harou
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

$TITLE    allocation.gms

* version: time-step by time-step

 option limrow=10000;
 option limcol=10000;

** ----------------------------------------------------------------------
**  Loading Data: sets, parameters and tables
** ----------------------------------------------------------------------

$        include "model_input.txt";
**for testing: $        include "shortage.txt";
**for testing: $        include "non_shortage.txt";


** ----------------------------------------------------------------------
**  Model variables and equations
** ----------------------------------------------------------------------

* Optimisation model variables

VARIABLES
objective_function(t) an interim variable for saving the value of the objective function at the end of each time step[-]
obj objective function [-]
;

POSITIVE VARIABLES
flow(i,j,t) flow in each link in each period [1e6 m^3 mon^-1]
Storage_level(i,t) storage volume in storage nodes [-]
percent_demand_met_ratio(i) target demand satisfaction ratio [-]
storage(storage_nodes,t) an interim variable for saving the value of the storage at the end of each time step [1e6 m^3]
percent_demand_met(i,t) an interim variable for saving the value of the satisfaction ratio at the end of each time step [-]
received_water(i,t) a variable for saving the amount of water received by every node at the end of each time step[1e6 m^3 mon^-1]
released_water(i,t) a variable for saving the amount of water released by every node at the end of each time step[1e6 m^3 mon^-1]
demand_met(i,t) a variable for saving the amount of demand met in each node at the end of each time step [-]
revenue(i,t) a variable for saving the value of revenue calculated for each hydropower node at the end of each time step [GBP mon^-1];



percent_demand_met_ratio.up(demand_nodes)=1;

EQUATIONS
MassBalance_storage(storage_nodes)
MassBalance_nonstorage(non_storage_nodes)
Minflow(i,j,t)
Maxflow(i,j,t)
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
    obj =E= sum(t$dv(t),SUM((demand_nodes), percent_demand_met_ratio(demand_nodes)
          * priority(demand_nodes, t)));

* Mass balance constraint for non-storage nodes:

MassBalance_nonstorage(non_storage_nodes)..

         SUM(t$dv(t),inflow(non_storage_nodes, t)
         +(1-percent_loss(non_storage_nodes))*SUM(j$links(j,non_storage_nodes), flow(j,non_storage_nodes,t)
         * flow_multiplier(j,non_storage_nodes, t))
         - SUM(j$links(non_storage_nodes,j), flow(non_storage_nodes,j,t))
         - (percent_demand_met_ratio(non_storage_nodes)* demand(non_storage_nodes, t)))
         =E= 0;

* Mass balance constraint for storage nodes:

MassBalance_storage(storage_nodes)..

         SUM(t$dv(t),inflow(storage_nodes, t)
         + (1-percent_loss(storage_nodes))*SUM(j$links(j,storage_nodes), flow(j,storage_nodes,t)
         * flow_multiplier(j, storage_nodes, t))
         - SUM(j$links(storage_nodes,j), flow(storage_nodes,j,t))
         - Storage_level(storage_nodes,t)
         + storage(storage_nodes,t-1)$(ord(t) GT 1)
         + initial_storage(storage_nodes)$(ord(t) EQ 1))
         =E= 0;

* Lower and upper bound of possible flow in links

Minflow(i,j,t)$(links(i,j) and dv(t)) ..
    flow(i,j,t) =G= min_flow(i,j, t);

Maxflow(i,j,t)$(links(i,j)  and dv(t))..
    flow(i,j,t) =L= max_flow(i,j, t);

* Lower and upper bound of Storage volume at storage nodes
MaxStor(storage_nodes,t)$dv(t)..
    Storage_level(storage_nodes,t) =L= max_storage(storage_nodes, t);

MinStor(storage_nodes,t)$dv(t)..
    Storage_level(storage_nodes,t)=G= min_storage(storage_nodes, t);

* Upper capacity limit at treatment and hydropower nodes
MaxStorForTratment(treatment_hydro_nodes,t)$dv(t)..
   SUM(j$links(j,treatment_hydro_nodes), flow(j,treatment_hydro_nodes,t)* flow_multiplier(j,treatment_hydro_nodes,t))
   =L=
   max_storage(treatment_hydro_nodes,t);



** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------

alias(t, tsteps)
MODEL allocation /MassBalance_storage,MassBalance_nonstorage,Minflow,Maxflow,MinStor,MaxStor,MaxStorForTratment,Objective/;

loop (tsteps,
            dv(tsteps)=t(tsteps);
            SOLVE allocation USING LP MAXIMIZING obj;
            storage.fx(storage_nodes,tsteps)=Storage_level.l(storage_nodes,tsteps) ;
            percent_demand_met.l(i,tsteps)=percent_demand_met_ratio.l(i);
            objective_function.l(tsteps)=obj.l;
            DISPLAY  obj.l, Storage_level.l, flow.l;
            dv(tsteps)=no;
      );


************************************* post-processing: ******************************

loop (tsteps,
            dv(tsteps)=t(tsteps);


*** Water tracking equations

* Equation to calculate the amount of water received by each node

    received_water.l(i,tsteps) =
         SUM(j$links(j,i), flow.l(j,i,tsteps)* flow_multiplier(j,i,tsteps));

* Equation to calculate the amount of water released from each node

    released_water.l(i,tsteps) =
         SUM(j$links(i,j), flow.l(i,j,tsteps));

* Equation to calculate the amount of demand met in each node

    demand_met.l(i,tsteps)$(demand_nodes(i)) =
         received_water.l(i,tsteps)-released_water.l(i,tsteps);

*** Equation to calculate the hydropower revenue:

*         revenue=power*unit price
*         Power=flow*g*efficiency*Net head
*                  Assume flow is in cubic metres per day and Net head is in metres and unit price is in GBP
*                  Conversion factor of 0.3858 is used to convert cubic metres per day to litres per second
*                  i.e. times by 1000 litres per m3 and divide by
*                  (60{seconds/minute}*60{minutes/hour}*24{hours/day}*30{days/month})
*                  An additional multiplication by 24 used to convert kW to kWh



    Revenue.l(hydropower,tsteps)= (1-percent_loss(hydropower))
         * SUM(j$links(j,hydropower), Flow.l(j,hydropower,tsteps)*flow_multiplier(j,hydropower,tsteps))
         * 9.81
         * net_head(hydropower)
         * unit_price
         * 0.3858
         * 24;



    dv(tsteps)=no;
      );

*Generating results output

execute_unload "Results.gdx" ,
    flow,
    percent_demand_met,
    objective_function,
    demand_met,
    storage,
    received_water,
    released_water,	
    revenue;




