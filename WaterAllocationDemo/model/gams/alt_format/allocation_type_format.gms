**    (c) Copyright 2014, University of Manchester
**
**    Authors: Majed Khadem, Silvia Padula, Khaled Mohamed, Stephen Knox and Julien Harou
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

$TITLE    allocation.gms.gms

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

Variables
Objective_function objective function [-]
Obj(t) an interim variable for saving the value of the objective function at the end of each time step[-];

POSITIVE VARIABLES
Flow(t,i,j) flow in each link in each period [-]
Storage_level(t,i) storage volume in storage nodes [-]
percent_demand_met_ratio(i) target demand satisfaction ratio [-];
percent_demand_met_ratio.up(demand_nodes)=1;

POSITIVE VARIABLES
storage(t,storage_nodes) an interim variable for saving the value of the storage at the end of each time step
percent_demand_met(t,i) an interim variable for saving the value of the satisfaction ratio at the end of each time step [-];


* Post-process variables

POSITIVE VARIABLES
received_water(t,i) a variable for saving the amount of water received by every node at the end of each time step[-]
released_water(t,i) a variable for saving the amount of water released by every node at the end of each time step[-]
demand_met (t,i) a variable for saving the amount of demand met in each node at the end of each time step [-]
Revenue(t,i) a variable for saving the value of revenue calculated for each hydropower node at the end of each time step [-];


EQUATIONS
MassBalance_storage(storage_nodes)
MassBalance_nonstorage(non_storage_nodes)
MinFlow(t,i,j)
MaxFlow(t,i,j)
MaxStor(t,storage_nodes)
MinStor(t,storage_nodes)
MaxStorForTratment(t,treatment_hydro_nodes)
Objective
;

* introducing a dummy variable to empty (reset) the time-step in each loop

$onempty
set dv(t) / /;


Objective..
    objective_function =E= sum(t$dv(t),SUM((demand_nodes),
          percent_demand_met_ratio(demand_nodes) * agricultural_timeseries_data(t, demand_nodes, "priority")
          + percent_demand_met_ratio(demand_nodes) * urban_timeseries_data(t, demand_nodes, "priority")
          + percent_demand_met_ratio(demand_nodes) * discharge_timeseries_data(t, demand_nodes, "priority")));


* Mass balance constraint for non-storage nodes:

MassBalance_nonstorage(non_storage_nodes)..


         SUM(t$dv(t),(1-(
          hydropower_timeseries_data(t,non_storage_nodes,"percent_loss")+
          watertreatment_timeseries_data(t,non_storage_nodes,"percent_loss")
          ))
         * SUM(j$links(j,non_storage_nodes), Flow(t,j,non_storage_nodes)
         * river_section_timeseries_data(t, j,non_storage_nodes, "flow_multiplier"))
         - SUM(j$links(non_storage_nodes,j), Flow(t,non_storage_nodes,j))
         - percent_demand_met_ratio(non_storage_nodes) * agricultural_timeseries_data(t, non_storage_nodes, "demand")
         - percent_demand_met_ratio(non_storage_nodes) * urban_timeseries_data(t, non_storage_nodes, "demand")
         - percent_demand_met_ratio(non_storage_nodes) * discharge_timeseries_data(t, non_storage_nodes, "demand"))
         =E= 0;

** Mass balance constraint for storage nodes:

MassBalance_storage(storage_nodes)..

         SUM(t$dv(t),
         surface_reservoir_timeseries_data(t, storage_nodes, "inflow")
         + desalination_timeseries_data(t, storage_nodes, "inflow")
         + (1-(
          hydropower_timeseries_data(t,storage_nodes,"percent_loss")+
          watertreatment_timeseries_data(t,storage_nodes,"percent_loss")
          ))
         * SUM(j$links(j,storage_nodes), Flow(t,j,storage_nodes)
         * river_section_timeseries_data(t, j, storage_nodes, "flow_multiplier"))
         - SUM(j$links(storage_nodes,j), Flow(t,storage_nodes,j))
         - Storage_level(t,storage_nodes)
         + storage(t-1,storage_nodes)$(ord(t) GT 1)
         + desalination_scalar_data(storage_nodes, "initial_storage")$(ord(t) EQ 1)
         + groundwater_scalar_data(storage_nodes, "initial_storage")$(ord(t) EQ 1)
         + surface_reservoir_scalar_data(storage_nodes, "initial_storage")$(ord(t) EQ 1))
         =E= 0;

