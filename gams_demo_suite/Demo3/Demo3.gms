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

VARIABLES
Q(i,j,t) flow in each link in each period [1e6 m^3 mon^-1]
S(i,t) storage volume in storage nodes [1e6 m^3]
receive(i) water delivered to every node i in each period [1e6 m^3 mon1]
release(i) water released from node i in each period [1e6 m^3 mon1]
delivery(i) water delivered to demand node i in each period [1e6 m^3 mon1]
alpha(i,t) an interim variable for saving the value of the satisfaction ratio at the end of each time-step [-]
Z objective function [-]
Obj(t) [-];
;

POSITIVE VARIABLES
Q 
S 
alpha_coeff(i) target demand satisfaction ratio [-];
alpha_coeff.up(demand_nodes)=1;

positive variable  storage(storage_nodes,t) an interim variable for saving the value of the storage at the end of each time-step
                   a(i,t) an interim variable for saving the value of the satisfaction ratio at the end of each time-step
				   received_water(i,t) an interim variable for saving the amount of water received by every node at the end of each time-step[1e6 m^3 mon1]
                   released_water(i,t) an interim variable for saving the amount of water released by every node at the end of each time-step[1e6 m^3 mon1];

positive variable  storage(storage_nodes,t) an interim variable for saving the value of the storage at the end of each time-step;


EQUATIONS
MassBalance_storage(storage_nodes)
MassBalance_nonstorage(non_storage_nodes)
MinFlow(i,j,t)
MaxFlow(i,j,t)
MaxStor(storage_nodes,t)
MinStor(storage_nodes,t)
ReceivingEQ(i)
ReleasingEQ(i)
Objective
;

* introducing a dummy variable to empty (reset) the time-step in each loop

$onempty
set dv(t) / /;


* Objective function for time step by time step formulation

Objective ..
    Z =E= sum(t$dv(t),SUM((demand_nodes), alpha_coeff(demand_nodes)
          * cost(demand_nodes, t)));

* Mass balance constraint for non-storage nodes:

MassBalance_nonstorage(non_storage_nodes)..

         SUM(t$dv(t),inflow(non_storage_nodes, t)
         +SUM(j$links(j,non_storage_nodes), Q(j,non_storage_nodes,t)
         * flow_multiplier(j,non_storage_nodes, t))
         - SUM(j$links(non_storage_nodes,j), Q(non_storage_nodes,j,t))
         - (alpha_coeff(non_storage_nodes)* demand(non_storage_nodes, t)))
         =E= 0;

* Mass balance constraint for storage nodes:

MassBalance_storage(storage_nodes)..

         SUM(t$dv(t),inflow(storage_nodes, t)
         + SUM(j$links(j,storage_nodes), Q(j,storage_nodes,t)
         * flow_multiplier(j, storage_nodes, t))
         - SUM(j$links(storage_nodes,j), Q(storage_nodes,j,t))
         - S(storage_nodes,t)
         + storage(storage_nodes,t-1)$(ord(t) GT 1)
         + initial_storage(storage_nodes, t)$(ord(t) EQ 1))
         =E= 0;

* Lower and upper bound of possible flow in links

MinFlow(i,j,t)$(links(i,j) and dv(t)) ..
    Q(i,j,t) =G= min_flow(i,j, t);

MaxFlow(i,j,t)$(links(i,j)  and dv(t))..
    Q(i,j,t) =L= max_flow(i,j, t);

* Lower and upper bound of Storage volume at storage nodes
MaxStor(storage_nodes,t)$dv(t)..
    S(storage_nodes,t) =L= max_storage(storage_nodes, t);

MinStor(storage_nodes,t)$dv(t)..
    S(storage_nodes,t) =G= min_storage(storage_nodes, t);


*** Water tracking equations

* Equation to calculate the amount of water received by each node
ReceivingEQ(i)..
    receive(i) =E= sum(t$dv(t),
         SUM(j$links(j,i), Q(j,i,t)* flow_multiplier(j,i,t)));

* Equation to calculate the amount of water released from each node
ReleasingEQ(i)..
    release(i) =E= SUM(t$dv(t),
         SUM(j$links(i,j), Q(i,j,t)));
		 
** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------
alias(t, tsteps)
MODEL Demo3 /ALL/;

loop (tsteps,
            dv(tsteps)=t(tsteps);
            SOLVE Demo3 USING LP MAXIMIZING Z;
            storage.fx(storage_nodes,tsteps)=S.l(storage_nodes,tsteps) ;
            a.l(i,tsteps)=alpha.l(i);
			received_water.fx(i,tsteps)=receive.l(i);
            released_water.fx(i,tsteps)=release.l(i);
			alpha.l(i,tsteps)=alpha_coeff.l(i);
            Obj.l(tsteps)=Z.l;
            DISPLAY  Z.l, Obj.l,storage.l,S.l, Q.l;
            dv(tsteps)=no;
      );

*Generating results output

execute_unload "Results.gdx" ,
    Q,
    S,
    MassBalance_storage,
    MinFlow,
    MaxFlow,
    MinStor,
    MaxStor,
    Z,    
	alpha_coeff,
	alpha,
    Obj,
    storage,
    a,
	received_water,
    released_water,
    storage;




