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

$TITLE    CostMinimisation.gmdataset 1s

* version: time-step by time-step

 option limrow=10000;
 option limcol=10000;

** ----------------------------------------------------------------------
**  Loading Data: sets, parameters and tables
** ----------------------------------------------------------------------

$        include "no_shortage.txt"

** ----------------------------------------------------------------------
**  Model variables and equations
** ----------------------------------------------------------------------

VARIABLES
Q(i,j,t) flow in each link in each period [1e6 m^3 mon^-1]
S(i,t) storage volume in storage nodes [1e6 m^3]
delivered_water(i) water delivered to demand node i in each period [1e6 m^3 mon^-1]
delivery(i,t) an interim variable for saving the value of the water delivery to each demand node at the end of each time-step [1e6 m^3 mon^-1]
Z objective function [-]
Obj (t) [-];
;

POSITIVE VARIABLES
Q
S
;

positive variable  storage(i,t) an interim variable for saving the value of the storage at the end of each time-step;

EQUATIONS
*MassBalance(i)
MassBalance_agricultural(agricultural)
MassBalance_urban(urban)
MassBalance_junction(junction)
MassBalance_storage(surface_reservoir)
MinFlow(i,j,t)
MaxFlow(i,j,t)
MaxStor(surface_reservoir,t)
MinStor(surface_reservoir,t)
Objective
;

* introducing a dummy variable to empty (reset) the time-step in each loop

$onempty
set dv(t) / /;

* Objective function for time step by time step formulation

Objective ..
    Z =E=sum(t$dv(t),SUM((i,j)$links(i,j), Q(i,j,t) * cost(i,j,t)));

* Mass balance constrait for non-storage nodes:

*This is an alternative approach, where mass balance of all non storage
*nodes are calculated in a single equation.

*MassBalance(i) $ (urban(i) or agricultural(i) or junction(i)) ..
*    sum(t$dv(t),inflow(i, t)
*    +SUM(j$links(j,i), Q(j,i,t)
*    * flow_multiplier(j,i,t))
*    - SUM(j$links(i,j), Q(i,j,t))
*    - consumption_coefficient(i, "0") * delivered_water(i))
*    =E= 0;


MassBalance_urban(urban) ..
    sum(t$dv(t),inflow(urban,t)
    +SUM(j$links(j,urban), Q(j,urban,t)
    * flow_multiplier(j,urban,t))
    - SUM(j$links(urban,j), Q(urban,j,t))
    - consumption_coefficient(urban,"0")
    * delivered_water(urban))
    =E= 0;

MassBalance_agricultural(agricultural) ..
    sum(t$dv(t),inflow(agricultural,t)
    +SUM(j$links(j,agricultural), Q(j,agricultural,t)
    * flow_multiplier(j,agricultural,t))
    - SUM(j$links(agricultural,j), Q(agricultural,j,t))
    - consumption_coefficient(agricultural,"0")
    * delivered_water(agricultural))
    =E= 0;

MassBalance_junction(junction) ..
    sum(t$dv(t),inflow(junction,t)
    + SUM(j$links(j,junction), Q(j,junction,t)
    * flow_multiplier(j,junction,t))
    - SUM(j$links(junction,j), Q(junction,j,t)))
    =E= 0;



* Mass balance constraint for storage nodes:

MassBalance_storage(surface_reservoir)..
         sum(t$dv(t),inflow(surface_reservoir,t)+
         SUM(j$links(j,surface_reservoir), Q(j,surface_reservoir,t) 
         * flow_multiplier(j,surface_reservoir,t))
         - SUM(j$links(surface_reservoir,j), Q(surface_reservoir,j,t))
         -S(surface_reservoir,t)
         +storage(surface_reservoir,t-1)$(ord(t) GT 1)
         + initial_storage(surface_reservoir,t)$(ord(t) EQ 1))
         =E= 0;

* Lower and upper bound of possible flow in links

MinFlow(i,j,t)$(links(i,j) and dv(t))..
    Q(i,j,t) =G= min_flow(i,j,t);

MaxFlow(i,j,t)$(links(i,j) and dv(t))..
    Q(i,j,t) =L= max_flow(i,j,t);

* Lower and upper bound of Storage volume at storage nodes

MaxStor(surface_reservoir,t)$dv(t)..
    S(surface_reservoir,t) =L= storageupper(surface_reservoir,t);

MinStor(surface_reservoir,t)$dv(t)..
    S(surface_reservoir,t) =G= storagelower(surface_reservoir,t);

** ----------------------------------------------------------------------
**  Model declaration and solve statements
** ----------------------------------------------------------------------
alias (t,tsteps);
MODEL CostMinimisation /ALL/;

loop (tsteps,
            dv(tsteps)=t(tsteps);
            display dv;
            SOLVE CostMinimisation USING LP MINIMIZING Z;
            storage.fx(i,tsteps)=S.l(i,tsteps) ;
            Obj.l(tsteps)=Z.l;
            delivery.l(urban,tsteps)=delivered_water.l(urban);
            delivery.l(agricultural,tsteps)=delivered_water.l(agricultural);
            delivery.l(junction,tsteps)=delivered_water.l(junction);
            DISPLAY  Z.l, Obj.l,storage.l,S.l, Q.l,delivered_water.l;
            dv(tsteps)=no;
      );

*Generating results output


execute_unload "Results.gdx" ,
    Q,
    S,
*    MassBalance,
    MassBalance_junction,
    MassBalance_urban,
    MassBalance_agricultural,
    MassBalance_storage,
    MinFlow,
    MaxFlow,
    MinStor,
    MaxStor,
    Z,
    Obj,
    storage,
    delivery,
    delivered_water;