* Lower and upper bound of possible flow in links

MinFlow(t,i,j)$(links(i,j) and dv(t)) ..
    Flow(t,i,j) =G= river_section_timeseries_data(t, i,j,"min_flow");

MaxFlow(t,i,j)$(links(i,j)  and dv(t))..
    Flow(t,i,j) =L= river_section_timeseries_data(t, i,j,"max_flow");

* Lower and upper bound of Storage volume at storage nodes
MaxStor(t,storage_nodes)$dv(t)..
    Storage_level(t,storage_nodes) =L= desalination_timeseries_data(t, storage_nodes, "max_storage") +
                           groundwater_timeseries_data(t, storage_nodes, "max_storage") +
                           surface_reservoir_timeseries_data(t, storage_nodes, "max_storage");

MinStor(t,storage_nodes)$dv(t)..
    Storage_level(t,storage_nodes) =G= desalination_timeseries_data(t, storage_nodes, "min_storage") +
                            groundwater_timeseries_data(t, storage_nodes, "min_storage") +
                            surface_reservoir_timeseries_data(t, storage_nodes, "min_storage");

* Upper capacity limit at treatment and hydropower nodes
MaxStorForTratment(t,treatment_hydro_nodes)$dv(t)..
   SUM(j$links(j,treatment_hydro_nodes), Flow(t,j,treatment_hydro_nodes)*
       river_section_timeseries_data(t, j, treatment_hydro_nodes, "flow_multiplier"))
   =L=
   hydropower_timeseries_data(t,treatment_hydro_nodes,"max_storage")+
   watertreatment_timeseries_data(t,treatment_hydro_nodes,"max_storage");



** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------

alias(t, tsteps)
MODEL allocation.gms /MassBalance_storage,MassBalance_nonstorage,MinFlow,MaxFlow,MinStor,MaxStor,MaxStorForTratment,Objective/;

loop (tsteps,
            dv(tsteps)=t(tsteps);
            SOLVE allocation.gms USING LP MAXIMIZING Objective_function;
            storage.fx(tsteps,storage_nodes)=Storage_level.l(tsteps,storage_nodes) ;
            percent_demand_met.l(tsteps,i)=percent_demand_met_ratio.l(i);
            Obj.l(tsteps)=Objective_function.l;
            DISPLAY  Objective_function.l, Storage_level.l, Flow.l;
            dv(tsteps)=no;
      );


************************************* post-processing: ******************************

loop (tsteps,
            dv(tsteps)=t(tsteps);

*** Water tracking equations

* Equation to calculate the amount of water received by each node

received_water.l(tsteps, i) =
         SUM(j$links(j,i), Flow.l(tsteps,j,i)*river_section_timeseries_data(tsteps,j,i, "flow_multiplier"));


* Equation to calculate the amount of water released from each node

released_water.l(tsteps,i) =
         SUM(j$links(i,j), Flow.l(tsteps,i,j));

* Equation to calculate the amount of demand met in each node

 Demand_met.l(tsteps,i)$(demand_nodes(i)) =
         received_water.l(tsteps,i)-released_water.l(tsteps,i);


*** Equation to calculate the hydropower revenue

*         Revenue=power*unit price
*         Power=Flow*g*efficiency*Net head
*                  Assume flow is in cubic metres per day and Net head is in metres and unit price is in GBP
*                  Conversion factor of 0.3858 is used to convert cubic metres per day to litres per second
*                  i.e. times by 1000 litres per m3 and divide by
*                  (60{seconds/minute}*60{minutes/hour}*24{hours/day}*30{days/month})
*                  An additional multiplication by 24 used to convert kW to kWh


Revenue.l(tsteps,hydropower)= (1-hydropower_timeseries_data(tsteps,hydropower,"percent_loss"))
         * SUM(j$links(j,hydropower), Flow.l(tsteps,j,hydropower)*river_section_timeseries_data(tsteps,j,hydropower, "flow_multiplier"))
         * 9.81
         * hydropower_scalar_data(hydropower,"net_head")
         * hydropower_scalar_data(hydropower,"unit_price")
         * 0.3858
         * 24
         ;
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



