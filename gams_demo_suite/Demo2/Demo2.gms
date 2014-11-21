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

$TITLE    Demo2.gmdataset 1s

* version: time-step by time-step

 option limrow=10000;
 option limcol=10000;

** ----------------------------------------------------------------------
**  Loading Data: sets, parameters and tables
** ----------------------------------------------------------------------

$        include "demo2.txt";

** -------------------------t ---------------------------------------------
**  Model variables and equations
** ----------------------------------------------------------------------

VARIABLES
Q(i,j,t) flow in each link in each period
S(i,t) storage volume in storage nodes
delivery (i) water delivered to demand node i in each period
Z objective function
Obj (t);
;

POSITIVE VARIABLES
Q
S
;

positive variable  storage(i,t) an interim variable for saving the value of the storage at the end of each time-step;

EQUATIONS
MassBalance_nonstorage(non_storage_nodes)
MassBalance_storage(storage_nodes)
MinFlow(i,j,t)
MaxFlow(i,j,t)
MaxStor(storage_nodes,t)
MinStor(storage_nodes,t)
DemandEQ(demand_nodes)
Objective
;

* introducing a dummy variable to empty (reset) the time-step in each loop

$onempty
set dv(t) / /;

* Objective function for time step by time step formulation

Objective ..
    Z =E=sum(t$dv(t),SUM((i,j)$links(i,j), Q(i,j,t) * link_timeseries_data(t,i,j,"cost")));

*Calculating water delivery for each demand node at each time step

DemandEQ(demand_nodes)..
         delivery(demand_nodes) =E= sum(t$dv(t),SUM(j$links(j,demand_nodes), Q(j,demand_nodes,t)
         * link_timeseries_data(t,j, demand_nodes,"flow_multiplier")));

* Mass balance constrait for non-storage nodes:

MassBalance_nonstorage(non_storage_nodes) ..
    sum(t$dv(t),surface_reservoir_timeseries_data(t,non_storage_nodes,"inflow")+SUM(j$links(j,non_storage_nodes), Q(j,non_storage_nodes,t)* link_timeseries_data(t, j,non_storage_nodes,"flow_multiplier"))
    - SUM(j$links(non_storage_nodes,j), Q(non_storage_nodes,j,t))
    - demand_scalar_data(non_storage_nodes, "consumption_coefficient")$demand_nodes(non_storage_nodes) * delivery(non_storage_nodes))
    =E= 0;

* Mass balance constraint for storage nodes:

MassBalance_storage(storage_nodes)..
         sum(t$dv(t),surface_reservoir_timeseries_data(t,storage_nodes,"inflow")+SUM(j$links(j,storage_nodes), Q(j,storage_nodes,t)* link_timeseries_data(t, j,storage_nodes,"flow_multiplier"))
         - SUM(j$links(storage_nodes,j), Q(storage_nodes,j,t))
         -S(storage_nodes,t)
         +storage(storage_nodes,t-1)$(ord(t) GT 1)
         + surface_reservoir_scalar_data(storage_nodes,"initial_storage")$(ord(t) EQ 1))
         =E= 0;

* Lower and upper bound of possible flow in links

MinFlow(i,j,t)$(links(i,j) and dv(t))..
    Q(i,j,t) =G= link_timeseries_data(t,i,j,"min_flow");

MaxFlow(i,j,t)$(links(i,j) and dv(t))..
    Q(i,j,t) =L= link_timeseries_data(t,i,j,"max_flow");

* Lower and upper bound of Storage volume at storage nodes

MaxStor(storage_nodes,t)$dv(t)..
    S(storage_nodes,t) =L= surface_reservoir_timeseries_data(t,storage_nodes,"storageupper");

MinStor(storage_nodes,t)$dv(t)..
    S(storage_nodes,t) =G= surface_reservoir_timeseries_data(t,storage_nodes,"storagelower");

** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------
alias (t,tsteps);
MODEL Demo2 /ALL/;

loop (tsteps,
            dv(tsteps)=t(tsteps);
            display dv;
            SOLVE Demo2 USING LP MINIMIZING Z;
            storage.fx(i,tsteps)=S.l(i,tsteps) ;
            Obj.l(tsteps)=Z.l;
            DISPLAY  Z.l, Obj.l,storage.l,S.l, Q.l,delivery.l;
            dv(tsteps)=no;
      );

*Generating results output

execute_unload "Results.gdx" ,
    Q,
    S,
    MassBalance_storage,
    MassBalance_nonstorage,
    MinFlow,
    MaxFlow,
    MinStor,
    MaxStor,
    Z,
    Obj,
    link_timeseries_data,
    storage,
    delivery;
